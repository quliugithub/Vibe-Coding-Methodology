# /pack:check

Validate pack completeness before execution.

## Required checks

1. Required fields exist:
   - `pack_id`, `spec_ref`, `goal`, `scope.files`, `constraints`,
     `verification_commands`, `rollback_plan`, `output_required`
2. `scope.files` is not empty.
3. Constraints include both `must` and `must_not`.
4. Risk-sensitive task check:
   - If pack has production bugfix intent, require `runtime_evidence`.
5. Emit PASS/FAIL plus missing fields.

## Exit criteria

- PASS: pack is executable.
- FAIL: no execution allowed until corrected.
