# Scripting

> **Skeleton** — structure plus verified facts; full prose to be written.

## Overview

Scripting in Matchmaker is the glue between selections and the outside world: commands run on accept, previews render item data, and bound actions execute scripts. The two building blocks are templates and environment variables.

## Templates

Templates expand placeholders like `{}` (current item), `{1}` (column 1), `{+}` (all selected), `{$1}` (trailing CLI argument) and run in preview commands, bound action scripts, and the `output_template` / `on_accept` hooks. They are **not** expanded in `start.command` or `envs` values. See [Templates](12-templates.md) for the full reference.

## Environment variables

When Matchmaker executes a command it injects variables: `MM_LINES`, `MM_COLUMNS`, `MM_TOTAL_COUNT`, `MM_MATCH_COUNT`, `MM_SELECT_COUNT`, `MM_POS`, `MM_QUERY`, `MM_PREVIEW_COMMAND`, `MM_OVERRIDE`, `MM_STORE`, `MM_INDEX`, and `MM_MODE` (plus `FZF_*` equivalents). See [Templates](12-templates.md#environment-variables).

## Script commands in binds

- `Execute`, `ExecuteAsync`, `ExecuteThen`, `ExecuteSilent`, `Become`, `BecomeSilent` run a command through `start.shell` (empty shell → `$SHELL`, falling back to `/bin/sh`).
- A first word starting with `@` treats that word as a script path relative to the parent of `MM_OVERRIDE` (absolute paths accepted) and passes the remaining words as arguments without shell parsing — used by presets to ship scripts.
- Exit-code semantics (e.g. distinguishing script exit 0 vs non-zero, resume on signal) are documented in [Queries & misc](13-queries-and-misc.md).

## Data hooks

- `on_accept` — template executed per accepted item (exclusive with `output_template`).
- `Store` action — saves a value into `MM_STORE` for later scripts.

## To write

- End-to-end script examples (pick a file → open in editor; pick a process → kill; etc.).
- `Become` replacement patterns.
- `--list` template testing for iterations.