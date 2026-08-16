# The interface

> **Skeleton** — structure plus verified facts; full prose to be written.

## Overview

The TUI is composed of a query input bar, a results table, a status line, an optional header/footer, and an optional preview panel. The layout is fully configurable via the `[query]`, `[results]`, `[status]`, `[header]`, `[footer]` and `[preview]` config sections.

## Query bar

- The prompt style is configurable (`[query] prompt_style.fg`, `prompt_style.modifier`).
- Word movement stops at whitespace plus any configured `word_boundaries` characters (e.g. `.`, `/`).

## Results

- `[results]` configures wrapping, truncation, and max height of the results list.
- Columns are split from each input line and display per `[columns]` config (see [Columns](05-columns.md)).
- Rows are fuzzy-matched and ranked (see [Queries & matching](07-querying.md)).

## Status, header, footer

- The status line renders a template (e.g. `\m/\t` for matched/total counts). Details of status template tokens to write.
- The header and footer are configurable free-form sections.

## Preview

- Shows a rendered command output for the current item (defaults: `eza`/`find` for directories, `bat`/`cat` for files).
- Layouts, sizes, sides and borders are configured under `[[preview.layout]]` (see [Preview](06-preview.md)).

## Modes

The application runs in one or more mode tags, which gate binds (e.g. `"0,1^^enter"`). Default tags depend on whether stdin and stdout are terminals:

| stdin | stdout | default mode |
| ----- | ------ | ------------ |
| tty   | tty    | `0,1`        |
| tty   | piped  | `0`          |
| piped | tty    | `1`          |
| piped | piped  | `""`         |

Binds can require or exclude modes with prefix filters (see [Binds & actions](11-binds-and-actions.md)).

## Fullscreen / overlay

- `-F` runs in fullscreen.
- The library also supports an overlay picker mode (see [Using the library](16-library.md)).

## To write

- Layout diagram and screenshot.
- Mouse support (`mouse_events`, scroll debounce) details.
- ReloadNext/ReloadPrev switching between additional commands from the UI.