# Technical Standards

Alignment with claw-code-parity-main technical practices.

## Code Style Standards

### Shell Script (Primary Language)

**Naming conventions:**

```bash
# Functions: lowercase_with_underscores
function check_api_key() { }
function get_project_info() { }

# Constants: UPPERCASE_WITH_UNDERSCORES  
readonly API_BASE_URL="https://generativelanguage.googleapis.com"
readonly MAX_TOKENS=2000

# Local variables: lowercase_with_underscores
local file_path="/tmp/test.rs"
local response_data=""

# Global variables: (avoid when possible, but prefix with underscore)
_global_state="initialized"
```

**Quoting rules:**

```bash
# ✅ GOOD: Always quote variables
echo "File: $file_path"
[[ "$result" == "success" ]]

# ❌ BAD: Unquoted variables
echo File: $file_path
[[ $result == success ]]

# ✅ Quoting command substitution
local files=$(find . -name "*.rs")

# Exception: Command substitution in conditionals
if [[ $(whoami) == "root" ]]; then
    echo "Running as root"
fi
```

**Exit handling:**

```bash
# ✅ At top of script: fail fast
set -e      # Exit on any error
set -u      # Error on undefined variables
set -o pipefail  # Pipe errors propagate

# ✅ Explicit error handling
if ! command "$arg"; then
    echo "Error: Command failed with code $?" >&2
    return 1
fi

# ✅ Trap for cleanup
trap 'rm -f "$temp_file"' EXIT

# ❌ BAD: Ignoring errors silently
command "$arg"  # Error? Who knows!
```

**Function documentation:**

```bash
################################################################################
# Print git status summary
#
# This prints a summary of git status for quick operational checks.
# Requires: git (globally available)
#
# Arguments:
#   None
#
# Output:
#   String describing git state
#
# Exit code:
#   0 if success
#   1 if git not found
#
# Example:
#   show_git_status
#   # Output: "On branch main, 3 commits ahead"
#
################################################################################
function show_git_status() {
    local output
    
    if ! command -v git &> /dev/null; then
        echo "Error: git not found" >&2
        return 1
    fi
    
    output=$(git status --short)
    echo "Git status: ${output:-clean}"
}
```

### Configuration (JSON Format)

**Structure & validation:**

```json
{
  "apiKeys": {
    "google": "${GOOGLE_GEMINI_API_KEY}",
    "anthropic": null
  },
  "limits": {
    "maxTokensPerRequest": 2000,
    "maxDailyRequests": 1000
  },
  "workspace": {
    "agentMode": "professional",
    "autoDetectFramework": true,
    "supportedLanguages": [
      "rust", "python", "javascript", "csharp", "go",
      "ruby", "php", "java", "c"
    ]
  }
}
```

**Validation rules:**
- [ ] Must be valid JSON (use `python3 -m json.tool`)
- [ ] All required keys present: `apiKeys`, `limits`, `workspace`
- [ ] API key format: Starts with `AIzaSy` for Google
- [ ] Numeric values: No strings for numbers, no negative limits
- [ ] Language list: All lowercase, valid identifiers

### File Organization

**Directory structure conventions:**

```
~/ClawRafaelIA/
├── automation/
│   └── my_scripts/        # Executable scripts
│       ├── agent.py       # Primary agent (Python 3)
│       ├── status.sh      # Quick health check
│       ├── panic.sh       # Emergency stop
│       ├── repair.sh      # Auto-repair
│       └── setup.sh       # Initial setup
├── config/                # Config templates (read-only)
│   └── .claude.template.json
├── logs/                  # Runtime logs (ignored)
├── *.md                   # Documentation
└── .devcontainer/         # Container definition
```

**File size limits:**

| Component | Max Size | Rationale |
|-----------|----------|-----------|
| agent.py | 1100 linhas | Primary script (Python 3), audit-friendly |
| status.sh | 4 KB | Quick checks only |
| Single .md doc | 50 KB | Readable in one sitting |
| .devcontainer | 10 KB | Fast container builds |

**Permissions:**

```bash
# Scripts: executable by user, readable by all
chmod 755 automation/my_scripts/*.sh

# Config files: readable by user only (API keys)
chmod 600 ~/.claw/config/.claude.json

# Logs: readable/writable by current user
touch ~/.claw/logs/agent.log
chmod 600 ~/.claw/logs/*.log

# Documentation: readable by all
chmod 644 *.md
```

## API Integration Standards

### Google Generative AI (Gemini)

**Endpoint format:**

```
GET https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent
?key=${GOOGLE_GEMINI_API_KEY}
```

**Request structure:**

```bash
curl -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$api_key" \
  -H "Content-Type: application/json" \
  -d "{
    \"contents\": [{
      \"parts\": [{ \"text\": \"$prompt\" }]
    }]
  }"
```

**Response parsing:**

```json
{
  "candidates": [{
    "content": {
      "parts": [
        { "text": "API response here..." }
      ]
    }
  }]
}
```

**Error cases:**

```bash
# Handle 401 (auth error)
if [[ "$response" == *"Invalid API key"* ]]; then
    echo "❌ API key invalid or expired"
    return 1
fi

# Handle 429 (rate limit)
if [[ "$response" == *"429"* ]]; then
    echo "⏸️  Rate limit exceeded, retry in 1 minute"
    return 2
fi

# Handle network errors
if [[ -z "$response" ]] || [[ "$response" == "null" ]]; then
    echo "❌ Network error or no response"
    return 3
fi
```

**Token accounting:**

```bash
# Margin of safety: Stop at 80% of limit
readonly API_LIMIT=2000
readonly MARGIN=1600  # 80% of limit

prompt_size() {
    # Rough estimation: 1 token ≈ 4 characters
    local text="$1"
    echo $(( ${#text} / 4 ))
}

if [[ $(prompt_size "$prompt") -gt $MARGIN ]]; then
    echo "❌ Prompt too large for API limits"
    return 1
fi
```

### Fallback & Retry Logic

**Retry strategy:**

```bash
function api_call_with_retry() {
    local prompt="$1"
    local max_attempts=3
    local attempt=1
    
    while [[ $attempt -le $max_attempts ]]; do
        local response=$(call_api "$prompt" 2>&1)
        local exit_code=$?
        
        if [[ $exit_code -eq 0 ]]; then
            echo "$response"
            return 0
        fi
        
        # Exponential backoff: 1s, 2s, 4s
        local wait_time=$((2 ** (attempt - 1)))
        echo "Attempt $attempt failed, retrying in ${wait_time}s..." >&2
        sleep "$wait_time"
        
        attempt=$((attempt + 1))
    done
    
    echo "❌ API call failed after $max_attempts attempts" >&2
    return 1
}
```

## Logging Standards

### Log Location

```
~/.claw/logs/
├── agent.log          # All agent operations
├── errors.log         # Only errors and warnings
└── debug.log          # Verbose debug info (development only)
```

### Log Format

```
[2026-04-05 14:32:15] INFO    Agent started with analyze mode
[2026-04-05 14:32:16] DEBUG   Reading file: /path/to/file.rs
[2026-04-05 14:32:17] INFO    API call succeeded
[2026-04-05 14:32:18] ERROR   File not found: /nonexistent/path
[2026-04-05 14:32:19] WARNING API response truncated (over limit)
```

**Structured logging:**

```bash
function log() {
    local level="$1"
    local message="$2"
    local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    
    echo "[$timestamp] $level    $message" | tee -a ~/.claw/logs/agent.log
    
    if [[ "$level" == "ERROR" ]] || [[ "$level" == "WARNING" ]]; then
        echo "[$timestamp] $level    $message" >> ~/.claw/logs/errors.log
    fi
}

# Usage:
log "INFO" "Starting analysis"
log "ERROR" "File not readable"
```

### Log Rotation

```bash
# Keep last 10 log files (1 per day)
function rotate_logs() {
    local log_dir="$HOME/.claw/logs"
    local max_files=10
    
    if [[ $(ls -1 "$log_dir"/agent.log.* 2>/dev/null | wc -l) -gt $max_files ]]; then
        ls -t "$log_dir"/agent.log.* | tail -n +$((max_files + 1)) | xargs rm -f
    fi
    
    mv "$log_dir/agent.log" "$log_dir/agent.log.$(date +%s)"
}
```

## Testing Standards (from claw-code-parity-main)

### Unit Test Structure

Tests should be organized like the original Claw Code tests:

```bash
#!/bin/bash
# tests/test_api_integration.sh

set -e

# Setup
readonly TEST_DIR="/tmp/claw_test"
mkdir -p "$TEST_DIR"

# Cleanup on exit
trap 'rm -rf "$TEST_DIR"' EXIT

# Test 1: API key validation
test_api_key_validation() {
    local result
    result=$(check_api_key)
    
    if [[ "$result" == *"valid"* ]]; then
        echo "✅ PASS: API key validation"
        return 0
    else
        echo "❌ FAIL: API key validation"
        return 1
    fi
}

# Test 2: Language detection
test_language_detection() {
    # ... test logic
}

# Run all tests
test_api_key_validation
test_language_detection
```

### Performance Standards

```bash
# Operations should complete in reasonable time:
# - Status check: < 1 second
# - Language detection: < 0.5 seconds
# - API call: < 10 seconds (including network)
# - Help display: < 0.1 second

# Test timing:
time agent status
# real    0m0.123s
```

## Compatibility Standards

### Supported Systems

| System | Shell | Status | Notes |
|--------|-------|--------|-------|
| Ubuntu 22.04+ | bash 5.1+ | ✅ Tested | Primary target |
| CentOS 7+ | bash 4.2+ | ✅ Works | Older bash supported |
| macOS 11+ | bash 5.1+ | ⚠️ Partial | Requires brew bash |
| Windows WSL2 | bash 5.1+ | ✅ Tested | Via Ubuntu image |

**Compatibility check:**

```bash
# Bash version requirement
if [[ "${BASH_VERSINFO[0]}" -lt 4 ]]; then
    echo "❌ Bash 4.0+ required (you have ${BASH_VERSION})" >&2
    exit 1
fi

# Required commands check
for cmd in curl grep sed awk; do
    if ! command -v "$cmd" &> /dev/null; then
        echo "❌ Command not found: $cmd" >&2
        exit 1
    fi
done
```

### Python Compatibility (for config validation)

```python
# Only Python 3.6+ features
import json
import subprocess
import sys

if sys.version_info < (3, 6):
    print("Error: Python 3.6+ required")
    sys.exit(1)

# Validate JSON config
with open("~/.claw/config/.claude.json") as f:
    config = json.load(f)
    assert "apiKeys" in config
    assert "limits" in config
```

## Security Standards

### API Key Handling

```bash
# ✅ GOOD: Read from config file (0600 permissions)
api_key=$(grep -oP '"google":\s*"\K[^"]+' ~/.claw/config/.claude.json)

# ❌ BAD: API key in script (exposed on git)
api_key="${GOOGLE_GEMINI_API_KEY}"

# ❌ BAD: API key in environment variable without protection
export GOOGLE_API_KEY="AIzaSyD3..."

# ✅ Protect during use
function call_api() {
    local prompt="$1"
    local api_key
    api_key=$(get_api_key)
    
    curl -s -X POST \
      "https://api.example.com?key=$api_key" \
      -d "$prompt"
      
    # Clear local variable
    unset api_key
}
```

### Input Validation

```bash
# ✅ Validate file inputs
function validate_file() {
    local file="$1"
    
    # Check exists
    if [[ ! -f "$file" ]]; then
        echo "❌ File not found: $file" >&2
        return 1
    fi
    
    # Check readable
    if [[ ! -r "$file" ]]; then
        echo "❌ File not readable: $file" >&2
        return 1
    fi
    
    # Check size (avoid huge files)
    local size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file")
    if [[ $size -gt 1000000 ]]; then  # 1 MB limit
        echo "❌ File too large: $file ($size bytes)" >&2
        return 1
    fi
    
    return 0
}
```

### Command Injection Prevention

```bash
# ❌ BAD: Command injection risk
eval "grep $pattern $file"

# ✅ GOOD: Proper quoting
grep "$pattern" "$file"

# ✅ GOOD: Use placeholders, not string building
grep -- "$query" "$file"  # -- prevents flags in $query
```

## Documentation Standards

### Comment Guidelines

```bash
# Bad: Obvious comment
x=$((x + 1))  # Increment x

# Good: Why, not what
count=$((count + 1))  # Start counting from 1, not 0

# Bad: Outdated comment
# TODO: Fix this in v2.0 (← what's v2.0?)

# Good: Clear commitment
# TODO: Improve error messages (Planned for v1.1, March 2026)
```

### Markdown Standards

```markdown
# Heading 1 (one per file)

## Heading 2 (major sections)

### Heading 3 (subsections)

#### Heading 4 (rarely needed)

- Use bulleted lists for items
  - With proper nesting
  - For structure

1. Numbered lists for sequences
2. In execution order
3. With clear hierarchy

**Bold** for emphasis, `code` for symbols
```

---

**Last Updated**: 5 de abril de 2026
**Version**: 1.0.0
**Reference**: Based on claw-code-parity-main standards
