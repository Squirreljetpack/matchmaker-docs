#!/usr/bin/env python3
"""Generate SVG and PNG logo/favicon assets in docs/public/ from icon.svg (or icon.png)."""

import io
import re
import shutil
import subprocess
import sys
from pathlib import Path
from PIL import Image


def make_square_favicon_svg(svg_text: str) -> str:
    """Return a square-viewBox copy of the SVG centered horizontally for favicons."""
    m = re.search(r'viewBox="([^"]+)"', svg_text)
    if not m:
        return svg_text
    parts = [float(x) for x in m.group(1).split()]
    if len(parts) != 4:
        return svg_text
    vx, vy, vw, vh = parts
    size = max(vw, vh)
    nx = vx - (size - vw) / 2.0
    ny = vy - (size - vh) / 2.0
    out = re.sub(r'viewBox="[^"]+"', f'viewBox="{nx:g} {ny:g} {size:g} {size:g}"', svg_text, count=1)
    out = re.sub(r'\bwidth="[^"]+"', 'width="128"', out, count=1)
    out = re.sub(r'\bheight="[^"]+"', 'height="128"', out, count=1)
    return out


def rasterize_svg(svg_path: Path, height: int = 1024) -> Image.Image:
    """Rasterize an SVG file into an RGBA PIL Image using resvg or rsvg-convert."""
    if shutil.which("resvg"):
        res = subprocess.run(
            ["resvg", "-h", str(height), str(svg_path), "-c"],
            check=True,
            capture_output=True,
        )
        return Image.open(io.BytesIO(res.stdout)).convert("RGBA")
    if shutil.which("rsvg-convert"):
        res = subprocess.run(
            ["rsvg-convert", "-h", str(height), str(svg_path)],
            check=True,
            capture_output=True,
        )
        return Image.open(io.BytesIO(res.stdout)).convert("RGBA")
    raise RuntimeError("Neither 'resvg' nor 'rsvg-convert' is installed to rasterize icon.svg")


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    svg_source = root / "icon.svg"
    png_source = root / "icon.png"

    public_dir = root / "docs" / "public"
    public_dir.mkdir(parents=True, exist_ok=True)

    if svg_source.exists():
        print(f"Using source SVG: {svg_source.name} ({svg_source})")
        svg_text = svg_source.read_text(encoding="utf-8")

        logo_svg = public_dir / "logo.svg"
        logo_svg.write_text(svg_text, encoding="utf-8")
        print(f"✓ Generated {logo_svg.relative_to(root)} ({logo_svg.stat().st_size} bytes)")

        favicon_svg = public_dir / "favicon.svg"
        favicon_svg.write_text(make_square_favicon_svg(svg_text), encoding="utf-8")
        print(f"✓ Generated {favicon_svg.relative_to(root)} ({favicon_svg.stat().st_size} bytes)")

        im = rasterize_svg(svg_source)
    elif png_source.exists():
        print(f"Using source image: {png_source.name} ({png_source})")
        im = Image.open(png_source)
        if im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGBA")
    else:
        print(f"Error: neither icon.svg nor icon.png found in repository root ({root}).", file=sys.stderr)
        sys.exit(1)

    existing_pngs = set(p.name for p in public_dir.glob("*.png"))
    standard_pngs = {"logo.png", "favicon.png"}

    targets = [
        (public_dir / "logo.png", 256, False),
        (public_dir / "favicon.png", 64, True),
    ]

    extra_pngs = existing_pngs - standard_pngs
    if not extra_pngs:
        repo_name = root.name.removesuffix("-docs")
        extra_pngs = {f"{repo_name}.png"}

    for name in sorted(extra_pngs):
        targets.append((public_dir / name, 512, False))

    for dest, max_dim, square_pad in targets:
        cur = im.copy()
        cur.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)

        if square_pad:
            canvas = Image.new("RGBA", (max_dim, max_dim), (0, 0, 0, 0))
            offset = ((max_dim - cur.width) // 2, (max_dim - cur.height) // 2)
            canvas.paste(cur, offset, cur if cur.mode == "RGBA" else None)
            canvas.save(dest, format="PNG", optimize=True)
        else:
            cur.save(dest, format="PNG", optimize=True)

        rel_path = dest.relative_to(root)
        print(f"✓ Generated {rel_path} ({dest.stat().st_size} bytes)")

    print("All icons successfully generated!")


if __name__ == "__main__":
    main()
