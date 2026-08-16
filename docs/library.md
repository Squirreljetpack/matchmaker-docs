# Using the library

`matchmaker-lib` exposes Matchmaker's `nucleo`-backed fuzzy matcher and `ratatui` interface as an embeddable Rust crate. You can run interactive pickers over arbitrary Rust types, attach custom previewers and overlays, or filter items headlessly without launching the terminal UI.

## Crate setup

The Cargo package is published as `matchmaker-lib` and exposes the library target `matchmaker`:

```toml
[dependencies]
matchmaker-lib = "0.1"
tokio = { version = "1", features = ["full"] }
```

Import items from `matchmaker` in your Rust code:

```rust
use matchmaker::nucleo::Worker;
use matchmaker::{MatchError, Matchmaker, Result};
```

Optional Cargo features on `matchmaker-lib`:

| Feature | Purpose |
| --- | --- |
| `bracketed-paste` | Bracketed paste events and `PickOptions::paste_handler` |
| `partial` | Partial configuration structs via `matchmaker-partial` |
| `image` | PNG and JPEG previews via the `<MM_IMAGE>` preview header |
| `image-svg` | `resvg`-backed SVG rasterization for `image` |
| `image-all` | `image`, `image-svg`, and GIF, BMP, ICO, TIFF, and WebP codecs |

## Core pipeline

Running a picker takes four steps: build a `Worker<T, D>`, feed items into it, wrap it in a `Matchmaker<T, S, D>` with an accept hook, and await `pick_default()` or `pick()`.

```rust
use matchmaker::nucleo::Worker;
use matchmaker::{MatchError, Matchmaker, Result};

#[tokio::main]
async fn main() -> Result<()> {
    let items = vec!["item1", "item2", "item3"];

    let worker = Worker::new_single_column();
    worker.append(items);
    let mm = Matchmaker::new_on_cloneable(worker);

    match mm.pick_default().await {
        Ok(selected) => {
            if let Some(first) = selected.into_iter().next() {
                println!("{first}");
            }
        }
        Err(MatchError::Abort(1)) => eprintln!("cancelled"),
        Err(err) => eprintln!("Error: {err}"),
    }

    Ok(())
}
```

### Single-column and multi-column workers

Every item type `T` stored in a `Worker<T, D>` must satisfy `Send + Sync + 'static` (aliased as `matchmaker::SSS`).

- **Single-column items**: `Worker::new_single_column()` accepts any `T: Render + SSS`. `Render` is blanket-implemented for all `T: AsRef<str>`, or you can implement `Render::as_str` / `Render::as_text` on your own type.
- **Multi-column indexable items**: Implement `ColumnIndexable` (`get_str(&self, i: usize)` and optionally `get_text(&self, i: usize)`) and call `Worker::new_indexable(column_names, default_column)`. `(String, String)` implements `ColumnIndexable` out of the box.
- **Custom column definitions**: Construct `Column<T, D>` values directly with `Column::new(name, format_fn)` (plus `.with_raw(...)`, `.without_filtering()`, or `.without_highlighting()`) and pass them to `Worker::new(columns, default_column)` or `Worker::new_with_preprocessors(...)`.

```rust
use std::borrow::Cow;
use matchmaker::config::StringOrInt;
use matchmaker::nucleo::{ColumnIndexable, Worker};
use matchmaker::Matchmaker;

#[derive(Clone)]
pub struct Entry {
    pub name: String,
    pub category: String,
    pub description: String,
}

impl ColumnIndexable for Entry {
    fn get_str(&self, i: usize) -> Cow<'_, str> {
        match i {
            0 => (&self.name).into(),
            1 => (&self.category).into(),
            _ => (&self.description).into(),
        }
    }
}

pub fn build_picker(items: impl IntoIterator<Item = Entry>) -> Matchmaker<Entry, Entry> {
    let worker = Worker::new_indexable(
        ["name", "category", "description"],
        Some(StringOrInt::String("name".to_string())),
    );
    worker.append(items);
    Matchmaker::new_on_cloneable(worker)
}
```

To stream items asynchronously while the picker is already running, clone a `WorkerInjector<T, D>` with `worker.injector()` (or `state.injector()` inside a handler) and push items from a background task using the `matchmaker::nucleo::Injector` trait (`injector.push(item)` or `injector.extend(items)`).

### Selection and accept hooks

`Matchmaker<T, S, D>` is generic over the worker item type `T`, the output item type `S`, and the per-row preprocessor data `D` (default `()`).

- `Matchmaker::new_on_cloneable(worker)` requires `T: Clone` and returns `Vec<T>` containing all multi-selected items, or the item currently under the cursor when the selection set is empty.
- `Matchmaker::new(worker, accept_hook)` takes a closure `FnOnce(&mut MMState<'_, T, D>) -> Vec<S> + Send + Sync + 'static`. Inside the closure, `state.map_selected_to_vec(|idx, item| ...)` maps selected items with a fallback to the cursor item, `state.map_selections_to_vec(|idx, item| ...)` maps only explicitly selected items (`state.selections()` returns `&Selector`), and `state.current_raw()` returns `Option<&T>` for the cursor row.

Before calling `pick`, you can configure the instance with builder methods on `Matchmaker`:

- `mm.config_render(RenderConfig)` — layout, colors, frames, query, results, status, header, footer, toast, and preview UI settings
- `mm.config_tui(TerminalConfig)` — I/O stream (`IoStream::Stdout`, `Stderr`, `Test`), inline vs fullscreen layout, and exit clearing
- `mm.config_exit(ExitConfig)` — `first` (auto-accept single match), `allow_empty`, `abort_empty`, and `last_key_path`
- `mm.config_matcher(MatcherConfig)` — `nucleo` or `frizbee` scoring backend configuration

### Running the picker and handling errors

Call `mm.pick_default().await` for default options, or pass a configured `PickOptions<T, D, A>` to `mm.pick::<A>(options).await`.

Importing `matchmaker::MatchResultExt` adds two convenience methods to `Result<Vec<S>>`:

- `.first()` extracts the first element of the returned collection, converting an empty vector into `Err(MatchError::NoMatch)`.
- `.abort()` intercepts `Err(MatchError::Abort(code))` and terminates the process with `std::process::exit(code)`.

```rust
use matchmaker::nucleo::{Render, Worker};
use matchmaker::{MatchResultExt, Matchmaker, Result, SSS};

pub async fn pick_one<T: SSS + Render + Clone>(items: impl IntoIterator<Item = T>) -> Result<T> {
    let worker = Worker::new_single_column();
    worker.append(items);
    Matchmaker::new_on_cloneable(worker)
        .pick_default()
        .await
        .abort()
        .first()
}
```

`MatchError` covers the non-accept exit paths:

| Variant | Cause |
| --- | --- |
| `MatchError::Abort(i32)` | `Action::Quit(code)` exit (`esc` and `ctrl-c` send `Quit(1)` by default) |
| `MatchError::Become(u8)` | `Become` or `BecomeSilent` interrupt handler exit with status code |
| `MatchError::NoMatch` | Empty selection in `MatchResultExt::first`, `RenderCommand::NoMatch`, or `state.should_quit_nomatch` |
| `MatchError::EventLoopClosed` | Render command channel closure before an exit action |
| `MatchError::TUIError(String)` | Terminal initialization or rendering failure |

## Events, interrupts, and handlers

Unlike the `mm` CLI binary, `matchmaker-lib` does not hardcode shell execution, process replacement, stdout printing, or command-driven reloading inside the render loop. Actions with side effects outside the UI (`Execute`, `ExecuteAsync`, `ExecuteThen`, `ExecuteSilent`, `Become`, `BecomeSilent`, `Reload`, `Print`, `Preview`, `Help`) only perform minimal TUI state transitions and emit an `Event` or `Interrupt`. Your application defines what those actions do by registering handlers that receive `&mut MMState<'_, T, D>`.

### Interrupt handlers

When the render loop processes an external-effect action, it prepares the terminal and invokes every handler registered for the corresponding `Interrupt`:

- `Action::Execute(payload)` pauses the event loop and leaves the TUI alternate screen before invoking `Interrupt::Execute` handlers, then re-enters the TUI before the next frame.
- `Action::Become(payload)` and `Action::BecomeSilent(payload)` pause the event loop and exit the TUI before invoking `Interrupt::Become` or `Interrupt::BecomeSilent` handlers. If the handler sets `state.discriminant_payload = Some(code)`, `pick` returns `Err(MatchError::Become(code))`; otherwise the TUI resumes.
- `Action::Reload(payload)` restarts the worker, clears selections, and invokes `Interrupt::Reload` handlers, where you can push fresh items into `state.injector()`.
- `Action::ExecuteSilent(payload)`, `Action::ExecuteAsync(payload)`, `Action::ExecuteThen(payload)`, and `Action::Print(payload)` invoke their respective interrupt handlers without leaving the TUI.

Register an interrupt handler with `mm.register_interrupt_handler(interrupt, handler)` and read the action's string argument from `state.payload()`:

```rust
use matchmaker::message::Interrupt;
use matchmaker::nucleo::Injector;

mm.register_interrupt_handler(Interrupt::Reload, |state| {
    let payload = state.payload().clone();
    let injector = state.injector();
    tokio::spawn(async move {
        let _ = injector.push(format!("reloaded: {payload}"));
    });
});
```

### Event handlers

`Event` (`matchmaker::message::Event`) is a bitflag tracking lifecycle and UI transitions across each render batch: `Start`, `QueryChange`, `CursorChange`, `CursorLost`, `PreviewChange`, `PreviewSet`, `OverlayChange`, `Restarted`, `Synced`, `Resynced`, `Resize`, `Redraw`, `Pause`, `Resume`, `Reloaded`, `PreviewStarted`, `PreviewFinished`, and `Tick`.

Register a listener with `mm.register_event_handler(event_mask, handler)`. A handler whose mask intersects any bit set during a frame is called once at the end of that frame:

```rust
use matchmaker::message::Event;

mm.register_event_handler(Event::QueryChange | Event::CursorChange, |state, events| {
    let (query, cursor_idx) = state.get_content_and_index();
    log::debug!("events={events:?} query={query} cursor={cursor_idx}");
});
```

### Connecting a previewer

The preview pane is also driven by event handlers. Calling `matchmaker::make_previewer(&mut mm, previewer_config, formatter, help_factory)` registers handlers on `mm` for `Event::CursorChange | Event::PreviewChange | Event::Synced` and `Event::PreviewSet`, and returns a `Previewer` actor that spawns preview commands and streams their output into the preview pane. Attach it to the picker via `PickOptions::new().previewer(previewer)`, or supply a standalone `Preview` view via `PickOptions::new().preview(view)`.

## Extending actions and UI

### Custom actions and action aliasing

`Action<A>` and `BindMap<A>` are parameterized by `A: ActionExt` (which defaults to `NullActionExt`). Any type implementing `Debug + Clone + PartialEq + Send + Sync + 'static` implements `ActionExt` automatically and converts into `Action::Custom(value)`. If you also implement `Display` and `FromStr<Err = String>`, your custom actions can be serialized and parsed alongside built-in actions in configuration files.

Use `bindmap!` and `key!` from `matchmaker::binds` to bind keys to built-in or custom actions, then register an `ext_handler` (and optionally an `ext_aliaser`) on `PickOptions`:

```rust
use matchmaker::action::{Action, acs};
use matchmaker::binds::{BindMap, BindMapExt, bindmap, key};
use matchmaker::{Matchmaker, PickOptions};

#[derive(Debug, Clone, PartialEq)]
enum AppAction {
    ClearAndReset,
}

let mut binds: BindMap<AppAction> = BindMap::default_binds().with_extras();
binds.extend(bindmap!(
    key!(ctrl-r) => AppAction::ClearAndReset,
));

let options = PickOptions::with_binds(binds)
    .ext_handler(|action, state| match action {
        AppAction::ClearAndReset => {
            state.picker_ui.query.clear();
            state.picker_ui.selector.clear();
        }
    })
    .ext_aliaser(|action, _state| match action {
        // Transform or filter actions before the render loop dispatches them
        Action::Quit(_) => acs![Action::Quit(2)],
        other => acs![other],
    });
```

See [Library actions](/library-actions) for the full table of built-in `Action<A>` variants and how they compare to the CLI's `MMAction` extensions.

### Overlays

Register overlays on `PickOptions` with `.overlay(overlay)` and open the `n`-th registered overlay with `Action::Overlay(n)`.

`matchmaker::ui::PickerOverlay` provides a self-contained multi-column fuzzy picker overlay with its own lazy `Worker` that starts when the overlay opens and drops when it closes:

```rust
use matchmaker::action::{Action, NullActionExt};
use matchmaker::binds::{bindmap, key};
use matchmaker::config::{OverlayConfig, QueryConfig, ResultsConfig};
use matchmaker::nucleo::{Injector, Worker, WorkerInjector};
use matchmaker::ui::PickerOverlay;
use matchmaker::{Matchmaker, PickOptions};

let worker = Worker::new_indexable(["name", "description"], None);
worker.append((0..50).map(|i| (format!("item {i}"), format!("detail {i}"))));
let mm = Matchmaker::new_on_cloneable(worker);

let options = PickOptions::<_, _, NullActionExt>::new()
    .overlay(PickerOverlay::new(
        ["name", "description"],
        None,
        |injector: &WorkerInjector<(String, String)>| {
            let items = (0..100).map(|i| (format!("result {i}"), format!("detail {i}")));
            let _ = injector.extend(items);
        },
        OverlayConfig::default(),
        ResultsConfig::default(),
        QueryConfig::default(),
    ))
    .binds(bindmap!(key!(ctrl-o) => Action::Overlay(0)));
```

For custom widgets, implement `matchmaker::ui::Overlay<Act, T, D>` (`on_enable`, `on_disable`, `handle_input`, `handle_action`, `draw`, and `area`). Returning `OverlayEffect::Disable` from `handle_input` or `handle_action` closes the active overlay.

### Non-interactive matching

To filter items with `nucleo` without initializing a terminal or event loop, call `matchmaker::noninteractive::get_matches(items, query, timeout, callback)`. The callback is invoked for each matched item in score order; returning `true` stops iteration early.

```rust
use std::time::Duration;
use matchmaker::noninteractive::get_matches;

let mut first_match = None;
get_matches(
    ["alpha", "beta", "gamma"],
    "bet",
    Duration::from_millis(10),
    |item| {
        first_match = Some(*item);
        true
    },
);
```
