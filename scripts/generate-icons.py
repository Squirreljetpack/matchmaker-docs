#!/usr/bin/env python3
"""Derive the docs/public/ favicon assets from the logo.svg source vector."""

import re
import shutil
import subprocess
import sys
from pathlib import Path


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


def render_png(svg_path: Path, dest: Path, width: int) -> None:
    """Rasterize an SVG file straight to a PNG of the requested width."""
    result = subprocess.run(
        ["resvg", str(svg_path), str(dest), "--width", str(width)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr.strip() or f"resvg failed rendering {dest.name}", file=sys.stderr)
        sys.exit(result.returncode)


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    source = root / "docs" / "public" / "logo.svg"

    if not source.exists():
        print(f"Error: {source.relative_to(root)} not found.", file=sys.stderr)
        sys.exit(1)

    if shutil.which("resvg") is None:
        print("Error: resvg not found on PATH (cargo install resvg).", file=sys.stderr)
        sys.exit(1)

    print(f"Using source vector: {source.name} ({source})")
    svg_text = source.read_text(encoding="utf-8")

    public_dir = root / "docs" / "public"
    public_dir.mkdir(parents=True, exist_ok=True)

    favicon_svg = public_dir / "favicon.svg"
    favicon_svg.write_text(make_square_favicon_svg(svg_text), encoding="utf-8")
    print(f"✓ Generated {favicon_svg.relative_to(root)} ({favicon_svg.stat().st_size} bytes)")

    favicon_png = public_dir / "favicon.png"
    render_png(favicon_svg, favicon_png, 64)
    print(f"✓ Generated {favicon_png.relative_to(root)} ({favicon_png.stat().st_size} bytes)")

    print("All icons successfully generated!")


if __name__ == "__main__":
    main()
