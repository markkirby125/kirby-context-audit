# 🔍 Kirby Context Audit (`ai-context-audit`)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Cross-IDE: Antigravity | Cursor | Windsurf | Grok | Kimi | Reasonix | Claude Code | zCode](https://img.shields.io/badge/IDEs-Antigravity%20%7C%20Cursor%20%7C%20Windsurf%20%7C%20Grok%20%7C%20Kimi%20%7C%20Reasonix%20%7C%20Claude%20Code%20%7C%20zCode-brightgreen.svg)](#supported-ecosystems)

**Cross-IDE AI coding agent context bloat, token burn, and skill health auditor.**

`ai-context-audit` inspects your global and workspace agent skills across **18 AI coding apps**: Antigravity, Cursor, Windsurf, Grok, Kimi Code, Reasonix, Claude Code, zCode CLI, OpenCode, Codex, Qwen Code, Aider, Augment, Continue, Roo Code, Kiro, Factory, and Trae. It detects silent prompt bloat, flags monolithic skills, verifies symlink integrity, and measures the token tax imposed on your LLM queries.

---

## ⚡ The Problem: Silent Context Bloat

As you install dozens or hundreds of agent skills, rules, and instruction sets:
1. **Smart Clients** (like Google Antigravity, Grok, or Kimi) parse YAML frontmatter and only inject metadata into the system prompt (progressive disclosure).
2. **Naive Clients** (like Cursor or Windsurf) often inject the **entire root file** (`SKILL.md` or `.cursorrules`) into the system prompt on *every single interaction*.

Having 50 monolithic skills can invisibly burn **100,000 to 300,000+ tokens** per request—slowing down responses, inflating API bills, and causing needle-in-a-haystack context loss.

`ai-context-audit` calculates both loads side-by-side so you can optimize your setup.

---

## 🖥️ Terminal Preview

```text
=== AI Coding Assistant Context Bloat & Skill Auditor ===

● Antigravity (145 skills installed) -> OPTIMAL (Protected)
  Paths: ~/.gemini/config/skills
  Progressive Disclosure Index: 14,238 tokens (Initial metadata injection)
  Brute-Force Injected Load:    270,519 tokens (Worst-case naive full load)

● Cursor (71 skills installed) -> WARNING (35 Bloat Risks)
  Paths: ~/.cursor/skills, ~/.cursor/skills-cursor
  Progressive Disclosure Index: 7,747 tokens (Initial metadata injection)
  Brute-Force Injected Load:    101,219 tokens (Worst-case naive full load)
  ↳ ⚠️  35 monolithic skill(s) exceeding 1,000 tokens!

-------------------------------------------------------------
Summary: 590 total skills scanned across active apps.
Audit Breakdown: 118 optimal, 88 moderate, 353 bloat risks, 0 errors.
```

---

## 🪄 The Magic Prompt

Copy and paste this directly to your AI agent (Cursor, Windsurf, Claude Code, Antigravity):

```markdown
@agent Please install the Kirby Context Audit skill into this workspace.
1. Read the `SKILL.md` file (and `references/` directory if applicable) from this repository: https://github.com/markkirby125/kirby-context-audit
2. Identify the correct rules system for our current environment (e.g., `.cursor/rules/` for Cursor, `.windsurfrules` for Windsurf, `.clinerules` for Cline, or `~/.gemini/config/skills/` for Antigravity).
3. Save the contents appropriately. If our environment supports multi-file dispatcher skills, clone the directory structure exactly.
4. Confirm when the installation is complete.
```

---

## 🚀 Installation

### Option 1: Standalone CLI (Zero Dependencies)

Run directly or install to your `~/.local/bin` (no external packages required, uses standard library with optional `tiktoken`/`PyYAML` support):

```bash
# Clone the repository
git clone https://github.com/markkirby125/kirby-context-audit.git

# Symlink the executable into your PATH
ln -sf "$(pwd)/kirby-context-audit/bin/ai-context-audit" ~/.local/bin/ai-context-audit

# Verify installation
ai-context-audit --help
```

### Option 2: Install as an Agent Skill

To allow your AI coding agents to self-diagnose context overhead, symlink the skill directory to your agent configuration:

```bash
# For Google Antigravity
ln -sf "$(pwd)/kirby-context-audit" ~/.gemini/config/skills/kirby-context-audit

# For Cursor
ln -sf "$(pwd)/kirby-context-audit" ~/.cursor/skills/kirby-context-audit

# For Windsurf
ln -sf "$(pwd)/kirby-context-audit" ~/.codeium/windsurf/skills/kirby-context-audit

# For Grok
ln -sf "$(pwd)/kirby-context-audit" ~/.grok/skills/kirby-context-audit

# For Reasonix
ln -sf "$(pwd)/kirby-context-audit" ~/.reasonix/skills/kirby-context-audit

# For Claude Code
ln -sf "$(pwd)/kirby-context-audit" ~/.claude/skills/kirby-context-audit

# For zCode CLI
ln -sf "$(pwd)/kirby-context-audit" ~/.zcode/skills/kirby-context-audit
```

---

## 📖 Usage & Examples

### 1. Standard Multi-IDE Health Check
```bash
ai-context-audit
```
Scans all detected AI coding environments and displays status badges (`OPTIMAL`, `WARNING`, `CRITICAL`) along with token consumption totals.

### 2. Verbose Per-Skill Inspection
```bash
ai-context-audit -v
```
Displays an aligned per-skill breakdown table showing token cost, symlink targets, and health diagnostics.

### 3. Filter by Specific Application
```bash
ai-context-audit --app cursor
ai-context-audit --app antigravity
ai-context-audit --app reasonix
```

### 4. Audit Workspace Rules & System Instructions
```bash
# Audit current working directory
ai-context-audit --workspace

# Audit a specific project workspace
ai-context-audit --workspace-path /path/to/project
```
Scans `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `ZCODE.md`, `.cursorrules`, `.windsurfrules`, `.github/copilot-instructions.md`, and all recursive `.cursor/rules/**/*.mdc` files.

### 5. Automated Remediation Hints
```bash
ai-context-audit --fix-hints
```
Provides exact shell commands to clean up dead symlinks and guidelines on converting monolithic skills into lean **Hollow Shells**.

### 6. JSON Mode for CI/CD & Pre-Commit Gates
```bash
ai-context-audit --json
```
Emits structured JSON output with standard Unix exit codes:
- **`0`**: Clean audit (zero broken symlinks, missing entrypoints, or dispatchers).
- **`1`**: Critical errors detected (broken symlinks, unreadable files, missing dispatchers).
- **`2`**: Invalid CLI arguments.

---

## 🛡️ The Hollow Shell Architecture

To eliminate context bloat while preserving deep skill functionality, `ai-context-audit` encourages the **Hollow Shell Pattern**:

```text
my-agent-skill/
├── SKILL.md                 <-- Hollow Shell: Frontmatter + Redirection (<150 tokens)
└── references/
    └── 00_dispatcher.md     <-- Complete SOP & Instructions (Loaded on demand)
```

1. **Root `SKILL.md`**: Contains YAML frontmatter and a simple pointer instruction. Naive agents only inject ~100 tokens.
2. **`references/00_dispatcher.md`**: Contains the full operational documentation. Progressive agents read it only when explicitly triggered.

`ai-context-audit` automatically detects Hollow Shell skills and grades them **`OPTIMAL`**, while verifying that the referenced dispatcher physically exists.

---

## 🤝 Supported Ecosystems

| AI Coding Assistant | Configuration Path(s) | Architecture Mode |
|---|---|---|
| **Google Antigravity** | `~/.gemini/config/skills` | Progressive Disclosure |
| **Cursor** | `~/.cursor/skills`, `~/.cursor/skills-cursor`, `.cursor/rules` | Hybrid / Brute-Force |
| **Windsurf** | `~/.codeium/windsurf/skills`, `.windsurfrules` | Hybrid / Brute-Force |
| **Grok** | `~/.grok/skills` | Progressive Disclosure |
| **Kimi Code** | `~/.kimi-code/skills` | Progressive Disclosure |
| **Reasonix** | `~/.reasonix/skills` | Progressive Disclosure |
| **Claude Code** | `~/.claude/skills` | Hybrid |
| **zCode CLI** | `~/.zcode/skills` | Progressive Disclosure |

---

## 📄 License

MIT License © 2026 [Mark Kirby](https://github.com/markkirby125)
