# ira_ai

Working repository for the IRA AI project.

## Contents

| Path | What it is |
| --- | --- |
| [`library/`](library/) | Stored source texts — see [`library/README.md`](library/README.md) for the layout and how to add a fragment |
| [`german/`](german/) | German study plan (A1 → A2 by 31.12.2026): day-by-day plan, daily lessons, progress tracker — see [`german/README.md`](german/README.md) |
| `tools/` | Ingest and build scripts for the library |

## Library at a glance

| Source | Held | Format |
| --- | --- | --- |
| The Lawyer's English Language Coursebook (Mason & Atkins, Global Legal English, 2007) | printed pages 1–200 (fragments 1–2): front matter, units 1A–5B complete, unit 6A up to p. 200 | OCR plain text per page + per-unit markdown |

## Tools

```bash
pip install pymupdf
apt-get install -y tesseract-ocr

# OCR a new PDF fragment into library/sources/<id>/text/
python3 tools/ingest_fragment.py FRAGMENT.pdf --source-id <id> --fragment N --first-page P

# rebuild the per-unit markdown from the page text
python3 tools/build_units.py --source-id <id>
```
