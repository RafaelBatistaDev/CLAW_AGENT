# 🔧 TROUBLESHOOTING — Guia de Diagnóstico CLAW v1.1.3

Guia completo para diagnosticar e corrigir problemas.

---

## 🎯 Quick Diagnostic

### Passo 1: Verificar Status Básico

```bash
# Abra VS Code e execute:
Ctrl+Shift+P → "CLAW: Status"
```

**Você deve ver algo como:**
```
✅ CLAW Extension Status
├─ Enabled: true
├─ Detected AI: Gemini
├─ Cache Hit Rate: 62%
├─ Last Suggestion: 500ms ago (cache)
├─ Available IAs:
│  ├─ Gemini ✅
│  ├─ OpenAI ❌ (OPENAI_API_KEY not found)
│  ├─ LocalAI ❌ (localhost:8000 not responding)
│  └─ Ollama ❌
└─ Status: Healthy 🟢
```

---

### Passo 2: Ativar Debug Mode

```json
// .vscode/settings.json (workspace ou user)
{
  "clawrafaelia.logLevel": "debug",
  "clawrafaelia.showInlineMessage": true
}
```

Então:
```
Ctrl+Shift+P → "Output"
Selecione → "CLAW" (dropdown)
Veja logs em tempo real
```

---

### Passo 3: Verificar Logs

```bash
# Linux/Mac
tail -f ~/.claw/logs/*.log

# Windows
type %USERPROFILE%\.claw\logs\claw.log
```

---

## 🚨 Problemas Comuns & Soluções

### ❌ Problema 1: "Sugestões não aparecem"

**Sintoma:** Digito código, mas nada aparece.

**Diagnóstico:**

```
1️⃣ Extensão está ativada?
   Status → "enabled: true" ✅

2️⃣ Linguagem é suportada?
   Status → Procure sua linguagem em "Supported Languages"
   
   Se não:
   └─ Suportadas: Python, TS, JS, C#, Rust, Go, SQL, Markdown
   
3️⃣ Uma IA foi detectada?
   Status → "detected AI: XXX" ✅
   
   Se não:
   └─ IR PARA SOLUÇÃO: "Nenhuma IA detectada"

4️⃣ Debounce é muito alto?
   Tentar: "clawrafaelia.debounceMs": 300
```

**Solução rápida:**

```json
{
  "clawrafaelia.enabled": true,
  "clawrafaelia.debounceMs": 300,
  "clawrafaelia.logLevel": "debug"
}
```

Depois:
```
1. Salvar settings
2. Ctrl+Shift+P → "Developer: Reload Window"
3. Output → "CLAW"
4. Digitar novamente
5. Ver logs
```

---

### ❌ Problema 2: "Nenhuma IA detectada"

**Sintoma:** Status mostra `detected: None` ou `Available IAs: []`

**Diagnóstico:**

```bash
# Verificar cada IA:

1. Gemini (via agent.py)
   $ agent status
   Se erro: Instalar CLAW agent (https://github.com/RafaelBatista/ClawRafaelIA)

2. OpenAI
   $ echo $OPENAI_API_KEY
   Se vazio: export OPENAI_API_KEY="sk-proj-..."
   Depois: Reload Window no VS Code

3. LocalAI
   $ curl http://localhost:8000
   Se erro: docker run -p 8000:8000 localai/localai:latest

4. Ollama
   $ curl http://localhost:11434
   Se erro: https://ollama.ai (download e instale)
```

**Solução:**

```bash
# Opção A: Instalar Gemini agent
cd ~/OneDrive/ClawRafaelIA
bash ACTIVATE.sh

# Opção B: Configurar OpenAI
export OPENAI_API_KEY="sk-proj-xxxxx"
source ~/.bashrc  # Recarregar

# Opção C: Rodar LocalAI via Docker
docker run -p 8000:8000 localai/localai:latest gemma:7b

# Opção D: Procurar em todo lugar
# Restart VS Code Completamente (não apenas "Reload Window"):
# Ctrl+Shift+Q para sair
# Reabrir VS Code
```

---

### ❌ Problema 3: "API Key não encontrada"

**Sintoma:** Logs mostram: `Error: API Key not found for OpenAI`

**Diagnóstico:**

```bash
# Verificar se variável está exportada
echo $OPENAI_API_KEY
# Se vazio: ❌ Erro confirmado

# Verificar ~/.bashrc
grep OPENAI_API_KEY ~/.bashrc
# Se não encontra: ❌ Export não permanente
```

**Solução:**

```bash
# Passo 1: Adicionar à ~/.bashrc (permanente)
echo 'export OPENAI_API_KEY="sk-proj-xxxxx"' >> ~/.bashrc

# Passo 2: Recarregar shell
source ~/.bashrc

# Passo 3: Verificar
echo $OPENAI_API_KEY
# Deve mostrar: sk-proj-xxxxx ✅

# Passo 4: Restart VS Code (não apenas Reload)
# Sair: Ctrl+Shift+Q
# Reabrir VS Code
```

**Alternativa (arquivo config):**

```bash
# ~/.claw/config/.claude.json
mkdir -p ~/.claw/config

cat > ~/.claw/config/.claude.json << 'EOF'
{
  "OPENAI_API_KEY": "sk-proj-xxxxx",
  "ANTHROPIC_API_KEY": "sk-ant-yyyyy"
}
EOF

chmod 600 ~/.claw/config/.claude.json
```

---

### ❌ Problema 4: "Sugestões aparecem muito devagar"

**Sintoma:** Sugestão demora 3-5s para aparecer

**Diagnóstico:**

```
Verificar logs:
├─ Last suggestion took: XXms
└─ Source: cache/gemini/openai/pattern/template

Se time > 2000ms:
├─ Verificar latência de rede
├─ Verificar carga CPU
└─ Verificar se IA está overloaded
```

**Soluções (ordem de efetividade):**

```json
{
  // 1. Aumentar timeout (permite mais tempo)
  "clawrafaelia.aiTimeout": 3000,
  
  // 2. Usar LocalAI (mais rápido)
  "clawrafaelia.preferredAI": "localai",
  
  // 3. Reduzir tokens (menos processamento)
  "clawrafaelia.maxTokens": 30,
  
  // 4. Aumentar debounce (menos chamadas)
  "clawrafaelia.debounceMs": 1000,
  
  // 5. Desativar algumas linguagens
  "clawrafaelia.languages": {
    "python": true,
    "typescript": true,
    "xml": false,  // desativar linguagens não usadas
    "html": false
  }
}
```

**Se ainda lento:**
```bash
# Diagnosticar internet
ping google.com
# Se timeouts: problema de conexão ❌

# Diagnosticar IA
curl -v http://api.google.com  # Gemini
curl -v https://api.openai.com  # OpenAI

# Diagnosticar máquina
htop  # Ver CPU/RAM
free -h  # Ver memória
```

---

### ❌ Problema 5: "Circuit breaker ativado"

**Sintoma:** Logs mostram: `Circuit breaker active: IA blacklisted for 5 min`

**Causa:** Uma IA falhou 5 vezes consecutivas

**Solução:**

```
Este é um COMPORTAMENTO CORRETO:
├─ CLAW detectou que IA está com problemas
├─ Pula automaticamente para próxima
└─ Tenta novamente após 5 minutos

Ações recomendadas:
1. Verificar status da IA
   - Gemini: agent status
   - OpenAI: curl https://status.openai.com
   - LocalAI: curl http://localhost:8000
   
2. Aumentar aiTimeout (IA pode estar lenta)
   "clawrafaelia.aiTimeout": 4000  // De 2000
   
3. Trocar IA preferida
   "clawrafaelia.preferredAI": "openai"  // Trocar
```

---

### ❌ Problema 6: "Cache muito grande (muito RAM)"

**Sintoma:** VS Code usando 300MB+ RAM

**Diagnóstico:**

```bash
# Checar tamanho do cache
ls -lh ~/.claw/cache/
# Se > 100MB: Cache está grande demais
```

**Solução:**

```json
{
  "clawrafaelia.cacheMaxEntries": 100,  // De 500 → 100
  "clawrafaelia.cacheSimilarityThreshold": 0.9  // Reusar menos
}
```

Depois:
```bash
# Limpar cache antigo
rm ~/.claw/cache/claw-suggestions-cache.json

# Reiniciar VS Code
```

---

### ❌ Problema 7: "LocalAI/Ollama não detectado"

**Sintoma:** Status mostra `LocalAI: ❌` mesmo com Ollama rodando

**Diagnóstico:**

```bash
# Verificar se Ollama está rodando
curl http://localhost:11434 -v
# Esperado: 200 OK, resposta JSON

# Verificar porta
lsof -i :11434
# Deve mostrar: ollama

# Verificar firewall
sudo ufw status  # Ubuntu
sudo firewall-cmd --list-all  # CentOS
```

**Solução:**

```bash
# Opção 1: Verificar se Ollama está rodando
ollama serve  # Deve aparecer "Listening on localhost:11434"

# Opção 2: Usar docker
docker run -p 11434:11434 ollama/ollama:latest ollama serve

# Opção 3: Configurar endpoint manualmente
# .vscode/settings.json:
{
  "clawrafaelia.ollamaEndpoint": "http://localhost:11434",
  "clawrafaelia.enableLocalAI": true
}

# Opção 4: Reiniciar VS Code completamente
# Não apenas "Reload Window", mas:
# Ctrl+Shift+Q (sair)
# Reabrir VS Code
```

---

## 🔍 Diagnóstico Avançado

### Verificar Detecção de IAs (Startup)

```
Ao abrir VS Code, CLAW faz:

1️⃣ Probe Gemini (3s timeout)
   └─ Executa: agent status
   └─ Esperado: exit code 0

2️⃣ Probe OpenAI (2s timeout)
   └─ HTTP GET: https://api.openai.com/v1/models
   └─ Header: Authorization: Bearer $OPENAI_API_KEY
   └─ Esperado: 200 OK

3️⃣ Probe Claude (2s timeout)
   └─ HTTP POST: https://api.anthropic.com/v1/messages
   └─ Header: x-api-key: $ANTHROPIC_API_KEY
   └─ Esperado: 200 OK

4️⃣ Probe LocalAI (1s timeout)
   └─ HTTP GET: http://localhost:8000/config
   └─ Esperado: 200 OK

5️⃣ Probe Ollama (1s timeout)
   └─ HTTP GET: http://localhost:11434/api/tags
   └─ Esperado: 200 OK, JSON com {"models": [...]}
```

**Ver probes em debug:**

```
Ctrl+Shift+P → Output → CLAW

Procure por:
[INFO] Probing IAs...
[DEBUG] Probing Gemini... timeout: 3000ms
[DEBUG] Probing OpenAI... timeout: 2000ms
...
[INFO] IAs detected: [Gemini, OpenAI]
[INFO] Selected AI: Gemini (priority 1)
```

---

### Coletar Logs para Report de Bug

```bash
# 1. Ativar debug mode em settings
"clawrafaelia.logLevel": "debug"

# 2. Reproduzir problema
# (digitar algo, esperar sugestão, etc)

# 3. Coletar logs
mkdir ~/claw-debug

# Linux/Mac
cp -r ~/.claw/logs/* ~/claw-debug/
cp ~/.claw/cache/claw-suggestions-cache.json ~/claw-debug/

# Windows
xcopy "%USERPROFILE%\.claw\logs" "%USERPROFILE%\claw-debug\*"

# 4. Coletar VS Code logs
cp -r ~/.config/Code/logs ~/claw-debug/  # Linux
cp -r ~/Library/Application\ Support/Code/logs ~/claw-debug/  # Mac
xcopy "%APPDATA%\Code\logs" "%USERPROFILE%\claw-debug\*"  # Windows

# 5. Criar tar
tar -czf ~/claw-debug.tar.gz ~/claw-debug/

# 6. Reportar em GitHub Issues como anexo
```

---

## 🧪 Testes de Diagnóstico

### Teste 1: Verificar Conectividade de API

```bash
# Gemini
agent status  # Deve responder com info

# OpenAI
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models | jq
# Deve listar modelos

# Claude
curl -X POST https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"claude-3-haiku","max_tokens":10,"messages":[{"role":"user","content":"hi"}]}' | jq
# Deve responder com message
```

---

### Teste 2: Verificar Cache Local

```bash
# Ver estrutura do cache
cat ~/.claw/cache/claw-suggestions-cache.json | jq '.' | head -100

# Contar entradas
jq '.entries | length' ~/.claw/cache/claw-suggestions-cache.json

# Ver maior entrada
jq '.entries | sort_by(.size) | .[-1]' ~/.claw/cache/claw-suggestions-cache.json
```

---

### Teste 3: Verificar Pattern Matching

```
Teste manual em Python:

Criar arquivo: test.py
Digitar:
  def hello(name
  
Aguardar 500ms (debounce)

Verificar:
  - Sugestão em cinza deve aparecer: ):\n    pass
  - Se não IA respondeu: checou Pattern
  - Se sim, mas errada: IA retornou algo
```

---

## 📋 Checklist para Report de Bug

Ao reportar bug em GitHub, forneça:

```
[ ] Versão CLAW (Ctrl+Shift+P → About)
    └─ Version: 1.1.3

[ ] VS Code version
    └─ File → About Visual Studio Code

[ ] Sistema operacional
    └─ Windows 10/11, macOS, Linux (qual distro?)

[ ] Arquitetura
    └─ x86_64, ARM64, etc

[ ] Linguagem de programação testada
    └─ Python, TypeScript, etc

[ ] IAs configuradas
    └─ Gemini, OpenAI, Claude, LocalAI, Ollama, ou nenhuma

[ ] Passos para reproduzir (numerados)
    Exemplo:
    1. Criar arquivo test.py
    2. Digitar "def hello("
    3. Esperar 500ms
    4. Observar: nada aparece
    5. Check logs

[ ] Comportamento esperado
    └─ Sugestão deve aparecer em 1s

[ ] Comportamento atual
    └─ Nada aparece

[ ] Logs do CLAW
    └─ tail -f ~/.claw/logs/*.log
    └─ ou Output panel no VS Code

[ ] Última versão testada
    └─ Já testei v1.1.2?

[ ] Screenshots (se aplicável)
    └─ Selecionar, editar, anexar
```

---

## 🆘 Escalation

Se nada funcionar:

```bash
# 1. Limpar cache
rm -rf ~/.claw/cache/*
rm -rf ~/.claw/logs/*

# 2. Desinstalar + reinstalar
code --uninstall-extension RafaelBatista.claw-rafaelia
code --install-extension claw-rafaelia-1.1.3.vsix

# 3. Reset VS Code
# Opção A: Hard reset (Linux)
rm -rf ~/.config/Code/User/workspaceStorage/*/GitHub.copilot-chat

# Opção B: Limpar tudo (mais drástico)
rm -rf ~/.config/Code
# (Vai perder todas extensões, reinstalar)

# 4. Reportar em GitHub
# https://github.com/RafaelBatista/ClawRafaelIA/issues
# Cole logs acima completos
```

---

**Versão:** 1.1.3  
**Data:** 6 de Abril de 2026  
**Próxima revisão:** v1.2.0
