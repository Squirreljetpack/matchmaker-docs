# Lua commands

> **Skeleton** — structure plus verified facts; full prose to be written.

## Overview

Matchmaker embeds a Lua runtime (vendored Lua 5.4) that can be used for scripting parts of the configuration.

> **To write** — the extent of Lua usage (config values, action logic, pre-processing), the full API surface exposed to scripts, and examples are not yet documented here.

## Verified facts

- Lua support is compiled into the CLI by default (`matchmaker-cli` depends on `mlua` with `lua54` + `vendored` features; the `mlua` cargo feature gates it, default features include it).
- Scripts can read the injected environment variables (e.g. `MM_OVERRIDE`, `MM_PREVIEW_COMMAND`, …) through an `env` table.

## Configuration points (candidates)

To write: which config fields accept Lua (e.g. command expressions, `envs` values, template functions), and the scripting entry points (binds, hooks, sort/completion logic).

## References

- [Scripting](14-scripting.md) — environment variables and templates shared with Lua scripts.
- [Templates](12-templates.md#environment-variables) — the injected variables available in scripts.