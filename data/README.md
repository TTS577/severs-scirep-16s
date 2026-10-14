# severs-scirep-16s

This repository contains figure-generation code for the manuscript:

**Multicenter evaluation of the EasySeq Full-Length 16S Sequencing kit for bacterial identification in clinical samples**

## Structure

- `data/` — input and processed data
- `figures/scripts/` — one script per figure
- `figures/output/` — generated figure files
- `src/severs_scirep_16s/` — reusable helpers
- `scripts/` — utility scripts such as data downloads and batch builds

## Typical usage

```bash
python scripts/download_data.py
make figures
```
