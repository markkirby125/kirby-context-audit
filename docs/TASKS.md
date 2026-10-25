# TASKS.md

Every user-requested task is recorded here before work starts.
Each task is one `###` entry with these fields, in this order:

- **id**: short slug, `YYYY-MM-DD-kebab-name`. Unique in this file.
- **title**: what the task delivers, 3 to 8 words.
- **Status**: `todo`, `in progress`, `done`, or `blocked: <reason>`.

---

## Open

<!-- Add new entries above this line. Move finished entries to Done. -->

## Done

<!-- Keep the entry; change Status to done. -->

### 2026-10-25-skip-empty-and-container-dirs Skip empty and container skill folders

Status: done. `ai-context-audit --workspace` exited 1 because the ECC plugin's continuous-learning hook runs `mkdir -p ~/.claude/skills/learned`, leaving an empty folder with no SKILL.md (NO_ENTRYPOINT). The audit now skips empty folders and the `learned` and `imported` containers. Unit tests in `tests/test_skip_dirs.py`: 5 of 5 pass, and the 2 new-behaviour tests fail on the old script. End to end on the real home with the empty `learned` folder present: old script exit 1, new script exit 0. A non-empty folder with no entrypoint and a dead symlink are still reported.
