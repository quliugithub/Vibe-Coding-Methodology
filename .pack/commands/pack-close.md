# /pack:close

Close one pack and write traceability back to spec/change docs.

## Steps

1. Confirm `/pack:verify` completed.
2. Append close record:
   - pack id
   - AC status
   - related PR/commit
   - risk notes
   - rollback notes (if any)
3. Mark pack status as `Done` or `Partially Done`.

## Rule

- Do not close a pack with unresolved FAIL items unless explicitly approved.
