# Unicode Annotation Offsets

A small Python library for exchanging text annotations between a browser UI (UTF-16 code units), a Python NLP pipeline (code points), and a byte-offset store (UTF-8). Every conversion preserves the labeled substring or rejects the span instead of silently rounding an offset.

```sh
python lab.py
```

The demo maps `€42` in `🧾 Café €42`. Its start is 7 in Python, 8 in UTF-16, and 11 in UTF-8. `Span` offsets are half-open. Build one `OffsetMap` per immutable string: O(n) indexing, O(n) storage, O(log n) reverse lookups. Combining marks are not normalized; boundaries are scalar boundaries, not grapheme boundaries. This is a text alignment component, not OCR or a tokenizer.

## Checks

Use Python 3.11 or newer. To reproduce the CI checks in a virtual environment:

```sh
python -m pip install pytest==8.4.2 ruff==0.14.14
ruff check .
ruff format --check .
python -m pytest -q
```
