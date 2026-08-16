# Configuration

> **Skeleton** — structure plus verified facts; full prose to be written.

## Overview

Matchmaker's configuration is a TOML file with hierarchical sections. Every setting can also be overridden from the command line, and presets bundle ready-made configurations (see [Presets & workflows](09-presets.md)).

## Getting the default config

```sh
mm --dump-config
```

- With stdout as a terminal, writes the default config to the default location (with comments).
- With stdout piped (`mm --dump-config | cat`), writes the current (resolved) configuration to stdout.

## Locations

The config directory is resolved in order:

1. `$MATCHMAKER_CONFIG_DIR` — if set and the directory exists.
2. `~/.config/matchmaker` — if it exists.
3. Platform config directory + `matchmaker` (e.g. `$XDG_CONFIG_HOME/matchmaker`).

The config file is `config.toml` in that directory. `-o/--override <PATH>` applies an override file (paths without a `.toml` extension refer to a preset); `--config <PATH>` selects an explicit config path.

## Sections

Top-level sections (see the shipped default config for full field lists):

| Section | Purpose |
| ------- | ------- |
| `[tui]` | Tick rate, mouse events, clear-on-exit, OSC52, fullscreen |
| `[query]` | Prompt style, word boundaries, debounce |
| `[results]` | Wrapping, truncation, max height |
| `[status]` / `[header]` / `[footer]` | Displayed bars and templates |
| `[preview]` / `[[preview.layout]]` / `[previewer]` | Preview behavior and panes (see [Preview](06-preview.md)) |
| `[matcher]` / `[sort]` | Matching and ranking (see [Queries & matching](07-querying.md)) |
| `[columns]` | Column splitting and naming (see [Columns](05-columns.md)) |
| `[start]` / `start.command` | Populating commands, separators, shell, modes (see [Input & data sources](04-input-and-data.md)) |
| `[exit]` | Auto-exit behaviors (`first`, `allow_empty`, `abort_empty`, `last_key_path`) |
| `[envs]` | Fixed environment variables injected into spawned commands |
| `[binds]` | Key/mouse/semantic bindings (see [Binds & actions](11-binds-and-actions.md)) |

## Command-line overrides

Configuration keys can be overridden directly on the command line as `path=value` or `path value` after the flags — see [Command line](10-command-line.md).

## To write

- Full field reference per section (option-by-option).
- The `on_accept` vs `output_template` interplay.
- Multiple-config management (`--download` targets, per-project configs).