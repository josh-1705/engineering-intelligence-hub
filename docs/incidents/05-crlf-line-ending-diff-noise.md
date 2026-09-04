# Incident 05: noisy diff after merging edited files into a fresh clone

**Component:** Repo hygiene / Git workflow
**Category:** Repo hygiene
**Status:** Resolved
**Severity:** Medium — risked burying real changes in a massive, unreviewable commit

## What broke

After merging edited files into a freshly cloned copy of the repo, `git status` showed nearly every file in the project as "modified" — far more than the actual set of intentional changes.

## Root cause

Suspected line-ending mismatch between the original files (likely CRLF, from Windows) and the freshly cloned files. Needed to confirm this before committing, since a huge diff could easily hide a real, unintended change.

## Fix

Ran `git diff -b --ignore-space-at-eol` to compare while ignoring whitespace and line-ending differences. This confirmed the diff was 100% CRLF line-ending noise with zero real content changes. Caught before it could be committed as one massive, meaningless diff that would have made future `git blame` and code review far harder.

## Takeaway

Before committing after any file merge or copy across operating systems, diff with whitespace/line-ending flags first (`-b --ignore-space-at-eol`) to separate real changes from formatting noise. A `.gitattributes` file enforcing consistent line endings (`* text=auto`) prevents this class of issue entirely going forward.
