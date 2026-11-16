# Benchmarks

`matchmaker` is built for rich multi-column, ANSI-styled, and wrapped terminal UIs without giving up interactive speed. `ResultsUI` double-buffers rendered table cells and column widths (`row_cache`) and skips table rebuilds when no state is invalidated (`is_clean`), while supporting both the `nucleo` and SIMD-accelerated `frizbee` matcher backends.

## Methodology & environment

- **Machine**: AMD Ryzen 9 7950X (16C/32T), Linux 7.3.4
- **Binaries**: `mm` `0.1.7` built with `--profile dist` (`codegen-units = 1`, `lto = "fat"`), `fzf` `0.75.0`, `sk` `0.20.5`
- **PTY harness**: [`benches/bench_tui.py`](https://github.com/Squirreljetpack/matchmaker/blob/main/benches/bench_tui.py) in a `120x40` PTY (`start.sync = true` / `--sync`, `tui.sleep_ms = 0` on `mm`, `FZF_DEFAULT_OPTS=""` on `fzf`)
- **Aggregation**: median of 5 measured runs after 1 warmup run

## Heavy 6-column ANSI + wrapped viewport (200k rows)

Each row contains ANSI color escapes and 6 tab-separated columns. `mm` runs with `ansi = true`, `results.wrap = true`, and `max_height = 4` (full column auto-sizing and line wrapping), while the other pickers run with `--ansi` and single-line truncation.

| Picker | First frame | Broad query | 50× cursor nav | Switch query (`Ctrl-U`) | Accept (`Enter`) | Peak RSS |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `mm` (`nucleo`) | 240.9 ms | **3.7 ms** | 5.1 ms | 4.6 ms | 20.1 ms | 124.3 MB |
| `mm` (`frizbee`) | **218.0 ms** | 5.3 ms | **4.5 ms** | 4.5 ms | 18.4 ms | 123.1 MB |
| `fzf --ansi` | 622.3 ms | 5.4 ms | 4.6 ms | **2.3 ms** | **6.0 ms** | **117.1 MB** |
| `sk --ansi` | 1103.9 ms | 13.0 ms | 381.4 ms | 17.0 ms | 10.9 ms | 175.9 MB |

- **2.6–2.9× faster** to first frame than `fzf` and **4.6–5.1× faster** than `sk` on 200k ANSI-colored multi-column rows, even with wrapping and column layout enabled.
- **Cached cursor navigation**: `50` cursor moves (`25× Down` + `25× Up`) complete in **4.5–5.1 ms** on `mm` (vs `381.4 ms` on `sk`).

## 500k scale & query-shape transitions

500,000 file paths with synchronous ingestion (`start.sync = true` / `--sync`), measuring first frame, incremental typing (`g` → `wp` → `robe`), switching to a disjoint unique match (`Ctrl-U` + `zxq_validator_9`), switching back to the 499-hit query (`Ctrl-U` + `gwprobe`), and peak RSS.

| Picker | First frame | Incremental (`gwprobe`) | Switch (`zxq_validator_9`) | Broad re-filter (`gwprobe`) | Peak RSS |
| --- | ---: | ---: | ---: | ---: | ---: |
| `mm` (`frizbee`) | **88.8 ms** | 22.4 ms | 20.2 ms | 24.5 ms | 109.9 MB |
| `mm` (`nucleo`) | 94.7 ms | 20.6 ms | 19.2 ms | 34.7 ms | 109.5 MB |
| `fzf` | 530.0 ms | **16.5 ms** | **4.4 ms** | **1.3 ms** | **99.2 MB** |
| `sk` | 645.0 ms | 32.5 ms | 22.7 ms | 18.5 ms | 225.6 MB |

- On 500k paths, `mm` renders its first frame **5.6–6.0× faster** than `fzf` and **6.8–7.3× faster** than `sk`, while keeping peak RSS (**109.5–109.9 MB**) less than half of `sk` (`225.6 MB`).

## Synchronous `select-1` / `exit.first` startup (200k paths)

Startup, full ingestion (`start.sync = true` / `--sync`), matching a unique initial query across 200,000 plain paths, and exiting automatically (`exit.first = true` / `-1`).

| Picker | Wall time | CPU time | Peak RSS |
| --- | ---: | ---: | ---: |
| `fzf --sync -1` | **20.9 ms** | **32.2 ms** | **45.3 MB** |
| `mm` (`frizbee`) | 37.5 ms | 154.9 ms | 94.2 MB |
| `mm` (`nucleo`) | 37.8 ms | 134.0 ms | 75.9 MB |
| `sk --sync -1` | 219.3 ms | 419.2 ms | 75.6 MB |

## `matchmaker-lib` microbenchmarks

Measured directly in Rust without PTY overhead via `cargo bench -p matchmaker-lib --bench ui_and_matcher` ([`matchmaker-lib/benches/ui_and_matcher.rs`](https://github.com/Squirreljetpack/matchmaker/blob/main/matchmaker-lib/benches/ui_and_matcher.rs)).

### `ResultsUI::update_table` caching (120×40, 6-col ANSI, `wrap = true`)

| Path | Median | Min | p95 | Speedup vs cold |
| --- | ---: | ---: | ---: | ---: |
| `cold_miss` (`set_dirty`) | 339.1 µs | 332.6 µs | 353.1 µs | 1.0× |
| `row_cache` (cursor navigation) | 16.3 µs | 14.8 µs | 19.2 µs | **20.8×** |
| `is_clean` (no-op tick) | < 0.1 µs | < 0.1 µs | < 0.1 µs | — |

### `nucleo` vs `frizbee` query throughput & typo tolerance

| Dataset | Backend | Ingest | `1-char` (`g`) | `3-char` (`gwp`) | `7-char` (`gwprobe`) | `15-char` | Backspace (`gwp`) | 1-typo (`zxq_validatxr_9`) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 200k | `nucleo` | 29.6 ms | **4.18 ms** | 7.36 ms | **7.27 ms** | **6.42 ms** | 7.22 ms | 6.21 ms (0 hits) |
| 200k | `frizbee` | 28.3 ms | 7.15 ms | 7.20 ms | 7.40 ms | 6.55 ms | 7.37 ms | 6.29 ms (0 hits) |
| 200k | `frizbee (max_typos=1)` | **27.7 ms** | 14.20 ms | **7.18 ms** | 7.33 ms | 6.92 ms | **7.07 ms** | **7.22 ms (1 hit)** |
| 500k | `nucleo` | 72.4 ms | 16.78 ms | 16.84 ms | 16.62 ms | 15.16 ms | **16.19 ms** | 15.05 ms (0 hits) |
| 500k | `frizbee` | 71.6 ms | **16.34 ms** | **16.22 ms** | **16.14 ms** | 15.32 ms | 16.92 ms | 15.72 ms (0 hits) |
| 500k | `frizbee (max_typos=1)` | **70.2 ms** | 44.60 ms | 16.71 ms | 16.61 ms | **15.06 ms** | 16.58 ms | **15.62 ms (1 hit)** |

## Reproducing locally

```sh
cargo build --profile dist -p matchmaker-cli
python3 benches/bench_tui.py --mm ./target/dist/mm --items 200000 --scale-items 500000 --runs 5 --warmup 1
cargo bench -p matchmaker-lib --bench ui_and_matcher
```
