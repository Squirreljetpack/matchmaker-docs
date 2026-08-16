# Preview

> **Skeleton** — structure plus verified facts; full prose to be written.

## Overview

The preview panel renders a command's output for the current item. It can be toggled, scrolled, and configured with one or more layouts.

## Layouts

`[[preview.layout]]` entries configure individual preview panes:

- `command` — template expanded per item (placeholders like `{1}` inject the item; see [Templates](12-templates.md)).
- `side` — `right` or `top`.
- `percentage`, `min`, `max` — adaptive sizing relative to the terminal.
- `border.type` and `border.padding`.

The shipped default config previews directories with `eza` (fallback `find`) and files with `bat` (fallback pager/`cat`).

## Triggering

- `[previewer] always_trigger` — always run preview commands (even when no item is focused).
- Preview commands are only run when the preview is visible (to write: exact trigger semantics).

## Environment

- `MM_PREVIEW_COMMAND` exposes the current preview command to scripts.
- `MM_QUERY` and other env vars are injected into preview commands (see [Templates](12-templates.md#environment-variables)).

## In the UI

- `[preview] wrap` and `scroll_wrap` control wrapping and edge scrolling.
- Preview scrolling actions and pane switching binds — see [Binds & actions](11-binds-and-actions.md).

## To write

- Multiple simultaneous layouts (right + top examples).
- Preview command timing/cancellation behavior.
- Follow-mode / always-render behavior when preview is hidden.