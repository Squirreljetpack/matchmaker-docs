#!/usr/bin/env python3
"""Sync reference docs and media assets from ../matchmaker into docs/."""

import re
import shutil
import subprocess
import sys
from pathlib import Path

REFERENCE_DOCS = [
    "options.md",
    "binds.md",
    "template.md",
    "pager.md",
    "image.md",
    "execute.md",
    "other.md",
]

MEDIA_ASSETS = [
    ("matchmaker-lib/assets/splash.png", "splash.png"),
    ("matchmaker-lib/assets/context.png", "context.png"),
    ("matchmaker-lib/assets/ripgrep.png", "ripgrep.png"),
    ("matchmaker-lib/assets/webm/ps.mp4", "ps.mp4"),
    ("matchmaker-lib/assets/webm/git.mp4", "git.mp4"),
    ("matchmaker-lib/assets/webm/all.gif", "all.gif"),
    ("matchmaker-cli/assets/presets/csv.png", "csv.png"),
]

OPTIONAL_MEDIA_ASSETS = [
    ("%%THEME_TOUR/theme-tour.mp4", "theme-tour.mp4"),
]

POSTER_SEEK_ARGS: dict[str, tuple[str, str]] = {
    "git.mp4": ("-ss", "35"),
    "theme-tour.mp4": ("-sseof", "-0.1"),
}

# Standard HTML/comment/autolink patterns that Vue's template compiler accepts as-is.
SAFE_ANGLE_RE = re.compile(
    r"^<(?:https?://\S+|mailto:\S+|!--.*?--|/?(?:a|br|code|details|em|img|kbd|p|pre|span|strong|sub|sup|summary|table|tbody|td|th|thead|tr|video|source)\b[^>]*>)",
    re.IGNORECASE,
)


def normalize_markdown(text: str) -> str:
    """Normalize raw angle brackets outside code spans/fences for VitePress/Vue."""
    out_lines: list[str] = []
    in_fence = False
    fence_marker = ""

    for line in text.splitlines(keepends=True):
        stripped = line.lstrip()
        if not in_fence:
            m = re.match(r"^(`{3,}|~{3,})", stripped)
            if m:
                in_fence = True
                fence_marker = m.group(1)[0] * len(m.group(1))
                out_lines.append(line)
                continue
        else:
            if stripped.startswith(fence_marker) and stripped[len(fence_marker):].strip() == "":
                in_fence = False
                fence_marker = ""
            out_lines.append(line)
            continue

        # Process line outside fenced blocks while preserving inline `...` code spans.
        parts = re.split(r"(`+[^`]*`+)", line)
        for idx in range(0, len(parts), 2):
            seg = parts[idx]
            if "<" not in seg:
                continue
            # Escape angle-bracket placeholders like <DOC> or <ARG> that are not HTML or autolinks.
            def _replace_angle(match: re.Match[str]) -> str:
                token = match.group(0)
                if SAFE_ANGLE_RE.match(token):
                    return token
                return f"&lt;{token[1:-1]}&gt;"

            seg = re.sub(r"<[^<>\s][^<>]*>", _replace_angle, seg)
            parts[idx] = seg
        out_lines.append("".join(parts))

    return "".join(out_lines)


def maybe_extract_poster(video_path: Path) -> None:
    """Generate a PNG poster for tracked video clips when ffmpeg is installed."""
    seek = POSTER_SEEK_ARGS.get(video_path.name)
    if seek is None or not shutil.which("ffmpeg"):
        return
    poster = video_path.with_suffix(".png")
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            seek[0],
            seek[1],
            "-i",
            str(video_path),
            "-update",
            "1",
            "-frames:v",
            "1",
            str(poster),
        ],
        check=True,
    )


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    source_root = root.parent / "matchmaker"
    docs_src = source_root / "matchmaker-cli" / "assets" / "docs"
    docs_dest = root / "docs"
    images_dest = docs_dest / "images"

    if not docs_src.is_dir():
        print(f"Error: reference docs directory not found: {docs_src}", file=sys.stderr)
        sys.exit(1)

    docs_dest.mkdir(parents=True, exist_ok=True)
    images_dest.mkdir(parents=True, exist_ok=True)

    synced_docs = 0
    for name in REFERENCE_DOCS:
        src = docs_src / name
        if not src.is_file():
            print(f"Error: missing reference doc: {src}", file=sys.stderr)
            sys.exit(1)
        content = src.read_text(encoding="utf-8")
        normalized = normalize_markdown(content)
        (docs_dest / name).write_text(normalized, encoding="utf-8")
        synced_docs += 1

    synced_media = 0
    for rel_src, dest_name in MEDIA_ASSETS:
        src = source_root / rel_src
        if not src.is_file():
            print(f"Error: missing media asset: {src}", file=sys.stderr)
            sys.exit(1)
        dst = images_dest / dest_name
        shutil.copy2(src, dst)
        synced_media += 1
        maybe_extract_poster(dst)

    for rel_src, dest_name in OPTIONAL_MEDIA_ASSETS:
        src = source_root / rel_src
        if src.is_file():
            dst = images_dest / dest_name
            shutil.copy2(src, dst)
            synced_media += 1
            maybe_extract_poster(dst)

    print(
        f"Synced {synced_docs} reference docs and {synced_media} media assets "
        f"from {source_root}"
    )


if __name__ == "__main__":
    main()
