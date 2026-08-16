# Library actions

`matchmaker::action::Action<A>` defines the built-in operations processed by `matchmaker-lib`. Keybindings, mouse triggers, lifecycle events, and semantic aliases in a `BindMap<A>` all map to `Actions<A>` (a `Vec<Action<A>>` sequence).

## Library built-ins vs CLI actions

The `mm` binary instantiates `Action<MMAction>`, where `MMAction` is the CLI's `ActionExt` implementation passed to `Action::Custom(MMAction)`. Because user configs deserialize `Action<MMAction>` transparently, the [Binds](/binds) reference lists both library built-ins and CLI-only `MMAction` variants together.

When embedding `matchmaker-lib`, keep two distinctions in mind:

- **External-effect built-ins require handlers**: Built-in variants such as `Execute`, `ExecuteAsync`, `ExecuteThen`, `ExecuteSilent`, `Become`, `BecomeSilent`, `Reload`, `Print`, `Preview`, and `Help` are defined in `Action<A>`, but `matchmaker-lib` only transitions TUI state and raises an `Interrupt` or `Event`. You must attach handlers on `Matchmaker` (or connect a `Previewer`) for them to spawn commands or reload data; see [Using the library](/library#events-interrupts-and-handlers).
- **CLI-only actions live in `MMAction`**: Actions documented in [Binds](/binds) that are not in the tables below belong to `matchmaker-cli` rather than `Action<A>`:
  - **Runtime rebinding and modes**: `Bind`, `Unbind`, `PushBind`, `PopBind`, `SetMode`, `PushMode`, `PopMode`. In `matchmaker-lib`, send a `matchmaker::message::BindDirective` through `event_loop.bind_controller()`.
  - **Sorting and filtering**: `Filtering`, `Sort`, `SortNumeric`, `SortReverse`, `SortThreshold`. In `matchmaker-lib`, call `state.picker_ui.set_filtering(...)` or `state.picker_ui.worker.set_stability(...)` from an `ext_handler`.
  - **UI text and toasts**: `SetHeader`, `PushHeader`, `SetFooter`, `PushFooter`, `SetPrompt`, `SetStyledPrompt`, `SetStatus`, `SetStyledStatus`, `Toast`, `ToastJoin`, `ClearToast`. In `matchmaker-lib`, mutate `state.picker_ui.header`, `state.footer_ui`, `state.picker_ui.query`, `state.picker_ui.status`, or `matchmaker::ui::toast` inside an `ext_handler`.
  - **CLI execution and preview helpers**: `ExecuteOrConfirm`, `ExecuteAndQuit`, `BecomeOrConfirm`, `BecomeOrResume`, `Copy`, `CopyAsync`, `RunPreview`, `ShowPreview`, `ReloadNext`, `ReloadPrev`, `Transform`, `TransformConfig`, `HistoryUp`, `HistoryDown`, `PresetHelp`.

## Built-in `Action<A>` variants

When parsed from strings via `FromStr` or `serde`, variant names are matched case-insensitively. The **String syntax** column shows the parsed form, including any short alias and default argument when `(...)` is omitted.

### Selection

| Variant | String syntax | Description |
| --- | --- | --- |
| `Select` | `Select` | Add cursor item to `Selector` |
| `Deselect` | `Deselect` | Remove cursor item from `Selector` |
| `ToggleSelection` | `ToggleSelection` / `Toggle` | Toggle cursor item in `Selector` |
| `CycleSelections` | `CycleSelections` / `Cycle` | Select all matched items, or clear `Selector` if all matched items are already selected |
| `ClearSelections` | `ClearSelections` / `Clear` | Clear all selected items in `Selector` |
| `Accept` | `Accept` | Exit the TUI and invoke the `Matchmaker` accept hook |
| `Quit(i32)` | `Quit` / `Quit(code)` (default `0`) | Exit the picker with `Err(MatchError::Abort(code))` |

### Results and navigation

| Variant | String syntax | Description |
| --- | --- | --- |
| `Up(u16)` | `Up` / `Up(n)` (default `1`) | Move result cursor up by `n` rows (respecting reverse layout) |
| `Down(u16)` | `Down` / `Down(n)` (default `1`) | Move result cursor down by `n` rows (respecting reverse layout) |
| `Pos(i32)` | `Pos(idx)` | Jump result cursor to 0-based index `idx` (negative values count from the end) |
| `HalfPageUp` | `HalfPageUp` | Move result cursor up by half the results pane height |
| `HalfPageDown` | `HalfPageDown` | Move result cursor down by half the results pane height |
| `HScroll(i8)` | `HScroll` / `HScroll(n)` (default `0`) | Horizontally scroll active column of current result by `n` (`0` resets) |
| `VScroll(i8)` | `VScroll` / `VScroll(n)` (default `0`) | Vertically scroll wrapped lines of current result by `n` (`0` resets) |
| `ToggleWrap` | `ToggleWrap` | Toggle line wrapping in the results pane |
| `ToggleHeaderWrap` | `ToggleHeaderWrap` | Toggle line wrapping in the header display |

### Preview

| Variant | String syntax | Description |
| --- | --- | --- |
| `NextPreview` | `NextPreview` | Cycle to the next configured preview layout and update `preview_payload` |
| `PrevPreview` | `PrevPreview` | Cycle to the previous configured preview layout and update `preview_payload` |
| `Preview(String)` | `Preview(cmd)` | Set `preview_payload` (emitting `Event::PreviewChange`) and show the preview, or toggle visibility if unchanged |
| `Help(String)` | `Help` / `Help(section)` (default `""`) | Set static help payload in `preview_set_payload` (emitting `Event::PreviewSet`), or unset if unchanged |
| `SetPreview(Option<u8>)` | `SetPreview` / `SetPreview(idx)` | Switch to preview layout `idx`; `None` restores the current layout's command in `preview_payload` |
| `SwitchPreview(Option<u8>)` | `SwitchPreview` / `SwitchPreview(idx)` | Switch to preview layout `idx` (hiding if already active); `None` toggles preview visibility |
| `TogglePreviewWrap` | `TogglePreviewWrap` | Toggle line wrapping in the preview pane |
| `PreviewUp(u16)` | `PreviewUp` / `PreviewUp(n)` (default `1`) | Scroll preview pane up by `n` lines |
| `PreviewDown(u16)` | `PreviewDown` / `PreviewDown(n)` (default `1`) | Scroll preview pane down by `n` lines |
| `PreviewHalfPageUp` | `PreviewHalfPageUp` | Scroll preview pane up by half its height |
| `PreviewHalfPageDown` | `PreviewHalfPageDown` | Scroll preview pane down by half its height |
| `PreviewHScroll(i8)` | `PreviewHScroll` / `PreviewHScroll(n)` (default `1`) | Persistently scroll preview horizontally by `n` (`0` resets); pans an active image preview |
| `PreviewScroll(i8)` | `PreviewScroll` / `PreviewScroll(n)` (default `1`) | Persistently scroll preview vertically by `n` (`0` resets); zooms an active image preview when scroll-zoom is enabled |
| `PreviewJump` | `PreviewJump` | Cycle preview scroll position between start, end, and target index |
| `ExpandPreview(u16)` | `ExpandPreview` / `ExpandPreview(n)` (default `1`) | Expand preview pane width or height by `n` cells |
| `ShrinkPreview(u16)` | `ShrinkPreview` / `ShrinkPreview(n)` (default `1`) | Shrink preview pane width or height by `n` cells |

### Columns

| Variant | String syntax | Description |
| --- | --- | --- |
| `NextColumn` | `NextColumn` | Append `%<col> ` to query for the next non-hidden column |
| `PrevColumn` | `PrevColumn` | Append `%<col> ` to query for the previous non-hidden column |
| `SwitchColumn(String)` | `SwitchColumn(name)` | Append `%<name> ` to query if `name` is a valid column and not already active |
| `HideColumn(Option<String>)` | `HideColumn` / `HideColumn(name)` | Hide named column (or active column when `None`); the primary column cannot be hidden |
| `UnhideColumn(Option<String>)` | `UnhideColumn` / `UnhideColumn(name)` | Unhide named column, or pop the most recently hidden column when `None` |
| `ExpandColumn(Option<usize>)` | `ExpandColumn` / `ExpandColumn(idx)` | Widen 0-based visible column `idx` (or active column when `None`) by 1 cell |
| `ShrinkColumn(Option<usize>)` | `ShrinkColumn` / `ShrinkColumn(idx)` | Narrow 0-based visible column `idx` (or active column when `None`) by 1 cell |

### Input and query

| Variant | String syntax | Description |
| --- | --- | --- |
| `Char(char)` | *(single character)* | Insert character at the query cursor (dispatched directly from key input) |
| `ForwardChar` | `ForwardChar` | Move query cursor forward by one character |
| `BackwardChar` | `BackwardChar` | Move query cursor backward by one character |
| `ForwardWord` | `ForwardWord` | Move query cursor forward by one word |
| `BackwardWord` | `BackwardWord` | Move query cursor backward by one word |
| `DeleteChar` | `DeleteChar` | Delete character before the query cursor |
| `DeleteWord` | `DeleteWord` | Delete word before the query cursor |
| `DeleteLineStart` | `DeleteLineStart` | Delete from query cursor to start of query |
| `DeleteLineEnd` | `DeleteLineEnd` | Delete from query cursor to end of query |
| `ClearQuery` | `ClearQuery` | Clear the entire query string |
| `ClearQueryLeft` | `ClearQueryLeft` / `Cancel` | Delete from start of query to cursor |
| `ClearQueryRight` | `ClearQueryRight` | Delete from cursor to end of query |
| `SetQuery(String)` | `SetQuery(text)` | Replace query string with `text` and move cursor to the end |
| `InsertQuery(String)` | `InsertQuery(text)` | Insert `text` at the current query cursor position |
| `QueryPos(i32)` | `QueryPos(pos)` | Move query cursor to 0-based character index `pos` (negative values count from the end) |

### Modes, binds, and overlays

| Variant | String syntax | Description |
| --- | --- | --- |
| `Overlay(usize)` | `Overlay` / `Overlay(idx)` (default `0`) | Enable registered overlay at 0-based index `idx` |
| `Semantic(String)` | `@name` | Expand and dispatch actions bound to `TriggerKind::Semantic(name)` |
| `Trace(String)` | `#description` | Delimit action sequences with a display label for `binds::display_help` |
| `Custom(A)` | *(parsed via `A::from_str`)* | Dispatch custom `ActionExt` payload `A` to `PickOptions::ext_handler` |
| `Redraw` | `Redraw` | Invalidate cached column widths and flush the terminal buffer |
| `ToggleExitFirst(Option<bool>)` | `ToggleExitFirst` / `ToggleExitFirst(bool)` | Set `exit_config.first`, or toggle it when `None` |

### Execution, reload, and effects

| Variant | String syntax | Description |
| --- | --- | --- |
| `Execute(String)` | `Execute(payload)` | Pause event loop, exit TUI alternate screen, raise `Interrupt::Execute` with `payload`, then re-enter TUI |
| `ExecuteAsync(String)` | `ExecuteAsync(payload)` | Stash remaining actions in batch (even discriminant) and raise `Interrupt::ExecuteAsync` with `payload` |
| `ExecuteThen(String)` | `ExecuteThen(payload)` | Stash remaining actions in batch (odd discriminant, requiring success) and raise `Interrupt::ExecuteAsync` with `payload` |
| `ExecuteSilent(String)` | `ExecuteSilent(payload)` | Raise `Interrupt::ExecuteSilent` with `payload` without leaving the TUI |
| `Become(String)` | `Become(payload)` | Pause event loop, exit TUI, and raise `Interrupt::Become` with `payload` |
| `BecomeSilent(String)` | `BecomeSilent(payload)` | Pause event loop, exit TUI without clearing, and raise `Interrupt::BecomeSilent` with `payload` |
| `Reload(String)` | `Reload` / `Reload(payload)` (default `""`) | Restart worker, clear selections, raise `Interrupt::Reload` with `payload`, and emit `Event::Reloaded` |
| `Print(String)` | `Print` / `Print(payload)` (default `""`) | Raise `Interrupt::Print` with `payload` |
| `PrintKey` | `PrintKey` | Rewrite to `Action::Print(key)` in `EventLoop` using the triggering key's formatted name |
| `Store(String)` | `Store(val)` | Store `val` in `state.envs` under `MM_STORE` |
