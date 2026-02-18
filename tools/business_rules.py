"""Tool for retrieving business rules from domain-specific guide files.

Three-stage retrieval:
  Stage 1 (regex/keyword): Fast exact and substring matching on schema names,
      file names, titles, headers, and domain terms. Returns immediately if
      a high-confidence match is found (score >= 50).
  Stage 2 (semantic embedding): If Stage 1 is uncertain, computes cosine
      similarity between the query and pre-computed guide embeddings using
      a local sentence-transformers model (all-MiniLM-L6-v2).
  Stage 3 (LLM validation): An optional LLM-based check that verifies the
      retrieved guide is the right one for the query. If the model disagrees,
      the next-best alternative is returned instead.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path

import numpy as np

from framework.agent import Tool
from framework.llm import completion_request

_logger = logging.getLogger(__name__)

# Directory containing all business rules guides
GUIDES_DIR = Path(__file__).parent.parent / "evaluation" / "data" / "guides"

# Local embedding model name (small, fast, 384-dim)
_EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# Module-level state for lazy-loaded model and cached guide embeddings
_embedding_model: object | None = None
_guide_embeddings: np.ndarray | None = None

# Stage 1 threshold: if the regex score is at or above this, skip Stage 2
_STAGE1_CONFIDENCE_THRESHOLD = 50.0
# Stage 2 threshold: minimum cosine similarity to accept a semantic match
_STAGE2_SIMILARITY_THRESHOLD = 0.25
# Multi-guide: if the runner-up Stage 1 score is >= this fraction of the
# top score AND >= this absolute value, include it alongside the top guide.
_MULTI_GUIDE_RELATIVE_THRESHOLD = 0.6   # runner-up must be >= 60% of top
_MULTI_GUIDE_ABSOLUTE_THRESHOLD = 30.0  # and at least this score

# ---------------------------------------------------------------------------
# Stage 3: LLM-based guide validation (optional)
# ---------------------------------------------------------------------------

# Module-level config for the guide validator model (set via init function)
_validator_api_key: str = ""
_validator_model: str = ""

_VALIDATOR_SYSTEM_PROMPT = """\
You validate whether the correct business rules guide was retrieved for a \
database query. You will see the search term, the selected guide, and a \
list of alternative guides.

Respond with EXACTLY one of:
- "CORRECT" if the selected guide matches the search domain
- "WRONG: <exact title of the better alternative>" if a listed alternative \
is more appropriate
"""


def init_guide_validator(api_key: str, model: str = "openai/gpt-oss-120b") -> None:
    """Initialise the LLM-based guide validator.

    Call this once before evaluations begin. If not called, Stage 3
    validation is silently skipped.
    """
    global _validator_api_key, _validator_model  # noqa: PLW0603
    _validator_api_key = api_key
    _validator_model = model
    _logger.info("Guide validator initialised with model %s", model)


def _validate_guide_selection(
    search_term: str,
    selected: _GuideEntry,
    alternatives: list[_GuideEntry],
) -> _GuideEntry:
    """Validate the selected guide using an LLM; return the best match.

    If the LLM says the selection is wrong and names a valid alternative,
    that alternative is returned. Otherwise the original selection is kept.
    """
    if not _validator_api_key:
        return selected

    alt_lines = "\n".join(
        f"- {e.title} (schema: {e.schema_hint})"
        for e in alternatives
        if e.path != selected.path
    )
    if not alt_lines:
        return selected

    user_content = (
        f"Search term: {search_term}\n\n"
        f"Selected guide: {selected.title} "
        f"(schema: {selected.schema_hint})\n\n"
        f"Alternative guides:\n{alt_lines}"
    )

    try:
        response = completion_request(
            api_key=_validator_api_key,
            model=_validator_model,
            messages=[
                {"role": "system", "content": _VALIDATOR_SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
            temperature=0.0,
        )
        response = response.strip()

        if response.upper().startswith("WRONG:"):
            suggested_title = response[6:].strip().strip('"').strip("'")
            _logger.info(
                "Guide validator override: %s → suggested %s",
                selected.title, suggested_title,
            )
            # Find the suggested alternative (fuzzy title match)
            suggested_lower = suggested_title.lower()
            for alt in alternatives:
                title = (alt.title or alt.path.stem).lower()
                if suggested_lower in title or title in suggested_lower:
                    return alt
            # Try matching on schema hint
            for alt in alternatives:
                if alt.schema_hint and suggested_lower in alt.schema_hint.lower():
                    return alt
            _logger.warning(
                "Validator suggested '%s' but no matching guide found",
                suggested_title,
            )
    except Exception:
        _logger.warning("Guide validator call failed; keeping original", exc_info=True)

    return selected


# ---------------------------------------------------------------------------
# Embedding helpers (local sentence-transformers)
# ---------------------------------------------------------------------------

def _get_embedding_model():
    """Lazily load the sentence-transformers model.

    The model is loaded once and cached in a module-level variable.
    Returns the SentenceTransformer model instance, or None on failure.
    """
    global _embedding_model  # noqa: PLW0603
    if _embedding_model is not None:
        return _embedding_model

    try:
        from sentence_transformers import SentenceTransformer

        _embedding_model = SentenceTransformer(_EMBEDDING_MODEL_NAME)
        _logger.info("Loaded embedding model: %s", _EMBEDDING_MODEL_NAME)
        return _embedding_model
    except Exception:
        _logger.warning(
            "Failed to load sentence-transformers model '%s'; "
            "Stage 2 semantic retrieval will be disabled.",
            _EMBEDDING_MODEL_NAME,
            exc_info=True,
        )
        return None


def _embed_texts(texts: list[str]) -> np.ndarray | None:
    """Embed a list of texts using the local sentence-transformers model.

    Args:
        texts: List of strings to embed.

    Returns:
        A numpy array of shape (len(texts), dim) with L2-normalized
        embeddings, or None if the model is unavailable.
    """
    model = _get_embedding_model()
    if model is None:
        return None
    return model.encode(texts, normalize_embeddings=True)


def _ensure_guide_embeddings() -> bool:
    """Lazily compute and cache embeddings for all guides.

    Returns True if embeddings are available, False otherwise.
    """
    global _guide_embeddings  # noqa: PLW0603
    if _guide_embeddings is not None:
        return True

    summaries = [entry.summary for entry in _GUIDE_INDEX]
    embeddings = _embed_texts(summaries)
    if embeddings is not None:
        _guide_embeddings = embeddings
        _logger.info("Computed embeddings for %d guides", len(summaries))
        return True
    return False


# ---------------------------------------------------------------------------
# Guide indexing (runs once at module load)
# ---------------------------------------------------------------------------

class _GuideEntry:
    """Index entry for a single guide file."""

    __slots__ = (
        "path", "title", "schema_hint", "keywords",
        "content", "summary",
    )

    def __init__(self, path: Path) -> None:
        self.path = path
        self.content = path.read_text(encoding="utf-8")
        self.title = ""
        self.schema_hint = ""
        self.keywords: set[str] = set()
        self.summary = ""
        self._parse()

    def _parse(self) -> None:
        """Extract title, schema hint, keywords, and summary."""
        lines = self.content.split("\n")

        # Title: first H1 line
        for line in lines:
            if line.startswith("# "):
                self.title = line[2:].strip()
                break

        # Schema hint: parenthetical in the title
        paren_match = re.search(r"\(([^)]+)\)", self.title)
        if paren_match:
            inner = paren_match.group(1)
            schema_raw = re.sub(
                r"\s*(Database|DB)\s*$", "", inner,
                flags=re.IGNORECASE,
            ).strip()
            self.schema_hint = schema_raw

        # Summary: title + all H2 headers (used for embedding)
        h2_headers = [
            line[3:].strip()
            for line in lines
            if line.startswith("## ")
        ]
        self.summary = self.title + ". " + ". ".join(h2_headers)

        # Build keyword set from multiple sources
        kw: set[str] = set()

        # 1. File name stem tokens
        for token in self.path.stem.split("_"):
            if len(token) >= 2:
                kw.add(token.lower())

        # 2. Schema hint tokens
        if self.schema_hint:
            kw.add(self.schema_hint.lower())
            for part in re.split(r"[_\s/]+", self.schema_hint):
                if len(part) >= 2:
                    kw.add(part.lower())

        # 3. Title tokens (minus stop words)
        stop_words = {
            "the", "and", "for", "are", "but", "not", "you", "all",
            "can", "her", "was", "one", "our", "out", "has", "its",
            "with", "from", "this", "that", "these", "those", "data",
            "rules", "standards", "guidelines", "database", "analytics",
            "metrics", "conventions", "must", "should", "when",
        }
        for word in re.findall(r"[A-Za-z]+", self.title):
            w = word.lower()
            if len(w) >= 2 and w not in stop_words:
                kw.add(w)

        # 4. H2 header tokens
        for line in lines:
            if line.startswith("## "):
                for word in re.findall(r"[A-Za-z]+", line[3:]):
                    w = word.lower()
                    if len(w) >= 3 and w not in stop_words:
                        kw.add(w)

        # 5. Quoted terms and backtick terms from content body
        for match in re.findall(r"'([^']+)'", self.content):
            if len(match) <= 20:
                kw.add(match.lower())
        for match in re.findall(r"`([^`]+)`", self.content):
            if len(match) <= 30:
                kw.add(match.lower())

        self.keywords = kw


def _build_index() -> list[_GuideEntry]:
    """Build the index over all guide files."""
    entries: list[_GuideEntry] = []
    if GUIDES_DIR.exists():
        for md_file in sorted(GUIDES_DIR.glob("*.md")):
            entries.append(_GuideEntry(md_file))
    return entries


# Module-level index (built once at import)
_GUIDE_INDEX: list[_GuideEntry] = _build_index()


# ---------------------------------------------------------------------------
# Stage 1: Regex / keyword scoring
# ---------------------------------------------------------------------------

def _score_entry(entry: _GuideEntry, search_tokens: list[str]) -> float:
    """Score a guide entry against search tokens. Higher is better."""
    score = 0.0

    for token in search_tokens:
        tok_lower = token.lower()

        # Exact schema hint match (highest priority)
        if entry.schema_hint and tok_lower == entry.schema_hint.lower():
            score += 100.0
            continue

        # Schema hint substring
        if entry.schema_hint and tok_lower in entry.schema_hint.lower():
            score += 50.0
            continue

        # Exact keyword match
        if tok_lower in entry.keywords:
            score += 10.0
            continue

        # Substring match in keywords
        for kw in entry.keywords:
            if tok_lower in kw or kw in tok_lower:
                score += 5.0
                break

        # Substring match in title
        if tok_lower in entry.title.lower():
            score += 3.0
            continue

        # Substring match in file name
        if tok_lower in entry.path.stem.lower():
            score += 2.0
            continue

    return score


# ---------------------------------------------------------------------------
# Stage 2: Semantic embedding similarity
# ---------------------------------------------------------------------------

def _semantic_search(query: str) -> tuple[_GuideEntry, float] | None:
    """Find the best guide via cosine similarity of local embeddings.

    Returns the best entry and its similarity score, or None if
    embeddings are unavailable.
    """
    if not _ensure_guide_embeddings() or _guide_embeddings is None:
        return None

    query_vec = _embed_texts([query])
    if query_vec is None:
        return None

    # Cosine similarity (vectors are already L2-normalized)
    similarities = _guide_embeddings @ query_vec[0]
    best_idx = int(np.argmax(similarities))
    best_sim = float(similarities[best_idx])

    if best_sim >= _STAGE2_SIMILARITY_THRESHOLD:
        return _GUIDE_INDEX[best_idx], best_sim
    return None


# ---------------------------------------------------------------------------
# Public retrieval function (two-stage)
# ---------------------------------------------------------------------------

def _format_catalog() -> str:
    """Return a formatted listing of all available guides."""
    lines: list[str] = [
        f"Available guides ({len(_GUIDE_INDEX)}):",
        "",
    ]
    for entry in _GUIDE_INDEX:
        hint = f"  (schema: {entry.schema_hint})" if entry.schema_hint else ""
        lines.append(f"  - {entry.path.stem}{hint}")
    lines.append("")
    lines.append("Try searching with a schema name or domain keyword.")
    return "\n".join(lines)


def _all_alternatives_for(
    selected: _GuideEntry,
    scored: list[tuple[float, _GuideEntry]],
) -> list[_GuideEntry]:
    """Collect candidate alternatives for the LLM validator."""
    seen_paths: set[Path] = {selected.path}
    alts: list[_GuideEntry] = []

    # Start with scored entries (they have some keyword relevance)
    for _, entry in scored:
        if entry.path not in seen_paths:
            alts.append(entry)
            seen_paths.add(entry.path)
        if len(alts) >= 10:
            return alts

    # Pad with remaining guides from the full index
    for entry in _GUIDE_INDEX:
        if entry.path not in seen_paths:
            alts.append(entry)
            seen_paths.add(entry.path)
        if len(alts) >= 10:
            break

    return alts


def _should_include_second_guide(
    top_score: float, runner_up_score: float,
) -> bool:
    """Return True if the runner-up is close enough to warrant inclusion."""
    return (
        runner_up_score >= _MULTI_GUIDE_ABSOLUTE_THRESHOLD
        and runner_up_score >= top_score * _MULTI_GUIDE_RELATIVE_THRESHOLD
    )


def _format_multi_guide_result(
    primary: _GuideEntry,
    secondary: _GuideEntry | None,
    close_alternatives: list[str],
) -> str:
    """Assemble the final return string for get_business_rules.

    When a secondary guide is included, it is appended with a clear
    separator so the agent can see both.  Any remaining alternatives are
    listed at the end so the agent knows to call again if needed.
    """
    result = primary.content

    if secondary is not None:
        result += (
            "\n\n===== ADDITIONAL GUIDE (also relevant) =====\n\n"
            + secondary.content
        )

    if close_alternatives:
        result += (
            "\n\n---\nOther potentially relevant guides "
            "(call get_business_rules again with a different keyword "
            "if the question spans multiple domains): "
            + ", ".join(close_alternatives)
        )

    return result


def get_business_rules(search_term: str) -> str:
    """Search for business rules guides by schema name, domain, or keyword.

    Uses three-stage retrieval:
      Stage 1 — regex/keyword scoring (fast, deterministic).
      Stage 2 — semantic embedding similarity (when Stage 1 is uncertain).
      Stage 3 — LLM validation of the selected guide (if configured).

    When two guides score closely (runner-up >= 60% of top AND >= 30 pts),
    both are returned in a single response so the agent has full context
    without needing a second call.

    Args:
        search_term: A schema name, domain keyword, or topic to search for.

    Returns:
        The full content of the best-matching guide (and optionally a second
        guide), or a list of available guides if no confident match is found.
    """
    if not _GUIDE_INDEX:
        return "No business rules guides found."

    # Tokenize the search term
    search_tokens = [
        t for t in re.split(r"[\s,_/]+", search_term) if len(t) >= 2
    ]
    if not search_tokens:
        search_tokens = [search_term.strip()]

    # ------------------------------------------------------------------
    # Stage 1: regex / keyword scoring + BM25 full-text
    # ------------------------------------------------------------------
    scored: list[tuple[float, _GuideEntry]] = []
    for entry in _GUIDE_INDEX:
        s = _score_entry(entry, search_tokens)
        if s > 0:
            scored.append((s, entry))
    scored.sort(key=lambda x: x[0], reverse=True)

    if scored and scored[0][0] >= _STAGE1_CONFIDENCE_THRESHOLD:
        top_score, best = scored[0]
        # Stage 3: LLM validation (may swap to a better alternative)
        best = _validate_guide_selection(
            search_term, best, _all_alternatives_for(best, scored),
        )

        # Multi-guide: include runner-up when scores are close
        secondary: _GuideEntry | None = None
        if len(scored) >= 2:
            runner_score, runner = scored[1]
            if (
                runner.path != best.path
                and _should_include_second_guide(top_score, runner_score)
            ):
                secondary = runner

        # Collect remaining alternatives for the footer hint
        close_alternatives = [
            e.title or e.path.stem
            for s, e in scored[2:5]
            if s >= 5.0 and e.path != best.path
            and (secondary is None or e.path != secondary.path)
        ]

        return _format_multi_guide_result(best, secondary, close_alternatives)

    # ------------------------------------------------------------------
    # Stage 2: semantic embedding similarity
    # ------------------------------------------------------------------
    semantic_result = _semantic_search(search_term)
    if semantic_result is not None:
        best_entry, similarity = semantic_result
        # Stage 3: LLM validation
        best_entry = _validate_guide_selection(
            search_term, best_entry, _all_alternatives_for(best_entry, scored),
        )

        # Mention the Stage 1 top candidate if it differs
        footer: list[str] = []
        if scored and scored[0][1].path != best_entry.path:
            footer.append(scored[0][1].title or scored[0][1].path.stem)

        return _format_multi_guide_result(best_entry, None, footer)

    # ------------------------------------------------------------------
    # Fallback: use Stage 1 results even if weak, or show catalog
    # ------------------------------------------------------------------
    if scored and scored[0][0] >= 10.0:
        best = scored[0][1]
        best = _validate_guide_selection(
            search_term, best, _all_alternatives_for(best, scored),
        )
        others = [
            e.title or e.path.stem
            for _, e in scored[1:4] if _ >= 5.0
        ]
        return _format_multi_guide_result(best, None, others)

    if scored and scored[0][0] >= 2.0:
        best = scored[0][1]
        best = _validate_guide_selection(
            search_term, best, _all_alternatives_for(best, scored),
        )
        return (
            f"Best match (confidence: moderate):\n\n{best.content}\n\n"
            f"---\n{_format_catalog()}"
        )

    return f"No strong match for '{search_term}'.\n{_format_catalog()}"


GET_BUSINESS_RULES: Tool = Tool(
    name="get_business_rules",
    description=(
        "Retrieve business rules for a specific domain or database schema. "
        "These rules define critical filters, exclusions, calculations, and "
        "classifications that MUST be applied when writing SQL queries. "
        "Search by schema name, domain keyword, or topic. "
        "ALWAYS call this tool before writing any SQL query."
    ),
    parameters={
        "type": "object",
        "properties": {
            "search_term": {
                "type": "string",
                "description": (
                    "A schema name, domain keyword, or topic to search for. "
                    "Examples: schema name (e.g. 'Sales', 'Inventory'), "
                    "domain (e.g. 'analytics', 'reporting'), or topic "
                    "(e.g. 'transactions', 'delays', 'classifications')."
                ),
            },
        },
        "required": ["search_term"],
    },
    function=get_business_rules,
)
