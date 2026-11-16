#!/usr/bin/env python3
"""Generate the folded-ribbon SVG icon and color variants."""

import argparse
import colorsys
import math
import sys
from pathlib import Path

PRESETS = {
    "blue-teal": [
        {"front": "#437ce7", "back": "#3361b7", "shadow": "#1d3d7a"},
        {"front": "#32b7bc", "back": "#21969d", "shadow": "#125b60"},
    ],
    "slate-green": [
        {"front": "#3d4a53", "back": "#2f3942", "shadow": "#1b2228"},
        {"front": "#17b278", "back": "#118a5d", "shadow": "#0a5438"},
    ],
    "black-indigo": [
        {"front": "#0a0a0c", "back": "#050507", "shadow": "#000000"},
        {"front": "#5942db", "back": "#3a2a8d", "shadow": "#201654"},
    ],
    "coral-maroon": [
        {"front": "#ee574e", "back": "#802b54", "shadow": "#4e1733"},
        {"front": "#fa6c62", "back": "#782956", "shadow": "#491634"},
    ],
}


def parse_hex(color: str) -> tuple[float, float, float]:
    c = color.strip().lstrip("#")
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    if len(c) != 6:
        raise ValueError(f"Invalid hex color: {color!r}")
    r = int(c[0:2], 16) / 255.0
    g = int(c[2:4], 16) / 255.0
    b = int(c[4:6], 16) / 255.0
    return r, g, b


def format_hex(r: float, g: float, b: float) -> str:
    ri = max(0, min(255, round(r * 255)))
    gi = max(0, min(255, round(g * 255)))
    bi = max(0, min(255, round(b * 255)))
    return f"#{ri:02x}{gi:02x}{bi:02x}"


def scale_lightness(hex_color: str, l_factor: float, s_factor: float = 1.0) -> str:
    r, g, b = parse_hex(hex_color)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    l = max(0.0, min(1.0, l * l_factor))
    s = max(0.0, min(1.0, s * s_factor))
    nr, ng, nb = colorsys.hls_to_rgb(h, l, s)
    return format_hex(nr, ng, nb)


def build_palette_from_colors(fronts: list[str], backs: list[str] | None = None) -> list[dict[str, str]]:
    palette = []
    for idx, front in enumerate(fronts):
        front_hex = format_hex(*parse_hex(front))
        if backs and idx < len(backs):
            back_hex = format_hex(*parse_hex(backs[idx]))
        else:
            back_hex = scale_lightness(front_hex, l_factor=0.76, s_factor=0.92)
        shadow_hex = scale_lightness(back_hex, l_factor=0.60, s_factor=0.95)
        palette.append({"front": front_hex, "back": back_hex, "shadow": shadow_hex})
    return palette


def capsule_segment_path(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    half_w: float,
    cap_start: bool = True,
    cap_end: bool = True,
) -> str:
    """Build a C1-smooth ribbon segment from (x1, y1) to (x2, y2) with given half-width."""
    dx = x2 - x1
    dy = y2 - y1
    length = math.hypot(dx, dy)
    ux, uy = dx / length, dy / length
    nx, ny = -uy, ux

    ax, ay = x1 + nx * half_w, y1 + ny * half_w
    bx, by = x2 + nx * half_w, y2 + ny * half_w
    cx, cy = x2 - nx * half_w, y2 - ny * half_w
    ex, ey = x1 - nx * half_w, y1 - ny * half_w

    parts = [f"M {ax:.2f} {ay:.2f}", f"L {bx:.2f} {by:.2f}"]
    if cap_end:
        parts.append(f"A {half_w:.2f} {half_w:.2f} 0 0 0 {cx:.2f} {cy:.2f}")
    else:
        parts.append(f"L {cx:.2f} {cy:.2f}")
    parts.append(f"L {ex:.2f} {ey:.2f}")
    if cap_start:
        parts.append(f"A {half_w:.2f} {half_w:.2f} 0 0 0 {ax:.2f} {ay:.2f}")
    else:
        parts.append(f"L {ax:.2f} {ay:.2f}")
    parts.append("Z")
    return " ".join(parts)


def generate_ribbon_svg(palette: list[dict[str, str]], turns: int = 4) -> str:
    """Generate the folded-ribbon SVG string for a given color palette and turn count."""
    if turns < 1:
        raise ValueError("turns must be >= 1")

    half_w = 37.5
    pad_x = 20.0
    pad_y = 64.0
    xL = pad_x + half_w
    xR = 346.0 - half_w
    dy = 96.0
    y0 = pad_y
    y_end = y0 + 2 * turns * dy
    total_w = 366.0
    total_h = y_end + pad_y

    xR_clip = xR + half_w
    slope = dy / (xR - xL)
    ext = 60.0  # extend past right clip so top/bottom ends are cleanly sliced vertically

    defs = [
        f'<clipPath id="ribbon-clip"><rect x="0" y="0" width="{xR_clip:.2f}" height="{total_h:.2f}"/></clipPath>'
    ]
    back_paths = []
    front_paths = []

    for i in range(turns):
        c = palette[i % len(palette)]
        ly = y0 + (2 * i + 1) * dy
        ry_top = y0 + (2 * i) * dy
        ry_bot = y0 + (2 * i + 2) * dy

        # Back segment: down-left from right side to left turn
        rx_start = xR + ext if i == 0 else xR
        ry_start = ry_top - ext * slope if i == 0 else ry_top
        back_d = capsule_segment_path(
            rx_start, ry_start, xL, ly, half_w, cap_start=(i > 0), cap_end=True
        )

        grad_id = f"bg_{i}"
        if i == 0:
            defs.append(
                f'<linearGradient id="{grad_id}" x1="0%" y1="100%" x2="100%" y2="0%">'
                f'<stop offset="0%" stop-color="{c["shadow"]}"/>'
                f'<stop offset="30%" stop-color="{c["back"]}"/>'
                f'<stop offset="100%" stop-color="{c["back"]}"/>'
                f"</linearGradient>"
            )
        else:
            defs.append(
                f'<linearGradient id="{grad_id}" x1="0%" y1="50%" x2="100%" y2="50%">'
                f'<stop offset="0%" stop-color="{c["shadow"]}"/>'
                f'<stop offset="28%" stop-color="{c["back"]}"/>'
                f'<stop offset="72%" stop-color="{c["back"]}"/>'
                f'<stop offset="100%" stop-color="{c["shadow"]}"/>'
                f"</linearGradient>"
            )
        back_paths.append(f'<path d="{back_d}" fill="url(#{grad_id})"/>')

        # Front segment: down-right from left turn to right side
        rx_end = xR + ext if i == turns - 1 else xR
        ry_end_seg = ry_bot + ext * slope if i == turns - 1 else ry_bot
        front_d = capsule_segment_path(
            xL, ly, rx_end, ry_end_seg, half_w, cap_start=True, cap_end=(i < turns - 1)
        )
        front_paths.append(f'<path d="{front_d}" fill="{c["front"]}"/>')

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_w:.0f} {total_h:.0f}" '
        f'width="{total_w:.0f}" height="{total_h:.0f}">\n'
        f"  <defs>\n    " + "\n    ".join(defs) + "\n  </defs>\n"
        f'  <g clip-path="url(#ribbon-clip)">\n'
        f'    <g id="back-segments">\n      ' + "\n      ".join(back_paths) + "\n    </g>\n"
        f'    <g id="front-segments">\n      ' + "\n      ".join(front_paths) + "\n    </g>\n"
        f"  </g>\n"
        f"</svg>\n"
    )


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(
        description="Generate the Matchmaker folded-ribbon SVG icon and color variants."
    )
    parser.add_argument(
        "-p",
        "--preset",
        default="blue-teal",
        help="Built-in color preset name, or 'all' to generate every preset (default: blue-teal).",
    )
    parser.add_argument(
        "-c",
        "--colors",
        help="Comma-separated hex colors for alternating turns (e.g. '#437ce7,#32b7bc'). Overrides --preset.",
    )
    parser.add_argument(
        "--back-colors",
        help="Optional comma-separated hex colors for the back folds when using --colors.",
    )
    parser.add_argument(
        "-t",
        "--turns",
        type=int,
        default=4,
        help="Number of left turns/peaks (default: 4).",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=root / "docs" / "public" / "logo.svg",
        help="Output SVG file path (default: docs/public/logo.svg).",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=root,
        help="Output directory when --preset all is used (writes icon-<preset>.svg).",
    )
    parser.add_argument(
        "--list-presets",
        action="store_true",
        help="List available built-in color presets and exit.",
    )

    args = parser.parse_args()

    if args.list_presets:
        for name, pal in PRESETS.items():
            colors_str = ", ".join(f"{c['front']} (back {c['back']})" for c in pal)
            print(f"  {name}: {colors_str}")
        return 0

    if args.colors:
        fronts = [c for c in args.colors.split(",") if c.strip()]
        backs = [c for c in args.back_colors.split(",") if c.strip()] if args.back_colors else None
        palette = build_palette_from_colors(fronts, backs)
        svg = generate_ribbon_svg(palette, turns=args.turns)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(svg, encoding="utf-8")
        print(f"Generated {args.output}")
        return 0

    if args.preset == "all":
        args.out_dir.mkdir(parents=True, exist_ok=True)
        for name, palette in PRESETS.items():
            dest = args.out_dir / f"icon-{name}.svg"
            dest.write_text(generate_ribbon_svg(palette, turns=args.turns), encoding="utf-8")
            print(f"Generated {dest}")
        return 0

    if args.preset not in PRESETS:
        print(
            f"Error: unknown preset {args.preset!r}. Available: {', '.join(PRESETS)}",
            file=sys.stderr,
        )
        return 1

    svg = generate_ribbon_svg(PRESETS[args.preset], turns=args.turns)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(svg, encoding="utf-8")
    print(f"Generated {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
