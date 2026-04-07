# ❓ FAQ — Perguntas Frequentes CLAW v1.1.3

---

## 📦 Instalação & Setup

### P: Como instalo CLAW?

**R:** Três opções:

```bash
# Opção 1: VS Code Marketplace (quando publicado)
Ctrl+Shift+X → Procure "CLAW" → Instale

# Opção 2: Build local
git clone https://github.com/RafaelBatista/ClawRafaelIA.git
cd vscode-extension
npm install
npm run compile
npm run package
code --install-extension claw-rafaelia-1.1.3.vsix

# Opção 3: Clone + Debug
git clone ... && npm install && npm run dev
# Abre VS Code dev window
```

---

### P: Qual é o tamanho do download?

**R:** ~2 MB após publicado no Marketplace

---

### P: CLAW funciona no Windows/Mac?

**R:** **Sim**, 100% suportado:
- ✅ Windows 10+ (build 19041+)
- ✅ macOS 10.12+
- ✅ Linux (Fedora, Ubuntu, etc)

---

### P: Preciso de Node.js/npm instalado?

**R:** **Não** para usuário final. Apenas se você fizer build das fontes (desenvolvedores).

---

## 🤖 IAs & Configuração

### P: Qual IA é melhor? Gemini ou OpenAI?

**R:** Depende do seu caso:

| Critério | Gemini | OpenAI | Claude | LocalAI | Ollama |
|----------|--------|--------|--------|---------|---------|
| Custo | 🟢 Grátis | 🔴 $5-20/mês | 🟡 $5-15/mês | 🟢 $0 | 🟢 $0 |
| Qualidade | 🟡 Bom | 🟢 Excelente | 🟢 Excelente | 🟡 OK | 🟡 OK |
| Velocidade | 🟡 1-2s | 🟡 1-2s | 🟡 1-2s | 🟢 100-500ms | 🟢 500ms-2s |
| Privacidade | 🟡 Google | 🟡 OpenAI | 🟡 Anthropic | 🟢 Local | 🟢 Local |
| Setup | 🟡 Via agent.py | 🟢 API Key | 🟢 API Key | 🟡 Docker | 🟡 Install |

**Recomendação:**
- 💼 **Empresa:** OpenAI (confiável, rápido, suportado)
- 💻 **Solo:** Gemini (grátis) ou LocalAI (privado)
- 🌍 **Offline:** LocalAI/Ollama (100% local)

---

### P: Como configuro OpenAI?

**R:** 3 passos:

```bash
# Passo 1: Obter chave em https://platform.openai.com/api/keys
# Passo 2: Exportar como variável
export OPENAI_API_KEY="sk-proj-xxxxx"

# Passo 3: CLAW auto-detecta na próxima arranque
# Pronto! ✅
```

---

### P: Como configuro Claude?

**R:** Mesmo processo que OpenAI:

```bash
export ANTHROPIC_API_KEY="sk-ant-xxxxx"
# CLAW detecta automaticamente
```

---

### P: Como configuro LocalAI/Ollama?

**R:** Duas opções:

**LocalAI (Docker):**
```bash
docker run -p 8000:8000 localai/localai:latest gemma:7b-instruct
# CLAW detecta em http://localhost:8000
```

**Ollama (Downloads):**
```bash
# Download em https://ollama.ai
ollama run mistral:7b
# CLAW detecta em http://localhost:11434
```

---

### P: CLAW funciona completamente offline?

**R:** **Sim!** Com LocalAI/Ollama:
- ✅ Nenhuma chamada para internet
- ✅ 100% privado
- ✅ 100% gratuito
- ✅ Funciona em avião/trens

Se sem IA: Pattern matching + Templates (também offline).

---

### P: Posso usar múltiplas IAs simultaneamente?

**R:** **Sim.** CLAW auto-detecta e prioriza:

```
Prioridade (ordem):
1. Gemini (se agent.py disponível)
2. OpenAI (se OPENAI_API_KEY definido)
3. Claude (se ANTHROPIC_API_KEY definido)
4. LocalAI (se http://localhost:8000 respondendo)
5. Ollama (se http://localhost:11434 respondendo)
6. Pattern matching (sempre disponível)
7. Templates (último recurso)
```

Se Gemini falha → tenta OpenAI → tenta Claude → etc.

---

### P: Qual é o custo mensal?

**R:** Depende do seu uso:

| Cenário | IA | Custo/mês |
|---------|----|----|
| Iniciante (100 sugestões/dia) | Gemini | $0 (limite gratuito) |
| Desenvolvedor (500/dia) | Gemini | $0-2 |
| Empresa (5000/dia) | OpenAI | $20-50 |
| Offline (com cache 60%) | Qualquer | -60% |
| LocalAI/Ollama | Próprio | $0 (apenas energia) |

**Com CLAW cache:** Reduzir em 60% automaticamente! 🔥

---

## ⚙️ Troubleshooting

### P: Sugestões não aparecem. O que fazer?

**R:** Checklist:

```
1✓ CLAW está ativado?
  → Ctrl+Shift+P → "CLAW: Status"
  → Procure por "enabled: true"

2✓ Uma IA está configurada?
  → Ctrl+Shift+P → "CLAW: Status"
  → Procure por "detected: Gemini/OpenAI/LocalAI"

3✓ Arquivo é linguagem suportada?
  → Procure por python, typescript, javascript, c#, rust, go, sql, markdown

4✓ Debounce não é muito alto?
  → Ctrl+Shift+P → "CLAW: Preferências"
  → debounceMs: tente 500 (padrão)

5✓ Relógio não está quebrado?
  → Debug Output → "CLAW"
  → Procure por erros
```

---

### P: Recebo erro "API Key não encontrada"

**R:** Certifique-se de exportar corretamente:

```bash
# ❌ ERRADO (apenas neste terminal)
export OPENAI_API_KEY="sk-..."

# ✅ CORRETO (permanente)
# No ~/.bashrc (Linux/Mac) ou .env (Windows):
export OPENAI_API_KEY="sk-..."
source ~/.bashrc

# ✅ ALTERNATIVA (arquivo config)
# Em ~/.claw/config/.claude.json:
{
  "OPENAI_API_KEY": "sk-..."
}
```

---

### P: Sugestões aparecem muito devagar

**R:** Tente isso:

```json
{
  "clawrafaelia.debounceMs": 300,    // Reduzir espera
  "clawrafaelia.aiTimeout": 1000,    // Timeout mais curto
  "clawrafaelia.maxTokens": 30,      // Sugestões menores
  "clawrafaelia.preferredAI": "openai"  // Trocar de IA
}
```

Se ainda lento:
- Usar LocalAI/Ollama (0 latência de rede)
- Ativar cache: `"enableCache": true`
- Reduzir máximon tokens para 20

---

### P: CLAW consome CPU/RAM demais

**R:** Reduzir footprint:

```json
{
  "clawrafaelia.cacheMaxEntries": 100,    // De 500 → 100
  "clawrafaelia.debounceMs": 1000,        // De 500 → 1000
  "clawrafaelia.maxTokens": 25,           // De 50 → 25
  "clawrafaelia.logLevel": "error"        // De info → error
}
```

---

### P: "Circuit breaker: IA blacklisted"

**R:** Uma IA falhou 5 vezes. CLAW pula para próxima por 5 min:

```
Razões comuns:
1. ❌ API key expirada → Renovar chave
2. ❌ Conexão internet → Verificar WiFi
3. ❌ IA instável → Trocar para outro provider
4. ❌ Timeout muito curto → Aumentar aiTimeout a 3000-5000ms
```

---

## 🎯 Performance & Otimização

### P: Como economizar API calls?

**R:** 5 estratégias:

```json
{
  "clawrafaelia.enableCache": true,           // +60% economia
  "clawrafaelia.cacheSimilarityThreshold": 0.8,  // Reusar mais
  "clawrafaelia.debounceMs": 1000,            // Menos disparo
  "clawrafaelia.maxTokens": 30,               // Sugestões curtas
  "clawrafaelia.preferredAI": "localai"       // $0/mês (offline)
}
```

**Resultado:** Economizar 60-80% de API calls = 60-80% menos custo! 💰

---

### P: Como ativar debug mode?

**R:**

```json
{
  "clawrafaelia.logLevel": "debug",
  "clawrafaelia.showInlineMessage": true
}
```

Então:
```
Ctrl+Shift+P → Output
Selecione → CLAW
Veja logs detalhados
```

---

## 🔒 Segurança & Privacy

### P: Meus dados são vazados para a IA?

**R:** **Não**, por design:

- ✅ CLAW envia apenas **contexto local** (próximas 300 chars)
- ✅ Arquivo inteiro **NÃO é enviado**
- ✅ Paths/credentials **NÃO são inclusos**
- ✅ Cache é **100% local** (não enviado a ninguém)

```json
// O que é enviado:
{
  "context": "def hello(name",
  "language": "python",
  "indent": 4
}

// O que NÃO é enviado:
{
  "fullFile": "...",  // ❌
  "apiKeys": "...",   // ❌
  "filePath": "/home/user/...",  // ❌
  "machineID": "...",  // ❌
}
```

---

### P: Onde armazena API keys?

**R:** **Nunca em VS Code settings.json**. Apenas:

```
1. Variáveis de ambiente ✅
   export OPENAI_API_KEY="..."

2. ~/.claw/config/.claude.json ✅
   {
     "OPENAI_API_KEY": "sk-..."
   }

3. .env (com .gitignore) ✅
   OPENAI_API_KEY=sk-...
```

**NÃO armazenar em:**
- ❌ settings.json (visível em git)
- ❌ Workspace settings (compartilhado)

---

### P: CLAW é GDPR compliant?

**R:** **Sim**:
- ✅ Sem rastreamento de usuário
- ✅ Sem telemetria (opt-in apenas)
- ✅ Cache local apenas
- ✅ Zero armazenamento em cloud

---

## 🐛 Known Issues

### P: Por que CLAW não funciona com GitHub Copilot?

**R:** Funciona! Nenhum conflito:
- Copilot: Multi-line completions
- CLAW: Single-line suggestions
- **Ambas podem rodar juntas** ✅

Se conflitar:
```
Desativar CLAW temporariamente:
Ctrl+Shift+P → "CLAW: Toggle"
```

---

### P: Por que não há sugestão para XML/HTML?

**R:** Planejado para v1.2:

```
Suportadas agora:
✅ Python, TypeScript, JavaScript, C#, Rust, Go, SQL, Markdown, Java, Bash

Planejadas:
🟡 XML, HTML, CSS, YAML, Dockerfile, Terraform (v1.2)
🟡 GraphQL, JSON, Protobuf (v1.3)
```

---

## 🔗 Integração com Ferramentas

### P: CLAW funciona com Prettier/Black?

**R:** **Sim**, sem conflito:

```python
def hello(name):  # CLAW sugere
    return name   # Prettier formata
    # Resultado final ✅ formatado
```

---

### P: CLAW funciona com linters?

**R:** **Sim**, CLAW respeita:
- ESLint rules
- PyLint rules
- C# StyleCop rules
- Prettier/Black formatting

Sem conflito! ✅

---

## 📚 Documentação

### P: Aonde está a documentação completa?

**R:** Vários arquivos:

```
├─ README.md (overview)
├─ QUICK-START.md (comece aqui!)
├─ FEATURES.md (lista completa)
├─ settings-reference.json (todas opções)
├─ ARCHITECTURE.md (design técnico)
├─ DEVELOPER.md (para devs)
├─ TROUBLESHOOTING.md (mais dicas)
└─ FAQ.md (este arquivo)
```

**Para começar:** Ler QUICK-START.md (3 min) depois FEATURES.md (10 min)

---

### P: Como reportar bug?

**R:** GitHub Issues:

```
1. Vá a https://github.com/RafaelBatista/ClawRafaelIA
2. Clique "Issues" → "New Issue"
3. Descreva:
   - Versão CLAW (Ctrl+Shift+P → "About")
   - VS Code version
   - Sistema (Windows/Mac/Linux)
   - Passos para reproduzir
   - Logs (Debug mode)
4. Envie! ✅
```

---

## 💡 Tips & Tricks

### P: Como usar CLAW mais eficientemente?

**R:** 7 dicas:

```
1✅ Use cache
   → enableCache=true, similarityThreshold=0.8

2✅ Prefira LocalAI para privacidade
   → preferredAI=localai (100% offline)

3✅ Customize debounce para seu estilo
   → 300ms (typing rápido), 800ms (typing lento)

4✅ Combine com git branches
   → Debug mode = facilita entender sugestões

5✅ Rejeite sugestões ruins frequente
   → Treina IA a entender seu estilo

6✅ Use Ctrl+/para ver histórico
   → Veja pattern matching em ação

7✅ Monitore status bar
   → Clique para ver métricas em tempo real
```

---

## 🚀 Futuro

### P: Qual é o roadmap?

**R:** Versões futuras:

```
v1.2 (Q2 2026)
├─ HTML/XML/CSS support
├─ Per-project .clawrc.json
└─ Custom patterns

v1.3 (Q3 2026)
├─ Multi-file context
├─ Test generation
└─ Refactoring suggestions

v2.0 (Q4 2026+)
├─ JetBrains plugin
├─ Visual Studio extension
├─ Web IDE integration
└─ Streaming responses
```

---

**Versão doc:** 1.1.3  
**Data:** 6 de Abril de 2026  
**Última atualização:** 2026-04-06
