# Pager

`mm` includes a built-in fullscreen pager based on [`minus`](https://docs.rs/minus), backing `ShowPreview`, `@help`, `mm --doc`, and the standalone `mm pager` mode.

minus draws on stdout when it is a terminal; when stdout is redirected (e.g.
`mm | head`) `ShowPreview` and `@help` draw on the controlling tty (`/dev/tty`) instead, so
piping or redirecting `mm`'s output never mixes pager UI into it.

## `mm pager`

Page one or more files, directories, markdown documents, images, or stdin:

```sh
mm pager Cargo.toml
mm pager +120 src/main.rs
mm pager +50p src/main.rs
mm pager +F /var/log/syslog
mm pager +200F /var/log/syslog
cat Cargo.toml | mm pager
```

### Opening at a position (`+OFFSET`) and context (`-C`)

| Form       | Meaning                                                                                          |
| ---------- | ------------------------------------------------------------------------------------------------ |
| `+N`       | Open with 1-based line `N` at the top of the screen (non-TTY stdout prints from line `N` to EOF) |
| `+Np`      | Open `N` percent into the file (requires a file path)                                            |
| `+F`       | Page the whole file or stream, scrolled to the end, and follow new lines (`Ctrl+f` toggles)      |
| `+NF`      | Page the last `N` lines of a file, then follow new growth                                        |
| `-C [NUM]` | Pad `+N` with `NUM` lines of context (bare `-C` = `0`) and highlight line `N` in `bat`           |

### Dispatch and flags

- `--`: Disambiguate options (`-C`, `+OFFSET`, `-h`/`--help`) from `PATHS`.

When given paths, `mm pager` dispatches each path in order (and exits `1` if any path failed):

1. **Directory**: runs `display_directory` from `pager.toml` when non-empty.
2. **Image**: shows fullscreen in `minus` on a TTY, or prints an `<MM_IMAGE>` header when piped (unless disabled by `PG_IMAGE=false`, `PG_MARKDOWN=true`, `+OFFSET`, or text hints).
3. **Markdown** (`.md` / `.markdown`, or `PG_MARKDOWN=true`): renders through `[markdown]` in `pager.toml` with async inline images on a TTY or ANSI on piped stdout.
4. **Text / Stream**: pipes through `bat` when installed and configured, falling back to plain text.

### Environment variables

| Variable         | Effect                                                                            |
| ---------------- | --------------------------------------------------------------------------------- |
| `PG_RAW=true`    | Skip `bat`, markdown, and image dispatch; pass the raw stream through             |
| `PG_FLAGS`       | Comma-separated `bat` flags replacing `bat_opts` (`,,` escapes a literal comma)   |
| `PG_LANG`        | `bat` language override: `-l <value>`                                             |
| `PG_FILENAME`    | `bat` file name hint: `--file-name <value>` (for language detection on stdin)     |
| `PG_IMAGE=false` | Disable image dispatch                                                            |
| `PG_MARKDOWN`    | `true` forces markdown rendering (including for piped stdin); `false` disables it |
| `HIGHLIGHT_LINE` | 1-based line number passed as `bat --highlight-line <value>`                      |

For piped stdin, `bat` is skipped unless `PG_LANG` or `PG_FILENAME` names the content, or `PG_FLAGS` is set alongside `PG_RAW=false`.

## `ShowPreview`

`ShowPreview` (default binds: `F11` and `ctrl-l`) pages the current preview fullscreen using `minus`.
The pager starts immediately: it does not wait for the preview command to
finish, and output streams in as the command produces it. `ShowPreview(cmd)`
pages an arbitrary template instead of the current preview command.

## Configuration — `pager.toml`

Pager settings and markdown styling live in `pager.toml` in matchmaker's configuration directory (next to `config.toml`; `~/.config/matchmaker/pager.toml` on Linux).

| Key                       | Type              | Default                                 | Description                                                                                                         |
| ------------------------- | ----------------- | --------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `bat_opts`                | list of strings   | `["--color=always", "--style=changes"]` | Arguments passed to `bat` in `mm pager`; `[]` disables `bat`                                                        |
| `line_numbers`            | bool              | `false`                                 | Show line numbers                                                                                                   |
| `follow`                  | bool              | `false`                                 | Stick to the newest output                                                                                          |
| `prompt`                  | string (optional) | `"alt-h for help, q to quit"`           | Footer prompt text (`""` hides it)                                                                                  |
| `horizontal_scroll`       | bool              | `true`                                  | Start with line wrapping off                                                                                        |
| `mouse_horizontal_scroll` | bool              | `false`                                 | Enable horizontal mouse wheel scrolling                                                                             |
| `smart_case`              | bool              | `true`                                  | Case-sensitive search unless the query has uppercase                                                                |
| `smart_changes`           | bool              | `false`                                 | Append `--style=+changes` or `--style=-changes` based on git status                                                 |
| `copy_on_select`          | bool              | `false`                                 | Copy the mouse selection on release                                                                                 |
| `display_directory`       | list of strings   | `[]`                                    | Command argv run for directory paths (directory path appended); empty disables                                      |
| `image_protocol`          | string            | `"auto"`                                | Graphics protocol for standalone `mm pager` / `mm image` (`auto`, `halfblocks`, `sixel`, `kitty`, `iterm2`, `none`) |

### `[markdown]` section

How markdown is rendered by `mm --doc`, `@help`, and `mm pager`. A palette for every `bat` theme ships under `matchmaker-cli/assets/markdown/`; copy its contents into `pager.toml` to switch.

- `variant`: Base palette for the terminal background: `neutral` (default), `dark`, or `light`.
- `header`, `bold`, `italic`, `inline_code`, `code_block`, `html`, `bullet`, `quote`, `link`, `link_url`: [style settings](options.md#style-settings) layered over the variant defaults.

Fenced `mermaid` code blocks are drawn as Unicode box diagrams sized to the available width.

```toml
[markdown]
variant = "dark"
header.fg = "#b8bb26"
bold.fg = "#fe8019"
inline_code.fg = "#fabd2f"
inline_code.bg = "#3c3836"
```

### minus keybindings

These are the defaults of minus 5.7 plus the image keys matchmaker registers. A
keybinding table for all of minus's actions lives in the [minus documentation](https://docs.rs/minus/latest/minus/).

| Key                            | Action                                                |
| ------------------------------ | ----------------------------------------------------- |
| `q`, `Ctrl-c`                  | Quit the pager (always resumes the picker)            |
| `j` / `↓`, `k` / `↑`           | Scroll one line (prefix a number to repeat)           |
| `Space`, `PageDown` / `PageUp` | Scroll one page                                       |
| `u`, `Ctrl-u` / `d`, `Ctrl-d`  | Scroll half a page                                    |
| `g` / `G`                      | Go to the top / bottom (or to line N)                 |
| `Enter`                        | Scroll N lines                                        |
| `h` / `←`, `l` / `→`           | Scroll horizontally                                   |
| `Ctrl+←` / `Ctrl+→`            | Scroll left / right by half a page                    |
| `Ctrl-l`                       | Toggle line numbers                                   |
| `Ctrl-f`                       | Toggle follow mode                                    |
| `Alt-w`, `Ctrl+H`              | Toggle line wrap                                      |
| `/`, `?`                       | Search forward / backward                             |
| `n`, `p`                       | Jump to the next / previous match                     |
| `i`                            | Focus the topmost visible image, or leave image focus |
| `+` / `-`                      | Zoom the focused image in / out                       |
| `r` / `R`                      | Rotate the focused image CW / CCW                     |
| `=`                            | Reset every image to its fitted size                  |

## Without the `pager` feature

Without the feature, `ShowPreview` pipes the command output through the
external pager chain `MM_PAGER` → `$PAGER` → `less` → `more`.
