# 🚀 Setup — Configuração para Novo Usuário

**Guia completo para configurar o CLAW Agent em seu ambiente.**

---

## ⚙️ Pré-requisitos

- **Python 3.7+** (verificar: `python3 --version`)
- **Git** para clonar o repositório
- **Internet** para chamar APIs (Google Gemini)
- **Linux, macOS ou WSL** (Windows com subsistema Linux)

---

## 📥 Etapa 1: Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/claw-agent.git
cd claw-agent
```

---

## � Estrutura de Pastas Após Instalação

Veja [INSTALLATION_PATHS.md](INSTALLATION_PATHS.md) para **guia completo** de todos os caminhos.

**Resumo rápido:**
- **Projeto:** `~/claw-agent/` (clonado)
- **Config privada:** `~/.claw/config/.claude.json` (chave API)
- **Cache:** `~/.claw/cache/` (automático)
- **Alias:** `agent` (adicionado ao `~/.bashrc`)

---

## ⚙️ Etapa 2: Obter Chave de API (Google Gemini)

### Opção A: Usar Google Gemini (Recomendado)

1. Vá para: https://ai.google.dev/
2. Clique em **"Get API Key"**
3. Crie um novo projeto ou use o padrão
4. Copie a chave de API (começa com `AIzaSy...`)

### Opção B: Usar Ollama (Local, Offline)

Se preferir não usar APIs remotas:

```bash
# Instalar Ollama (https://ollama.ai)
curl -fsSL https://ollama.ai/install.sh | sh

# Baixar modelo (ex: Mistral)
ollama pull mistral
ollama serve  # Roda em localhost:11434
```

---

## 🛠️ Etapa 3: Configurar o Projeto

### 3.1 Criar arquivo de configuração

```bash
mkdir -p ~/.claw/config
cat > ~/.claw/config/.claude.json << 'EOF'
{
  "version": "1.0.1",
  "agents": [
    {
      "name": "Gemini-Flash-Primary",
      "type": "llm",
      "provider": "google",
      "model": "models/gemini-2.0-flash",
      "key": "SEU_API_KEY_AQUI",
      "priority": 1,
      "status": "active"
    },
    {
      "name": "LocalAI-Fallback",
      "type": "local",
      "provider": "local",
      "model": "local-ai",
      "priority": 2,
      "status": "active"
    }
  ]
}
EOF
```

### 3.2 Adicionar a chave de API

```bash
# Edite o arquivo e substitua "SEU_API_KEY_AQUI" pela chave de Google
nano ~/.claw/config/.claude.json
```

**OU**, use o comando one-liner:

```bash
# Linux/macOS
sed -i 's|SEU_API_KEY_AQUI|YOUR_ACTUAL_API_KEY|g' ~/.claw/config/.claude.json

# macOS (com xargs)
sed -i '' 's|SEU_API_KEY_AQUI|YOUR_ACTUAL_API_KEY|g' ~/.claw/config/.claude.json
```

### 3.3 Adicionar ao PATH (opcional, mas recomendado)

```bash
# Adicione ao ~/.bashrc ou ~/.zshrc
echo 'export PATH="$PATH:$(git rev-parse --show-toplevel)/bin"' >> ~/.bashrc
source ~/.bashrc
```

---

## ⚡ Etapa 4: Testar a Instalação

```bash
# Verificar status
python3 automation/my_scripts/agent.py status

# Ou, se adicionou ao PATH
agent status
```

**Resultado esperado:**
```
✅ Configuração validada
🔑 Google Gemini: Configurada
📊 Fallback Local: Pronto
```

---

## 🎯 Etapa 5: Primeira Análise

```bash
# Criar arquivo de teste
cat > test_sample.py << 'EOF'
def greet(name):
    print("Hello, " + name)
    
greet("World")
EOF

# Analisar com o agente
agent analyze test_sample.py

# Melhorar automaticamente
agent improve test_sample.py

# Gerar documentação
agent document test_sample.py

# Criar testes
agent test test_sample.py
```

---

## 📖 Etapa 6: Entender os Comandos

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `analyze` | Encontra bugs, segurança, performance | `agent analyze app.py` |
| `improve` | Refatora e otimiza código | `agent improve app.py` |
| `document` | Gera documentação automática | `agent document app.py` |
| `test` | Cria testes unitários | `agent test app.py` |
| `status` | Valida configuração e APIs | `agent status` |

---

## 🔒 Boas Práticas de Segurança

### ✅ Sempre faça:

1. **Não commit de chaves de API**
   ```bash
   # Verificar se .gitignore está correto
   cat .gitignore | grep ".claude.json"
   ```

2. **Usar variáveis de ambiente** (alternativa)
   ```bash
   export GOOGLE_GEMINI_API_KEY="sua_chave"
   agent analyze file.py
   ```

3. **Rotar chaves periodicamente**
   ```bash
   # Se expôs uma chave:
   # 1. Vá para Google AI Studio
   # 2. Delete a chave antiga
   # 3. Crie uma nova
   # 4. Atualize ~/.claw/config/.claude.json
   ```

### ❌ Nunca faça:

- Commitar `.claude.json` com chaves reais
- Compartilhar a chave de API publicamente
- Usar a mesma chave em múltiplos projetos
- Deixar chaves em histórico do Git

---

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'requests'"

Python puro, sem dependências externas. Se ocorrer, use:

```bash
pip install --user requests urllib3
```

### Erro: "API key not found"

Verifique se o arquivo existe:

```bash
cat ~/.claw/config/.claude.json | grep "key"
```

Se não existir, repita a **Etapa 3**.

### Erro: "Connection refused"

Se usar Ollama local:

```bash
# Verifique se Ollama está rodando
curl http://localhost:11434/api/tags

# Se não, inicie:
ollama serve
```

### Erro: "Rate limit exceeded"

Google Gemini tem limite de requisições gratuitas. Alternativas:

1. Esperar alguns minutos
2. Usar Ollama local (sem limites)
3. Atualizar para plano pago no Google

---

## 🚀 Próximos Passos

1. ✅ Leia [README.md](README.md) — visão geral do projeto
2. ✅ Explore [QUICKSTART.md](QUICKSTART.md) — uso rápido
3. ✅ Veja [docs/examples/](docs/examples/) — exemplos práticos
4. ✅ Contribua! Veja [DEVELOPMENT.md](DEVELOPMENT.md)

---

## 📞 Suporte

- 📖 [Documentação](docs/)
- 🐛 [Issues](https://github.com/seu-usuario/claw-agent/issues)
- 💬 [Discussões](https://github.com/seu-usuario/claw-agent/discussions)

---

**Versão:** 1.0.1  
**Última atualização:** 2026-04-07  
**Status:** Production-ready ✅
