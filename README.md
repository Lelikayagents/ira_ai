# ira_ai

Working repository for the IRA AI project.

## Contents

| Path | What it is |
| --- | --- |
| [`library/`](library/) | Stored source texts — see [`library/README.md`](library/README.md) for the layout and how to add a fragment |
| `tools/` | Ingest and build scripts for the library |

## Library at a glance

| Source | Held | Format |
| --- | --- | --- |
| The Lawyer's English Language Coursebook (Mason & Atkins, Global Legal English, 2007) | printed pages 1–200 (fragments 1–2): front matter, units 1A–5B complete, unit 6A up to p. 200 | OCR plain text per page + per-unit markdown |
| Principles of Roman Law (Fritz Schulz, Clarendon Press, 1936) | printed pages 40–65 and 140–163 (fragments 1–2): chapters IV, 'Abstraction', and VIII, 'Liberty', complete | extracted plain text per page + Russian translation |

## Tools

```bash
pip install pymupdf
apt-get install -y tesseract-ocr

# OCR a new PDF fragment into library/sources/<id>/text/
python3 tools/ingest_fragment.py FRAGMENT.pdf --source-id <id> --fragment N --first-page P

# rebuild the per-unit markdown from the page text
python3 tools/build_units.py --source-id <id>
```
