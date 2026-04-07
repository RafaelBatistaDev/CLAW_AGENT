# ⚡ QUICKSTART — Comece em 30 Segundos

**Setup rápido + referência dos 4 comandos principais.** | Data: 6 de abril de 2026

---

## 🚀 SETUP (30 segundos)

```bash
# 1️⃣ Recarregar configuração
source ~/.bashrc

# 2️⃣ Validar instalação
agent status

# 3️⃣ Usar o agente
agent analyze seu_arquivo.py
```

✅ **Pronto!** Agora vem os 4 comandos.

---

## 🎯 OS 4 COMANDOS

| Comando | O Que Faz | Uso |
|---------|-----------|-----|
| **`analyze`** | 🐛 Detecta bugs, vulnerabilidades, ineficiências | `agent analyze FILE` |
| **`improve`** | 🚀 Refatora e otimiza o código | `agent improve FILE` |
| **`document`** | 📝 Gera documentação automática | `agent document FILE` |
| **`test`** | ✅ Cria testes unitários automaticamente | `agent test FILE` |

---

## 💡 EXEMPLOS RÁPIDOS

### Python
```bash
agent analyze src/main.py       # Ver problemas
agent improve src/main.py       # Melhorar código
agent document src/main.py      # Gerar docs
agent test src/main.py          # Criar testes
```

### JavaScript/TypeScript
```bash
agent analyze src/app.ts
agent improve src/app.ts
agent document src/app.ts
agent test src/app.ts
```

### Rust
```bash
agent analyze src/lib.rs
agent improve src/lib.rs
agent document src/lib.rs
agent test src/lib.rs
```

### JSON
```bash
agent analyze config.json
agent improve config.json
agent document config.json
```

---

## 📊 O QUE VOCÊ VÊ

### Exemplo: `agent analyze app.py`

```
📊 Analisando: app.py
📚 Carregando contexto do projeto...
✅ 2 arquivo(s) .md carregado(s) — 53,938 chars

🔄 Processando com IA...

─────────────────────────────────────────────
🐛 BUGS ENCONTRADOS (2):
  • Line 42: Unwrap sem error handling
  • Line 87: Possível integer overflow

🚀 MELHORIAS (3):
  • Usar Result<T> em vez de Option<T>
  • Cache regex compilation
  • Adicionar type hints

⚠️ CAUTELAS:
  • Performance pode sofrer com arquivos > 10MB
  • Validar saída em código crítico

✅ CÓDIGO ESTÁ BEM ESTRUTURADO
─────────────────────────────────────────────
```

---

## 📖 ESTRUTURA DO PROJETO

```
claw-agent/
├── README.md .................... Visão geral (comece aqui)
├── SETUP.md ..................... Instalação e configuração
├── QUICKSTART.md ................ Este arquivo (referência rápida)
├── TROUBLESHOOTING.md .......... Soluções de problemas
├── PHILOSOPHY.md ............... Princípios de design
├── DEVELOPMENT.md .............. Guidelines de contribuição
├── STANDARDS.md ................ Padrões técnicos
├── TESTING.md .................. Testes e validação
├── ROADMAP.md .................. Visão de 4 fases
│
├── automation/my_scripts/
│   ├── agent.py ................ Agente principal (1500+ linhas)
│   ├── agent ................ Fallback bash
│   └── 10+ scripts auxiliares
│
└── config/
    ├── .claude.json ............ API Keys + limites
    └── CLAUDE.template.md ...... Template para novos PCs
```

---

## 🔧 CONFIGURAÇÃO CRÍTICA

### Arquivo: `~/.claw/config/.claude.json`

```json
{
  "api": {
    "google_gemini_api_key": "${GOOGLE_GEMINI_API_KEY}no",
    "model": "gemini-2.0-flash",
    "base_url": "https://generativelanguage.googleapis.com/v1beta/models"
  },
  "limits": {
    "max_daily_requests": 1000,
    "max_tokens_per_request": 2000,
    "model_timeout": 60
  }
}
```

✅ **Já pré-configurado!** (Vem com chave válida)

---

## ❓ FAQ RÁPIDO

**P: Como usar o agente?**  
R: `agent <comando> <arquivo>`  Exemplos acima.

**P: Quais linguagens são suportadas?**  
R: 10+ (Python, JS, TS, Rust, Go, C#, Java, C++, PHP, Ruby)

**P: Quanto custa usar?**  
R: Grátis! Usa API do Google Gemini (limite 1000 req/dia)

**P: Algo não funciona?**  
R: Ver [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

**P: Posso usar em novo PC?**  
R: Sim! Clone o repositório e rode `bash docs/setup/ACTIVATE.sh`

**P: Como contribuir?**  
R: Ver [DEVELOPMENT.md](DEVELOPMENT.md)

---

## 🔗 LINKS RÁPIDOS

- **Mapa Completo:** [INDEX.md](INDEX.md)
- **Guia Completo:** [AGENTE.md](AGENTE.md)
- **Setup Detalhado:** [PRIMEIRO-USO.md](PRIMEIRO-USO.md)
- **Problemas?** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Status do Sistema:** `agent status`
- **Ajuda:** `agent help`

---

## 📦 O QUE FOI CRIADO

✅ **agent.py** — Agente principal em Python 3 (1500+ linhas)  
✅ **4 Comandos** — analyze, improve, document, test  
✅ **10+ Linguagens** — Auto-detecção automática  
✅ **Documentação** — 16 arquivos (220+ KB)  
✅ **Portável** — Funciona em qualquer PC com Python 3  
✅ **API Integrada** — Google Gemini pré-configurado  

---

**Próximo passo:** `agent analyze seu_arquivo.py`  
**Precisa de mais detalhe?** Ver [AGENTE.md](AGENTE.md) ou [INDEX.md](INDEX.md)

1. **Configurar chaves**: Edite `~/.claw/config/.claude.json`
2. **Clonar projeto**: Use em seu novo projeto
3. **Customizar scripts**: Adicione seus próprios em `automation/my_scripts/`
4. **Documentar**: Atualize `CLAUDE.md` conforme necessário

---

**Mais detalhes**: Veja [README.md](README.md)
