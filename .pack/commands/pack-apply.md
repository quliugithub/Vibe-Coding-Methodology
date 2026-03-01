# /pack:apply

Execute implementation strictly under pack guardrails.

## Required flow

1. Run `/pack:check` first.
2. Implement only in files listed by `scope.files`.
3. If out-of-scope edits are required, stop and ask for approval.
4. Avoid public interface changes unless explicitly allowed in constraints.
5. Output:
   - constraints summary
   - git diff
   - regression checklist
   - risks and impact

## Blocking conditions

- Missing required pack fields.
- Out-of-scope file modifications detected.
