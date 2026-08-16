# Using the library

> **Skeleton** — structure plus verified facts; full prose to be written.

## Overview

The core of Matchmaker is a reusable Rust library (`matchmaker-lib`) with a thin CLI (`matchmaker-cli`, binary `mm`) on top. Applications can embed a picker, an overlay, or a non-interactive matcher.

## Crates

| Crate | Purpose |
| ----- | ------- |
| `matchmaker-lib` | Core: event loop, renderer, matcher, preview, configurations |
| `matchmaker-cli` | The `mm` binary and its support code (config loading, presets, Lua) |
| `matchmaker-partial` (+ `-macros`) | Partial-config types for building configurations incrementally |

## Running the examples

The library ships examples in `matchmaker-lib/examples/`:

- `basic.rs` — minimal picker setup.
- `noninteractive.rs` — non-interactive matching.
- `overlay.rs` — overlay-style picker.
- `pick_1.rs` — single-item pick.
- `ripgrep.rs` — rg-powered picker.

Run with `cargo run -p matchmaker-lib --example <name>` (to verify exact invocation syntax before publishing this page).

## Key integration points (candidates)

- `Matchmaker::new_from_config(config, ...)` — build a matcher from a `Config`.
- Configuration types come from `matchmaker-lib` with a `partial` feature for incremental construction.
- Modes, actions and events (`event::set_mode`, `EventLoop::with_binds`, `MMAction`) mirror the CLI's behavior.

## To write

- Minimal "hello world" embedded picker walkthrough.
- Overlay integration (parent application rendering, input forwarding).
- Non-interactive usage for tests/scripts.
- Feature flags (`partial`, `experimental`).