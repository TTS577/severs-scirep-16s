import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from severs_scirep_16s.config import FIGURES_OUTPUT_DIR, RAW_DATA_DIR
from severs_scirep_16s.plotting import save_figure, set_plot_style

FIGURE_NAME = "fig02_microbial_community_performance"
INPUT_FILE = RAW_DATA_DIR / "input.csv"


def main() -> None:
    set_plot_style()

    # Load data (delimiter as in the original analysis)
    df = pd.read_csv(INPUT_FILE, index_col=0, delimiter=";", encoding="ISO-8859-1")

    # Clean column names and index
    df.columns = df.columns.str.strip()
    df.index.name = "Bacterial species"

    # Reshape to long format
    df_long = df.reset_index().melt(id_vars="Bacterial species", var_name="Condition", value_name="Value")

    # Convert values to numeric (decimal comma -> decimal point)
    df_long["Value"] = df_long["Value"].astype(str).str.replace(",", ".").str.strip()
    df_long["Value"] = pd.to_numeric(df_long["Value"], errors="coerce")

    # Extract center and replicate from condition name
    df_long["Center"] = df_long["Condition"].str.extract(r"([A-Z]+)")
    df_long["Replicate"] = df_long["Condition"].str.extract(r"_(\d+)")

    # Combine replicates: mean and SD per species and center
    df_stats = df_long.groupby(["Bacterial species", "Center"]).agg(
        Mean=("Value", "mean"),
        SD=("Value", "std"),
        n=("Value", "count"),
    ).reset_index()

    # SEM
    df_stats["SEM"] = df_stats["SD"] / np.sqrt(df_stats["n"])

    # Colours and markers
    species = df_stats["Bacterial species"].unique()
    colors = dict(zip(species, sns.color_palette("tab20", len(species))))
    markers = ["o", "s", "D", "^", "v", "p", "*", "X", "P"]
    marker_dict = dict(zip(species, markers * (len(species) // len(markers) + 1)))

    fig, ax = plt.subplots(figsize=(12, 6))

    for bacterium in species:
        subset = df_stats[df_stats["Bacterial species"] == bacterium]
        ax.errorbar(subset["Center"], subset["Mean"], yerr=subset["SEM"], fmt="none",
                    ecolor=colors[bacterium], elinewidth=1.5, capsize=5, alpha=0.7)
        ax.scatter(subset["Center"], subset["Mean"], color=colors[bacterium],
                   marker=marker_dict[bacterium], label=bacterium,
                   edgecolor="black", s=100, alpha=0.9)

    ax.set_yscale("log")
    ax.tick_params(axis="x", rotation=45)
    for label in ax.get_xticklabels():
        label.set_ha("right")
    ax.set_title("Microbial Community Performance")
    ax.set_xlabel("Centers")
    ax.set_ylabel("Abundance (%)")
    ax.legend(title="Bacteria", bbox_to_anchor=(1.05, 1), loc="upper left")
    ax.grid(True, which="both", linestyle="--", linewidth=0.5)

    fig.tight_layout()
    save_figure(fig, FIGURES_OUTPUT_DIR / f"{FIGURE_NAME}.pdf")
    save_figure(fig, FIGURES_OUTPUT_DIR / f"{FIGURE_NAME}.png")
    plt.close(fig)


if __name__ == "__main__":
    main()
