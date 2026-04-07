# 🚀 CLAW VS Code Extension — Quick Start (v1.1.3)

Comece a usar a extensão em **menos de 3 minutos**! 

**NEW v1.1.0:** Auto-detecção de IAs! Funciona com Gemini, OpenAI, Claude, LocalAI e Ollama 🎉

## 0️⃣ Antes de Começar — Escolha Uma IA (ou skip para fallback)

### Opção A: Usar Google Gemini (⭐ Recomendado)

```bash
# Verificar se agent.py está pronto
python3 ~/OneDrive/ClawRafaelIA/automation/my_scripts/agent.py status

# Deve retornar: ✅ Google Gemini: Configurada
```

### Opção B: Usar OpenAI ChatGPT

```bash
# Adicionar a chave ao shell
export OPENAI_API_KEY="sk-your-key-here"

# Ou adicionar ao arquivo ~/.claw/config/.claude.json
{
    "OPENAI_API_KEY": "sk-your-key-here"
}
```

### Opção C: Usar Anthropic Claude

```bash
# Adicionar a chave ao shell
export ANTHROPIC_API_KEY="sk-ant-your-key-here"

# Ou em ~/.claw/config/.claude.json
{
    "ANTHROPIC_API_KEY": "sk-ant-your-key-here"
}
```

### Opção D: Usar LocalAI/Ollama (GRÁTIS + Offline!)

```bash
# Em um terminal separado, rodar:
ollama run mistral:7b

# Extension detecta automaticamente em localhost:11434 ✅
```

### Opção E: Sem IA (Fallback local)

```bash
# Nenhuma IA configurada?
# Tudo bem! Extension usa patterns + templates
# Gratuito, rápido, sem dependências ✅
```

---

## ⚡ Quick Start (Escolha o seu Sistema)

### 🐧 Linux / macOS — Bash

```bash
cd ~/OneDrive/ClawRafaelIA/vscode-extension
bash setup.sh
```

**Opções:**
```bash
bash setup.sh --dev       # Modo desenvolvimento (watch files)
bash setup.sh --package   # Empacotar para release
```

---

### 🪟 Windows — Batch

Duplo clique em `setup.bat` OR:

```cmd
cd %USERPROFILE%\OneDrive\ClawRafaelIA\vscode-extension
setup.bat
```

**Opções:**
```cmd
setup.bat --dev       # Modo desenvolvimento
setup.bat --package   # Empacotar para release
```

---

### 🪟 Windows — PowerShell (Moderno)

```powershell
cd $env:USERPROFILE\OneDrive\ClawRafaelIA\vscode-extension
.\setup.ps1
```

**Opções:**
```powershell
.\setup.ps1 -Mode "dev"       # Modo desenvolvimento
.\setup.ps1 -Mode "package"   # Empacotar para release
```

---

### 🐍 Qualquer Sistema — Python

```bash
python3 ~/OneDrive/ClawRafaelIA/vscode-extension/install.py
```

Esta opção é **mais robusta** pois:
- ✅ Funciona em Linux, macOS e Windows
- ✅ Detecta automaticamente VS Code e Node.js
- ✅ Valida compatibilidade antes de instalar
- ✅ Dá feedback detalhado de cada etapa

---

## ✨ O que Cada Script Faz

| Script | SO | Função |
|--------|----|----|
| `setup.sh` | Linux/macOS | Setup rápido com bash |
| `setup.bat` | Windows | Setup rápido com batch |
| `setup.ps1` | Windows | Setup moderno com PowerShell |
| `install.py` | Todos | Setup robusto e portável |

---

## 📋 Requisitos

Antes de rodar qualquer script, você precisa ter:

- **Node.js 16+** → [Baixar](https://nodejs.org)
- **npm 8+** → Vem com Node.js
- **VS Code** → [Baixar](https://code.visualstudio.com) (opcional, pode instalar depois)

### Verificar Requisitos

```bash
# Linux/macOS/PowerShell
node --version    # Should be v16+
npm --version     # Should be 8+
code --version    # VS Code (opcional)

# Windows Batch
node --version
npm --version
```

---

## 🎯 Passo a Passo (Modo Manual)

Se preferir fazer tudo manualmente:

```bash
# 1. Entrar na pasta
cd ~/OneDrive/ClawRafaelIA/vscode-extension

# 2. Instalar dependências
npm install

# 3. Compilar TypeScript
npm run compile

# 4. Empacotar
npm run package

# 5. Instalar no VS Code
code --install-extension clawrafaelia-suggestions.vsix
```

---

## 🚀 Depois de Instalar

### 1️⃣ Início da Extensão

Quando você abrir **qualquer arquivo** (`.py`, `.ts`, `.js`, `.cs`, etc.):

1. Pare de digitar por **500ms** (padrão)
2. A extensão coleta o contexto
3. Sugestões aparecem em **cinza** (fantasmas)
4. Pressione `Tab` para aceitar, `Esc` para rejeitar

### 2️⃣ Ativar/Desativar

**Paleta de Comandos:** `Ctrl+Shift+P`

Procure por:
- `CLAW: Toggle suggestions` — Liga/desliga
- `CLAW: Clear cache` — Limpar cache
- `CLAW: Show status` — Ver status

**Atalho rápido:** `Ctrl+Alt+C` (toggle)

### 3️⃣ Configurar

**Abrir Settings:** `Ctrl+,`

Procure por `clawrafaelia`:

```json
{
  "clawrafaelia.enabled": true,
  "clawrafaelia.debounceMs": 500,           // Aguardar 500ms
  "clawrafaelia.maxTokens": 100,            // Max tokens por sugestão
  "clawrafaelia.enableLocalAI": true,       // Fallback local
  "clawrafaelia.logLevel": "warn",          // off, error, warn, info, debug
  "clawrafaelia.agentPythonPath": "/home/user/OneDrive/ClawRafaelIA/automation/my_scripts/agent.py"
}
```

---

## 🔧 Desenvolvimento

### Modo Watch (Auto-compile)

```bash
npm run dev
# OU
bash setup.sh --dev
```

Qualquer mudança em `src/` é compilada automaticamente.

### Build Production

```bash
npm run compile:prod
```

Minifica e otimiza para release.

### Testes (Quando disponíveis)

```bash
npm test
```

---

## 🔌 Troubleshooting

### ❌ "command not found: npm"

**Solução:** Instale Node.js em https://nodejs.org

### ❌ "VS Code not found"

**Solução:** Instale VS Code em https://code.visualstudio.com OR execute:
```bash
code --install-extension clawrafaelia-suggestions.vsix
```

### ❌ Extensão não aparece sugestões

**Teste rápido:**
1. Abrir `Ctrl+Shift+P`
2. Digitar `CLAW: Show status`
3. Ver log detalhado no painel **Output**

**Debug:** 
```json
// settings.json
"clawrafaelia.logLevel": "debug"
```

Veja em **Output → CLAW Debug Log**

### ❌ "Timed out connecting to agent.py"

**Cause:** agent.py não encontrado

**Solução:** 
1. Verificar se `agent.py` existe:
   ```bash
   ls ~/OneDrive/ClawRafaelIA/automation/my_scripts/agent.py
   ```
2. Configure manualmente:
   ```json
   // settings.json
   "clawrafaelia.agentPythonPath": "/caminho/para/agent.py"
   ```
3. A extensão funcionará com **fallback local** (sugestões menos inteligentes)

---

## 📊 Performance

### Cache Semântico

A extensão usa **cache semântico** com algoritmo Jaccard:

- Se uma sugestão é 75%+ similar a uma já solicitada
- **ZERO chamadas à API** (sugestão vem do cache)
- **~80% das sugestões vêm do cache**

### Debounce

- **Padrão:** 500ms após parar de digitar
- **Ajustável:** `clawrafaelia.debounceMs`
- **Mais rápido:** 300ms (mais requisições, mais consumo)
- **Mais lento:** 1000ms (menos requisições, mais latência)

### Token Limit

- **Padrão:** 100 tokens por sugestão
- **Aumentar:** Sugestões mais longas, mais consumo
- **Diminuir:** Sugestões mais curtas, mais rápidas

---

## 📚 Documentação Completa

Para detalhes técnicos avançados, veja:

- [README.md](./README.md) — Documentação técnica completa
- [package.json](./package.json) — Configurações e scripts
- [src/](./src/) — Código-fonte TypeScript

---

## 💡 Dicas e Truques

### 1️⃣ Modo Offline

Se a API falhar (circuit breaker acionado), a extensão automaticamente:
- ✅ Funciona com sugestões **LocalAI** (fallback)
- ✅ Segue gerando sugestões
- ✅ Tenta reconectar a cada 5 minutos

### 2️⃣ Limpar Cache

Se as sugestões não melhoram:

```
Ctrl+Shift+P → CLAW: Clear cache
```

### 3️⃣ Ver Status

```
Ctrl+Shift+P → CLAW: Show status
```

Mostra:
- Se está online/offline
- Quantos hits de cache
- Últimas sugestões
- Tempo de resposta

### 4️⃣ Multi-idioma

Automático para:

```
Python, TypeScript, JavaScript, C#, Rust, 
Go, Ruby, PHP, Java, C++, JSX/TSX
```

### 5️⃣ Configuração por Workspace

Crie `.vscode/settings.json` na raiz do seu projeto:

```json
{
  "clawrafaelia.enabled": true,
  "clawrafaelia.debounceMs": 300,      // Mais rápido neste projeto
  "clawrafaelia.maxTokens": 150
}
```

---

## 🎓 Exemplos

### Python

```python
def hello():  # ← parando aqui por 500ms...
    # ✨ Sugestão aparece: print("Hello, World!")
```

### TypeScript

```typescript
interface User {
  name: string;
  // ✨ Sugestão: email: string;
}
```

### C#

```csharp
public class Program
{
    // ✨ Sugestão: public static void Main() { }
}
```

---

## 🚀 Próxima Etapa

Depois que a extensão estiver instalada, leia:
- [CONTRIBUTING.md](./CONTRIBUTING.md) — Para desenvolver
- [ARCHITECTURE.md](./ARCHITECTURE.md) — Para entender internals

---

## 📞 Suporte

### Problemas?

1. Verifique output: `Ctrl+Shift+P` → `Python: Show Logs`
2. Amente log level: `"clawrafaelia.logLevel": "debug"`
3. Reporte issue com log completo

### Quer contribuir?

```bash
npm run dev              # Modo desenvolvimento
npm test                 # Rodar testes
npm run lint             # Verificar estilo
```

---

**Pronto para começar?** 🚀

```bash
bash setup.sh    # Linux/macOS
# OU
setup.bat        # Windows
# OU
python3 install.py    # Qualquer sistema
```

Boa sorte! 🎉
