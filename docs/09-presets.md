# Presets & workflows

> **Skeleton** — structure plus verified facts; full prose to be written.

## Overview

Presets are TOML override files that bundle a ready-made configuration (binds, previews, sources). They are stored in the config directory's `presets/` subfolder and referenced by `-o <NAME>` (an override path without a `.toml` extension resolves to a preset).

## Managing presets

- `mm --presets` — list installed presets (prints their paths).
- `mm --download [<FOLDER>]` — download presets from the GitHub repository. With no argument, downloads all presets; with `<FOLDER>` (no space: `--download=<FOLDER>`), downloads a subfolder.
- `mm --list [<N@ALIAS | N-M | N:TEMPLATE | TEMPLATE>]` — test a preset or command directly (see [Command line](10-command-line.md); the modes are explained in `mm --doc other`).

## Authoring guide

The shipped presets' README recommends a definition order:

1. Initial section: `source`, `[start]`, `[envs]`, `[tui]`, `[matcher]`, `[exit]`.
2. UI: `[tui]` plus `RenderConfig` subfields such as `[query]`.
3. Preview: `[previewer]`, `[preview]`.
4. Scripts: `[binds]` — actual binds first, then alias definitions.

## Environment

- `MM_OVERRIDE` is set to the path of the first applied override (canonicalized), so preset commands can reference `dirname "$MM_OVERRIDE"` for files shipped alongside the preset.
- Preset scripts (binds starting with `@`) resolve relative to the parent of `MM_OVERRIDE` (see [Binds & actions](11-binds-and-actions.md)).

## To write

- Preset gallery and walkthroughs.
- `@next` / `@prev` aliases for cycling additional commands in presets.
- Downloading and pinning preset versions.