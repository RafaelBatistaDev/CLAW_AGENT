# 📚 Documentação Organizada do Claw_Agent

Esta pasta contém toda a documentação secundária, histórico e exemplos do projeto.

## 📂 Estrutura

### [`setup/`](./setup/)
Scripts de inicialização e setup já executados:
- `ACTIVATE.sh` - Setup completo do agente
- `ACTIVATE-SIMPLE.sh` - Setup simplificado
- `START-HERE.sh` - Tutorial interativo (não necessário após primeiro uso)
- `ComeçarPCNovo.py` - Onboarding para novo PC
- `GITHUB-RELEASE-SETUP.md` - Configuração de releases (uma única vez)

**Quando usar:** Apenas para novo setup em outro PC/máquina

---

### [`history/`](./history/)
Relatórios, auditorias e histórico técnico do projeto:
- `AUDITORIA-FINAL.md` - Auditoria final completa
- `CHECKLIST-PRODUCAO.md` - Checklist de produção
- `RELATORIO-CONSOLIDACAO.md` - Relatório v3.0
- `EXTENSION-BUILD-SUMMARY.md` - Build da extensão VS Code
- `EVOLUCAO-SISTEMA.md` - Evolução técnica do projeto
- `AGENT_PYTHON_MIGRATION.md` - Histórico da migração Python

**Quando usar:** Referência histórica, compreender decisões técnicas passadas

---

### [`examples/`](./examples/)
Exemplos práticos e demos de funcionalidades:
- `DEMO-AUTO-IMPROVE.md` - Demo completa de auto-melhoria
- `EXEMPLOS-GEMINI-FALLBACK.md` - Exemplos de fallback Gemini

**Quando usar:** Aprender por exemplos práticos

---

### [`reference/`](./reference/)
Documentação técnica redundante ou secundária:
- `AGENTE.md` - Referência completa do agente (veja PRIMEIRO-USO.md)
- `INTEGRACAO-SMARTFALLBACK.md` - SmartFallback (veja DEVELOPMENT.md)
- `GEMINI-FALLBACK-STRATEGY.md` - Estratégia de fallback
- `QUICKREF-SMARTFALLBACK.md` - Quick reference (veja QUICKSTART.md)
- `IA-AGNOSTICA-AUTO-DETECCAO.md` - Auto-detecção de linguagens
- `TOKEN-OPTIMIZATION-EXAMPLES.md` - Exemplos de otimização (veja TOKEN-OPTIMIZATION-GUIDE.md)

**Quando usar:** Referência detalhada de tópicos específicos

---

## 🎯 Documentação Ativa (Raiz do Projeto)

Para uso diário, consulte estes arquivos na raiz:

| Arquivo | Propósito |
|---------|-----------|
| **README.md** | Entry point principal |
| **PRIMEIRO-USO.md** | Guia de onboarding |
| **QUICKSTART.md** | Referência rápida |
| **STANDARDS.md** | Padrões do código |
| **PHILOSOPHY.md** | Visão e valores |
| **DEVELOPMENT.md** | Guia de desenvolvimento |
| **TESTING.md** | Testes |
| **TOKEN-OPTIMIZATION-GUIDE.md** | Otimização de tokens |
| **TROUBLESHOOTING.md** | Resolução de problemas |
| **ROADMAP.md** | Futuro do projeto |
| **CHANGELOG.md** | Histórico de mudanças |
| **CLAUDE.md** | Guia IA/CLAUDE |
| **GEMINI.md** | API Gemini |
| **INDEX.md** | Índice completo |

---

## 💾 Espaço Economizado

```
ANTES:  46 arquivos .md + scripts na raiz
DEPOIS: 15 arquivos essenciais + /docs/ organizado

Espaço liberado: ~200 KB
Ganho: Raiz limpa e mais fácil de navegar
```

---

## 🔧 Como Usar

### Setup em novo PC:
```bash
bash docs/setup/ACTIVATE.sh
```

### Consultar histórico:
```bash
cat docs/history/EVOLUCAO-SISTEMA.md
```

### Ver exemplos:
```bash
cat docs/examples/DEMO-AUTO-IMPROVE.md
```

---

**Última atualização:** 7 de abril de 2026
