# IGDR Health Alert — 2026-08-31

Generated: `2026-08-31T12:08:47Z`
Critical failure: **True**
Status: `missing`

## Reasons
- no snapshots/2026-08-31/index.json (and no acceptable yesterday)

## Recovery

This PR is opened automatically when the daily IGDR snapshot is missing or stale.
It is **closed automatically** when Health Monitor reports recovery.

1. Re-run **Daily IGDR Snapshot** (workflow_dispatch)
2. Re-run **IGDR Health Monitor**

