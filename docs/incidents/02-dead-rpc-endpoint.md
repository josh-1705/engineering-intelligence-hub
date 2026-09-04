# Incident 02: dead RPC endpoint silently broke automated admin grants

**Component:** Backend (registryService.js) / Blockchain RPC
**Category:** Backend
**Status:** Resolved
**Severity:** High — silent failure, no error surfaced to the user

## What broke

The public `https://rpc.sepolia.org` endpoint started returning 404s. Every automatic `addAdmin()` call the backend made in the background failed silently — registration still "succeeded" from the user's point of view, but nobody actually received on-chain admin rights.

## Root cause

The app depended on a free public RPC endpoint with no uptime guarantee. When it went down, the backend's transaction calls failed, but the failure wasn't caught or surfaced anywhere — the registration flow itself didn't depend on the RPC call succeeding, so it reported success regardless.

## Fix

Switched from the public RPC endpoint to a proper Alchemy Sepolia RPC URL, which is reliable and monitored.

## Related incidents

This outage caused one account to get stuck mid-registration — see Incident 03 for how that specific orphaned account was reconciled.

## Takeaway

Public/free RPC endpoints are not production-safe — no SLA, no alerting on downtime. Any transaction the backend depends on for correctness should either use a reliable provider or the calling code should surface (not swallow) failures, so broken state doesn't propagate silently.
