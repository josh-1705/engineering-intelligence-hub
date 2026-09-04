# Incident log — SupplyChainX

A record of real issues found and fixed during production hardening of SupplyChainX, organized by component. Used as source material for the Engineering Intelligence Hub RAG assistant.

| # | Title | Component | Category | Status |
|---|---|---|---|---|
| 01 | Supplier verification hard-locked to one wallet | SupplierRegistry contract | Blockchain | Resolved |
| 02 | Dead RPC endpoint silently broke admin grants | registryService.js | Backend | Resolved |
| 03 | Orphaned admin account from the RPC outage | Backend / chain sync | Blockchain | Resolved |
| 04 | Horizontal scrollbar on Supplier Management table | Frontend | Frontend | Resolved |
| 05 | Noisy diff from CRLF line endings | Git workflow | Repo hygiene | Resolved |
| 06 | `ethers` installed into the wrong package.json | Dependency management | Repo hygiene | Resolved |
| 07 | Swapped `.env.example` files | Environment config | Repo hygiene | Resolved |

## By category

**Blockchain (2):** contract-level access control design, and the state-consistency fallout from an infrastructure outage.

**Backend (1):** dependency on an unreliable public RPC provider causing a silent, unlogged failure mode.

**Frontend (1):** a CSS layout bug from fixed-width table styling.

**Repo hygiene (3):** the class of issues that don't break functionality but actively mislead future contributors — line-ending noise, dependency misplacement, and mismatched documentation.

## Why this matters for the project

All seven issues are fully resolved with a documented root cause and fix — the kind of debugging narrative that's hard to find in generic public GitHub issues. This gives the RAG assistant real, specific "why did this break and how was it fixed" content across blockchain, backend, frontend, and repo hygiene.
