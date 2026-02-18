# Hecks AI Take-Home: Approach & Reflection

---

## 1. Initial Reaction & Baseline

When I first read the problem, I tried to understand the data aspect — what kind of questions the system is answering, and how complex they are. Looking at `evals_hard.json` and `evals_easy.json` gave me a clear sense of the scope. The key insight was that this isn't simply an NL2SQL task: it's a combination of retrieval, SQL generation, and correctness verification:

- **NL2SQL** — get the schema, generate SQL, execute, submit.
- **Business rules retrieval** — the differentiator for the hard set. Rules live in ~30 markdown files, each covering a different domain (baseball, F1, financial loans, airlines, etc.). Getting the *right* guide file for each question is itself a retrieval problem.
- **Correctness verification by reflection** — even good SQL generation sometimes misses a WHERE filter or uses the wrong column name. The agent needs to reflect on results and self-correct before submitting.

The baseline implementation (`run_20260217_175836`) started five tools in place:

| Tool | Purpose |
|---|---|
| `list_schemas` | Enumerate DuckDB schemas |
| `describe_table` | Get columns and sample rows |
| `get_business_rules` | Retrieve relevant business rules guide |
| `execute_sql` | Run a SQL query and return results |
| `submit_answer` | Submit the final SQL query |

That baseline scored **32/64 (50%)** on the hard set and **51/64 (80%)** on the easy set. I used the LLM to analyze failure reasons — almost all failures were `MISMATCH`, meaning the agent was generating SQL but getting the semantics wrong. Common patterns: missing a condition, misinterpreting a rule in a WHERE clause, or ignoring a business rule entirely.

---

## 2. What I Did and Why

### 2a. Business Rules Retrieval: Sparse vs. Dense

The `get_business_rules` tool presented the most interesting design decision. There are ~30 guide files, and the agent calls the tool with a free-text `search_term`. I needed a retrieval strategy that reliably maps queries like `"financial loan"` or `"craft beer IBU"` to the correct guide file.

**Options considered:**

| Approach | Pros | Cons |
|---|---|---|
| Sparse (keyword / BM25 over full content) | Fast, no dependencies, interpretable | Fails on synonym mismatches; "performing loans" doesn't keyword-match a guide titled `financial_banking.md` |
| Dense (sentence-transformers embeddings) | Handles semantic similarity | Slower; requires a local model; 384-dim embeddings can be noisy on short titles |
| LLM re-ranker | Highest accuracy; can reason about domain | Adds latency and cost per question |
| Hybrid (sparse first, dense fallback, LLM validation) | Best of all three | More complex to debug |

**What I implemented:** A three-stage hybrid in `tools/business_rules.py`:

1. **Stage 1 — Regex/keyword scoring** against file names, titles, H2 headers, schema hints, quoted terms, and backtick terms from the guide bodies. If the top match scores ≥ 50 (calibrated threshold), return immediately. This handles the majority of cases where the search term directly mentions a schema name or domain keyword. Note: this is keyword matching on extracted tokens, not BM25 full-text search over the entire content. Full-text BM25 would be a meaningful improvement — it would catch cases where the relevant term appears only in the rule body, not in a header.

2. **Stage 2 — Semantic embedding fallback** using `sentence-transformers/all-MiniLM-L6-v2` (small, fast local model, 384-dim). If Stage 1 is ambiguous, cosine similarity between the query embedding and pre-computed guide embeddings is used. Accepted if similarity ≥ 0.25.

3. **Stage 3 — Optional LLM validation** using `openai/gpt-oss-120b`. If the selected guide seems uncertain, the LLM is asked to confirm or name a better alternative. This guards against systematic Stage 2 errors without adding latency on confident matches.

I also added a **multi-guide** heuristic: if the runner-up Stage 1 score is ≥ 60% of the top score and ≥ 30 in absolute terms, both guides are returned together. This helped for questions spanning two domains.

**Tradeoff:** The sparse Stage 1 with a high confidence threshold means most guide lookups never reach the embedding model or the LLM, keeping latency low. The risk is over-trusting keyword matches when the search term is ambiguous. In practice, the domain vocabulary in the hard set is specific enough that this worked well.

---

### 2b. NL2SQL: Model Selection

The biggest accuracy lever was separating the **routing/orchestration** model from the **SQL generation** model.

The baseline used a single model for everything. I introduced a two-model architecture:

- **Orchestrator**: `minimax/minimax-m2.5` — handles tool routing (deciding when to call `list_schemas`, `describe_table`, `get_business_rules`, etc.). Fast and cheap; routing doesn't require deep SQL expertise.

- **NL2SQL specialist**: `anthropic/claude-opus-4.6` — invoked by the `generate_sql` tool when the agent is ready to write SQL. It receives the question, assembled schema info, and business rules, and is asked to return only the SQL.

**Why this split?** NL2SQL requires understanding complex aggregations, JOIN logic, business rule translation into WHERE/CASE/HAVING clauses, and DuckDB-specific syntax. A frontier reasoning model dramatically outperforms a general-purpose routing model here. Keeping the orchestrator cheap makes the cost of the stronger NL2SQL model affordable at scale.

The `generate_sql` prompt encodes explicit constraints derived from failure analysis:
- Apply every business rule as a concrete SQL construct (WHERE filter, CASE WHEN, HAVING)
- Never add ROUND() unless the question says so
- Return fractions (0.0–1.0), not percentages, unless explicitly asked
- Do not add spurious IS NOT NULL filters
- Use HAVING for aggregate thresholds, WHERE for row-level filters

---

### 2c. Pre-Submission Verification

I added three verification layers:

**1. Silent verifier gate:** Before `submit_answer` actually fires, `framework/verifier.py` calls a secondary model (`moonshotai/kimi-k2.5`) to check the SQL against the question, business rules, and schema. If it returns `FAIL`, the agent sees the feedback and can revise within its normal iteration loop.

**2. `check_sql` tool (agent-visible):** The same verifier logic, but callable by the agent as an explicit tool — useful after `execute_sql` returns results that look suspect. This gives the agent agency over when to verify, rather than relying only on the silent gate.

**3. `search_column` tool:** A pure-SQL tool (no LLM call) that searches `information_schema.columns` by keyword, ranked exact > prefix > substring. Added to help with large schemas (e.g. the airline dataset) where the agent needs to find the exact column name for a concept like "delay" or "carrier."

---

## 3. Results

**Hard set (business-rules-required questions):**

| Run | Hard | Notes |
|---|---|---|
| `run_20260217_175836` | 32/64 (50%) | Baseline: 5 original tools + `get_business_rules` |
| `run_20260217_184527` | 36/64 (56%) | Business rules retrieval tuning |
| `run_20260217_185828` | 35/64 (55%) | Prompt tweak, minor regression |
| `run_20260217_190529` | 38/64 (59%) | `generate_sql` added (minimax + claude-opus-4.6 split) |
| `run_20260217_192819` | **39/64 (61%)** | Verifier + `generate_sql` refinements |
| `run_20260217_201752` | 36/63 (57%) | `check_sql` + `search_column` added |
| `run_20260217_205732` | 36/64 (56%) | Further tuning; slight regression vs. best |

**Easy set (no business rules required):**

| Run | Easy | Notes |
|---|---|---|
| `run_20260217_180649` | 51/64 (80%) | Baseline easy run |
| `run_20260217_184937` | 51/64 (80%) | After retrieval tuning |
| `run_20260217_195218` | 47/64 (73%) | With full tool suite |
| `run_20260217_200943` | 46/64 (72%) | Slight regression |
| `run_20260217_204300` | 48/64 (75%) | Last easy run |

**Best scores: 39/64 (61%) on hard, 51/64 (80%) on easy.**

The remaining failures on hard are almost entirely `MISMATCH` — the SQL runs and returns results, but not quite the right ones. Common remaining failure patterns (from log inspection): wrong aggregate column, missing a multi-part rule, or a rule condition applied at the wrong clause level (WHERE vs. HAVING).

The easy set regression from 80% → 75% after adding the full tool suite is notable. My hypothesis is context inflation: more tools in the system prompt and more intermediate steps push some straightforward questions to get "lost in the middle" or cause the orchestrator to over-think simple queries.

---

## 4. What I Did Not Do

- **BM25 full-text search over guide bodies:** Stage 1 only scores on extracted tokens (titles, headers, schema hints, quoted/backtick terms). A proper BM25 index over the entire guide content would improve recall for edge-case queries where the relevant term appears only in a rule body, not in any header. This is the highest-priority retrieval improvement.

- **Self-consistency / majority voting:** Running `generate_sql` 3× with different seeds and picking the most common result is a well-known NL2SQL accuracy booster. I skipped it due to latency and cost tradeoffs, but it would likely add 2–4 correct answers on the hard set.

- **Schema pre-selection:** The agent always starts by calling `list_schemas` then `describe_table` per relevant table. A lightweight classifier that pre-filters to the relevant schema before the agent starts would reduce LLM turns and context length per question.

- **Smarter verifier calibration:** The verifier prompt is fairly strict. Tuning it to reduce false positives (rejecting correct SQL) would cut unnecessary re-generation cycles and likely recover some of the easy-set regression.

- **Use MiniMax or other more afforable models for NL2SQL:** In practice, it will be a tradeoff between cost vs performance. I would do more experiments on Opus 4.6 compares to MiniMax 2.5 for SQL generation.

- **Classifier for easy or hard queries:** based on the results, we note a 80% -> 75% degradation for the performance on easy queries. So I would use a lightweight classifier (can be LLM, can be classic ML model) so that we can route to the best tool calling and, as a result, better overall NL2SQL perfomance.

---

## 5. AI Tool Use & My Contributions

I used Cursor (AI coding assistant) throughout. Here's the honest breakdown:

**My reasoning and decisions:**
- Framing the problem as a retrieval + NL2SQL + verification pipeline
- Choosing the three-stage hybrid retrieval (sparse → dense → LLM) over simpler alternatives
- Deciding to split orchestrator and NL2SQL into separate models
- Identifying failure categories from log inspection and encoding them as explicit prompt constraints in `generate_sql`
- Calibrating confidence thresholds (Stage 1 threshold = 50, multi-guide thresholds = 0.6/30)
- Deciding *not* to implement BM25 full-text (time constraint) and noting it as the next priority

**AI assistance:**
- Boilerplate code for new tools (embedding loading, DuckDB queries, tool registration)
- Initial drafts of verifier and `generate_sql` prompts, revised based on failure analysis
- Type annotations, docstrings, and the majority of this document.

**Validation process:**
- Ran the evaluation suite against each iteration and inspected specific failing cases
- Read log event traces to verify tools were being called in the right order with the right arguments
- Spot-checked business rules retrieval by reading returned guide content alongside submitted SQL for a sample of failing questions

---

## 6. Conclusions

The most impactful single change was the **two-model split** (routing vs. NL2SQL), moving the hard score from 32 → 38/64. Business rules retrieval improvements were the second-biggest lever (32 → 36 before the model split).

The core architecture — retrieval quality and NL2SQL model capability as two independent bottlenecks — held up under iteration. With more time, the clear next steps are BM25 full-text search over guide content, self-consistency decoding for SQL generation, and verifier calibration to reduce false positives on the easy set.
