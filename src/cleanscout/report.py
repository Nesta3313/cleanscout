import os
import pandas as pd

def generate_report_html(df: pd.DataFrame, outdir: str, title: str = "Cleanscout Report") -> str:
    os.makedirs(outdir, exist_ok=True)

    # Lazy, optional import — avoids IDE “unresolved” at module import time
    ProfileReport = None
    try:
        from ydata_profiling import ProfileReport  # type: ignore
    except Exception:
        pass

    if ProfileReport is not None:
        prof = ProfileReport(df, title=title, minimal=True)
        path = os.path.join(outdir, "profile.html")
        prof.to_file(path)
        return path

    # Fallback minimal report
    from .eda import profile_table, plot_distributions, plot_missingness, correlation_heatmap
    pt = profile_table(df)
    pt.to_csv(os.path.join(outdir, "profile_table.csv"), index=True)

    files = []
    files += plot_distributions(df, outdir=outdir)
    if plot_missingness(df, outpath=os.path.join(outdir, "missing.png")):
        files.append(os.path.join(outdir, "missing.png"))
    if correlation_heatmap(df, outpath=os.path.join(outdir, "corr.png")):
        files.append(os.path.join(outdir, "corr.png"))

    html_path = os.path.join(outdir, "report_minimal.html")
    with open(html_path, "w") as f:
        f.write(f"<h1>{title}</h1><p>Profile table saved.</p>")
        for p in files:
            f.write(f"<div><img src='{os.path.basename(p)}' width='600'></div>")
    return html_path
