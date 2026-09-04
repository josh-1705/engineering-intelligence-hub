# Incident 06: `ethers` installed into the wrong package.json

**Component:** Repo hygiene / Dependency management
**Category:** Repo hygiene
**Status:** Resolved
**Severity:** Medium — would have caused `Cannot find module 'ethers'` on a fresh backend install

## What broke

During a file copy, `ethers` ended up installed into the root `package.json` / `package-lock.json` instead of `backend/`'s. Meanwhile the actual `backend/package.json` — which is what `registryService.js` needs at runtime — was still missing the dependency entirely.

## Root cause

A file copy operation moved dependency changes into the wrong workspace's manifest. Because the root and backend both have their own `package.json` in this project structure, npm didn't surface any error locally (root's `node_modules` still resolved `ethers` during development).

## Fix

Caught during a pre-commit file audit, before it was pushed. Moved the `ethers` entry to `backend/package.json` where `registryService.js` actually imports it from.

## Takeaway

In multi-package-json projects (root + backend + frontend), always verify which `package.json` a new dependency actually needs to live in — installing from the wrong working directory silently works locally but breaks on a clean `npm install` elsewhere. A pre-commit check of `git diff` on every `package.json` catches this class of bug before it reaches a teammate's machine.
