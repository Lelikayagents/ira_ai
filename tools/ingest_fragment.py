#!/usr/bin/env python3
"""Ingest a scanned book fragment (PDF) into the library.

The scans in this library have no text layer, so pages are rendered to
grayscale images and passed through Tesseract OCR. The script writes one
plain-text file per book page plus a fragment manifest.

Usage:
    python3 tools/ingest_fragment.py SOURCE.pdf --source-id <id> \
        --fragment 1 --first-page 1 [--dpi 300] [--lang eng]

Requirements: pymupdf (pip), tesseract-ocr (apt).
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date

WATERMARK = re.compile(r"vk\.com/\S+", re.I)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def clean(text):
    lines = [ln.rstrip() for ln in text.splitlines() if not WATERMARK.search(ln)]
    out, blanks = [], 0
    for ln in lines:
        blanks = blanks + 1 if not ln else 0
        if blanks < 2:
            out.append(ln)
    return "\n".join(out).strip() + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--source-id", required=True)
    ap.add_argument("--fragment", type=int, required=True)
    ap.add_argument("--first-page", type=int, required=True,
                    help="book page number of the first PDF page")
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--lang", default="eng")
    args = ap.parse_args()

    if not shutil.which("tesseract"):
        sys.exit("tesseract not found; install tesseract-ocr")
    import pymupdf

    src_dir = os.path.join(ROOT, "library", "sources", args.source_id)
    text_dir = os.path.join(src_dir, "text")
    os.makedirs(text_dir, exist_ok=True)

    doc = pymupdf.open(args.pdf)
    pages, empty = [], []
    with tempfile.TemporaryDirectory() as tmp:
        for i in range(doc.page_count):
            page_no = args.first_page + i
            img = os.path.join(tmp, "page.png")
            doc[i].get_pixmap(dpi=args.dpi, colorspace=pymupdf.csGRAY).save(img)
            env = dict(os.environ, OMP_THREAD_LIMIT="1")
            res = subprocess.run(
                ["tesseract", img, "stdout", "-l", args.lang, "--psm", "3"],
                capture_output=True, text=True, env=env)
            text = clean(res.stdout)
            dest = os.path.join(text_dir, "page-%03d.txt" % page_no)
            with open(dest, "w") as fh:
                fh.write(text)
            chars = len(text.strip())
            pages.append({"page": page_no, "chars": chars})
            if chars < 30:
                empty.append(page_no)
            print("page %d -> %s (%d chars)" % (page_no, dest, chars))

    manifest = {
        "fragment": args.fragment,
        "source_id": args.source_id,
        "book_pages": {"first": args.first_page,
                       "last": args.first_page + doc.page_count - 1},
        "pdf": {"file_name": os.path.basename(args.pdf),
                "page_count": doc.page_count,
                "sha256": sha256(args.pdf)},
        "ocr": {"engine": "tesseract", "lang": args.lang, "dpi": args.dpi,
                "renderer": "pymupdf", "colorspace": "gray"},
        "ingested_on": date.today().isoformat(),
        "pages": pages,
        "pages_without_text": empty,
    }
    frag_dir = os.path.join(src_dir, "fragments")
    os.makedirs(frag_dir, exist_ok=True)
    out = os.path.join(frag_dir, "fragment-%02d.json" % args.fragment)
    with open(out, "w") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print("manifest ->", out)


if __name__ == "__main__":
    main()
