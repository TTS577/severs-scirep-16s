import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib_venn import venn2, venn2_unweighted

from severs_scirep_16s.config import FIGURES_OUTPUT_DIR
from severs_scirep_16s.plotting import save_figure, set_plot_style

FIGURE_NAME = "fig04_venn_background_filtered"

# --- Size settings -----------------------------------------------------------
WEIGHTED = True          # True: circle areas proportional to counts; False: equal circles
SCALE_BY_TOTAL = True    # True: panel areas proportional to their total number of taxa
SIZE_SCALE = 1.0         # Multiplier for all diagrams (e.g. 0.8 shrinks, 1.2 enlarges)

SUBSET_FONTSIZE = 10
TITLE_FONTSIZE = 14

# "10" = comparator workflow only, "01" = EasySeq - GD pipeline only, "11" = both.
PANELS = [
    ("A", "Sanger", {"10": 1, "01": 35, "11": 29}),
    ("B", "tNGS - Illumina", {"10": 31, "01": 57, "11": 112}),
    ("C", "tNGS - ONT", {"10": 32, "01": 92, "11": 141}),
]


def plot_venn(ax, counts, title, normalize_to):
    if WEIGHTED:
        venn = venn2(subsets=counts, set_labels=("", ""), ax=ax, normalize_to=normalize_to)
    else:
        venn = venn2_unweighted(subsets=counts, set_labels=("", ""), ax=ax)
    for label in venn.subset_labels:
        if label:
            label.set_fontsize(SUBSET_FONTSIZE)
    ax.set_title(title, fontsize=TITLE_FONTSIZE)
    return venn


def main() -> None:
    set_plot_style()
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    totals = [sum(counts.values()) for _, _, counts in PANELS]
    max_total = max(totals)

    venns = []
    for ax, (letter, name, counts), total in zip(axes, PANELS, totals):
        relative = total / max_total if SCALE_BY_TOTAL else 1.0
        venns.append(plot_venn(ax, counts, f"{letter}. {name} (n = {total})", SIZE_SCALE * relative))

    first = venns[0]
    legend_handles = [
        Patch(facecolor=first.get_patch_by_id("10").get_facecolor(), label="Comparator workflow"),
        Patch(facecolor=first.get_patch_by_id("11").get_facecolor(), label="Concordance"),
        Patch(facecolor=first.get_patch_by_id("01").get_facecolor(), label="EasySeq - GD pipeline"),
    ]

    fig.tight_layout(rect=[0.01, 0.1, 0.98, 0.9], w_pad=0.02, h_pad=0.1)
    fig.subplots_adjust(wspace=0.01)
    fig.legend(handles=legend_handles, loc="lower center", bbox_to_anchor=(0.5, 0.04), ncol=3, frameon=False)

    save_figure(fig, FIGURES_OUTPUT_DIR / f"{FIGURE_NAME}.pdf")
    save_figure(fig, FIGURES_OUTPUT_DIR / f"{FIGURE_NAME}.png")
    plt.close(fig)


if __name__ == "__main__":
    main()
