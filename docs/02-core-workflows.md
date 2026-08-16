# Core workflows

> **Skeleton** — structure plus verified facts; full prose to be written.

## File picker

The shipped default config runs a file-listing command (`fd` when available, else `find`) with a `\0` separator, so filenames with spaces and newlines survive intact. Paths are previewed with `eza`/`bat`/`cat` (see [Preview](06-preview.md)).

## Accepting selections

- `enter` (default bind `@accept`) prints the current item to stdout.
- `alt-enter` (`@accept_2`) prints the second output.
- What is printed is controlled by `start.output_template` / `start.on_accept` (see [Templates](12-templates.md) and [Command line](10-command-line.md)).
- When stdout is not a terminal, output is printed as plain lines (`file:line:col` style for editors, etc. — to write: details).

## Multi-select

- `tab` toggles the current item into the selection and moves down; `shift-tab` toggles and moves up (default binds).
- `ctrl-a` cycles selections.
- Templates like `{+}` / `{-}` / `{+col}` expand to all selected items (see [Templates](12-templates.md)).

## Actions and scripts

Bound keys can run commands, become shells, or execute scripts. Commands run through the configured `start.shell`; scripts (first word starting with `@`) resolve relative to the parent of `MM_OVERRIDE` and receive their arguments without shell parsing (see [Binds & actions](11-binds-and-actions.md)).

## Interactive regions

The header, footer, and status line can define clickable regions that trigger semantic actions (see [Templates](12-templates.md#interaction-regions)).

## To write

- Editor / IDE integration and shell scripts wrapping `mm`.
- Ripgrep-based workflows.
- `Become`/`BecomeOrConfirm` replacements of the shell and their exit-code semantics.