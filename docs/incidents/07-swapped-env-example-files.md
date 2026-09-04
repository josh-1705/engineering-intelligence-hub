# Incident 07: swapped `.env.example` files

**Component:** Repo hygiene / Environment configuration
**Category:** Repo hygiene
**Status:** Resolved
**Severity:** Medium — misleading documentation for anyone setting up the project fresh

## What broke

`frontend/.env.example` ended up containing the backend's environment variable documentation — Mongo URI, JWT secret, server port, and the new relayer wallet variables. Meanwhile `backend/.env.example`, which should document those exact variables, did not have them.

## Root cause

Mixed up during the same file-copy pass that caused Incident 06 (misplaced `ethers` dependency) — both point to files being moved into the wrong workspace folder during cleanup.

## Fix

- Moved the Mongo/JWT/server/relayer variable documentation from `frontend/.env.example` into `backend/.env.example`
- Restored `frontend/.env.example` to only contain frontend-relevant variables (`REACT_APP_API_URL`, `REACT_APP_SOCKET_URL`)
- Re-verified against the README's Section 3 (Environment variables) table to confirm both files now match documented expectations

## Takeaway

`.env.example` files are documentation, not just templates — a swap like this doesn't break the running app (since real `.env` files are git-ignored and set up manually), but it actively misleads the next person setting up the project. Catching this before publishing the repo kept the README's "Notes for the reviewer" claim — that env templates are correctly separated — actually true.
