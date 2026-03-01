# /pack:create

Create a pack file for one OpenSpec change or one task.

## Inputs

- `change`: OpenSpec change name (required)
- `task-id`: task id from tasks.md (optional)

## Behavior

1. Resolve change folder, then locate related `spec.md` and `tasks.md`.
2. Create pack from template:
   - use `pack-full.yaml` when `task-id` exists
   - otherwise use `pack-lite.yaml`
3. Write output under `docs/ai/packs/YYYY/MM/`.
4. Return created file path.

## Notes

- Do not auto-fill unknown runtime evidence. Leave placeholders if missing.
