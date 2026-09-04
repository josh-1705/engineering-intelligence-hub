# Incident 03: orphaned admin account from the RPC outage

**Component:** Backend / Blockchain sync
**Category:** Blockchain
**Status:** Resolved
**Severity:** Medium — affected one specific user account, not a systemic failure once caught

## What broke

One admin account (Sanjay's) registered during the window the RPC endpoint (Incident 02) was down. His account was created successfully in MongoDB, but the automatic on-chain `addAdmin()` call silently failed, leaving the account stuck with `onChainAdminSynced: false` — he had a valid login but no actual on-chain admin rights.

## Root cause

Direct downstream effect of Incident 02: the dead RPC endpoint caused the relayer's `addAdmin()` call to fail during this account's registration, and there was no retry or reconciliation logic to catch accounts that registered during the outage.

## Fix

Applied as a one-time manual fix in Remix IDE: called `addAdmin()` directly for this specific wallet address to reconcile the on-chain state with the database record, after the root-cause RPC issue was already patched.

## Takeaway

A single root-cause fix doesn't automatically repair state that was already corrupted before the fix landed. After patching an outage-causing bug, it's worth auditing for records created during the outage window (e.g. querying for `onChainAdminSynced: false`) rather than assuming the fix alone cleared everything.
