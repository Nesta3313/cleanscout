# cleanscout

**cleanscout** is a tiny, reusable toolkit for **data cleaning + quick EDA**.  
It deliberately excludes modeling/pipelines.

## Install (editable for local dev)
```bash
pip install -U pip build
pip install -e .
# optional extras
pip install 'ydata-profiling>=4.6.0'
```

## Quick start
```python
import pandas as pd
from cleanscout import (
    standardize_text, coerce_numeric_like, parse_dates_by_name,
    drop_exact_duplicates, fix_negative_to_nan, iqr_clip,
    collapse_rare, canonical_map,
    profile_table, plot_distributions, plot_missingness, correlation_heatmap,
    generate_report_html
)

df = pd.read_csv("data.csv")

# Non-learning cleaning
df = parse_dates_by_name(df)
for c in ["price","sales","cogs"]:
    if c in df: df[c] = coerce_numeric_like(df[c])
text_cols = [c for c in df.select_dtypes(include=["object","string"]).columns]
df = standardize_text(df, text_cols)
df = drop_exact_duplicates(df)
if "price" in df: df = fix_negative_to_nan(df, ["price"])

# Quick profile + simple plots
print(profile_table(df).head(10))
plot_missingness(df, outpath="reports/missing.png")
correlation_heatmap(df, outpath="reports/corr.png")
generate_report_html(df, outdir="reports", title="My EDA Report")
```

## What it includes
- **Cleaning:** text standardization, numeric coercion (currency/commas), date parsing by name,
  duplicate removal, negative-to-NaN for specific columns, **IQR clipping**, rare-category collapse,
  canonical mapping (e.g., DHL/dhl → DHL).
- **EDA:** compact profile table; simple histograms, missingness bar chart, correlation heatmap.
- **Reports:** optional **ydata-profiling** HTML if installed; otherwise a minimal HTML with PNGs.

## Philosophy
- Keep “learning” transforms (imputers/encoders/scalers) **out** of this package to avoid teaching leakage.
- Use it as a **pre-EDA** helper; do modeling pipelines in your project code.

## License
MIT
