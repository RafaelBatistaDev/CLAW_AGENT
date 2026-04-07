# 🏛️ CLAW Extension — Architecture & Design

Deep dive técnico na arquitetura da extensão.

## 📊 Fluxograma de Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                        User Types                           │
│  (Editor JS→TypeScript→Python→C#→Rust→Go→Ruby→PHP→Java→C++)│
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│              VS Code Editor       (Wayland/X11)             │
│  • Detects language & position                              │
│  • Captures cursor context                                  │
│  • Triggers on "pause typing"                               │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│         InlineCompletionProvider (JavaScript)               │
│  • Debounce: 500ms (configurable)                           │
│  • Collects last 10 lines before cursor                     │
│  • Tracks language type                                     │
└────────────────────────────┬────────────────────────────────┘
                             │
          ┌──────────────────┴──────────────────┐
          │                                     │
    ┌─────▼──────┐                    ┌────────▼────────┐
    │ TokenCache │                    │  AgentManager   │
    │ (Semantic) │                    │ (subprocess)    │
    │            │                    │                 │
    │ • Jaccard  │                    │ • Python call   │
    │   match    │                    │ • 2s timeout    │
    │ • 75%      │                    │ • Circuit break │
    │   threshold│                    │ • JSON payload  │
    │ • LRU      │                    │                 │
    │ • Disk     │                    │                 │
    │   persist  │                    │                 │
    └─────┬──────┘                    └────────┬────────┘
          │                                    │
          │ HIT (75%+ similarity)             │ NO HIT
          │ ZERO API CALLS                    │
          │                                    │
          └────────────┬──────────────────────┘
                       │
          ┌────────────▼──────────────┐
          │                           │
    ┌─────▼──────┐          ┌────────▼────────┐
    │InlineComp  │          │  agent.py       │
    │Item[]      │          │  (subprocess)   │
    │(cached)    │          │                 │
    │            │          │ Gets JSON:      │
    │Return      │          │ {context,       │
    │suggestion  │          │  language,      │
    └────────────┘          │  fileName,      │
                            │  maxTokens}     │
                            │                 │
                            │ Returns JSON:   │
                            │ {suggestion,    │
                            │  confidence,    │
                            │  source,        │
                            │  tokens_used}   │
                            │                 │
                            └────────┬────────┘
                                     │
                        ┌────────────┴──────────────┐
                        │                           │
                ┌───────▼───────┐        ┌─────────▼───────┐
                │  API Success  │        │  API Error OR   │
                │  (200 tokens) │        │  Timeout (2s)   │
                │               │        │                 │
                │  CALL MADE    │        │ FALLBACK:       │
                │               │        │ LocalAI         │
                │  Cache store  │        │ suggestions     │
                │  next time    │        │                 │
                └───────┬───────┘        └─────────┬───────┘
                        │                           │
                        └───────────┬───────────────┘
                                    │
                            ┌───────▼───────┐
                            │ Display in    │
                            │ gray text     │
                            │ (ghost text)  │
                            │               │
                            │ User action:  │
                            │ Tab (accept)  │
                            │ Esc (reject)  │
                            └───────────────┘
```

---

## 📂 Estrutura de Arquivos

```
vscode-extension/
├── src/                              # TypeScript source code
│   ├── extension.ts                  # Entry point (195L)
│   ├── inlineCompletionProvider.ts   # Core provider (155L)
│   ├── agentManager.ts               # Subprocess mgmt (320L)
│   ├── tokenCache.ts                 # Semantic cache (235L)
│   └── logger.ts                     # Logging (65L)
│
├── dist/                             # Compiled JavaScript (auto)
│   ├── extension.js
│   ├── inlineCompletionProvider.js
│   ├── agentManager.js
│   ├── tokenCache.js
│   └── logger.js
│
├── out/                              # Test output (auto)
│
├── node_modules/                     # Dependencies (npm install)
│
├── package.json                      # Manifest (172L)
├── package-lock.json                 # Lock file
├── tsconfig.json                     # TypeScript config
├── webpack.config.js                 # Bundler config
├── .eslintrc.json                    # Linter config
├── .gitignore                        # Git ignore
│
├── README.md                         # Full documentation
├── QUICK-START.md                    # Quick start guide
├── ARCHITECTURE.md                   # This file
│
├── setup.sh                          # Setup (Linux/macOS)
├── setup.bat                         # Setup (Windows batch)
├── setup.ps1                         # Setup (Windows PS)
└── install.py                        # Setup (Python)
```

---

## 🔧 Core Components

### 1️⃣ extension.ts (Entry Point)

**Responsabilidades:**
- Ciclo de vida da extensão (activate, deactivate)
- Inicializar Logger, TokenCache, AgentManager
- Registrar InlineCompletionProvider
- Registrar commands (toggle, clearCache, showStatus)
- Criar status bar item
- Listener de config changes

**Fluxo:**
```typescript
export async function activate(context: ExtensionContext) {
  // 1. Create Logger
  const logger = new Logger(logLevel);
  
  // 2. Create TokenCache in globalStoragePath
  const cache = new TokenCache(globalStorage);
  
  // 3. Create AgentManager
  const agentManager = new AgentManager(agentPythonPath, logger);
  
  // 4. Register InlineCompletionProvider
  const provider = new InlineCompletionProvider(
    agentManager,   // calls agent.py
    cache,          // semantic cache
    logger,         // debugging
    debounceMs      // responsiveness
  );
  
  languages.registerInlineCompletionItemProvider(
    [patterns],     // 11 languages
    provider
  );
  
  // 5. Register commands & status bar
  commands.registerCommand('clawrafaelia.toggleSuggestions', ...);
  commands.registerCommand('clawrafaelia.clearCache', ...);
  commands.registerCommand('clawrafaelia.showStatus', ...);
  
  // 6. Watch config changes
  workspace.onDidChangeConfiguration(...);
}
```

**Key Points:**
- ExtensionContext provides storage paths
- GlobalStorageUri is multiuser-safe
- Commands registered with vscode.commands namespace
- Status bar background update loop

---

### 2️⃣ inlineCompletionProvider.ts (Core Logic)

**Responsabilidades:**
- Implements vscode.InlineCompletionItemProvider interface
- Debouncing user pauses
- Context collection
- Calling agent.py via AgentManager
- Cache lookup
- UI rendering

**Fluxo:**

```typescript
async provideInlineCompletionItems(
  document: TextDocument,
  position: Position,
  context: InlineCompletionContext,
  token: CancellationToken
): Promise<InlineCompletionItem[]> {
  // 1. Global state per document
  if (!debounceTimers) debounceTimers = new Map();
  
  // 2. Clear previous timer
  if (debounceTimers.has(document.uri.toString())) {
    clearTimeout(debounceTimers.get(document.uri.toString()));
  }
  
  // 3. Set new debounce timer (500ms)
  const timer = setTimeout(() => {
    (async () => {
      try {
        // 4. Check cancellation token
        if (token.isCancellationRequested) return [];
        
        // 5. Collect context
        const context = this.collectContext(document, position);
        
        // 6. Determine language
        const language = document.languageId;
        
        // 7. Check TokenCache first
        const cached = this.tokenCache.lookup(context);
        if (cached) {
          this.logger.debug(`Cache HIT: ${context.substring(0, 20)}...`);
          return [new vscode.InlineCompletionItem(cached.suggestion)];
        }
        
        // 8. Call agent.py
        const result = await this.agentManager.suggest({
          context,
          language,
          fileName: document.fileName,
          maxTokens: this.maxTokens
        });
        
        // 9. Cache result for next time
        this.tokenCache.put(context, result.suggestion);
        
        // 10. Return InlineCompletionItem
        const item = new vscode.InlineCompletionItem(
          result.suggestion,
          new vscode.Range(position, position),
          vscode.InlineCompletionItemKind.Text
        );
        
        return [item];
        
      } catch (error) {
        this.logger.error(`Inline provider error: ${error.message}`);
        return [];
      }
    })();
  }, this.debounceMs);
  
  debounceTimers.set(document.uri.toString(), timer);
  return []; // Empty first response (debounced)
}

// Helper: Collect context (last 10 lines)
private collectContext(document: TextDocument, position: Position): string {
  const lineNum = position.line;
  const startLine = Math.max(0, lineNum - 9);
  const endLine = lineNum;
  
  const lines = [];
  for (let i = startLine; i <= endLine; i++) {
    const line = document.lineAt(i).text;
    if (i < lineNum) {
      lines.push(line);
    } else {
      // Include partial line up to cursor
      lines.push(line.substring(0, position.character));
    }
  }
  
  return lines.join('\n');
}
```

**Key Decisions:**
- **Debounce per-document:** Different files can be edited simultaneously
- **Empty initial response:** Prevents jank, suggestion added next request
- **Token handling:** Cancellation cancels pending agent.py call
- **Error silent:** Failures don't interrupt user experience

---

### 3️⃣ agentManager.ts (Subprocess Communication)

**Responsabilidades:**
- Encontrar agent.py no filesystem
- Validar agent.py no startup
- Executar agent.py como subprocess
- JSON serialization/deserialization
- Circuit breaker para falhas
- Fallback LocalAI
- Timeout handling

**Fluxo:**

```typescript
class AgentManager {
  private agentPath: string;
  private circuitBreaker: CircuitBreaker;
  private lastCheck: number = 0;
  
  async initialize(): Promise<void> {
    // 1. Try to find agent.py
    this.agentPath = await this.findAgentPython();
    
    if (!this.agentPath) {
      this.logger.warn("agent.py not found, using LocalAI fallback");
      return;
    }
    
    // 2. Validate with 'status' command (5s timeout)
    const valid = await this.validateAgent();
    if (!valid) {
      this.logger.error("agent.py validation failed");
    }
  }
  
  async suggest(payload: SuggestionPayload): Promise<SuggestionResult> {
    // 1. Check circuit breaker
    if (!this.circuitBreaker.isOpen()) {
      try {
        // 2. Call agent.py
        const result = await this.callAgent(payload);
        
        // 3. Reset on success
        this.circuitBreaker.recordSuccess();
        
        return result;
      } catch (error) {
        // 4. Record failure
        this.circuitBreaker.recordFailure();
        
        if (this.circuitBreaker.isOpen()) {
          this.logger.warn("Circuit breaker OPEN: using LocalAI");
        }
      }
    }
    
    // 5. Fallback to LocalAI
    return this.generateLocalSuggestion(payload);
  }
  
  private async callAgent(payload: SuggestionPayload): Promise<SuggestionResult> {
    const json = JSON.stringify(payload);
    
    // Execute: python3 agent.py inline "<JSON>"
    const promise = new Promise<SuggestionResult>((resolve, reject) => {
      const child = spawn('python3', [
        this.agentPath,
        'inline',
        json
      ]);
      
      // 2s timeout
      const timeout = setTimeout(() => {
        child.kill();
        reject(new Error('Timeout (2s)'));
      }, 2000);
      
      let stdout = '';
      let stderr = '';
      
      child.stdout.on('data', (data) => {
        stdout += data.toString();
      });
      
      child.stderr.on('data', (data) => {
        stderr += data.toString();
      });
      
      child.on('close', (code) => {
        clearTimeout(timeout);
        
        if (code === 0) {
          const result = JSON.parse(stdout);
          resolve(result);
        } else {
          reject(new Error(`Exit code ${code}: ${stderr}`));
        }
      });
      
      child.on('error', (error) => {
        clearTimeout(timeout);
        reject(error);
      });
    });
    
    return promise;
  }
  
  private generateLocalSuggestion(payload): SuggestionResult {
    // Fallback patterns by language
    const patterns = {
      python: [
        'pass',
        'return',
        'print()',
        'def ',
      ],
      typescript: [
        '}',
        'return;',
        'const ',
        'interface ',
      ],
      // ... more languages
    };
    
    const pattern = patterns[payload.language] || patterns.python;
    const suggestion = pattern[Math.floor(Math.random() * pattern.length)];
    
    return {
      suggestion,
      confidence: 0.5,  // Lower confidence for fallback
      source: 'localai',
      tokens_used: 0,
    };
  }
}
```

**Circuit Breaker Pattern:**

```
Normal state: call agent.py
  ↓
3 consecutive failures
  ↓
OPEN state: use LocalAI for 5 minutes
  ↓
5 minutes pass
  ↓
Half-OPEN: try agent.py again
  ↓
Success → Normal, Failure → OPEN again
```

---

### 4️⃣ tokenCache.ts (Semantic Caching)

**Responsabilidades:**
- In-memory semantic cache (Map)
- Disk persistence (JSON file)
- Jaccard similarity algorithm
- LRU + frequency pruning
- Stats tracking

**Fluxo:**

```typescript
class TokenCache {
  private cache: Map<string, CacheEntry> = new Map();
  private maxSize = 500;
  private similarityThreshold = 0.75;  // 75% match
  
  lookup(context: string): CacheEntry | null {
    // 1. Iterate all cached entries
    for (const [cached, entry] of this.cache) {
      // 2. Calculate Jaccard similarity
      const similarity = this.jaccard(context, cached);
      
      // 3. If 75%+ similar, return cached result
      if (similarity >= this.similarityThreshold) {
        entry.hits++;
        entry.lastUsed = Date.now();
        return entry;
      }
    }
    
    return null;
  }
  
  put(context: string, suggestion: string): void {
    if (this.cache.size >= this.maxSize) {
      // Prune bottom 20% by frequency
      this.prune();
    }
    
    this.cache.set(context, {
      suggestion,
      hits: 0,
      created: Date.now(),
      lastUsed: Date.now(),
      tokens: substring(suggestion).length / 4,
    });
    
    this.persist();
  }
  
  private jaccard(a: string, b: string): number {
    // Jaccard = intersection / union of words
    
    const setA = new Set(a.toLowerCase().split(/\s+/));
    const setB = new Set(b.toLowerCase().split(/\s+/));
    
    const intersection = new Set(
      [...setA].filter(x => setB.has(x))
    );
    
    const union = new Set([...setA, ...setB]);
    
    return intersection.size / union.size;
  }
  
  private prune(): void {
    // Sort by hits (frequency)
    const sorted = Array.from(this.cache.entries())
      .sort((a, b) => a[1].hits - b[1].hits);
    
    // Remove bottom 20%
    const toRemove = Math.ceil(this.maxSize * 0.2);
    for (let i = 0; i < toRemove; i++) {
      this.cache.delete(sorted[i][0]);
    }
  }
  
  private persist(): void {
    // Save to ~/.vscode/clawrafaelia-cache.json
    const json = JSON.stringify(
      Array.from(this.cache.entries()),
      null,
      2
    );
    
    fs.writeFileSync(this.cacheFile, json);
  }
}
```

**Why Jaccard?**

```
Exemplo:
Context A: "def hello():\n    print"
Context B: "def hello():\n    print()"

Words in A: {def, hello, print}
Words in B: {def, hello, print}

Intersection: 3, Union: 3
Jaccard = 3/3 = 100% (CACHE HIT!)

Exemplo 2:
Context A: "def foo(): return"
Context B: "class Bar: pass"

Words in A: {def, foo, return}
Words in B: {class, Bar, pass}

Intersection: 0, Union: 6
Jaccard = 0/6 = 0% (NO HIT)
```

---

### 5️⃣ logger.ts (Structured Logging)

**Responsabilidades:**
- Console + file output
- Configurable log levels
- Timestamp formatting
- Performance measurements

```typescript
class Logger {
  private logLevel: 'off' | 'error' | 'warn' | 'info' | 'debug';
  private logFile: string;
  
  constructor(level: string) {
    this.logLevel = level;
    this.logFile = path.join(os.homedir(), '.claw', 'logs', `vscode-${formatDate()}.log`);
    mkdirSync(path.dirname(this.logFile), { recursive: true });
  }
  
  error(msg: string, error?: Error): void {
    if (this.logLevel === 'off') return;
    
    const timestamp = this.getTimestamp();
    const line = `[${timestamp}] ERROR: ${msg}`;
    
    console.error(line);
    appendFileSync(this.logFile, line + '\n');
    
    if (error) {
      appendFileSync(this.logFile, error.stack + '\n');
    }
  }
  
  warn(msg: string): void {
    if (['off', 'error'].includes(this.logLevel)) return;
    
    const timestamp = this.getTimestamp();
    const line = `[${timestamp}] WARN: ${msg}`;
    
    console.warn(line);
    appendFileSync(this.logFile, line + '\n');
  }
  
  info(msg: string): void {
    if (['off', 'error', 'warn'].includes(this.logLevel)) return;
    
    const timestamp = this.getTimestamp();
    const line = `[${timestamp}] INFO: ${msg}`;
    
    console.log(line);
    appendFileSync(this.logFile, line + '\n');
  }
  
  debug(msg: string): void {
    if (this.logLevel !== 'debug') return;
    
    const timestamp = this.getTimestamp();
    const line = `[${timestamp}] DEBUG: ${msg}`;
    
    console.log(line);
    appendFileSync(this.logFile, line + '\n');
  }
}
```

---

## 🔄 Data Flow

### Happy Path (Cache Hit)

```
1. User types "def hello" → pause
2. 500ms debounce fires
3. inlineProvider.provideInlineCompletionItems()
4. Collect context: "def hello"
5. Check tokenCache.lookup("def hello")
6. Cache finds similar entry "def hel" (Jaccard: 0.8 > 0.75)
7. Return cached suggestion: "print('hi')"
8. Render gray text in editor
9. User presses Tab
10. Suggestion inserted

RESULT: ZERO API calls, instant response
```

### API Path (Cache Miss + Success)

```
1. User types new code → pause
2. 500ms debounce fires
3. Check tokenCache: NO HIT
4. agentManager.suggest() called
5. spawn('python3', ['agent.py', 'inline', JSON])
6. agent.py analyzes context + language
7. Returns: {"suggestion": "print(...)", "tokens": 45}
8. agentManager caches result
9. Render suggestion
10. User accepts

RESULT: 1 API call, cache entry for next time
```

### Error Path (Timeout + Fallback)

```
1. User types → pause
2. Check cache: NO HIT
3. Call agent.py
4. 2s timeout elapses (API down?)
5. subprocess.kill() called
6. circuitBreaker.recordFailure()
7. After 3 failures: OPEN circuit
8. generateLocalSuggestion() called
9. Return LocalAI pattern: "pass" or "return"
10. Render with confidence: 0.5

RESULT: Graceful degradation, UX not interrupted
```

---

## 📊 Performance Characteristics

| Operation | Time | Notes |
|-----------|------|-------|
| Debounce | 500ms | User configurable |
| Cache lookup | <1ms | In-memory Map |
| Jaccard calc | ~2ms | O(n) words |
| subprocess spawn | ~50ms | Python startup |
| agent.py analyze | ~500ms | API call |
| **Total happy path** | ~502ms | 500 debounce + 2 cache |
| **Total API path** | ~720ms | 500 debounce + 50 spawn + 500 API |
| **Total error path** | 2,050ms | 500 debounce + 2000 timeout |

---

## 🔌 Extension Lifecycle

### Activation

```typescript
1. VS Code loads vscode-extension/dist/extension.js
2. activation event: ["onLanguage:python", ...]
3. activate(context) called
4. Logger, TokenCache, AgentManager created
5. InlineCompletionProvider registered
6. Commands registered
7. Status bar created
8. Ready for inline suggestions
```

### deactivate()

```typescript
1. User uninstalls extension OR restarts VS Code
2. deactivate() called (clean up)
3. Timers cleared
4. Child processes killed (if any)
5. Cache persisted to disk
6. Logs flushed
```

---

## 🔐 Security Considerations

| Threat | Mitigation |
|--------|-----------|
| Code injection via agent.py args | JSON serialization (no shell) |
| DoS via large context | Trim to last 10 lines max |
| Secrets in context | User responsible (don't paste tokens) |
| Privilege escalation | No sudo/elevation required |
| Network sniffing | HTTPS only (configured in agent.py) |

---

## 📈 Scalability

- **Single editor session:** 1 extension instance per window
- **Multiple editors:** Each window has own cache
- **Multiple users:** Cache isolated by globalStoragePath
- **Cache size:** 500 entries max (~10MB estimated)
- **Log rotation:** Manual management (user deletes old logs)

---

## 🧪 Testing Architecture

```
Tests would cover:

✓ Debounce timer fires at correct interval
✓ Jaccard similarity algorithm accuracy
✓ Cache eviction (LRU + frequency)
✓ Circuit breaker state machine
✓ JSON (de)serialization
✓ agent.py subprocess communication
✓ LocalAI fallback generation
✓ Config change listener
✓ Log level filtering
```

---

## 📚 Key Design Patterns

| Pattern | Usage | File |
|---------|-------|------|
| **Provider** | InlineCompletionItemProvider interface | inlineCompletionProvider.ts |
| **Circuit Breaker** | Fail-safe for API calls | agentManager.ts |
| **Adapter** | LocalAI fallback | agentManager.ts |
| **Observer** | Config change listener | extension.ts |
| **Strategy** | Similarity algorithms | tokenCache.ts |
| **Singleton** | Logger instance | logger.ts |

---

## 🎯 Design Decisions Rationale

### Why Debounce 500ms?
- 300ms: Too aggressiv (many concurrent requests)
- 500ms: Perfect balance (user feels typing pace)
- 1000ms: Too lazy (feels unresponsive)

### Why Jaccard not regex?
- Jaccard: Language-agnostic, works for any code
- Regex: Requires manual rules for each language

### Why 2s subprocess timeout?
- <1s: Kills legitimate slow responses
- 2s: Acceptable latency, user won't retry
- >5s: Editor feels frozen (bad UX)

### Why circuit breaker?
- Prevents cascading failures
- Automatic recovery (half-open retry)
- Metrics collection (5min stats)

### Why LocalAI fallback?
- Extension stays useful offline
- No wait for API recovery
- Graceful degradation

---

**For implementation details, see source code in `src/` directory.**
