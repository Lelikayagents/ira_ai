# Library

Storage for source texts that have been studied and kept for reuse.

## Layout

```
library/
  catalog.json                  index of all sources
  sources/<source-id>/
    metadata.json               bibliographic data, scan and OCR provenance, coverage
    contents.md                 the source's own table of contents, with holdings marked
    structure.json              machine-readable unit -> page-range map
    fragments/fragment-NN.json  per-fragment manifest (pages, PDF hash, OCR settings)
    text/page-NNN.txt           one plain-text file per printed page
    units/<unit>.md             pages joined into one file per unit, for reading
    translations/<lang>/*.md    translations of held material, one file per chapter/unit
```

## Conventions

- **Page numbers are printed book pages.** In most scans here the PDF page number
  equals the printed page number, so `page-073.txt` is book page 73. Where a fragment
  starts mid-book the two differ; the offset is recorded in the source's
  `metadata.json` and in its fragment manifest.
- **A "fragment" is one delivered PDF chunk**, not a unit of the book. Fragments
  are numbered in the order they arrived and recorded in `fragments/`. A fragment
  can start and end mid-unit; `structure.json` says which units are complete.
- **`text/` holds raw OCR.** It is not proof-read. Running heads, page numbers
  and rotated side tabs may appear as stray lines, and full-page unit dividers
  (dark background art) may come out empty. Original page images are not stored —
  only the text.
- **`units/` is derived** from `text/` and can be regenerated at any time; treat
  `text/` as the source of truth.
- **`translations/` is hand-written** and derived from nothing. Each file names the
  pages it covers and the conventions it follows — what is left in the original
  language, how footnotes and pagination are carried over. Where the raw OCR in `text/`
  is defective the translation is corrected against the sense; `text/` itself is left
  untouched.

## Adding a fragment

```bash
pip install pymupdf
apt-get install -y tesseract-ocr

python3 tools/ingest_fragment.py FRAGMENT.pdf \
    --source-id lawyers-english-language-coursebook \
    --fragment 3 --first-page 201

python3 tools/build_units.py --source-id lawyers-english-language-coursebook
```

Then update `catalog.json`, and the `fragments_held` / `coverage_note` fields in
the source's `metadata.json`.

## A note on rights

These are personal study copies of material the repository owner supplied. The
texts are reproduced here for private study only; the copyright stays with the
authors and publisher named in each `metadata.json`. Do not redistribute.
