import matplotlib.pyplot as plt

from severs_scirep_16s.config import FIGURES_OUTPUT_DIR
from severs_scirep_16s.plotting import save_figure, set_plot_style

FIGURE_NAME = "fig01_sample_sources"

# Number of clinical samples per specimen type
labels = ["Tissue", "Cerebrospinal fluid", "Abscess/Pus", "Pleural fluid", "Aspirate", "Joint fluid", "Other"]
sizes = [67, 19, 23, 16, 11, 9, 15]


def main() -> None:
    set_plot_style()

    # Sort data by size in descending order
    sorted_data = sorted(zip(labels, sizes), key=lambda x: x[1], reverse=True)
    sorted_labels = [item[0] for item in sorted_data]
    sorted_sizes = [item[1] for item in sorted_data]

    # Pastel palette
    colors = plt.cm.Pastel1.colors[: len(sorted_sizes)]

    fig, ax = plt.subplots(figsize=(8, 8))
    # Start at 12 o'clock, going clockwise
    wedges, texts, autotexts = ax.pie(
        sorted_sizes, labels=None, colors=colors, autopct="%1.1f%%", startangle=90, counterclock=False
    )

    # Move percentages outward
    for autotext in autotexts:
        autotext.set_size(12)
        autotext.set_color("black")
        x, y = autotext.get_position()
        autotext.set_position((x * 1.45, y * 1.45))
        autotext.set_visible(True)

    legend_labels = [f"{label} ({size})" for label, size in zip(sorted_labels, sorted_sizes)]
    ax.legend(wedges, legend_labels, title="Specimen Types", loc="center left",
              bbox_to_anchor=(1, 0.5), handlelength=1.5)
    ax.axis("equal")

    save_figure(fig, FIGURES_OUTPUT_DIR / f"{FIGURE_NAME}.pdf")
    save_figure(fig, FIGURES_OUTPUT_DIR / f"{FIGURE_NAME}.png")
    plt.close(fig)


if __name__ == "__main__":
    main()
