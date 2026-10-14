# Data

Expected input file names are figure-specific and should be placed in `data/raw/`.

| Figure | Script | Expected input file | Description |
|---|---|---|---|
| Fig. 1 | `fig01_main.py` | `INPUT1.csv` | Specimen type counts (hardcoded in the script) |
| Fig. 2 | `fig02_microbial_community_performance.py` | `INPUT2.csv` | Microbial community DNA standard II, abundance (%) per center and replicate |
| Fig. 3 | `fig03_negative_controls_across_centers.py` | `INPUT3.csv` | Taxa detected in negative controls across all centers |
| Fig. 4 | `fig04_venn_background_filtered.py` | `INPUT4.csv` | Taxa detected after background filtering (counts hardcoded in the script) |
| Fig. 5 | `fig05_bland_altman_taxon_level.py` | `INPUT5.csv` | Taxon-level HAC vs SUP counts |
| Fig. S1 | `figS01_supplementary.py` | `INPUTS1.csv` | HAC vs SUP total read counts per sample |

Add your own source / DOI metadata here when the final data locations are known.
