import sys
import os
import numpy as np
from PIL import Image

# Dense (dark) to sparse (light) — 70-level ramp
CHARS = "@$B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`'. "


def to_ascii(path, cols=80, char_aspect=0.55):
    img = Image.open(path).convert("L")
    w, h = img.size
    rows = int(cols * (h / w) * char_aspect)
    img = img.resize((cols, rows), Image.LANCZOS)
    px = np.array(img)
    n = len(CHARS) - 1
    return ["".join(CHARS[int(p / 255 * n)] for p in row) for row in px]


def make_svg(lines, out, fs=8, cw=4.8, lh=10,
             bg="#0d1117", fg="#c9d1d9", row_delay=0.04):
    W = int(max(len(l) for l in lines) * cw) + 10
    H = int(len(lines) * lh) + 10

    defs, texts = [], []
    for i, line in enumerate(lines):
        t0 = f"{i * row_delay:.3f}s"
        cid = f"c{i}"
        yt = 5 + i * lh
        defs.append(
            f'<clipPath id="{cid}">'
            f'<rect x="0" y="{yt}" width="0" height="{lh}">'
            f'<animate attributeName="width" from="0" to="{W}" '
            f'dur="0.12s" begin="{t0}" fill="freeze"/>'
            f'</rect></clipPath>'
        )
        safe = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        texts.append(
            f'<text clip-path="url(#{cid})" x="5" y="{yt + fs}" '
            f'font-family="\'Courier New\',Courier,monospace" font-size="{fs}" '
            f'fill="{fg}" xml:space="preserve">{safe}</text>'
        )

    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">\n'
            f'<rect width="{W}" height="{H}" fill="{bg}"/>\n'
            f'<defs>\n' + "\n".join(defs) + "\n</defs>\n"
            + "\n".join(texts) + "\n</svg>"
        )
    print(f"Saved: {out} ({W}x{H}px, {len(lines)} rows)")


if __name__ == "__main__":
    img_path = sys.argv[1] if len(sys.argv) > 1 else "profile_processed.png"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "assets/ascii-portrait.svg"
    make_svg(to_ascii(img_path), out_path)
