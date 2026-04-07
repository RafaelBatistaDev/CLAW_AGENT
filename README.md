# 🤖 CLAW_AGENT v1.0.1 — Agente Profissional de IA

Assistente inteligente de código para análise, refatoração, documentação e testes automáticos.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.7+](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![Status: Production Ready](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)](.)

---

## ⚡ Instruções Rápidas

```
═════════════════════════════════════════════════════════════════
  🤖 AGENTE PROFISSIONAL - 5 Comandos Principais
═════════════════════════════════════════════════════════════════

  agent analyze <arquivo>      → Encontra bugs e melhorias
  agent improve <arquivo>      → Refatora e melhora código
  agent document <arquivo>     → Gera documentação automática
  agent test <arquivo>         → Cria testes automáticos
  agent ask PERGUNTA           → Responde qualquer pergunta!
  agent status                 → Mostra status e ajuda

═════════════════════════════════════════════════════════════════

  💬 Dica 1: use descrições em português!
  💬 Dica 2: ex: agent ask qual é a capital do Brasil?
  💬 Dica 3: ex: agent analyze meu_codigo.py
```

---

## 🚀 Começar em 30 segundos

```bash
# 1. Clone
git clone https://github.com/RafaelBatistaDev/CLAW_AGENT.git

# 2. Setup
bash docs/setup/ACTIVATE.sh && source ~/.bashrc

# 3. Configure sua chave API (Google Gemini)
nano ~/.claw/config/.claude.json

# 4. Use!
agent analyze seu_arquivo.py
```

---

## 🎯 O Que Faz?

### 🔍 **ANALYZE** — Encontra Bugs

Detecta bugs, vulnerabilidades de segurança e problemas de performance.

```bash
agent analyze app.py
```

**Resultado:**
```
🐛 BUGS ENCONTRADOS (2):
  • Linha 42: Exception não capturada
  • Linha 87: Risco de overflow inteiro

🚀 MELHORIAS (3):
  • Use 'with' para file operations
  • Cache de regex
  • Adicionar type hints
```

### ♻️ **IMPROVE** — Refatora Código

Melhora código automaticamente mantendo funcionalidade.

```bash
agent improve app.py
```

**O que melhora:**
- Readability e clareza
- Performance
- Best practices
- Código moderno

### 📚 **DOCUMENT** — Gera Documentação

Cria documentação markdown profissional automaticamente.

```bash
agent document app.py
```

**Gera:**
- Assinaturas de funções
- Descrições detalhadas
- Exemplos de uso
- Type hints

### ✅ **TEST** — Cria Testes

Gera testes unitários automaticamente.

```bash
agent test app.py
```

**Inclui:**
- Testes de cobertura completa
- Edge cases
- Mocking
- Assertions

### 💬 **ASK** — Pergunta Qualquer Coisa

IA responde qualquer pergunta sobre código.

```bash
agent ask "como otimizar loops em Python?"
agent ask "qual é a melhor prática para API REST?"
```

---

## 📋 Linguagens Suportadas

✅ Python  
✅ JavaScript  
✅ TypeScript  
✅ Rust  
✅ C#  
✅ Go  
✅ Ruby  
✅ PHP  
✅ Java  
✅ C++  
✅ SQL  

---

## 🔧 Configuração

### Setup Básico

```bash
# 1. Instale (cria ~/.claw/)
bash docs/setup/ACTIVATE.sh

# 2. Reconfigure shell
source ~/.bashrc

# 3. Configure chave Google Gemini
nano ~/.claw/config/.claude.json

# 4. Teste
agent status
```

### Usar Ollama (Sem Internet)

```bash
# 1. Instale Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Baixe modelo
ollama pull mistral
ollama serve

# 3. Agent usa automaticamente como fallback
agent analyze seu_arquivo.py
```

### Variáveis de Ambiente

```bash
export GOOGLE_GEMINI_API_KEY="sua_chave"
export API_TIMEOUT=60
export OLLAMA_HOST="localhost:11434"
```

---

## 📖 Documentação Completa

| Documento | Para Quem |
|-----------|-----------|
| [SETUP.md](SETUP.md) | Mais detalhes de instalação |
| [QUICKSTART.md](QUICKSTART.md) | Referência rápida dos comandos |
| [INSTALLATION_PATHS.md](INSTALLATION_PATHS.md) | Onde ficam os arquivos após setup |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Soluções para problemas comuns |

---

## 💡 Exemplos Práticos

### Exemplo 1: Analisar Código

```bash
echo 'def soma(a,b):
    return a+b' > teste.py

agent analyze teste.py
```

### Exemplo 2: Melhorar Código

```bash
agent improve teste.py
```

### Exemplo 3: Documentar

```bash
agent document teste.py
```

### Exemplo 4: Testar

```bash
agent test teste.py
```

### Exemplo 5: Perguntar

```bash
agent ask "qual é a diferença entre == e is em Python?"
```

---

## ✨ Por Que Usar?

✅ **Economiza Tempo** — Análise automática e instantânea  
✅ **Encontra Bugs** — Antes de ir para produção  
✅ **Melhora Código** — Com best practices automáticas  
✅ **Documentação Seca** — Sem escrever nada  
✅ **Testes Grátis** — Coverage automático  
✅ **Aprenda** — Dúvidas sobre código respondidas  
✅ **Totalmente Offline** — Com Ollama/LocalAI  
✅ **Code Review** — Segunda opinião profissional  

---

## 🔐 Segurança & Privacidade

✅ Nenhuma chave API no repositório  
✅ Secrets como variáveis de ambiente  
✅ Cache local apenas (`~/.claw/`)  
✅ Nenhum dado enviado sem permissão  
✅ Suporta rodas totalmente offline (Ollama)  
✅ MIT License — Uso comercial permitido  

---

## 📊 Status

| Aspecto | Status |
|---------|--------|
| **Core Agent** | ✅ Estável |
| **APIs** | ✅ Google Gemini + Ollama |
| **Linguagens** | ✅ 10+ |
| **Documentação** | ✅ Completa |
| **Produção** | ✅ Pronto |

---

## 🎊 Estatísticas

- **2000+ linhas** de código profissional
- **10+ linguagens** suportadas
- **3 APIs** com fallback automático
- **Zero** dependências externas
- **100% Python** puro

---

## 📞 Precisa de Ajuda?

- Instalar? → [SETUP.md](SETUP.md)
- Comandos? → [QUICKSTART.md](QUICKSTART.md)
- Arquivos? → [INSTALLATION_PATHS.md](INSTALLATION_PATHS.md)
- Problemas? → [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Bug? → [Issues](https://github.com/RafaelBatistaDev/CLAW_AGENT/issues)

---

## 📜 License

MIT — Livre para uso pessoal, acadêmico e comercial!

---

**Feito com ❤️ para devs que amam código limpo.**

**v1.0.1** • **Production Ready** ✅ • **MIT License**
