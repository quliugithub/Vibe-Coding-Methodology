# Pack Plugin Skeleton

This folder defines a `pack` execution layer that can be used together with OpenSpec.

- Planning layer (unchanged): OpenSpec `spec/change/tasks`
- Execution layer (this folder): `pack` commands and guardrails

## Command Set

- `/pack:create <change> [task-id]`
- `/pack:check <pack-file>`
- `/pack:apply <pack-file>`
- `/pack:verify <pack-file>`
- `/pack:close <pack-file>`

## Directory Layout

- `templates/`: starter pack templates
- `schemas/`: JSON schema for pack validation
- `commands/`: command behavior docs

Use `scripts/pack/*.py` for local automation.

## Unified Entrypoint

You can route all `/pack:*` commands to one script:

- `py -3 scripts/pack/pack_dispatch.py`

Detailed command mapping is in:

- `.pack/COMMAND_MAPPING.md`

One-click setup script:

- `scripts/pack/setup_pack_openspec.cmd`

Agent compatibility guide:

- `.pack/AGENT_COMPAT.md`
