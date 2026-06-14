# Bruker RAW XRD → Origin Automated Toolchain

> 中文说明见下方 / See Chinese description below

Drag-and-drop toolchain for Bruker RAW (V3/V4) XRD data:
parsing → 2θ/Relative Intensity table → Nature-style stacked plot in Origin Pro.

## Files

| File | Purpose |
|------|---------|
| `raw_to_table.py` | Core parser: RAW → CSV/XLSX (2θ + rel. intensity) |
| `raw_to_origin.py` | Parse + push to Origin Pro, auto-create Y-offset Nature-style stacked plot |
| `拖入RAW出表格.bat` | Drop `.raw` file → table |
| `拖入RAW到Origin出图.bat` | Drop `.raw` files → Origin graph |

## Dependencies

- Python 3.10+ with `numpy`
- `originpro` (Origin Pro's Python package, for `raw_to_origin.py`)
- Origin Pro installed

## Quick Start

1. Drop a single `.raw` file onto `拖入RAW出表格.bat` → CSV + XLSX with 2θ and relative intensity
2. Drop multiple `.raw` files onto `拖入RAW到Origin出图.bat` → Origin auto-opens with Nature-style stacked plot (Y-offset, auto-colored, curve labels at endpoints)

---

# Bruker RAW XRD → Origin 自动化工具链

拖拽式 Bruker RAW（V3/V4）XRD 数据处理工具链：
RAW 解析 → 2θ/相对强度表格 → Origin Pro Nature 风格 Y 偏移堆积图。

## 文件

| 文件 | 用途 |
|------|------|
| `raw_to_table.py` | 核心解析：RAW → CSV/XLSX（2θ + 相对强度） |
| `raw_to_origin.py` | 解析并导入 Origin Pro，自动创建 Nature 风格堆积图 |
| `拖入RAW出表格.bat` | 拖入 `.raw` → 出表格 |
| `拖入RAW到Origin出图.bat` | 拖入 `.raw` 文件 → Origin 出图 |

## 依赖

- Python 3.10+ + `numpy`
- `originpro`（Origin Pro 的 Python 包，`raw_to_origin.py` 需要）
- 已安装 Origin Pro

## 快速开始

1. 将单个 `.raw` 文件拖到 `拖入RAW出表格.bat` 上 → 同目录生成 CSV + XLSX 表格
2. 将多个 `.raw` 文件拖到 `拖入RAW到Origin出图.bat` 上 → Origin 自动打开并生成 Nature 风格 Y 偏移堆积图（自动配色、曲线末端标注样品名）
