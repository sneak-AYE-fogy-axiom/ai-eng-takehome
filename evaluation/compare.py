"""Loose dataframe comparison utilities for evaluation.

This module provides functions to compare dataframes with flexible matching rules,
suitable for comparing SQL query results where exact formatting may differ.
"""

from __future__ import annotations

import math
from itertools import product

import polars as pl

# Default tolerance for floating point comparison
DEFAULT_EPSILON: float = 1e-4


def _epsilon_to_precision(epsilon: float) -> int:
    """Convert an epsilon tolerance to an appropriate float precision.

    The precision is chosen such that values within epsilon will typically
    normalize to the same string representation.

    Args:
        epsilon: The tolerance for floating point comparison.

    Returns:
        Number of decimal places to use for normalization.
    """
    if epsilon <= 0:
        return 9  # Fallback to high precision
    # Use one fewer decimal place than the epsilon magnitude
    # e.g., epsilon=1e-6 -> precision=5
    return max(0, -int(math.floor(math.log10(epsilon))) - 1)


def _normalize_value(value: object, float_precision: int = 6) -> str:
    """Normalize a value to a canonical string for comparison.

    This handles:
    - int vs float equivalence (1 == 1.0)
    - Floating point precision issues (0.1 + 0.2 ≈ 0.3)
    - None/null values

    Args:
        value: The value to normalize.
        float_precision: Number of decimal places to round floats to.

    Returns:
        A normalized string representation.
    """
    if value is None:
        return "__NULL__"

    # Handle numeric types with special care
    if isinstance(value, float):
        # Check for NaN
        if value != value:  # NaN != NaN
            return "__NAN__"
        # Check for infinity
        if value == float("inf"):
            return "__INF__"
        if value == float("-inf"):
            return "__NEG_INF__"
        # Round to handle precision issues
        rounded = round(value, float_precision)
        # If it's effectively an integer, represent as integer
        if rounded == int(rounded):
            return str(int(rounded))
        # Otherwise, use rounded float representation
        # Strip trailing zeros for consistency
        return f"{rounded:.{float_precision}f}".rstrip("0").rstrip(".")

    if isinstance(value, int):
        return str(value)

    if isinstance(value, bool):
        # Handle bool before int check (bool is subclass of int in Python)
        return str(value)

    # For all other types, use string representation
    return str(value)


def loosely_compare_dataframes(
    gold_df: pl.DataFrame,
    submitted_df: pl.DataFrame,
    epsilon: float = DEFAULT_EPSILON,
) -> bool:
    """Compare two dataframes loosely.

    The comparison allows:
    - Extra columns in submitted dataframe (ignored)
    - Different column names (matched by content)
    - Different row ordering (compared as multisets)
    - Numeric type flexibility (int 1 == float 1.0)
    - Floating point tolerance (values within epsilon are equal)

    Args:
        gold_df: The expected dataframe from the gold query.
        submitted_df: The dataframe from the submitted query.
        epsilon: Tolerance for floating point comparison (default 1e-6).

    Returns:
        True if the dataframes match under the loose comparison rules.
    """
    # Row count must match exactly
    if gold_df.height != submitted_df.height:
        return False

    # Empty dataframes trivially match, but this shouldn't actually happen
    if gold_df.height == 0:
        raise ValueError("Empty dataframe returned from gold query")

    # Column count check: submitted must have at least as many columns as gold
    if submitted_df.width < gold_df.width:
        return False

    gold_cols = gold_df.columns
    float_precision = _epsilon_to_precision(epsilon)

    def col_to_multiset(df: pl.DataFrame, col: str) -> tuple[str, ...]:
        """Convert a column to a sorted tuple of normalized values for comparison."""
        return tuple(
            sorted(_normalize_value(v, float_precision) for v in df[col].to_list())
        )

    # For each gold column, find candidate submitted columns with matching value multisets
    candidates: dict[str, list[str]] = {g: [] for g in gold_cols}
    for g_col in gold_cols:
        g_multiset = col_to_multiset(gold_df, g_col)
        for s_col in submitted_df.columns:
            if col_to_multiset(submitted_df, s_col) == g_multiset:
                candidates[g_col].append(s_col)
        # If no candidates found for a gold column, comparison fails
        if not candidates[g_col]:
            return False

    # Try all valid column assignments (each gold col maps to a unique submitted col)
    # This handles the case where multiple gold columns have identical value multisets
    for assignment in product(*[candidates[g] for g in gold_cols]):
        # Check that each submitted column is used at most once
        if len(set(assignment)) != len(assignment):
            continue

        mapping = dict(zip(gold_cols, assignment, strict=True))

        # Build comparable row tuples using normalized values
        gold_rows = sorted(
            tuple(_normalize_value(v, float_precision) for v in row)
            for row in gold_df.rows()
        )
        submitted_rows = sorted(
            tuple(
                _normalize_value(submitted_df[mapping[g]][i], float_precision)
                for g in gold_cols
            )
            for i in range(submitted_df.height)
        )

        if gold_rows == submitted_rows:
            return True

    return False
