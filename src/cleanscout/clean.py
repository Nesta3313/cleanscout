from __future__ import annotations
import numpy as np
import pandas as pd
from typing import Dict, Iterable, Tuple

def standardize_text(df: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    """Trim/normalize whitespace for given text columns."""
    out = df.copy()
    for c in columns:
        out[c] = (out[c].astype("string")
                    .str.normalize("NFKC")
                    .str.replace(r"\s+", " ", regex=True)
                    .str.strip())
    return out

def coerce_numeric_like(s: pd.Series) -> pd.Series:
    """Convert currency/comma strings to numeric; non-numeric -> NaN."""
    if pd.api.types.is_numeric_dtype(s):
        return s
    if pd.api.types.is_string_dtype(s) or s.dtype == "object":
        stripped = (s.astype("string")
                      .str.replace(r"[,$\s]", "", regex=True)
                      .str.replace(",", ".", regex=False))  # handle 99,99
        return pd.to_numeric(stripped, errors="coerce")
    return s

def parse_dates_by_name(df: pd.DataFrame, tokens=("date","_at","time")) -> pd.DataFrame:
    """Parse columns that look like dates."""
    out = df.copy()
    for c in out.columns:
        cl = c.lower()
        if any(tok in cl for tok in tokens):
            out[c] = pd.to_datetime(out[c], errors="coerce")
    return out

def drop_exact_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Drop exact duplicate rows."""
    return df.drop_duplicates()

def fix_negative_to_nan(df: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    """Set negative values to NaN for columns that should be non-negative."""
    out = df.copy()
    for c in columns:
        if c in out:
            out.loc[out[c] < 0, c] = np.nan
    return out

def iqr_bounds(s: pd.Series, k: float = 1.5) -> Tuple[float, float]:
    q1, q3 = s.quantile([0.25, 0.75])
    iqr = q3 - q1
    return q1 - k*iqr, q3 + k*iqr

def iqr_clip(df: pd.DataFrame, columns: Iterable[str], k: float = 1.5) -> pd.DataFrame:
    """Clip numeric columns to Tukey fences (safer than dropping rows)."""
    out = df.copy()
    for c in columns:
        if c in out and pd.api.types.is_numeric_dtype(out[c]):
            lo, hi = iqr_bounds(out[c].dropna(), k=k)
            out[c] = out[c].clip(lower=lo, upper=hi)
    return out

def collapse_rare(s: pd.Series, min_frac=0.01, other_label="__other__") -> pd.Series:
    """Group infrequent categories to a single level."""
    counts = s.value_counts(dropna=False, normalize=True)
    rare = counts[counts < min_frac].index
    return s.where(~s.isin(rare), other_label)

def canonical_map(s: pd.Series, mapping: Dict[str, str]) -> pd.Series:
    """Map variants to canonical labels (e.g., DHL/dhl/U.S.P.S. -> USPS)."""
    return s.map(mapping).fillna(s)
