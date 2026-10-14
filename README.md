# severs-scirep-16s

Figure-generation code for:

> Severs TT, Gebbink AJ, Gard L, Rossen JWA, van Alphen LB, Koeck RM, Smit PW, Yahiaoui RY, Matamoros SPF, van den Bosch B, Koopman P, Cartuyvels R, Dingemans J, Ivens MJR, Pas SD\*, Boers SA\*. **Multicenter evaluation of the EasySeq Full-Length 16S Sequencing kit for bacterial identification in clinical samples.** *Scientific Reports*.
>
> \*Equal contribution.

This repository contains the scripts used to generate the figures of the manuscript.

## Figures

| Figure | Script | Description |
|---|---|---|
| Fig. 1 | `figures/scripts/fig01_main.py` | Distribution of clinical sample sources included in this study |
| Fig. 2 | `figures/scripts/fig02_microbial_community_performance.py` | Performance of the Microbial Community DNA Standard II across all centers |
| Fig. 3 | `figures/scripts/fig03_negative_controls_across_centers.py` | Taxa detected in negative controls across all centers |
| Fig. 4 | `figures/scripts/fig04_venn_background_filtered.py` | Venn diagrams of taxa detected after exclusion of taxa flagged during background signal assessment |
| Fig. 5 | `figures/scripts/fig05_bland_altman_taxon_level.py` | Bland-Altman plot comparing HAC and SUP models at taxon level (log10 abundances) |
| Fig. S1 | `figures/scripts/figS01_supplementary.py` | HAC vs SUP total read counts per sample (linear and log10) |

## Repository layout

```text
.
├── data/                 # input data (raw/ is not tracked); see data/README.md
├── figures/
│   ├── scripts/          # one script per figure
│   └── output/           # generated PDF/PNG (not tracked)
├── scripts/              # download_data.py, build_all_figures.py
├── src/severs_scirep_16s/ # shared paths and plotting helpers
├── notebooks/
├── CITATION.cff
├── Makefile
├── environment.yml
├── pyproject.toml
└── requirements.txt
```

## Installation

```bash
# conda
conda env create -f environment.yml
conda activate severs-scirep-16s

# or pip
pip install -r requirements.txt
pip install -e .
```

## Reproducing the figures

1. Put the input files in `data/raw/` (see `data/README.md`).
2. Run everything:

```bash
make figures
```

or a single figure:

```bash
python figures/scripts/fig05_bland_altman_taxon_level.py
```

Figures are written to `figures/output/` as PDF and PNG.

## Data availability

TODO: add the repository / DOI where the data are deposited.

## Citation

See `CITATION.cff`.

## License

MIT, see `LICENSE`.
