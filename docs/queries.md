# Queries

As you type in the prompt, Matchmaker parses your query into per-column patterns and scores every row concurrently across all active matcher threads.

## Matching backends and scoring

Matchmaker supports two fuzzy matching backends under `[matcher]`:

- **`nucleo` (default)**: Subsequence fuzzy matching with smart case (case-insensitive unless a query token contains an uppercase letter), Unicode normalization (`normalize`), bonuses for consecutive characters and word starts, and optional prefix and path matching modes.
- **`frizbee` (`matcher.backend = "frizbee"`)**: Typo-tolerant matching controlled by `max_typos` and configurable match/penalty weights under `[matcher]`.

Within any column query, space-separated tokens combine with logical AND. Individual tokens accept fzf-style operators:

| Token | Match condition |
| --- | --- |
| `abc` | Fuzzy subsequence match |
| `'abc` | Exact substring match |
| `^abc` | Prefix match at the start of the column |
| `abc$` | Suffix match at the end of the column |
| `^abc$` | Exact full-column match |
| `!abc` | Exclusion of rows matching `abc` |
| `foo\ bar` | Literal space inside a single token |

See [Other](/other) for operator examples and [Options](/options) for `[matcher]` configuration.

## Column filtering and focus

When rows are split into multiple columns ([Input and data sources](/input-and-data#splitting-rows-into-columns)), a single query can filter several columns at once using `%col` selectors:

```text
main %path src/ %ext .rs !mod
```

- **Primary column**: Any query text before the first `%col` token filters the primary column (`columns.default`, which defaults to the first column).
- **`%col` prefix matching**: A word starting with `%` switches the target column for the tokens that follow. You only need to type a prefix—`%p` selects the shortest column name starting with `p` (such as `path`). When `columns.names` is unset, columns are named `1` through `columns.max`, so `%1`, `%2`, and so on target them by number.
- **Unmatched `%` tokens**: If the name after `%` does not match the prefix of any column, the token is treated as literal search text in the current column. Escape a leading percent sign with `\%`.
- **Repeated selectors**: Naming the same column more than once in a query appends the new terms to that column's pattern separated by a space.
- **Cross-column options (`columns.names[].options`)**: Setting `OrUseDefault` on a column causes it to match against the primary column's query whenever no explicit `%col` pattern is given for it. Setting `Optional` prevents a non-match in that column from rejecting the row when other columns also have active patterns.

### Active column focus

The **active column** is the column owning the query span under your text cursor: if the cursor rests inside a `%path ...` segment, `path` is active; if the cursor is before any `%col` selector, the primary column is active.

Active column focus controls four things in the interface:

- **Highlighting**: The active column is drawn with `results.current_style` and `results.prefix_style`, while other columns use `results.inactive_style` and `results.inactive_current_style` (according to `results.row_connection`).
- **Template expansion**: The `{!}`, `{=!}`, `{+!}`, and `{-!}` placeholders resolve to the active column of the current or selected rows ([Template](/template)).
- **Keyboard navigation**: `NextColumn` (`alt-.` / `ctrl-.`) and `PrevColumn` (`alt-shift-.` / `ctrl-shift-.`) cycle focus across visible columns by appending `%<col> ` to the query (replacing a trailing bare `%col` selector if you have not typed a pattern after it). `SwitchColumn(col)` focuses a specific column by name.
- **Column actions**: `HideColumn`, `ExpandColumn`, `ShrinkColumn`, `Sort`, and `SortNumeric` act on the active column when invoked without an explicit column argument.

<video controls preload="none" src="./images/ps.mp4"></video>

## Visibility, widths, and scrolling

Matchmaker sizes visible columns automatically to fit their content and the terminal width, and lets you hide, resize, wrap, or scroll columns interactively:

| Action | Default keys (`--dump-config`) | Effect |
| --- | --- | --- |
| `HideColumn([col])` | `alt-\` | Hiding of `col` or the active column (the primary column cannot be hidden) |
| `UnhideColumn([col])` | `alt-shift-\` | Restoration of `col` or the most recently hidden column |
| `ExpandColumn([n])` | `alt-=` | Widening of the active column (or 0-based visible column `n`) by 1 cell |
| `ShrinkColumn([n])` | `alt-hyphen` | Narrowing of the active column (or 0-based visible column `n`) by 1 cell |
| `ToggleWrap` | `alt-w` | Line-wrapping toggle for result rows (`results.wrap`) |
| `ToggleHeaderWrap` | `alt-w` | Line-wrapping toggle for header rows (`header.wrap`) |
| `HScroll(n)` | `alt-left` / `alt-right`, `alt-shift-left` / `alt-shift-right` | Horizontal scroll of result cells by `n` cells (`0` resets) |
| `VScroll(n)` | `alt-up` / `alt-down`, `alt-shift-up` / `alt-shift-down` | Vertical line scroll inside multi-line result rows (`0` resets) |

- **Hidden columns**: Columns can start hidden via `columns.names[].hidden = true` or be hidden at runtime with `HideColumn`. Hiding the currently focused column strips its trailing `%col` selector from the query. Hidden columns are omitted from `{..}` visible-range templates ([Template](/template)) but remain accessible by name or index (such as `{2}` or `{id}`) and can still be queried by typing `%name`.
- **Width allocation and mouse dragging**: Initial column widths can be seeded with `results.width_overrides` and bounded by `results.min_width` (see [Options](/options)). When `results.column_spacing` is non-zero (default `1`), dragging the spacing gutter between two columns with the mouse resizes the left column in place.
- **Multi-line rows and stacked layout**: `results.max_height` (`0` for unlimited) caps the rendered height of wrapped or multi-line rows; `VScroll` scrolls through clipped lines on the current row. Setting `results.vertical = true` (`r.v`, alias `stacked_columns`) renders each row's visible columns stacked vertically on consecutive lines instead of side by side.
- **Horizontal autoscroll**: When `results.autoscroll.enabled` is `true` (default), unwrapped columns automatically pan horizontally to keep matched characters in view around the match. Moving the selection cursor to another row resets manual `HScroll` and `VScroll` offsets.

## Sorting results

By default, rows are ranked by fuzzy match score, with ties broken by arrival order. You can adjust score stability or sort rows by any column at startup (`matcher.sort`, CLI alias `S`) or at runtime:

| Action | Default keys (`--dump-config`) | Effect |
| --- | --- | --- |
| `Sort([n])` | `alt-s` | Ascending lexicographic sort on the active column (or 0-based displayed column `n`), or toggle off |
| `SortNumeric([n])` | `alt-n` | Ascending numeric sort (integers and decimals before text) on the active or `n`-th displayed column, or toggle off |
| `SortReverse([bool])` | `alt-r` | Direction toggle (or explicit set) for base item order and active column sorts |
| `SortThreshold([n])` | *(unbound)* | Matcher score-stability threshold set to `n` (omitted restores maximum stability) |

- **Toggling column sorts**: Triggering `Sort` or `SortNumeric` overrides score ranking (`SortThreshold` is raised to maximum stability) and orders all matched rows by the target column. Pressing the same sort key again on the same column turns the column sort off and restores the configured `matcher.sort.threshold`.
- **Score stability (`matcher.sort.threshold`, CLI alias `t`)**: Controls how much a higher fuzzy score must beat an earlier item's score to overtake it. `0` (or `true`) always sorts strictly by match score, positive integers require that minimum score difference before reordering, and `false` sets the maximum threshold to keep items in their input order regardless of score differences.

## Pausing internal filtering

To decouple the query bar from the built-in matcher—for example, when re-running an external search tool like `rg` on `QueryChange`—trigger `Filtering(false)` to pause internal refiltering and `Filtering(true)` (or `Filtering` with no argument) to resume it.
