# Data

Input files are expected in `data/raw/` (not tracked by git). Place them there before running the figure scripts.

| Figure | Script | Expected input file | Description |
|---|---|---|---|
| Fig. 1 | `fig01_main.py` | none (counts in script) | Specimen type counts |
| Fig. 2 | `fig02_microbial_community_performance.py` | `input.csv` | Microbial community DNA standard II, relative abundance (%) per center, replicates as `X_1`, `X_2`, `X_3` |
| Fig. 3 | `fig03_negative_controls_across_centers.py` | `2511_Test_NTC_reads_nolabmicta.csv` | Reads per taxon in negative controls, per center (semicolon-separated, alternating taxon/reads columns) |
| Fig. 4 | `fig04_venn_background_filtered.py` | none (counts in script) | Taxa detected after background filtering |
| Fig. 5 | `fig05_bland_altman_taxon_level.py` | `INPUT.csv` | Columns `OTU`, `HAC`, `SUP` (semicolon-separated) |
| Fig. S1 | `figS01_supplementary.py` | `20250714_mastersheet_HAC_SUP.csv` | Per-sample OTU read counts for HAC and SUP basecalling |

TODO: add source / DOI (e.g. Zenodo) for each dataset.
