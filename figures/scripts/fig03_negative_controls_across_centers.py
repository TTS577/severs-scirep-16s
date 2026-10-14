import matplotlib.pyplot as plt
import pandas as pd

from severs_scirep_16s.config import FIGURES_OUTPUT_DIR, RAW_DATA_DIR
from severs_scirep_16s.plotting import save_figure, set_plot_style

FIGURE_NAME = "fig03_negative_controls_across_centers"
INPUT_FILE = RAW_DATA_DIR / "2511_Test_NTC_reads_nolabmicta.csv"


def parse_wide_center_table(path):
    """Parse a semicolon-separated wide table of center-specific reads.

    Expected row layout:
    OTU;Center1;Reads1;Center2;Reads2;...
    """
    raw = pd.read_csv(path, sep=";", header=None, dtype=str)
    raw = raw.dropna(how="all")

    # First row contains the center names in alternating columns.
    header = raw.iloc[0].tolist()
    center_names = [str(x).strip() for x in header[1::2] if pd.notna(x)]

    records = []
    for _, row in raw.iloc[1:].iterrows():
        values = row.tolist()
        if not values or pd.isna(values[0]):
            continue

        otu = str(values[0]).strip()
        for i, center in enumerate(center_names, start=1):
            reads_idx = i * 2
            if reads_idx >= len(values):
                continue
            reads = pd.to_numeric(values[reads_idx], errors="coerce")
            records.append({"OTU": otu, "Center": center, "Reads": reads})

    long = pd.DataFrame(records).dropna(subset=["Reads"])
    long["OTU"] = long["OTU"].astype(str).str.strip()
    long["Center"] = long["Center"].astype(str).str.strip()
    return long, center_names


def main() -> None:
    set_plot_style()

    center_long, center_names = parse_wide_center_table(INPUT_FILE)

    otu_reads = (
        center_long.groupby("OTU", as_index=False)["Reads"]
        .sum()
        .sort_values("Reads", ascending=False)
        .reset_index(drop=True)
    )

    detection_counts = (
        center_long[center_long["Reads"] > 0]
        .groupby("OTU")["Center"]
        .nunique()
    )

    otu_reads["Centers"] = otu_reads["OTU"].map(detection_counts).fillna(0).astype(int)

    otu_labels = otu_reads["OTU"].tolist()
    x = list(range(len(otu_reads)))

    n_centers = len(center_names)
    fig_width = max(16, 0.32 * len(otu_reads))
    fig, ax_reads = plt.subplots(figsize=(fig_width, 7))

    ax_reads.bar(x, otu_reads["Reads"], color="gray")
    ax_reads.set_xlabel("OTUs")
    ax_reads.set_ylabel("Read count")
    ax_reads.set_yscale("log")
    ax_reads.grid(True, axis="y", alpha=0.3)

    ax_reads.set_xticks(x)
    ax_reads.set_xticklabels(
        otu_labels,
        rotation=90,
        fontstyle="italic",
        fontsize=6,
        ha="center",
    )

    ax_centers = ax_reads.twinx()
    ax_centers.scatter(
        x,
        otu_reads["Centers"],
        marker="v",
        facecolors="none",
        edgecolors="black",
        s=90,
        linewidths=1.5,
        zorder=5,
    )
    ax_centers.set_ylabel("Number of centers")
    ax_centers.set_ylim(0, n_centers + 0.5)
    ax_centers.set_yticks(range(n_centers + 1))
    ax_centers.grid(False)

    fig.tight_layout()
    save_figure(fig, FIGURES_OUTPUT_DIR / f"{FIGURE_NAME}.pdf")
    save_figure(fig, FIGURES_OUTPUT_DIR / f"{FIGURE_NAME}.png")
    plt.close(fig)


if __name__ == "__main__":
    main()
