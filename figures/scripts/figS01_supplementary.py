import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import linregress

from severs_scirep_16s.config import FIGURES_OUTPUT_DIR, PROCESSED_DATA_DIR, RAW_DATA_DIR
from severs_scirep_16s.plotting import save_figure, set_plot_style

FIGURE_NAME = "figS01_hac_vs_sup_reads"
INPUT_FILE = RAW_DATA_DIR / "20250714_mastersheet_HAC_SUP.csv"
OUTLIERS_CSV = PROCESSED_DATA_DIR / "figS01_read_count_outliers.csv"


def load_read_totals() -> pd.DataFrame:
    df = pd.read_csv(INPUT_FILE, sep=";", low_memory=False)
    df = df.rename(columns={"Unnamed: 0": "Center", "Unnamed: 1": "Basecaller", "Unnamed: 2": "Sample"})

    # OTU columns = everything except metadata
    otu_cols = [c for c in df.columns if c not in ["Center", "Basecaller", "Sample", "Sample_ID"]]

    hac_samples = df[df["Basecaller"] == "HAC"].copy()
    sup_samples = df[df["Basecaller"] == "SUP"].copy()
    hac_samples["Reads_HAC"] = hac_samples[otu_cols].sum(axis=1)
    sup_samples["Reads_SUP"] = sup_samples[otu_cols].sum(axis=1)

    # Match HAC and SUP on Sample
    return pd.merge(
        hac_samples[["Sample", "Reads_HAC"]],
        sup_samples[["Sample", "Reads_SUP"]],
        on="Sample",
    )


def main() -> None:
    set_plot_style()
    otu_summary = load_read_totals()

    # --- Plot 1: raw read counts ---------------------------------------------
    fig1, ax1 = plt.subplots()
    ax1.scatter(otu_summary["Reads_SUP"], otu_summary["Reads_HAC"], alpha=0.7)

    max_val = max(otu_summary["Reads_SUP"].max(), otu_summary["Reads_HAC"].max())
    ax1.plot([0, max_val], [0, max_val], "--", color="gray")

    slope, intercept, r_value, p_value, std_err = linregress(otu_summary["Reads_SUP"], otu_summary["Reads_HAC"])
    x_vals = np.array([0, max_val])
    ax1.plot(x_vals, intercept + slope * x_vals, color="red", label=f"Fit: $R^2$={r_value**2:.3f}")
    ax1.legend()
    ax1.set_xlabel("Reads (SUP)")
    ax1.set_ylabel("Reads (HAC)")
    fig1.tight_layout()

    # --- Outliers: |HAC - SUP| > mean + 2 SD of the absolute difference ------
    otu_summary["abs_diff"] = np.abs(otu_summary["Reads_HAC"] - otu_summary["Reads_SUP"])
    outlier_threshold = otu_summary["abs_diff"].mean() + 2 * otu_summary["abs_diff"].std()
    outliers = otu_summary[otu_summary["abs_diff"] > outlier_threshold]
    if outliers.empty:
        print("No outliers found (|HAC - SUP| > 2 std from mean).")
    else:
        OUTLIERS_CSV.parent.mkdir(parents=True, exist_ok=True)
        outliers.to_csv(OUTLIERS_CSV, index=False)
        print(outliers)

    # --- Plot 2: log10-transformed read counts -------------------------------
    otu_summary["Reads_HAC_log"] = np.log10(otu_summary["Reads_HAC"] + 1)
    otu_summary["Reads_SUP_log"] = np.log10(otu_summary["Reads_SUP"] + 1)

    fig2, ax2 = plt.subplots(figsize=(8, 6))
    ax2.scatter(otu_summary["Reads_SUP_log"], otu_summary["Reads_HAC_log"], alpha=0.7)

    max_val_log = max(otu_summary["Reads_SUP_log"].max(), otu_summary["Reads_HAC_log"].max())
    ax2.plot([0, max_val_log], [0, max_val_log], "--", color="gray")

    slope_l, intercept_l, r_l, p_l, se_l = linregress(otu_summary["Reads_SUP_log"], otu_summary["Reads_HAC_log"])
    x_log = np.array([otu_summary["Reads_SUP_log"].min(), otu_summary["Reads_SUP_log"].max()])
    ax2.plot(x_log, intercept_l + slope_l * x_log, color="red", label=f"Fit: $R^2$={r_l**2:.3f}")
    ax2.legend()
    ax2.set_xlabel("Reads (SUP, log10)")
    ax2.set_ylabel("Reads (HAC, log10)")
    fig2.tight_layout()

    save_figure(fig1, FIGURES_OUTPUT_DIR / f"{FIGURE_NAME}_linear.pdf")
    save_figure(fig1, FIGURES_OUTPUT_DIR / f"{FIGURE_NAME}_linear.png")
    save_figure(fig2, FIGURES_OUTPUT_DIR / f"{FIGURE_NAME}_log10.pdf")
    save_figure(fig2, FIGURES_OUTPUT_DIR / f"{FIGURE_NAME}_log10.png")
    plt.close(fig1)
    plt.close(fig2)


if __name__ == "__main__":
    main()
