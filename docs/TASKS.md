# TASKS.md

Every user-requested task is recorded here before work starts.
Each task is one `###` entry with these fields, in this order:

- **id**: short slug, `YYYY-MM-DD-kebab-name`. Unique in this file.
- **title**: what the task delivers, 3 to 8 words.
- **Status**: `todo`, `in progress`, `done`, or `blocked: <reason>`.


---

Open tasks live in Backlog.md (`backlog/tasks/`, 0 open tasks at import on 2026-11-25). Run `npx backlog.md task list --plain` from the project root to list them, `npx backlog.md task <id> --plain` to read one, and `npx backlog.md task create` or `task edit` to change them.

Finished work: docs/TASKS-ARCHIVE.md. Long evidence: docs/TASKS-EVIDENCE.md (each task's description names its evidence section). The pre-migration copy of this file is in git history and in `~/backups/tasks-backlog-2026-11-25/kirby-context-audit/`.
