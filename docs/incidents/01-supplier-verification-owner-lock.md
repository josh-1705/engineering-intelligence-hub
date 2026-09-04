# Incident 01: supplier verification hard-locked to one wallet

**Component:** Smart contract (SupplierRegistry)
**Category:** Blockchain
**Status:** Resolved
**Severity:** High — blocked all admin wallets except the deployer, burned real Sepolia gas on every failed attempt

## What broke

`verifySupplier()` on the deployed `SupplierRegistry` contract was owner-gated to whoever originally deployed it. Any other admin wallet that called it got a silent revert. Confirmed via Etherscan: `Fail with error 'Only admin'`. Each failed attempt still cost real Sepolia gas.

## Root cause

The contract used a single hardcoded owner address for admin checks instead of a proper admin list. Only the deploying wallet passed the check.

## Fix

Redesigned the contract with an on-chain admin allowlist:
- Added an `isAdmin` mapping plus `addAdmin()` / `removeAdmin()` functions
- Automated admin grants end-to-end: the backend now calls `addAdmin()` automatically via a dedicated relayer wallet the moment someone registers as Admin

Result: no wallet is ever locked out, and admin rights are granted without manual on-chain intervention.

## Related incidents

The automated `addAdmin()` relayer flow introduced here depends on a working RPC connection — see Incident 02 for what happened when that RPC endpoint went down, and Incident 03 for the account that got stuck as a result.

## Takeaway

Never gate contract permissions on `msg.sender == deployer`. Use an explicit, updatable allowlist from the start — retrofitting it after deployment means migrating state and re-testing every dependent flow.
