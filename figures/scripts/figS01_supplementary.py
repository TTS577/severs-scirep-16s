from pathlib import Path

import matplotlib.pyplot as plt

from severs_scirep_16s.config import FIGURES_OUTPUT_DIR
from severs_scirep_16s.plotting import save_figure, set_plot_style


def main() -> None:
    set_plot_style()
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.text(0.5, 0.5, "Supplementary Figure placeholder", ha="center", va="center")
    ax.set_axis_off()
    save_figure(fig, FIGURES_OUTPUT_DIR / "figS01_supplementary.pdf")
    save_figure(fig, FIGURES_OUTPUT_DIR / "figS01_supplementary.png")
    plt.close(fig)


if __name__ == "__main__":
    main()
