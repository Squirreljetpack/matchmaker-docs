# Creating presets

A preset turns any command or data source into a reusable Matchmaker workflow. Because presets are partial TOML configurations layered over `config.toml`, a preset only needs to specify the settings it changes.

## Minimal preset structure

The bundled `csv.toml` preset is a complete, minimal example: it finds a `.csv` or `.tsv` file in the working directory, splits rows using RFC 4180 CSV rules, promotes the first input line to a sticky table header, and previews the currently focused column (`{!}`):

```toml
# CSV/TSV viewer

[start]
command = '''
set -- *.csv
[ -e "$1" ] || set -- *.tsv

[ -e "$1" ] && cat -- "$1"
'''

[columns]
split = "csv"

[header]
header_lines = 1

[[preview.layout]]
command = '''
printf '%s\n' {!}
'''
```

For larger presets, keep sections in a consistent order separated by comment headers:

1. `source` (when inheriting from a shared `base.toml`)
2. `[start]` and `[envs]`
3. `[columns]` and `[matcher]`
4. UI sections (`[tui]`, `[query]`, `[results]`, `[header]`, `[footer]`, `[exit]`)
5. `[previewer]` and `[[preview.layout]]`
6. `[binds]`, with key bindings first and `@` semantic aliases below

When a folder contains several related pickers (such as `git/` or `zellij/`), put shared settings in `base.toml` and inherit them at the top of each sibling preset with `source = "base.toml"`. `mm --presets` automatically omits `base.toml` from the selectable preset list.

## Populating rows and environment

`[start].command` produces the stream of rows fed into the matcher. Keep diagnostic messages on standard error so standard output contains only data rows:

```toml
[start]
command = 'git branch --all --color=always --format="%(refname:short)%09%(subject)" "$@"'
output = "{=1}"
directory = { value = "git rev-parse --show-toplevel", exec = true, force = true }

[envs]
CATcmd = { value = "command -v bat >/dev/null 2>&1 && echo 'bat --color=always -pp' || echo cat", exec = true, force = true }
```

- **Arguments** — Trailing arguments passed after `--` on the command line reach `start.command` as positional parameters (`"$@"`, `"$1"`, ...).
- **Working directory and environment** — Both `start.directory` and entries in `[envs]` accept `{ value = "...", exec = true, force = true }` to evaluate a command at startup and use its trimmed standard output. With `force = true` on `start.directory`, startup aborts if the command fails or the directory does not exist.
- **No templates in startup settings** — Matchmaker [templates](/template) (`{}`, `{1}`, `{name}`) are expanded in preview commands, bind actions, `start.output_template` (`output`), and `start.on_accept`, but **not** in `start.command` or `[envs]`.

## Splitting columns and headers

Use `[columns]` to split each input line into addressable fields for filtering, display, and templating:

```toml
[columns]
split = "tsv"
max = 4
default = "session"
names = [
    { name = "age", options = "Optional | OrUseDefault" },
    { name = "session", options = "Optional" },
    { name = "path", hidden = true },
    { name = "state" },
]

[header]
content = ["AGE", "SESSION", "PATH", "STATE"]
```

- **Delimiters and parsers** — `columns.split` accepts a delimiter regex (`'\t'`, `' +'`, `"\\x00"`), a regex with unnamed or named capture groups (`'^(.*?):(\d+:\d+):(.*)$'`), or `"csv"` / `"tsv"`.
- **Hidden metadata columns** — Set `hidden = true` on columns that carry internal identifiers or file paths needed by previews and actions. Putting openable file paths in column 1 (or naming the column `file`) lets the default `@open` (`ctrl-o`) bind work without redefinition.
- **Column-aligned headers** — `[header].content` accepts an array with one label per column, **including hidden columns**, so visible labels stay aligned over their columns. When the populating command emits its own header row (such as `ps` or `kubectl get pods`), set `header.header_lines = 1` instead.
- **Column templates** — In previews and actions, select the specific column you need (`{0}` for the default column, `{1}` by 1-based index, or `{session}` by alphanumeric name) rather than bare `{}`. Bare `{}` expands to the entire raw input line, which embeds a literal NUL byte if `columns.split = "\\x00"`. See [Template](/template) for all modifiers (`{=col}`, `{+col}`, `{-col}`).

## Configuring previews

Each `[[preview.layout]]` block defines a view that you can cycle through with `alt-/` or toggle with `?`:

```toml
[preview]
show = true
wrap = false

[[preview.layout]]
command = '"$(dirname -- "$MM_OVERRIDE")"/helper.sh preview {session}'
frame = { title = "Session Overview" }
side = "right"
percentage = 50

[[preview.layout]]
command = '$CATcmd -- {path}'
frame = { title = "Source" }

# Disable the third layout inherited from the default config.toml
[[preview.layout]]
max = 0
```

Because `preview.layout` is merged positionally, setting `max = 0` on an unused trailing slot disables it. Use `[previewer]` for runner behavior such as `always_trigger = false` or custom `shell` interpreters; see [Preview](/preview) and [Options](/options).

## Binds, traces, and semantic aliases

Bind keys to semantic aliases (`@name`) and attach command payloads to the aliases. Prefixing an action array with a `#description` trace replaces the raw command in `@help` and `alt-h` with a short label:

```toml
[binds]
"ctrl-k" = "@kill"
"alt-]" = "@next"

"@accept" = "Become(zellij attach {session})"
"@return" = "Accept"
"@kill" = [
    "#kill session",
    "ExecuteOrConfirm(zellij kill-session {+session})",
    "Reload",
]
"@next" = "BecomeSilent(mm -o zellij/current)"
```

- **Reusing default aliases** — Override `@accept` when `enter` should run a workflow action; keep `"@return" = "Accept"` (bound to `alt-enter` by default) so you can still print the selected row to standard output. Reuse `@open`, `@rm`, `@copy`, and `@reload` where they fit.
- **Choosing an execution action** — Use `Execute` to run a foreground command and return to the picker, `ExecuteOrConfirm` to pause only when a command exits non-zero, `ExecuteAsync` or `ExecuteThen` to run a background command before chaining `"Reload"`, `Become` to replace `mm` with an external interactive program, and `BecomeSilent` to switch to another `mm -o` preset without clearing the screen. See [Binds](/binds) and [Execute](/execute).

## Helper scripts and `MM_OVERRIDE`

When a preset is loaded with `-o`, Matchmaker sets `MM_OVERRIDE` to the canonical path of the first applied override file. You can keep presets declarative by moving complex logic into sibling scripts inside the preset folder.

When the first word of a `start.command` or action payload starts with `@`, Matchmaker resolves relative paths against the parent directory of `MM_OVERRIDE`:

| Prefix | Execution model |
| --- | --- |
| `@script.sh args` | Configured shell (`start.shell` or `$SHELL`) |
| `@./script args` | Direct kernel execution via the file's `#!` shebang (requires `chmod +x`) |
| `@script.lua args` | Internal Lua VM with `state` and `env` globals (see [Execute](/execute)) |

Inside a multi-line inline shell script where `@` is not the first token, resolve sibling files from `MM_OVERRIDE` directly:

```shell
"$(dirname -- "$MM_OVERRIDE")"/helper.sh subcommand {1}
```

## Writing preset help (`README.md`)

Pressing `F1` (`@help`) in the picker looks for a `README.md` file in the same directory as `MM_OVERRIDE` (falling back to the leading `#` comment block of the `.toml` file), renders it with the `[markdown]` skin, and pages it fullscreen above the live keybinding table.

See [AUTHORING_README.md](https://github.com/Squirreljetpack/matchmaker/blob/main/matchmaker-cli/assets/presets/AUTHORING_README.md) for the preset `README.md` structure and conventions.

## Testing and debugging presets

Validate configuration merging and exercise your preset non-interactively with `--dump-config` and `--list`:

```shell
# Verify the merged TOML configuration
mm -o path/to/preset.toml --dump-config | cat

# Run start.command and inspect raw output rows
mm -o path/to/preset.toml --list

# Run preview layout 0 on matcher item 0
mm -o path/to/preset.toml --list="0-0"

# Run the Execute/Become actions bound to @accept on matcher item 0
mm -o path/to/preset.toml --list="0@accept"
```

In `--list="N-M"` and `--list="N@alias"`, `N` is the 0-based **matcher** index rather than the raw input line number (with an empty query, the matcher ranks shorter items first). Run `mm -o path/to/preset.toml --list` first to check item ordering, and see [Other](/other) for all `--list` modes.

## Agent skill

Point your coding agent at [SKILL.md](https://github.com/Squirreljetpack/matchmaker/blob/main/matchmaker-cli/assets/plugins/SKILL.md) when creating, reviewing, debugging, or porting TOML presets and companion helper scripts.
