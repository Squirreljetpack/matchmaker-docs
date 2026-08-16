# Diagnostics & logging

> **Skeleton** — structure plus verified facts; full prose to be written.

## Overview

Matchmaker logs to a file and reports errors/steps on stderr with a severity prefix. Verbosity is controlled with repeated flags.

## Verbosity

- `-q...` — reduce verbosity (repeatable).
- `-v...` — increase verbosity (repeatable).

## Logging

- A log file (named after the binary, e.g. `mm.log`) is written to the state directory (platform state dir, falling back to `~/.local/state`).

## Reported errors

Errors are printed to stderr with a tag such as `[ERRO: TUI]` / `[ERRO]` / `[INFO]`. The exit code distinguishes the failure kind (see [Queries & misc](13-queries-and-misc.md#exit-codes)):

| Code | Meaning                                  |
| ---- | ---------------------------------------- |
| 0    | Success                                  |
| 11   | Start error (config/command setup)       |
| 100  | Resumed — signal from `BecomeOrConfirm` scripts |
| 125  | Event loop closed                        |
| 400  | No match, with a chunk error             |
| 404  | No match                                 |
| n    | Exit code passed through from `Abort(n)` |

## Last key

- `mm --last-key` prints the last key pressed in the previous `mm` run; the key is persisted to the state directory (configurable via `exit.last_key_path`).

## To write

- Log file rotation/cleanup.
- TUI error surfaces (config parse errors, invalid binds) and how to recover.
- `--test-keys` as a diagnostics tool for key escapes.