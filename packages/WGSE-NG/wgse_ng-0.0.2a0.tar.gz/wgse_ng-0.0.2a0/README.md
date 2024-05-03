[![Documentation Status](https://readthedocs.org/projects/wgse-ng/badge/?version=latest)](https://wgse-ng.readthedocs.io/en/latest/?badge=latest)
[![Python application](https://github.com/chaplin89/WGSE-NG/actions/workflows/python-app.yml/badge.svg)](https://github.com/chaplin89/WGSE-NG/actions/workflows/python-app.yml/badge.svg)
[![Python Publish](https://github.com/chaplin89/WGSE-NG/actions/workflows/python-publish.yml/badge.svg)](https://github.com/chaplin89/WGSE-NG/actions/workflows/python-publish.yml/badge.svg)
[![Python Publish](https://github.com/chaplin89/WGSE-NG/actions/workflows/python-pyinstaller.yml/badge.svg)](https://github.com/chaplin89/WGSE-NG/actions/workflows/python-pyinstaller.yml/badge.svg)

- [Read the docs](https://wgse-ng.readthedocs.io/en/latest/)

## Develop/Launch

```bash
git clone https://github.com/chaplin89/WGSE-NG
cd WGSE-NG
python -m venv .venv
./.venv/Scripts/activate
python -m pip install -r requirements.txt
python main.py
```

## What's working

- [x] Basic file info extraction
- [x] Index stats
- [x] Alignment stats
- [ ] Coverage stats
- [ ] FASTQ <-> Aligned file conversion
- [ ] SAM <-> BAM <-> CRAM conversion
- [ ] Alignment
- [ ] Variant calling
- [x] Microarray converter
- [ ] Mitochondrial data extraction
- [ ] Y-DNA data extraction
- [ ] Unaligned data extraction
- [x] Reference genome identification (68 references supported)
- [ ] Installer
- [ ] Crash stats
- [ ] Usage stats
- [X] Reference ingestion procedure (partial)
- [ ] Documentation