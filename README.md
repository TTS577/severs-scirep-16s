# severs-scirep-16s

Figure-generation repository for the paper:
**Multicenter evaluation of the EasySeq Full-Length 16S Sequencing kit for bacterial identification in clinical samples**

## Overview

This repository contains the scripts and supporting code used to generate the figures for the manuscript by Severs et al. in *Scientific Reports*.

## Suggested workflow

1. Set up the Python environment.
2. Place raw inputs in `data/raw/` or download them with `scripts/download_data.py`.
3. Run the figure scripts in `figures/scripts/` or use `make figures`.
4. Generated outputs will be written to `figures/output/`.

## Repository layout

```text
├── data/
├── figures/
├── notebooks/
├── scripts/
├── src/
├── CITATION.cff
├── LICENSE
├── Makefile
├── README.md
├── environment.yml
└── requirements.txt
```

## Reproducibility notes

- Keep raw data immutable in `data/raw/`.
- Put shared helper functions in `src/severs_scirep_16s/`.
- Keep one script per figure where possible.
- Pin package versions for reproducibility.

## Citation

If you use this repository, please cite the associated manuscript once available.
