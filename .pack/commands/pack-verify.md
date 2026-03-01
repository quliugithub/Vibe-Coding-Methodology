# /pack:verify

Verify acceptance criteria and regression behavior for one pack.

## Steps

1. Run each command in `verification_commands`.
2. Validate AC items against observable outputs.
3. Produce result summary:
   - AC status: PASS/WARN/FAIL
   - command outputs (short form)
   - remaining risks

## Output contract

- Must include explicit failures.
- Must include whether rollback should be triggered.
