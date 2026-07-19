import sys
import os

LINES = [
    ("header", "filippo", "pers-fs"),
    ("sep",),
    ("empty",),
    ("kv", "Role",      "Analytics Engineer"),
    ("kv", "Location",  "Berlin"),
    ("kv", "Focus",     "Music data projects"),
    ("empty",),
    ("sep",),
    ("empty",),
    ("kv", "Languages", "SQL · Python · Bash"),
    ("kv", "ELT",       "Fivetran · dlt · Airflow · dbt"),
    ("kv", "Warehouse", "BigQuery · Snowflake"),
    ("kv", "BI",        "Looker · LookML · Tableau · Lightdash"),
    ("kv", "Cloud",     "AWS · GCP · Docker"),
    ("empty",),
    ("sep",),
    ("empty",),
    ("kv", "Contact",   "linkedin/filippo-struffi"),
    ("empty",),
]


def make_info_card(out, width=490, fs=13, lh=22,
                   bg="#0d1117", lc="#7ee787", vc="#e6edf3",
                   dc="#484f58", delay=0.07):
    H = len(LINES) * lh + 20
    elems = []

    for i, line in enumerate(LINES):
        kind = line[0]
        if kind == "empty":
            continue
        t0 = f"{i * delay:.3f}s"
        y = 15 + i * lh + fs
        anim = (
            f'<animate attributeName="opacity" from="0" to="1" '
            f'dur="0.15s" begin="{t0}" fill="freeze"/>'
        )
        mono = "font-family=\"'Courier New',Courier,monospace\""

        if kind == "header":
            user, host = line[1], line[2]
            elems.append(
                f'<text opacity="0" x="15" y="{y}" {mono} '
                f'font-size="{fs}" font-weight="bold">'
                f'<tspan fill="{lc}">{user}</tspan>'
                f'<tspan fill="{dc}">@</tspan>'
                f'<tspan fill="{vc}">{host}</tspan>'
                f'{anim}</text>'
            )
        elif kind == "sep":
            elems.append(
                f'<text opacity="0" x="15" y="{y}" {mono} '
                f'font-size="{fs}" fill="{dc}">'
                f'{"─" * 26}{anim}</text>'
            )
        elif kind == "kv":
            key, val = line[1], line[2]
            safe_val = val.replace("&", "&amp;")
            label = key.ljust(10)
            elems.append(
                f'<text opacity="0" x="15" y="{y}" {mono} font-size="{fs}">'
                f'<tspan fill="{lc}">{label}</tspan>'
                f'<tspan fill="{vc}">{safe_val}</tspan>'
                f'{anim}</text>'
            )

    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{H}">\n'
            f'<rect width="{width}" height="{H}" fill="{bg}"/>\n'
            + "\n".join(elems) + "\n"
            f'</svg>\n'
        )
    print(f"Saved: {out} ({width}x{H}px)")


if __name__ == "__main__":
    make_info_card(sys.argv[1] if len(sys.argv) > 1 else "assets/info-card.svg")
