# Getting started

Matchmaker (binary `mm`) is a fast, configurable and intuitive fuzzy searcher for the terminal. It filters rows piped into it, lets you pick one or more with the keyboard (or mouse), and prints the selections back to stdout.

> **Skeleton** — this page is part of the documentation skeleton: structure plus verified facts. Full prose to be written.

## Overview

- Fuzzy matching with fzf-style scoring, smart case, and word-boundary awareness (see [Queries & matching](07-querying.md)).
- Keyboard-first TUI with an optional preview panel (see [The interface](03-interface.md)).
- Input is piped in, or produced by a configured command (see [Input & data sources](04-input-and-data.md)).
- Output is printed as the full line (or per-column templates) to stdout.
- Everything is configurable through a TOML config file, CLI overrides, and presets (see [Configuration](08-configuration.md)).

## Installation

To write: platform install instructions (cargo install, install script, brew/npm packaging). The release binary is named `mm`; release assets follow `matchmaker-cli-<arch>-<os>` naming.

## First run

- `mm` with no arguments runs the default command (files in the current directory) when stdin is a terminal.
- Pipe a command's output into it: `fd . | mm` or `find . -print0 | mm -- -0` style patterns.
- Type to filter, press `enter` to accept; the selected line is printed to stdout.
- `mm --test-keys` prints key events (for validating terminal key reporting).
- `mm --doc options` prints the command-line reference in the terminal.

## Getting help

- `mm --help` lists all flags.
- `mm --doc <options|binds|template|other>` displays the built-in documentation.
- See [Command line](10-command-line.md), [Binds & actions](11-binds-and-actions.md), [Templates](12-templates.md), and [Queries & misc](13-queries-and-misc.md) for the same content on the web.

## Next steps

- [Core workflows](02-core-workflows.md) — common usage patterns.
- [Configuration](08-configuration.md) — write your first config file with `mm --dump-config`.
- [Presets & workflows](09-presets.md) — ready-made config bundles.