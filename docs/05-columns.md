# Columns

> **Skeleton** — structure plus verified facts; full prose to be written.

## Overview

Each input line can be split into columns. Columns support filtering, hidden columns, per-column templates, and column-aware sorting.

## Splitting

`columns.split` controls how lines are parsed:

- `None` — no splitting (single column).
- `Delimiter(regex)` — split the line by a regex (e.g. `\s+` or `,`).
- `Regexes([regex])` — apply a sequence of regexes to capture specific parts of the line.

### Capture groups

When a delimiter regex contains named groups, each named match is assigned to the column of that name (e.g. `(?P<name>\w+),(?P<age>\d+),(\w+)` maps `name` → column `"name"`, `age` → `"age"`); unnamed groups map to columns in sequence.

## Naming

- `columns.names` is a list of per-column settings (`name`, `filter`, `hidden`).
- If names are unspecified, columns are automatically named `1`, `2`, … up to `columns.max`.
- Column names must be alphanumeric; numeric names can conflict with template column indices, so avoid integer column names when names are set (see [Templates](12-templates.md)).

## Filtering by column

- Filter a specific column with `%name` or any unambiguous abbreviation: `%path .toml` matches items whose `path` column ends with `.toml`.
- Columns after `columns.max` are inaccessible.

## Hidden columns

Hidden columns hide a column from the display while keeping it available to filters, sorting, and templates.

## Templates

- `{col}`, `{=col}`, `{+col}`, `{-col}` reference a column by name or 1-based index; `{0}` is the primary (default) column; `!` is the active column.
- Column ranges are supported (see [Templates](12-templates.md)).

## To write

- Column-aware sorting (`sort` modes and columns).
- `PreprocessOptions` (ansi/trim/sanitize) as they affect column parsing.
- Examples for common data shapes (git status, JSON, etc.).