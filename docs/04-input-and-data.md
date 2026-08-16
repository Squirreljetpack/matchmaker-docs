# Input & data sources

> **Skeleton** — structure plus verified facts; full prose to be written.

## Piped input

- When stdin is not a terminal, Matchmaker reads items from stdin (the default command is skipped).
- `input_separator` (`start.input_separator`, absolute alias `n`) chooses the character that separates items; the default config uses `\0` so filenames with spaces/newlines are preserved.
- `skip_invalid_lines` controls whether lines that fail UTF-8 parsing are skipped (true) or raise an error (false).

## Populating commands

- `start.command` runs when stdin is a terminal (or `--no-read` forces it).
- `start.additional_commands` provides extra commands that can be cycled through with the `ReloadNext` / `ReloadPrev` actions.
- When multiple commands exist, `MM_INDEX` reports which one is active (0-indexed); setting `_MM_INDEX` in the environment selects one.
- A per-command object form supports a custom `separator` overriding `input_separator` for that command.

## Context lines

- `-C <N>` (context) rolls N lines around each match into the item, so results show surrounding context and previews/templates can reference it.

## Trailing arguments

- Arguments after `--` are passed to the populating command and are also available to templates as `{$0}`, `{$1}`, `{$n}` (see [Templates](12-templates.md)).
- Warning: trailing arguments are ignored when input is piped.

## Output

- `output_separator` (string, alias `os`) joins printed selections.
- `output_template` (alias `ot`/`output`) is the template used to print results; it is exclusive with `on_accept`.
- `on_accept` runs a template as a command on accepted items.

## To write

- Streaming/async feeding of huge inputs.
- Environment variables available to the populating command.
- Behavior when the command exits non-zero.