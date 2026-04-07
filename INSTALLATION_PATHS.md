# 📂 Caminhos de Instalação — Guia Completo

**Versão:** 1.0.1  
**Data:** 2026-04-07

---

## 🎯 Visão Geral

Após instalar o **Claw_Agent**, aqui estão **TODOS os caminhos** e suas funções:

```
HOME (~)
├── claw-agent/                    ← Pasta do projeto clonado
│   ├── automation/my_scripts/     ← Scripts Python
│   │   └── agent.py              ← Agente principal (executável)
│   ├── bin/                       ← Executáveis
│   │   ├── agent                 ← Entry point (script Python wrapper)
│   │   └── claw                  ← Alias para 'agent'
│   ├── config/                   ← Configuration
│   │   ├── agents.json.template  ← Template (copiar para ~/.claw/config/)
│   │   └── CLAUDE.template.md    ← Template da documentação
│   ├── docs/                     ← Documentação
│   ├── tests/                    ← Testes
│   └── [outros arquivos README, SETUP.md, etc]
│
└── .claw/                        ← Dados do usuário (NÃO está no git)
    ├── config/
    │   ├── .claude.json          ← Chave da API (SEU secreto!)
    │   └── agents.json           ← Cópia de agents.json.template
    └── cache/
        ├── context_cache/        ← Cache de arquivos .md lidos
        ├── response_cache/       ← Cache de respostas da IA
        └── [arquivos temporários]
```

---

## 📍 1. Pasta Principal do Projeto

**Localização:** `~/claw-agent/` (ou onde você clonou)

```bash
# Exemplo
cd ~/claw-agent
ls -la
```

**Conteúdo:**
- Scripts executáveis (`bin/agent`, `bin/claw`)
- Código-fonte (`automation/my_scripts/agent.py`)
- Configurações (`config/`)
- Documentação (`docs/`, `*.md`)

**Nota:** Esta pasta está **no Git** e é compartilhada entre usuários.

---

## 🔑 2. Pasta de Configuração do Usuário

**Localização:** `~/.claw/config/`

```bash
# Verificar
ls -la ~/.claw/config/
```

**Arquivos:**
1. **`.claude.json`** (NÃO no git)
   - Chave do Google Gemini
   - Timeout de API
   - Configurações privadas
   ```json
   {
     "GOOGLE_GEMINI_API_KEY": "sua_chave_real_aqui",
     "API_TIMEOUT": 30,
     "CACHE_TTL": 3600
   }
   ```

2. **`agents.json`** (Cópia de template)
   - Configuração dos agentes
   - Modelos LLM disponíveis
   - Prioridades e fallbacks

---

## 💾 3. Pasta de Cache

**Localização:** `~/.claw/cache/`

```bash
# Ver tamanho do cache
du -sh ~/.claw/cache/

# Limpar cache (seguro)
rm -rf ~/.claw/cache/*
```

**Subpastas:**
- **`context_cache/`** — Arquivos `.md` já lidos (acelera startup)
- **`response_cache/`** — Respostas da IA cacheadas (economiza API calls)
- **Arquivos temporários** — Processamento em andamento

**Nota:** Cache é **automático e seguro** de deletar. Agent recria quando necessário.

---

## 🔗 4. Alias no Bashrc

**Arquivo:** `~/.bashrc`

```bash
# Adiciona alias 'agent' (feito pelo ACTIVATE.sh)
alias agent='python3 ~/claw-agent/bin/agent'
```

**Qual é o resultado:**
- Pode usar `agent analyze file.py` de qualquer pasta
- Automático redireciona para o script correto
- Funciona com `source ~/.bashrc`

---

## 📊 Tabela de Caminhos Rápida

| Tipo | Caminho | Conteúdo | Git |
|------|---------|----------|-----|
| **Projeto** | `~/claw-agent/` | Código, docs, scripts | ✅ SIM |
| **Config privada** | `~/.claw/config/.claude.json` | Chave API | ❌ NÃO |
| **Config pública** | `~/.claw/config/agents.json` | Agentes, prioridades | ❌ NÃO |
| **Cache** | `~/.claw/cache/` | Respostas, contexto | ❌ NÃO |
| **Logs** | `~/.claw/logs/` (opcional) | Histórico de uso | ❌ NÃO |
| **Bashrc alias** | `~/.bashrc` | Alias 'agent' | Local |

---

## 🔄 Fluxo de Execução

Quando você digita `agent analyze file.py`:

```
1. Shell vê alias 'agent' no ~/.bashrc
   ↓
2. Redireciona para: python3 ~/claw-agent/bin/agent
   ↓
3. bin/agent (script wrapper) executa:
   - automation/my_scripts/agent.py
   ↓
4. agent.py lê configuração:
   - ~/.claw/config/.claude.json (chave da API)
   - ~/.claw/config/agents.json (modelos disponíveis)
   ↓
5. Carrega cache (se existir):
   - ~/.claw/cache/context_cache/
   - ~/.claw/cache/response_cache/
   ↓
6. Executa análise e salva resultado no cache
```

---

## 📦 Instalação Padrão (Resultado)

Se você seguir [SETUP.md](SETUP.md), isto é o que criará:

```bash
# 1. Você clona o repo
git clone https://github.com/seu-usuario/claw-agent.git
cd claw-agent

# 2. Roda ACTIVATE.sh que:
bash docs/setup/ACTIVATE.sh

# 3. Resulta em:
✅ ~/claw-agent/                    (projeto clonado)
✅ ~/.claw/config/                  (pasta criada)
✅ ~/.claw/cache/                   (pasta criada)
✅ ~/.bashrc atualizado com alias   (agent command)

# 4. Você adiciona a chave:
nano ~/.claw/config/.claude.json    (edita chave API)

# 5. Agora funciona:
source ~/.bashrc
agent status        # ✅ Deve funcionar
agent analyze file.py
```

---

## 🗂️ Estrutura Completa (Com Exemplos)

```
/home/seu-usuario/ (equivalente a ~)
│
├── claw-agent/                           [git repository]
│   ├── automation/my_scripts/
│   │   ├── agent.py                      [2000 linhas, main agent]
│   │   └── Teste_Agente.py               [test suite]
│   │
│   ├── bin/
│   │   ├── agent                         [executable wrapper]
│   │   └── claw                          [alias]
│   │
│   ├── config/
│   │   ├── agents.json.template          [generic template]
│   │   └── CLAUDE.template.md
│   │
│   ├── docs/
│   │   ├── examples/                     [example usage]
│   │   ├── reference/                    [technical docs]
│   │   └── setup/                        [ACTIVATE.sh]
│   │
│   ├── README.md
│   ├── SETUP.md
│   ├── QUICKSTART.md
│   ├── PRODUCTION_CHECKLIST.md
│   └── [mais .md files]
│
├── .claw/                               [user data, NOT in git]
│   ├── config/
│   │   ├── .claude.json                 [🔐 SECRET!]
│   │   └── agents.json                  [cópia do template]
│   │
│   ├── cache/
│   │   ├── context_cache/
│   │   │   ├── readme.md.cache
│   │   │   ├── doc.md.cache
│   │   │   └── [...]
│   │   │
│   │   └── response_cache/
│   │       ├── analyze_app.py.cache
│   │       ├── improve_lib.rs.cache
│   │       └── [...]
│   │
│   └── logs/                            [optional]
│       └── agent_2026-04-07.log
│
├── .bashrc                              [seu bashrc local]
│   # ... suas outras configurações ...
│   alias agent='python3 ~/claw-agent/bin/agent'
│
└── .ssh/
    ([não afeta claw-agent])
```

---

## 🔐 Segurança: O Que Não Deve Ser Commitado

No `.gitignore` do projeto:

```
# Nunca no Git:
config/.claude.json          ← Aí está sua chave!
config/agents.json           ← Configuração privada
.claw/                       ← Dados do usuário
.env                         ← Secrets
~/.claw/                     ← Em outro lugar, protegido
```

---

## ⚡ Comandos Úteis

```bash
# Ver estrutura de pastas
tree ~/claw-agent -L 2

# Verificar configuração
ls -la ~/.claw/config/
cat ~/.claw/config/agents.json | head -20

# Ver cache
du -sh ~/.claw/cache/
find ~/.claw/cache -type f | wc -l

# Limpar cache (seguro)
rm -rf ~/.claw/cache/*

# Ver logs (se habilitado)
tail -f ~/.claw/logs/agent_*.log

# Remover completamente (se quiser)
rm -rf ~/claw-agent ~/.claw

# Re-instalar depois
git clone [repo] ~/claw-agent
cd ~/claw-agent && bash docs/setup/ACTIVATE.sh
```

---

## 📋 Checklist: Após Instalação

- [x] Pastas criadas: `~/.claw/config/` e `~/.claw/cache/`
- [x] Alias adicionado ao `~/.bashrc`
- [x] Arquivo `~/.claw/config/.claude.json` contém sua chave API
- [x] Comando `agent status` funciona
- [x] Cache vazio (será preenchido automaticamente)
- [x] Nenhum arquivo de projeto em pastas pessoais (tudo em `~/.claw/`)

---

## 🎯 Resumo

| Pergunta | Resposta |
|----------|----------|
| Onde está o código? | `~/claw-agent/` (clonado do GitHub) |
| Onde está a chave da API? | `~/.claw/config/.claude.json` (SECRETO) |
| Onde está o cache? | `~/.claw/cache/` (automático) |
| Posso deletar `~/.claw/`? | ✅ Sim, agent recria quando necessário |
| Posso deletar `~/claw-agent/`? | ❌ Não, aí está o código! (Re-clone se precisar) |
| Quantos usuários podem usar? | Todos! Cada um tem seu `~/.claw/config/` |
| Como fazer backup das chaves? | Copie `~/.claw/config/` para seguro |

---

**Gerado:** 2026-04-07  
**Versão:** 1.0.1  
**Status:** ✅ Production Ready
