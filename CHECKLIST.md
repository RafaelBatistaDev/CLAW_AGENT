# ✅ CLAW Extension — Complete Checklist

Status final de implementação e próximos passos.

---

## 🎯 Phase 1: Agent Consolidation (COMPLETED ✅)

- [x] Analisar 113 referências a agent.sh em todo projeto
- [x] Remover duplicatas em scripts de geração de bashrc
- [x] Atualizar 17 .md files com consolidação
- [x] Validar agent.py com `agent status`
- [x] Validar agent.py com `agent analyze`
- [x] Criar ComeçarPCNovo.py professional setup guide
- [x] Remover bashrc aliases duplicados

**Status:** ✅ 100% Completo

---

## 🎯 Phase 2: VS Code Extension Development (IN PROGRESS 🟨)

### 2.1: Core Extension Files ✅

- [x] Estrutura de pasta vscode-extension/
- [x] package.json (172L, manifest completo)
- [x] extension.ts (195L, entry point)
- [x] inlineCompletionProvider.ts (155L, core logic)
- [x] agentManager.ts (320L, subprocess + fallback)
- [x] tokenCache.ts (235L, semantic cache)
- [x] logger.ts (65L, logging system)
- [x] tsconfig.json (strict TypeScript)
- [x] webpack.config.js (bundle config)
- [x] .eslintrc.json (linter rules)
- [x] .gitignore (VCS config)

**Status:** ✅ 100% Completo

### 2.2: Setup & Installation Scripts ✅

- [x] setup.sh (Bash script para Linux/macOS)
- [x] setup.bat (Batch script para Windows)
- [x] setup.ps1 (PowerShell script para Windows moderno)
- [x] install.py (Python script cross-platform)

**Status:** ✅ 100% Completo

### 2.3: Documentation ✅

- [x] README.md (350+ linhas, documentação técnica)
- [x] QUICK-START.md (guia de início rápido)
- [x] ARCHITECTURE.md (design deep-dive)
- [x] CONTRIBUTING.md (guidelines para contribuidores)
- [x] Este CHECKLIST.md

**Status:** ✅ 100% Completo

### 2.4: Build & Compilation 🟨

- [ ] **PENDENTE:** Primeiro `npm install` na pasta vscode-extension/
  - Responsabilidade: Usuário ou CI/CD
  - Comando: `cd vscode-extension && npm install`
  - Tempo estimado: 2-3 minutos

- [ ] **PENDENTE:** Compilar TypeScript para JavaScript
  - Responsabilidade: Usuário (via setup.sh/setup.bat) ou CI/CD
  - Comando: `npm run compile`
  - Resultado esperado: `dist/extension.js` criado
  - Tempo estimado: 30 segundos

- [ ] **PENDENTE:** Gerar .vsix para VS Code
  - Responsabilidade: Opcional (para release)
  - Comando: `npm run package`
  - Resultado esperado: `clawrafaelia-suggestions.vsix` criado

**Status:** 🟨 Pronto para execução (faltam apenas comandos)

### 2.5: agent.py Enhancement 🟨

- [ ] **PENDENTE:** Implementar comando `inline` em agent.py
  - Localização: `automation/my_scripts/agent.py` (linha ~1600+)
  - Função desejada:
    ```python
    def inline_suggest(context: str, language: str, fileName: str, max_tokens: int) -> dict:
        """
        Aceita JSON payload de VS Code
        Retorna: {"suggestion": "...", "confidence": 0.95, "source": "api", "tokens_used": 45}
        """
    ```
  - Integração: AgentManager chama `python3 agent.py inline <JSON>`
  - Responsabilidade: Claude ou usuario (simples adição)
  - Tempo estimado: 15-30 minutos

**Status:** 🟨 Design completo, implementação pendente

### 2.6: VS Code Integration Testing 🔴

- [ ] **PENDENTE:** npm install (gera node_modules/)
- [ ] **PENDENTE:** npm run compile (gera dist/)
- [ ] **PENDENTE:** Testar em VS Code (F5 debug)
  - Abrir novo VS Code window com extension loaded
  - Criar arquivo .py/.ts/.js
  - Digitar código
  - Verificar sugestões aparecerem em cinza
  - Testar Tab (aceita) e Esc (rejeita)
  
**Status:** 🔴 Bloqueado por npm install

### 2.7: Optional: Release & Marketplace 🔴

- [ ] **OPCIONAL:** Publicar no VS Code Marketplace
  - Requer: conta no Visual Studio marketplace
  - Comando: `npm run publish`
  - Benefício: Instalação 1-clique para usuários
  
- [ ] **OPCIONAL:** GitHub releases & tags
  - Criar tag: `git tag v1.0.0`
  - Push: `git push origin v1.0.0`
  - Criar release notes

**Status:** 🔴 Opcional (extensão funciona localmente)

---

## 📋 Detailed Task Breakdown

### **Task 1: npm install** (CRITICAL)

```bash
cd ~/OneDrive/ClawRafaelIA/vscode-extension
npm install
```

**What happens:**
- Downloads ~100 npm packages
- Installs to node_modules/ (170MB)
- Creates package-lock.json
- Validates versions

**Success criteria:**
- `ls node_modules/@types` shows TypeScript types
- No "404 not found" errors
- No "peer dependency" errors

**Time: 2-3 minutes**

---

### **Task 2: npm run compile** (CRITICAL)

```bash
npm run compile
```

**What happens:**
- TypeScript compiler reads src/*.ts
- Compiles to JavaScript in dist/
- Type checks entire codebase
- Validates for 23 error types (strict mode)

**Success criteria:**
- `ls dist/extension.js` exists
- No TypeScript errors
- No whitespace in output

**Time: 30 seconds**

---

### **Task 3: Add `inline` command to agent.py** (BLOCKING)

**Location:** `automation/my_scripts/agent.py` (end of file, add new function)

**Code pattern:**
```python
@cli.command(
    name="inline",
    help="Suggest next code inline for VS Code"
)
@click.argument("payload", type=click.STRING)
def inline_suggest(payload: str):
    """
    Receive JSON payload from VS Code:
    {
      "context": "def hello()\n    ",
      "language": "python",
      "fileName": "test.py",
      "maxTokens": 100
    }
    
    Return JSON:
    {
      "suggestion": "print('hello')",
      "confidence": 0.95,
      "source": "api",  // or "localai" if fallback
      "tokens_used": 23
    }
    """
    import json
    
    try:
        payload_dict = json.loads(payload)
        
        context = payload_dict["context"]
        language = payload_dict["language"]
        fileName = payload_dict.get("fileName", "unknown")
        maxTokens = payload_dict.get("maxTokens", 100)
        
        # Call Gemini API
        suggestion = client.generate_content(
            f"Given this {language} code:\n{context}\n\nSuggest the next line (be brief, one line only)",
            max_output_tokens=maxTokens
        ).text.strip()
        
        response = {
            "suggestion": suggestion,
            "confidence": 0.85,
            "source": "api",
            "tokens_used": len(suggestion.split()) * 4,  # Approximate
        }
        
        click.echo(json.dumps(response))
        
    except json.JSONDecodeError:
        click.echo(json.dumps({
            "suggestion": "pass",
            "confidence": 0.0,
            "source": "error",
            "tokens_used": 0,
        }))
        sys.exit(1)
    except Exception as e:
        click.echo(json.dumps({
            "suggestion": "# Error: " + str(e),
            "confidence": 0.0,
            "source": "error",
            "tokens_used": 0,
        }))
        sys.exit(1)
```

**Integration point:**
- AgentManager calls: `python3 agent.py inline <JSON>`
- Expects JSON response on stdout
- Exit code 0 = success, 1 = error

**Time: 20-30 minutes**

---

### **Task 4: Test in VS Code** (INTEGRATION)

**Prerequisites:**
- npm install ✅
- npm run compile ✅
- agent.py inline command ✅

**Steps:**

```bash
# 1. Open VS Code
cd ~/OneDrive/ClawRafaelIA/vscode-extension
code .

# 2. Press F5 to start debugging
# → Opens new VS Code window with extension loaded

# 3. Create test file
touch test.py

# 4. Type Python code
def hello():
    # pause here for 500ms...
    # should see suggestion in gray

# 5. Test interactions
# Tab to accept, Esc to reject

# 6. Check Output panel
# Ctrl+Shift+P → Output → CLAW Debug Log
```

**Success criteria:**
- Extension activates without errors
- Suggestions appear after 500ms pause
- Suggestions are presented in gray (ghost text)
- Tab accepts, Esc rejects
- Output panel shows debug logs

**Time: 5-10 minutes**

---

### **Task 5: Package for Release** (OPTIONAL)

```bash
npm run package
```

**What happens:**
- Bundles extension into .vsix file
- Minifies JavaScript
- Creates installable artifact

**Result:**
- `clawrafaelia-suggestions.vsix` (1-2MB)

**Install in VS Code:**
```bash
code --install-extension clawrafaelia-suggestions.vsix
```

**Time: 1 minute**

---

## 🎯 Priority Matrix

| Task | Depends On | Blocks | Priority | Est. Time |
|------|-----------|--------|----------|-----------|
| npm install | Node.js 16+ | compile | 🔴 CRITICAL | 2-3m |
| npm compile | npm install | testing | 🔴 CRITICAL | 30s |
| add inline cmd | agent.py | testing | 🔴 CRITICAL | 20-30m |
| Test in VS Code | compile+inline | quality | 🟠 HIGH | 5-10m |
| Package .vsix | compile | publish | 🟡 MEDIUM | 1m |
| Publish marketplace | .vsix | release | 🟢 LOW | varies |

---

## 📊 Completion Status

```
Phase 1 (Agent Consolidation):    ████████████████████ 100%  ✅ DONE
Phase 2 (Extension - Code):        ████████████████████ 100%  ✅ DONE
Phase 2 (Extension - Build):       ██████████░░░░░░░░░░  50%  🟨 NEEDED
Phase 2 (Extension - Testing):     ░░░░░░░░░░░░░░░░░░░░   0%  🔴 BLOCKED
Phase 2 (Extension - Publishing):  ░░░░░░░░░░░░░░░░░░░░   0%  🟢 OPTIONAL

OVERALL:                           ████████░░░░░░░░░░░░  40%  🟨 IN PROGRESS
```

---

## 🚀 Next Immediate Steps

### **For Claude (Agent):**

1. **Create script to add `inline` command**
   - File: `automation/my_scripts/agent.py`
   - Location: End of file, within Click CLI
   - Effort: 30 minutes
   - Request: Read agentManager.ts to understand JSON format

2. **Test agent.py changes**
   - Run: `agent inline <JSON>`
   - Expect: JSON response
   - Fallback: If no agent, create stub for testing

### **For User (Running locally):**

1. **Execute setup script** (choose one):
   ```bash
   bash ~/OneDrive/ClawRafaelIA/vscode-extension/setup.sh
   # OR
   python3 ~/OneDrive/ClawRafaelIA/vscode-extension/install.py
   # OR
   # Windows: Double-click setup.bat or setup.ps1
   ```

2. **Or manual build:**
   ```bash
   cd ~/OneDrive/ClawRafaelIA/vscode-extension
   npm install
   npm run compile
   ```

3. **Test in VS Code:**
   - F5 to debug
   - Create test file
   - Type code & pause
   - See suggestions

---

## 📞 Support & Troubleshooting

### **npm install fails**
```bash
# Solution 1: Clean cache
npm cache clean --force
npm install

# Solution 2: Update npm
npm install -g npm@latest
npm install
```

### **TypeScript compilation error**
```bash
# Check tsconfig
cat tsconfig.json | grep -A5 '"strict"'

# Recompile with verbose output
npx tsc --pretty --listFiles
```

### **Extension not showing suggestions**
- Check: `Ctrl+Shift+P` → `CLAW: Show Status`
- Enable debug: Settings → `clawrafaelia.logLevel` → `debug`
- Check logs: Output → `CLAW Debug Log`

### **agent.py not found**
- Verify path: `ls ~/OneDrive/ClawRafaelIA/automation/my_scripts/agent.py`
- Manual config: Settings → `clawrafaelia.agentPythonPath`
- Fallback: Works with LocalAI if agent not found

---

## 📚 Files to Reference

| File | Purpose | Size |
|------|---------|------|
| QUICK-START.md | Simple 3-min setup guide | 500L |
| ARCHITECTURE.md | Technical deep-dive | 800L |
| CONTRIBUTING.md | Developer guidelines | 600L |
| README.md | Full documentation | 850L |
| agentManager.ts | Understands JSON format | 320L |

---

## 🎓 Learning Checklist

Before attempting advanced tasks:

- [ ] Understand VS Code extension lifecycle (activation/deactivation)
- [ ] Know how InlineCompletionItemProvider works
- [ ] Familiar with subprocess communication (spawn, JSON, timeout)
- [ ] Know Jaccard similarity algorithm
- [ ] Understand circuit breaker pattern
- [ ] Comfortable with TypeScript types & strict mode

**Time to learn: 2-4 hours** (reading ARCHITECTURE.md + code inspection)

---

## 🎉 Final Checklist (for release)

- [ ] All tasks from Phase 2 complete
- [ ] npm install successful
- [ ] npm run compile successful
- [ ] agent.py inline command works
- [ ] VS Code testing successful
- [ ] Extension passes all tests
- [ ] Documentation updated
- [ ] CHANGELOG entry written
- [ ] Version bumped (package.json)
- [ ] .vsix generated
- [ ] Ready for marketplace submission

**Time to complete all: 3-4 hours** (once dependencies are known)

---

**Próximo Passo?** 

```bash
# Choose one:

# 1. Quick setup (recommended)
bash ~/OneDrive/ClawRafaelIA/vscode-extension/setup.sh

# 2. Manual setup
cd ~/OneDrive/ClawRafaelIA/vscode-extension
npm install && npm run compile

# 3. Or request Claude to add inline command to agent.py
```

🚀 **You're in Phase 2C of development. Almost there!**
