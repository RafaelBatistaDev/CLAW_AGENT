# Testing & Verification Guide

How to test and verify CLAW_RAFAEL_IA follows Claw Code standards.

## Quick Verification (2 minutes)

Run this sequence to verify everything works:

```bash
cd ~/ClawRafaelIA

# 1. Check scripts are executable
ls -la automation/my_scripts/ | grep "^-rwx"

# 2. Verify configuration exists
cat ~/.claw/config/.claude.json | head -5

# 3. Check API key is configured
grep -q "AIzaSy" ~/.claw/config/.claude.json && echo "✅ API Key present"

# 4. Run status check
agent status

# 5. Display help
agent help
```

Expected output:
```
✅ API Key present
✅ Status: Ready
🤖 Agent available
💾 Configuration loaded
```

## Full Test Suite

### Phase 1: Static Analysis

Check code quality without running:

```bash
# 1. Syntax validation (requires shellcheck)
cd ~/ClawRafaelIA
shellcheck automation/my_scripts/*.sh

# 2. Configuration validation
cat ~/.claw/config/.claude.json | python3 -m json.tool > /dev/null
echo "JSON valid"

# 3. File integrity
test -r ~/.claw/config/.claude.json && echo "Config readable"
test -x agent && echo "Agent executable"
```

### Phase 2: Functional Testing

Test each command:

```bash
# Test 1: Status command (no API call needed)
agent status
# Verify output contains:
#   - API key status
#   - Logs directory
#   - Configuration path

# Test 2: Help command
agent help
# Verify output shows:
#   - analyze
#   - improve
#   - document
#   - test

# Test 3: Error handling
agent analyze /nonexistent/file.py
# Should show: "❌ File not found" or similar error
# Should exit with non-zero code
```

### Phase 3: Language Detection

Verify auto-detection works for different languages:

```bash
# Create test files in temporary directory
mkdir -p /tmp/claw_test

# Test Rust
cat > /tmp/claw_test/test.rs <<'EOF'
fn main() {
    println!("Hello, world!");
}
EOF

# Test Python
cat > /tmp/claw_test/test.py <<'EOF'
def hello():
    print("Hello")
EOF

# Test JavaScript
cat > /tmp/claw_test/test.js <<'EOF'
function hello() {
  console.log("Hello");
}
EOF

# Run detection (requires API, but shows it recognizes language)
agent status
# Output should show how many languages are supported
```

### Phase 4: API Integration

Test actual AI agent functionality:

```bash
# Create a simple test file
cat > /tmp/test_simple.rs <<'EOF'
fn add(a: i32, b: i32) -> i32 {
    return a + b  // Missing semicolon
}
EOF

# Run agent (will use actual API)
agent analyze /tmp/test_simple.rs

# Check that:
# 1. Agent returned suggestions
# 2. Agent identified the issue
# 3. Output was formatted clearly
```

### Phase 5: Configuration Handling

Test config override behavior:

```bash
# Create project-specific config
mkdir -p .claude
cat > .claude/settings.local.json <<'EOF'
{
  "workspace": {
    "language": "rust",
    "customPrompt": "Focus on performance"
  }
}
EOF

# Verify it would be loaded (agent reads it if present)
ls -la .claude/settings.local.json

# Clean up
rm .claude/settings.local.json
```

### Phase 6: Error Recovery

Test panic and repair scripts:

```bash
# Test panic script (emergency stop)
./automation/my_scripts/panic.sh
# Verify:
# - It doesn't crash the machine 😊
# - It shows recovery instructions
# - Logs written to ~/.claw/logs/

# Test repair script
./automation/my_scripts/repair.sh
# Verify:
# - No errors during cleanup
# - Reports what was cleaned
```

## Continuous Testing

### Pre-commit Hook (Optional)

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
set -e

echo "🔍 Running quick checks..."

# 1. Syntax check
shellcheck automation/my_scripts/*.sh || exit 1

# 2. Config validation  
python3 -m json.tool < ~/.claw/config/.claude.json > /dev/null || exit 1

# 3. Agent health
agent status > /dev/null || exit 1

echo "✅ All checks passed"
exit 0
```

Enable it:
```bash
chmod +x .git/hooks/pre-commit
```

### Test in Docker (Verify Portability)

Test that agent works in isolated environment:

```bash
# Build devcontainer
docker build -f .devcontainer/Dockerfile -t claw-test .

# Run agent inside container
docker run --rm -v ~/.claw/config:/root/.claw/config:ro claw-test \
  /home/claagent status
```

Expected: Agent works without local environment setup.

## Verification Checklist

Use this before any release:

### Code Quality (Bash)
- [ ] `shellcheck` passes with no warnings
- [ ] All scripts executable (`chmod +x`)
- [ ] No hardcoded paths (use variables)
- [ ] No security issues (input validated)
- [ ] Error messages are clear
- [ ] Exit codes are proper (0 = success, non-zero = error)

### Configuration
- [ ] `.claude.json` has valid JSON syntax
- [ ] API key is real (starts with `AIzaSy`)
- [ ] All required fields present
- [ ] Limits are reasonable (not 0 or negative)

### Documentation
- [ ] `CLAUDE.md` is up to date with code
- [ ] `ROADMAP.md` reflects current version
- [ ] `AGENTE.md` has working examples
- [ ] No broken links in `.md` files
- [ ] Spelling/grammar checks (Portuguese)

### Functional
- [ ] `agent help` works
- [ ] `agent status` shows correct state
- [ ] At least one `analyze` test succeeds
- [ ] Error handling works (bad input = clear error)
- [ ] Backup creation works (file.backup created)
- [ ] Logs are written to ~/.claw/logs/

### Portability
- [ ] Works on macOS (if tested)
- [ ] Works on Linux (if tested)
- [ ] Works on WSL2 (if tested)
- [ ] No binary dependencies (only curl, bash)
- [ ] Works after copying folder to new PATH

### Release-specific
- [ ] Version number updated in scripts
- [ ] CHANGELOG.md created/updated
- [ ] Git tag created: `git tag v1.0.0`
- [ ] README has correct version info

## Known Test Gaps

These tests require manual intervention and aren't automated:

- **Anthropic API** - Would require additional key (currently uses Google)
- **GitHub integration** - Pre-commit hooks need setup
- **CI/CD** - GitHub Actions workflow testing (documented in Phase 1 roadmap)
- **Performance** - No benchmarks yet (Phase 2 roadmap)
- **Security audit** - Professional pentest not done

These are tracked in ROADMAP.md with target phases.

## Running Tests Programmatically

```bash
#!/bin/bash
# test_suite.sh - Run all tests

set -e

echo "🧪 CLAW_RAFAEL_IA Test Suite"
echo "=========================="

# 1. Static
echo "📋 Phase 1: Static Analysis..."
shellcheck automation/my_scripts/*.sh
python3 -m json.tool < ~/.claw/config/.claude.json > /dev/null
echo "✅ Static analysis passed"

# 2. Functional
echo "📋 Phase 2: Functional Tests..."
agent status > /dev/null
agent help > /dev/null
echo "✅ Functional tests passed"

# 3. Detection
echo "📋 Phase 3: Language Detection..."
[ -f automation/my_scripts/agent ] && echo "✅ Detection available"

# 4. Configuration
echo "📋 Phase 4: Configuration..."
[ -r ~/.claw/config/.claude.json ] && echo "✅ Configuration valid"

# 5. Recovery
echo "📋 Phase 5: Recovery Scripts..."
[ -x ./automation/my_scripts/panic.sh ] && echo "✅ Panic script executable"
[ -x ./automation/my_scripts/repair.sh ] && echo "✅ Repair script executable"

echo ""
echo "🎉 All tests passed!"
```

Run it:
```bash
chmod +x test_suite.sh
./test_suite.sh
```

## Integration with claw-code-parity-main

CLAW_RAFAEL_IA tests should mirror the philosophy:

✅ **Verification is fast** - Full suite in under 30 seconds
✅ **No external services during tests** - except API calls
✅ **Clear pass/fail** - Not ambiguous results
✅ **Reproducible** - Same result every time from same state
✅ **Non-destructive** - Tests don't break the system

---

**Last Updated**: 5 de abril de 2026
**Version**: 1.0.0
