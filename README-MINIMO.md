# 🚀 CLAW — Agente IA Minimalista e Funcional

**Versão:** 2.0.0 | **Status:** ✅ Operacional | **API:** Google Gemini

---

## 📁 Estrutura

```
claw-agent/
├── automation/my_scripts/
│   ├── agent.py              ← Seu agente (intacto)
│   ├── Teste_Agente.py       ← Testes
│   └── [outras ferramentas]
├── bin/
│   └── claw                  ← Entry point único
├── config/
│   └── .claude.json          ← API Keys
├── docs/                     ← Documentação
├── 📄 Arquivos .md essenciais
```

---

## 🚀 Como Usar

### Método 1: Via `bin/claw`
```bash
python3 bin/claw status
python3 bin/claw analyze seu_arquivo.py
python3 bin/claw improve seu_arquivo.py
```

### Método 2: Direto do agent.py
```bash
python3 automation/my_scripts/agent.py analyze seu_arquivo.py
```

---

## 📋 Comandos Disponíveis

| Comando | Descrição |
|---------|-----------|
| `status` | Verifica configuração e API |
| `analyze <arquivo>` | Analisa bugs, segurança, performance |
| `improve <arquivo>` | Refatora e otimiza |
| `document <arquivo>` | Gera documentação |
| `test <arquivo>` | Cria testes unitários |
| `ask "PERGUNTA"` | Responde com IA + contexto |

---

## ✨ Funcionalidades

✅ Análise automática de código  
✅ Detecção de bugs e vulnerabilidades  
✅ Refatoração inteligente  
✅ Geração de documentação  
✅ Criação de testes  
✅ Suporte a 10+ linguagens  
✅ Cache semântico (economiza API)  
✅ Contexto automático do projeto  
✅ Fallback inteligente  

---

## ⚙️ Configuração

API Key automaticamente carregada de `~/.claw/config/.claude.json`

Para verificar:
```bash
python3 bin/claw status
```

---

## 📚 Documentação Completa

- `PRIMEIRO-USO.md` — Guia detalhado
- `GEMINI.md` — Padrões e melhores práticas
- `CLAUDE.md` — Expertise técnica
- `docs/` — Histórico e referências

---

## 🎯 O que Ficou

✅ `automation/` — **100% intacto** (seu agente original)  
✅ `config/` — Configuração e API keys  
✅ `docs/` — Documentação organizada  
✅ `bin/claw` — Entry point único e minimalista  
✅ `📄 .md files` — Documentação essencial  

---

## 🗑️ O que Foi Removido

❌ `src/`, `tests/`, `assets/` — Cópias redundantes  

**Resultado:** Projeto 100% minimalista mas **totalmente funcional**

---

**Seu agente está pronto para usar!** 🎉
