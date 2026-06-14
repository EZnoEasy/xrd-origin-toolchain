"""
Bruker RAW V3/V4 -> Origin XRD Stack Plot (Nature-style)
拖入多个 .raw 文件，自动解析 -> 导入 Origin -> Nature风格Y偏移堆积图 -> 保存 opju

Usage:
    python raw_to_origin.py file1.raw file2.raw file3.raw
    python raw_to_origin.py --gap 20 file1.raw file2.raw

Features:
    - 自动计算偏移量（曲线紧贴不重叠）
    - 自动调整Y轴范围（2%留白）
    - Nature风格：隐藏Y轴、曲线右端标注样品名
"""

import struct
import sys
import os

try:
    import numpy as np
except ImportError:
    print("ERROR: numpy required.")
    input("Press Enter to exit...")
    sys.exit(1)

try:
    import originpro as op
except ImportError:
    print("ERROR: originpro required (Origin's Python package).")
    print("Run: pip install originpro")
    input("Press Enter to exit...")
    sys.exit(1)


# ====================================================================
# RAW Parser (same logic as raw_to_table.py)
# ====================================================================

def _r32(data, off):
    return struct.unpack('<I', data[off:off+4])[0]

def _f64(data, off):
    return struct.unpack('<d', data[off:off+8])[0]

def _f32(data, off):
    return struct.unpack('<f', data[off:off+4])[0]

def _str(data, off, n):
    return data[off:off+n].decode('latin-1', errors='replace').rstrip('\x00').strip()


def parse_raw(filepath):
    """Parse Bruker RAW1.01 -> (angles_2theta, intensities, meta)"""
    with open(filepath, 'rb') as f:
        data = f.read()

    R = 712

    measure_date = _str(data, 16, 10)
    measure_time = _str(data, 26, 10)
    sample_id    = _str(data, 326, 60)
    comment      = _str(data, 386, 160)

    hdr_len   = _r32(data, R)
    steps     = _r32(data, R + 4)
    start_2theta = _f64(data, R + 16)

    step_size = 0.01637
    try:
        v = _f64(data, R + 176)
        if 0.001 < v < 0.2:
            step_size = v
    except:
        pass
    if step_size == 0.01637:
        try:
            v = _f64(data, 888)
            if 0.001 < v < 0.2:
                step_size = v
        except:
            pass

    high_voltage  = _f32(data, R + 96)
    used_lambda   = _f64(data, R + 240)

    total_len = len(data)
    DATA_START = total_len - steps * 4

    try:
        first_val = struct.unpack('<f', data[DATA_START:DATA_START+4])[0]
    except:
        first_val = 0

    if not (50 < first_val < 200000):
        for off in range(total_len - steps * 4,
                         min(total_len - steps * 4 + 400, total_len - 4), 1):
            try:
                v = struct.unpack('<f', data[off:off+4])[0]
                if 50 < v < 200000:
                    DATA_START = off
                    break
            except:
                continue

    intensities = np.array(
        struct.unpack(f'<{steps}f', data[DATA_START:DATA_START + steps * 4]),
        dtype=np.float64
    )

    if steps > 1 and step_size > 0:
        angles = np.linspace(start_2theta,
                              start_2theta + step_size * (steps - 1),
                              steps)
    else:
        angles = np.array([start_2theta])

    end_2theta = start_2theta + step_size * (steps - 1) if steps > 1 else start_2theta

    meta = {
        'filename': os.path.splitext(os.path.basename(filepath))[0],
        'num_points': steps,
        'start': start_2theta,
        'end': end_2theta,
        'step': step_size,
        'wavelength': used_lambda if 0.5 < used_lambda < 3.0 else 1.5406,
        'voltage': high_voltage,
        'date': measure_date,
        'time': measure_time,
        'sample_id': sample_id,
        'comment': comment,
    }
    return angles, intensities, meta


# ====================================================================
# Origin Integration
# ====================================================================

def push_to_origin(all_data, gap=None):
    """
    Push parsed XRD data to Origin and create Y-offset stacked plot.

    all_data: list of (angles, intensities, meta) tuples
    gap:      optional extra gap between curves (None = no extra gap)
    """
    n = len(all_data)
    gap = gap if gap is not None else 0

    # ---- Connect & show Origin ----
    print("\nConnecting to Origin...")
    op.set_show(True)

    # ---- Calculate per-curve offsets ----
    # Curve i baseline = sum of all preceding curves' max intensities
    offsets = [0]
    for d in all_data[:-1]:
        offsets.append(offsets[-1] + d[1].max() + gap)

    # ---- Create workbook & write data with offsets ----
    wb = op.new_book('w')
    wb.lname = 'XRD_Stack'
    ws = wb[0]
    ws.lname = 'Data'

    print(f"Writing {n} dataset(s) to worksheet...")

    for i, (angles, intensities, meta) in enumerate(all_data):
        col_x = i * 2
        col_y = i * 2 + 1
        ws.cols = col_y + 1

        ws.from_list(col_x, list(angles), lname='2\u03b8', axis='X')
        ws.from_list(col_y, list(intensities + offsets[i]),
                     lname=meta['filename'][:25], axis='Y')

        label = meta['filename'][:25]
        print(f"  [{i+1}] {label}: "
              f"{meta['start']:.2f}-{meta['end']:.2f} deg, "
              f"{meta['num_points']} pts, baseline {offsets[i]:.0f}")

    # ---- Create graph ----
    print("\nCreating Y-offset stacked plot...")
    gp = op.new_graph()
    gl = gp[0]

    for i in range(n):
        gl.add_plot(ws, i * 2 + 1, i * 2, type='l')
        print(f"  plot [{i+1}]: {all_data[i][2]['filename'][:25]}")

    # ---- Assign distinct scientific colors to each curve ----
    # Origin color indices: 2=Red 3=Green 4=Blue 5=Cyan 6=Magenta
    #   8=DarkCyan 9=DarkYellow 11=Navy 12=Purple 13=Wine 14=Olive
    palette = [4, 2, 9, 3, 13, 11, 8, 14, 5, 12, 6, 1]
    for i in range(n):
        c = palette[i % len(palette)]
        op.lt_exec(f'layer.plot{i+1}.color = {c};')

    # ---- Format graph (Nature-style XRD) ----
    # Y-axis: auto-range with 2% padding
    y_max_total = offsets[-1] + all_data[-1][1].max() if n > 1 else all_data[0][1].max()
    y_pad = y_max_total * 0.02
    gl.set_ylim(-y_pad, y_max_total + y_pad)

    # X-axis
    gl.set_xlim(5, 90)
    gl.axis('x').title = '2\u03b8 (degree)'

    # Nature style: remove Y-axis title (curves are self-labeled)
    gl.axis('y').title = ''

    # ---- Add curve labels at right endpoints (Nature style) ----
    for i in range(n):
        data = all_data[i]
        angles = data[0]
        intensities = data[1]
        label = data[2]['filename'][:30]
        x_label = angles[-1] + 0.5
        y_label = intensities[-1] + offsets[i]
        op.lt_exec(
            f'{gl.name}!label -p {x_label:.1f} {y_label:.0f} -n "{label}";'
        )

    # ---- Save OPJU ----
    save_dir = os.path.dirname(os.path.abspath(sys.argv[1].strip('"')))
    opju_path = os.path.join(save_dir, 'XRD_Stack.opju')
    op.save(opju_path)
    print(f"\nSaved: {opju_path}")

    # Print summary
    print()
    print("=" * 60)
    print("  Done!  Nature-style XRD stacked plot saved.")
    print(f"  文件数: {n}")
    print("=" * 60)

    return opju_path


# ====================================================================
# Main
# ====================================================================

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nExamples:")
        print("  python raw_to_origin.py sample1.raw sample2.raw")
        print("  python raw_to_origin.py --offset 10000 *.raw")
        input("\nPress Enter to exit...")
        sys.exit(0)

    # Parse arguments
    gap = None       # None = Origin auto gap; user can override with --gap
    files = []
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '--gap' and i + 1 < len(sys.argv):
            gap = float(sys.argv[i + 1])
            i += 2
        else:
            files.append(arg.strip('"'))
            i += 1

    if not files:
        print("ERROR: No .raw files specified.")
        input("Press Enter to exit...")
        sys.exit(1)

    # ---- Parse all RAW files ----
    print("=" * 60)
    print("  Bruker RAW -> Origin XRD Stack Plot")
    print("=" * 60)
    print()

    all_data = []
    for f in files:
        if not os.path.exists(f):
            print(f"  SKIP: not found -> {f}")
            continue
        print(f"  Parsing: {os.path.basename(f)}")
        try:
            angles, intensities, meta = parse_raw(f)
            all_data.append((angles, intensities, meta))
        except Exception as e:
            print(f"  ERROR parsing {f}: {e}")

    if not all_data:
        print("\nERROR: No valid files to process.")
        input("Press Enter to exit...")
        sys.exit(1)

    print(f"\n  Parsed {len(all_data)} file(s) successfully.")

    if gap is not None:
        print(f"  Manual gap: {gap}")

    # ---- Push to Origin ----
    try:
        push_to_origin(all_data, gap=gap)
    except Exception as e:
        print(f"\nERROR connecting to Origin: {e}")
        print("Make sure Origin is installed and originpro package is available.")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)

    input("\nPress Enter to exit...")


if __name__ == '__main__':
    main()
