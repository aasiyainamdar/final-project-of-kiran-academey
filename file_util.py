"""File handling: export report rows to CSV / read skills file."""
import csv
import os
from datetime import datetime

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")


def export_to_csv(rows, report_name):
    """Write a list of dict rows to output/<report_name>_<timestamp>.csv and return the path."""
    if not rows:
        return None
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, f"{report_name}_{datetime.now():%Y%m%d_%H%M%S}.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return path


def print_table(rows):
    """Pretty-print a list of dict rows on the console."""
    if not rows:
        print("  (no records)")
        return
    headers = list(rows[0].keys())
    widths = {h: max(len(str(h)), *(len(str(r[h])) for r in rows)) for h in headers}
    line = " | ".join(str(h).ljust(widths[h]) for h in headers)
    print(line)
    print("-" * len(line))
    for r in rows:
        print(" | ".join(str(r[h]).ljust(widths[h]) for h in headers))
