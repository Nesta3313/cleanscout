import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Optional

def profile_table(df: pd.DataFrame) -> pd.DataFrame:
    """Return a compact profile table: dtype, non-null, missing%, unique."""
    return pd.DataFrame({
        "dtype": df.dtypes.astype(str),
        "non_null": df.notna().sum(),
        "missing": df.isna().sum(),
        "missing_pct": (df.isna().sum() / len(df)).round(4),
        "n_unique": df.nunique(dropna=False),
    })

def plot_distributions(df: pd.DataFrame, numeric_max: int = 12, figsize=(4,3), outdir: Optional[str]=None) -> List[str]:
    """Quick histograms for up to `numeric_max` numeric columns."""
    files = []
    num_cols = df.select_dtypes(include=[np.number]).columns[:numeric_max]
    for c in num_cols:
        plt.figure(figsize=figsize)
        df[c].plot(kind="hist", bins=30)
        plt.title(f"Distribution: {c}")
        plt.tight_layout()
        if outdir:
            import os
            os.makedirs(outdir, exist_ok=True)
            path = f"{outdir}/dist__{c}.png"
            plt.savefig(path, dpi=150)
            files.append(path)
        plt.close()
    return files

def plot_missingness(df: pd.DataFrame, outpath: Optional[str]=None) -> Optional[str]:
    """Simple missingness bar chart (matplotlib only)."""
    miss = (df.isna().sum() / len(df)).sort_values(ascending=False)
    plt.figure(figsize=(6,3))
    miss.head(30).plot(kind="bar")
    plt.title("Missingness (top 30)")
    plt.ylabel("fraction")
    plt.tight_layout()
    if outpath:
        import os
        os.makedirs(os.path.dirname(outpath), exist_ok=True)
        plt.savefig(outpath, dpi=150)
        plt.close()
        return outpath
    plt.close()
    return None

def correlation_heatmap(df: pd.DataFrame, outpath: Optional[str]=None) -> Optional[str]:
    """Naive Pearson correlation heatmap for numeric columns."""
    corr = df.select_dtypes(include=[np.number]).corr(numeric_only=True)
    plt.figure(figsize=(5,4))
    im = plt.imshow(corr, aspect="auto")
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
    plt.yticks(range(len(corr.index)), corr.index)
    plt.colorbar(im, fraction=0.046, pad=0.04)
    plt.title("Correlation (numeric)")
    plt.tight_layout()
    if outpath:
        import os
        os.makedirs(os.path.dirname(outpath), exist_ok=True)
        plt.savefig(outpath, dpi=150)
        plt.close()
        return outpath
    plt.close()
    return None
