# Incident 04: horizontal scrollbar on the Supplier Management table

**Component:** Frontend (Supplier Management table)
**Category:** Frontend
**Status:** Resolved
**Severity:** Low — UI/UX issue, not a functional bug

## What broke

The Supplier Management table forced a horizontal scrollbar on smaller screens instead of fitting its container.

## Root cause

An inline `minWidth: 750px` combined with `white-space: nowrap` on the table headers forced the table wider than its container, regardless of available screen width.

## Fix

- Replaced the fixed min-width with `table-layout: fixed`
- Added a `<colgroup>` defining percentage-based column widths

The table now always fits its container and wraps cell content instead of forcing a scrollbar.

## Takeaway

Fixed pixel widths on table elements don't respond to container size. `table-layout: fixed` with percentage-based `<colgroup>` widths is the more robust pattern for responsive tables — it also improves rendering performance since the browser doesn't need to measure cell content before laying out columns.
