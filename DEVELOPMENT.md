# Development Guidelines

This document outlines how CLAW_RAFAEL_IA follows the Claw Code standards.

## Stack Consistency

### Alignment with claw-code-parity-main

Like the original Claw Code project, CLAW_RAFAEL_IA:

✅ **Is autonomously executable** - Runs without human interaction
✅ **Has clear verification steps** - Easy to test and validate
✅ **Maintains organized repository structure** - Clear separation of concerns
✅ **Uses shared configuration** - `.claude.json` for defaults, `.claude/settings.local.json` for overrides
✅ **Documents for Claude Code** - This CLAUDE.md guides AI agents

Unlike the original (which uses Rust + Python):
- **Primary language**: Bash/Shell (portable)
- **Framework**: Standalone (no cargo dependencies)
- **Distribution**: Script-based (not compiled binary)

## Configuration Management

### Global Configuration (~/.claw/config/.claude.json)

Shared across all projects:
```json
{
  "apiKeys": {
    "google": "${GOOGLE_GEMINI_API_KEY}"
  },
  "limits": {
    "maxTokensPerRequest": 2000
  },
  "workspace": {
    "autoDetectFramework": true
  }
}
```

### Project-Specific Overrides (~/.claude/settings.local.json)

Per-project customization (NOT committed):
```json
{
  "workspace": {
    "language": "rust",
    "customPrompt": "This is a systems programming project"
  }
}
```

## Code Quality Standards

### Script Style

Following bash best practices:
```bash
#!/bin/bash
set -e  # Exit on error
set -u  # Error on undefined variable

# Use shellcheck compatible syntax
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Clear variable naming
local_variable="lowercase"
CONSTANT_VALUE="UPPERCASE"

# Proper quoting
echo "Use quotes: $var"

# Clear error handling
command || { echo "Error: $?"; exit 1; }
```

Validation:
```bash
shellcheck automation/my_scripts/*.sh
```

### CLI Design

Following the pattern of main Claw Code:

**commands** are explicit:
```bash
agent analyze FILE      # Clear intent
./agent improve FILE      # Single responsibility
./agent help              # Help is always available
```

**not** magic flags:
```bash
# ❌ Avoid this (implies guessing)
./agent FILE              # What operation?

# ❌ Avoid this (implicit behavior)
./agent -a -v -j FILE     # What do these mean?
```

**output** is clear:
```bash
# ✅ Good
🐛 Bugs Found (3):
  - Line 42: Error handling missing

# ❌ Avoid
Found 3 issues in file
```

## Testing Standards

### Manual Verification

Before committing changes:

```bash
# 1. Syntax check
shellcheck automation/my_scripts/*.sh

# 2. Agent status
agent status

# 3. Help display
agent help

# 4. Test on real code
agent analyze /path/to/sample.rs
agent analyze /path/to/sample.py
```

### Integration Testing

Test with different project types:

```bash
# Test Rust project
agent analyze rust_project/src/main.rs

# Test Python project  
agent analyze python_project/main.py

# Test JavaScript project
agent analyze js_project/index.js
```

## Documentation Standards

### File Purposes

| File | Purpose | Audience |
|------|---------|----------|
| CLAUDE.md | Claude Code guidance | AI agents & developers |
| PHILOSOPHY.md | Why this way, not that way | Decision makers |
| ROADMAP.md | Where we're going | Contributors |
| README.md | What this is | New users |
| AGENTE.md | How to use the agent | Daily users |
| PRIMEIRO-USO.md | Get started in 2 min | Impatient users |

### Comment Style

In scripts:

```bash
################################################################################
# Section Headers - For major logical sections
################################################################################

# Function headers - What does this do?
# Input: description
# Output: description
function my_function() {
    # Inline comments - Why, not what
    # The 'what' should be clear from code
    local result=$(command)
    
    # Inline comment explaining non-obvious logic
    echo "$result"
}
```

### Deprecation Policy

When changing API:

```bash
# OLD (deprecated)
command old-way FILE    # ❌ Don't use

# NEW (use this)
command analyze FILE    # ✅ Use this instead

# Removal timeline: Will be removed in v2.0 (Apr 2026)
```

## Release & Versioning

### Version Format

```
v1.0.0
│ │ └─ Patch (bug fixes)
│ └─── Minor (new features)
└───── Major (breaking changes)
```

### Release Checklist

- [ ] Update version in scripts (VERSION="1.0.0")
- [ ] Update CLAUDE.md if stack/process changes
- [ ] Update ROADMAP.md with completed items  
- [ ] Run full verification (shellcheck, status, tests)
- [ ] Tag in git: `git tag -a v1.0.0 -m "Release message"`
- [ ] Update changelog

### Breaking Changes

For breaking changes (major version):
1. Announce in ROADMAP.md (at least 3 months before)
2. Provide migration guide in README
3. Offer deprecated flag for transition period
4. Document in CHANGELOG

## Alignment with claw-code-parity-main Values

### Autonomy

Like Claw Code, this agent works autonomously:
- ✅ No interactive prompts (except where needed)
- ✅ Deterministic results (same input = same output)
- ✅ Clear success/failure indicators
- ✅ Works in CI/CD pipelines

### Clarity

Clear over clever:
- ✅ One command = one job (analyze, improve, document, test)
- ✅ No hidden behavior (all operations explicit)
- ✅ Readable source (anyone can verify)
- ✅ Understandable output (humans and machines both)

### Coordination

Like the three-part Claw system:
- **Agent** (agent.py) - Does the work
- **Reporting** (status.sh) - Reports state
- **Recovery** (panic.sh + repair.sh) - Handles failures

These work together, not in mysterious ways.

### Reliability

Production-ready:
- ✅ Error handling (proper exit codes)
- ✅ Logging (to ~/.claw/logs/)
- ✅ Backups (before modifications)
- ✅ Safety guards (confirmation before applying changes)

## Contributing

Before submitting changes:

1. **Read CLAUDE.md** - Understand the philosophy
2. **Follow the style** - Consistent with existing code
3. **Test thoroughly** - Works on multiple languages/frameworks
4. **Document changes** - Update relevant .md files
5. **Get approval** - Code review before merge

---

**Last Updated**: 5 de abril de 2026
**Version**: 1.0.0
**Maintainers**: Community contributors
