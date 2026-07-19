import sys
from PIL import Image, ImageEnhance, ImageOps


def prep_photo(inp, out, size=(220, 220)):
    img = Image.open(inp).convert("L")
    img = ImageOps.autocontrast(img, cutoff=2)
    img = ImageEnhance.Contrast(img).enhance(1.4)
    img = img.resize(size, Image.LANCZOS)
    img.save(out)
    print(f"Saved: {out}")


if __name__ == "__main__":
    prep_photo(
        sys.argv[1] if len(sys.argv) > 1 else "profile.jpg",
        sys.argv[2] if len(sys.argv) > 2 else "profile_processed.png",
    )
