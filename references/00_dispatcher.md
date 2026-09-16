# Kirby Context Audit — Dispatcher & Operational Guide

## Overview
`kirby-context-audit` provides cross-IDE diagnostic scanning to protect AI coding agents against **system prompt context bloat**, **token burn**, and **broken skill configurations**.

As developers install hundreds of agent skills and custom instructions across multiple IDEs (Antigravity, Cursor, Windsurf, Grok, Kimi Code, Reasonix), naive environments inject full monolithic markdown files into the system prompt on *every turn*, devouring 50,000 to 300,000+ tokens before the user even types a prompt.

`ai-context-audit` scans all registered global and workspace configurations, calculates both the **Progressive Disclosure Load** (what smart agents like AGY or Kimi load) and the **Brute-Force Injected Load** (what naive agents like Cursor inject), and verifies the physical integrity of skill files and symlinks.

---

## Agent Invocation Workflow

When asked to check, audit, or measure context bloat or skill health:

1. **Run Diagnostic Scan**:
   ```bash
   ai-context-audit
   ```
2. **For Verbose Per-Skill Inspection**:
   ```bash
   ai-context-audit -v
   ```
3. **To Audit Workspace Rules Files**:
   ```bash
   ai-context-audit --workspace
   ```
4. **For Automated / CI Pipeline Verification**:
   ```bash
   ai-context-audit --json
   ```

---

## Understanding Diagnostic Outputs

### 1. Headline Metrics
- **Progressive Disclosure Index**: Total tokens consumed when the client only injects frontmatter metadata (name + description). This is the gold standard for clean agent libraries.
- **Brute-Force Injected Load**: Total tokens consumed if the client naively injects the full body of every detected root file.

### 2. Status Badges
| Status | Meaning | Action Required |
|---|---|---|
| `OPTIMAL` | File is under 250 tokens or protected by the Hollow Shell pattern with a verified dispatcher. | None. Fully safe. |
| `MODERATE` | File is between 250 and 1,000 tokens. | Acceptable, but monitor growth. |
| `BLOAT_RISK` | Monolithic root exceeding 1,000 tokens. Injects massive overhead into naive IDE prompts. | Refactor using the Hollow Shell pattern. |
| `BROKEN` | Symlink target is deleted or dead. | Delete dead symlink (`find ... -xtype l -delete`). |
| `NO_ENTRYPOINT` | Skill directory exists but lacks `SKILL.md`, `README.md`, or entrypoint file. | Add `SKILL.md` or remove directory. |
| `UNREADABLE` | Permission error or unreadable binary file. | Fix file permissions. |
| `CRITICAL` | Hollow shell signature detected, but referenced `references/00_dispatcher.md` is MISSING. | Restore dispatcher or revert shell. |

---

## Remediation: The Hollow Shell Architecture

If an audit reveals `BLOAT_RISK` skills, convert them to Hollow Shells:

1. **Extract Body**: Move the detailed instructions, procedures, and reference material from `SKILL.md` into `references/00_dispatcher.md`.
2. **Trim Root File**: Keep `SKILL.md` under 150 tokens containing only:
   - Complete YAML frontmatter (`name`, `description`, `triggers`, `category`).
   - A single redirection line:
     ```markdown
     # Skill Title
     **To execute this skill, you MUST first read the dispatcher instructions located at:**
     `references/00_dispatcher.md`
     ```
3. **Verify**: Run `ai-context-audit -v` to ensure the skill status transitions from `BLOAT_RISK` to `OPTIMAL`.
