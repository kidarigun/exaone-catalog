"""차트/chart.json 설정대로 CSV 데이터를 차트가 들어간 엑셀로 만든다 (프로젝트 루트에서 실행)."""
import csv
import json
import sys
from pathlib import Path

CONFIG = Path("차트/chart.json")

from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, PieChart, Reference


def number(text, row, col):
    try:
        return float(str(text).replace(",", "").strip())
    except ValueError:
        sys.exit(f"숫자로 바꿀 수 없는 값이 있습니다: {row}행 {col}열 '{text}'")


def main():
    if not CONFIG.exists():
        sys.exit(f"설정 파일이 없습니다: {CONFIG}")
    cfg = json.loads(CONFIG.read_text(encoding="utf-8-sig"))
    src = Path(cfg.get("csv", "차트/data.csv"))
    out = Path(cfg.get("output", "차트/결과.xlsx"))
    kind = cfg.get("type", "bar")

    with src.open(encoding="utf-8-sig", newline="") as f:
        rows = [r for r in csv.reader(f) if any(c.strip() for c in r)]
    if len(rows) < 2 or len(rows[0]) < 2:
        sys.exit("CSV에 머리글과 데이터가 최소 한 줄씩, 열이 두 개 이상 있어야 합니다.")

    wb = Workbook()
    ws = wb.active
    ws.title = "데이터"
    ws.append(rows[0])
    for i, r in enumerate(rows[1:], start=2):
        ws.append([r[0]] + [number(v, i, j + 2) for j, v in enumerate(r[1:])])
    ws.column_dimensions["A"].width = 16

    n_rows, n_cols = len(rows), len(rows[0])
    chart = {"line": LineChart, "pie": PieChart}.get(kind, BarChart)()
    chart.title = cfg.get("title", "")
    last_col = 2 if kind == "pie" else n_cols
    data = Reference(ws, min_col=2, max_col=last_col, min_row=1, max_row=n_rows)
    cats = Reference(ws, min_col=1, min_row=2, max_row=n_rows)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    if kind != "pie":
        chart.y_axis.title = cfg.get("y_title", "")
    chart.width, chart.height = 18, 9
    ws.add_chart(chart, f"{chr(ord('A') + n_cols + 1)}2")

    out.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)
    print(f"저장함: {out.as_posix()}")


if __name__ == "__main__":
    main()
