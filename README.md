# Bruker RAW XRD → Origin Automated Toolchain

Drag-and-drop toolchain for Bruker RAW (V3/V4) XRD data:
parsing → 2θ/Relative Intensity table → Nature-style stacked plot in Origin Pro.

## Files

| File | Purpose |
|------|---------|
| `raw_to_table.py` | Core parser: RAW → CSV/XLSX (2θ + rel. intensity) |
| `raw_to_origin.py` | Parse + push to Origin Pro, auto-create Y-offset stacked plot |
| `拖入RAW出表格.bat` | Drop `.raw` → table |
| `拖入RAW到Origin出图.bat` | Drop `.raw` files → Origin graph |
| `RAW转表格(放桌面).bat` | Desktop shortcut for table |
| `RAW到Origin堆积图(放桌面).bat` | Desktop shortcut for Origin plot |

## Dependencies

- Python 3.10+ with `numpy`
- `originpro` (Origin Pro's Python package, for `raw_to_origin.py`)
- Origin Pro installed

## Quick Start

1. Drop a single `.raw` file onto `拖入RAW出表格.bat` → CSV + XLSX with 2θ and relative intensity
2. Drop multiple `.raw` files onto `拖入RAW到Origin出图.bat` → Origin auto-opens with Nature-style stacked plot (Y-offset, auto-colored, curve labels at endpoints)
