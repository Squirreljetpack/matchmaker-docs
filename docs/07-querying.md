# Queries & matching

> **Skeleton** — structure plus verified facts; full prose to be written.

## Overview

Matchmaker's matcher is built on [Nucleo](https://github.com/helix-editor/nucleo) with fzf-style scoring: smart case, consecutive-match boosting, and start-of-word preference.

## How matching works

1. Characters match in order but not necessarily consecutively; shorter gaps and consecutive runs score higher.
2. Multiple whitespace-separated tokens must each match (logical AND).
3. Smart case: a lowercase query matches case-insensitively; uppercase letters force case-sensitivity.

## Query operators

`abc` fuzzy match, `'abc` literal substring, `^abc` prefix, `abc$` suffix, `^abc$` exact, `!abc` exclude, `\ ` escaped space. For the full reference see [Queries & misc](13-queries-and-misc.md) (this page will host the deeper walkthroughs).

## Word boundaries

- Word-movement in the query bar and boundary-aware tokenization stop at whitespace plus configured `word_boundaries` characters (`[query] word_boundaries`, e.g. `['.', '/']`), in addition to whitespace.

## Matcher configuration

- `[matcher]` configures matching options (e.g. `ansi` pre-processing of ANSI sequences).
- `[sort]` configures initial sorting: `sort` mode, reverse, threshold, and column-aware sorting.
- The matcher runs on a worker thread and rescans as you type (debounce configurable via `[tui] sleep_ms` / `[query]`… — to verify exact debounce option).

## To write

- Column-scoped queries and how `%column` filters interact with tokens.
- Ranking details: exact matches, prefix matches, positions of matches.
- Long-input performance notes.