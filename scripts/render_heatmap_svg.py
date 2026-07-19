import sys
import json
import os
from datetime import date, timedelta

COLORS = {0: "#161b22", 1: "#0e4429", 2: "#006d32", 3: "#26a641", 4: "#39d353"}


def render(data_path="contributions.json", out="assets/contrib-heatmap.svg",
           box=12, gap=3, pad_x=30, pad_y=20, bg="#0d1117", tc="#8b949e"):
    with open(data_path) as f:
        days = json.load(f)

    step = box + gap
    today = date.today()
    dow = (today.weekday() + 1) % 7  # days since last Sunday
    start = today - timedelta(days=dow) - timedelta(weeks=52)

    weeks = []
    cur = start
    while cur <= today:
        weeks.append([cur + timedelta(days=d) for d in range(7)])
        cur += timedelta(weeks=1)

    W = len(weeks) * step + pad_x * 2
    H = 7 * step + pad_y + 20

    rects, month_labels = [], []
    prev_month = None

    for wi, week in enumerate(weeks):
        x = pad_x + wi * step
        if week[0].month != prev_month and week[0] <= today:
            month_labels.append(
                f'<text x="{x}" y="{H - 6}" '
                f'font-family="\'Courier New\',Courier,monospace" '
                f'font-size="9" fill="{tc}">{week[0].strftime("%b")}</text>'
            )
            prev_month = week[0].month
        for di, day in enumerate(week):
            if day > today:
                continue
            y = pad_y // 2 + di * step
            lvl = days.get(day.strftime("%Y-%m-%d"), 0)
            delay = f"{(wi + di) * 0.007:.3f}s"
            rects.append(
                f'<rect x="{x}" y="{y}" width="{box}" height="{box}" rx="2" '
                f'fill="{COLORS.get(lvl, COLORS[0])}" opacity="0">'
                f'<animate attributeName="opacity" from="0" to="1" '
                f'dur="0.25s" begin="{delay}" fill="freeze"/>'
                f'</rect>'
            )

    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">\n'
            f'<rect width="{W}" height="{H}" fill="{bg}"/>\n'
            + "\n".join(rects) + "\n"
            + "\n".join(month_labels) + "\n"
            f'</svg>\n'
        )
    print(f"Saved: {out} ({W}x{H}px)")


if __name__ == "__main__":
    render(
        sys.argv[1] if len(sys.argv) > 1 else "contributions.json",
        sys.argv[2] if len(sys.argv) > 2 else "assets/contrib-heatmap.svg",
    )
