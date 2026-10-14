import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from severs_scirep_16s.config import FIGURES_OUTPUT_DIR, PROCESSED_DATA_DIR, RAW_DATA_DIR
from severs_scirep_16s.plotting import save_figure, set_plot_style

INPUT_CSV = RAW_DATA_DIR / "INPUT.csv"
OUTLIERS_CSV = PROCESSED_DATA_DIR / "bland_altman_outliers.csv"
FIGURE_NAME = "fig05_bland_altman_taxon_level"


def compute_bland_altman(df: pd.DataFrame):
    hac_means = df.groupby("OTU")["HAC"].sum()
    sup_means = df.groupby("OTU")["SUP"].sum()
    all_otus = sorted(set(hac_means.index).union(set(sup_means.index)))

    ba_df = pd.DataFrame({
        "OTU": all_otus,
        "HAC": hac_means.reindex(all_otus, fill_value=0).values,
        "SUP": sup_means.reindex(all_otus, fill_value=0).values,
    })
    ba_df["HAC"] = pd.to_numeric(ba_df["HAC"], errors="coerce")
    ba_df["SUP"] = pd.to_numeric(ba_df["SUP"], errors="coerce")
    ba_df = ba_df.dropna(subset=["HAC", "SUP"])

    # log10 with pseudocount of 1
    ba_df["HAC_log"] = np.log10(ba_df["HAC"] + 1)
    ba_df["SUP_log"] = np.log10(ba_df["SUP"] + 1)
    ba_df["Mean"] = ba_df[["HAC_log", "SUP_log"]].mean(axis=1)
    ba_df["Difference"] = ba_df["HAC_log"] - ba_df["SUP_log"]

    mean_diff = ba_df["Difference"].mean()
    sd_diff = ba_df["Difference"].std()
    return ba_df, mean_diff, mean_diff - 1.96 * sd_diff, mean_diff + 1.96 * sd_diff


def main() -> None:
    set_plot_style()
    df = pd.read_csv(INPUT_CSV, sep=";", low_memory=False)
    ba_df, mean_diff, loa_lower, loa_upper = compute_bland_altman(df)

    outliers = ba_df[(ba_df["Difference"] > loa_upper) | (ba_df["Difference"] < loa_lower)]
    OUTLIERS_CSV.parent.mkdir(parents=True, exist_ok=True)
    outliers.to_csv(OUTLIERS_CSV, index=False)
    print(outliers[["OTU", "HAC", "SUP", "Difference"]].head(40))

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(ba_df["Mean"], ba_df["Difference"], alpha=0.5)
    ax.axhline(mean_diff, color="blue", linestyle="--", label=f"Mean Diff = {mean_diff:.2f}")
    ax.axhline(loa_upper, color="red", linestyle="--", label=f"+1.96 SD = {loa_upper:.2f}")
    ax.axhline(loa_lower, color="red", linestyle="--", label=f"-1.96 SD = {loa_lower:.2f}")
    ax.set_xlabel("Average Abundance Reads(log10)")
    ax.set_ylabel("HAC - SUP Abundance difference (log10)")
    ax.legend()
    ax.grid(True)
    fig.tight_layout()

    save_figure(fig, FIGURES_OUTPUT_DIR / f"{FIGURE_NAME}.pdf")
    save_figure(fig, FIGURES_OUTPUT_DIR / f"{FIGURE_NAME}.png")
    plt.close(fig)


if __name__ == "__main__":
    main()
