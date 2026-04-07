# 🚀 RELEASE v1.1.5 - Publicação VS Code Marketplace + GitHub

**Data:** 6 de Abril de 2026  
**Status:** ✅ PRONTO PARA PUBLICAR  
**Versão:** 1.1.5  

---

## 📦 Arquivo de Distribuição

```
✅ clawrafaelia-suggestions-1.1.5.vsix (2.01 MB)
   📍 Localização: ~/OneDrive/ClawRafaelIA/vscode-extension/
   📝 Conteúdo: 457 arquivos, 175 JavaScript files
   🔒 Assinado e pronto para publicar
```

---

## ✅ Verificação de Referências (v1.1.5)

### 1. package.json
```json
{
  "name": "clawrafaelia-suggestions",
  "version": "1.1.5",        ✅ ATUALIZADO
  "publisher": "RafaelBatista",
  "displayName": "CLAW - Sugestões Inline com IA Automática"
}
```

**Verificado em:**
- ✅ `package.json` line 5: `"version": "1.1.5"`

### 2. README.md
- ✅ Badge de versão: `[![Version](https://img.shields.io/badge/version-1.1.5-blue)](package.json)`
- ✅ Características: `## ✨ Características (v1.1.5 - NEW!)`

### 3. Compilação
- ✅ TypeScript compilation: OK
- ✅ Webpack bundling: OK (14 KB minified)
- ✅ dist/extension.js: 15 KB

### 4. Caminhos Portáveis (Nova Feature v1.1.5)
- ✅ `pathResolver.ts` - Novo módulo
- ✅ `agentManager.ts` - Usa PathResolver
- ✅ `aiSelector.ts` - Usa PathResolver
- ✅ Default: `~/.local/bin/agent.py` (sem UserId hardcoded)
- ✅ README atualizado com caminhos portáveis

---

## 🔗 Links para Publicação

### VS Code Marketplace
```
Publisher: RafaelBatista
Extension ID: RafaelBatista.clawrafaelia-suggestions
URL: https://marketplace.visualstudio.com/items?itemName=RafaelBatista.clawrafaelia-suggestions&ssr=false#overview
```

### GitHub Release
```
Repository: https://github.com/RafaelBatistaDev/CLAW---Sugest-es-Inline-com-IA
Tag: v1.1.5
VSIX Upload: clawrafaelia-suggestions-1.1.5.vsix
```

---

## 📋 Checklist Pré-Publicação

### ✅ Código
- [x] Compilação sem erros
- [x] VSIX gerado com sucesso
- [x] Caminhos portáveis implementados
- [x] Versão atualizada para 1.1.5
- [x] README.md atualizado

### ✅ Documentação
- [x] package.json correto
- [x] LICENSE.md presente (MIT)
- [x] CHANGELOG.md atualizado
- [x] README.md com instruções
- [x] badges de versão atualizados

### ✅ Marketplace VS Code
- [ ] PAT Token configurado (se necessário)
- [ ] Descrição curta: "Sugestões de código em tempo real. Auto-detecta e usa qualquer IA: Gemini, OpenAI, Claude, LocalAI, Ollama"
- [ ] Ícone/Screenshot pronto
- [ ] Categorias: Programming Languages, Formatters, Other

### ✅ GitHub Release
- [ ] Tag v1.1.5 criada
- [ ] Release notes escritas
- [ ] VSIX file anexado
- [ ] Changelog mencionado

---

## 🎯 Mudanças v1.1.5

### Features Adicionadas
1. **Caminhos Portáveis** - Sem hardcoding de usuários específicos
2. **PathResolver Module** - Auto-detecção inteligente de agent.py
3. **Multi-localização** - Suporta: `~/.local/bin/`, `~/bin/`, `/usr/local/bin/`, `~/.claw/`
4. **Fallback automático** - Procura múltiplas localizações

### Bug Fixes
- Removido: `/home/recifecrypto/OneDrive/...` (usuário-específico)
- Adicionado: Suporte a `~/.local/bin/` (portável)
- Corrigido: Imports não-utilizados (clean compilation)

---

## 🚀 Instruções de Publicação

### 1. Publicar no VS Code Marketplace

```bash
cd ~/OneDrive/ClawRafaelIA/vscode-extension

# Option A: CLI (requer PAT token)
npm run publish

# Option B: Upload manual do VSIX
# Ir para: https://marketplace.visualstudio.com/manage
# Upload: clawrafaelia-suggestions-1.1.5.vsix
```

### 2. Publicar no GitHub

```bash
# Criar tag
git tag -a v1.1.5 -m "Release v1.1.5: Portable paths support"

# Push tag
git push origin v1.1.5

# Criar GitHub Release
# - ir para: https://github.com/RafaelBatistaDev/CLAW---Sugest-es-Inline-com-IA/releases
# - Selecionar tag v1.1.5
# - Anexar clawrafaelia-suggestions-1.1.5.vsix
# - Escrever release notes
```

### 3. Anunciar no LinkedIn

```
🚀 CLAW v1.1.5 — Agora com Suporte a Caminhos Portáveis!

✅ Removido hardcoding de usuários
✅ Funciona para qualquer usuário em qualquer máquina
✅ Auto-detecção inteligente de agent.py
✅ Suporte múltiplas localizações (bin, .local/bin, .claw)

📦 Download: https://marketplace.visualstudio.com/items?itemName=RafaelBatista.clawrafaelia-suggestions&ssr=false#overview
```

---

## 📊 Informações do Release

| Campo | Valor |
|-------|-------|
| **Version** | 1.1.5 |
| **Extension Name** | clawrafaelia-suggestions |
| **Publisher** | RafaelBatista |
| **VSIX File** | clawrafaelia-suggestions-1.1.5.vsix |
| **File Size** | 2.01 MB |
| **Files Included** | 457 |
| **VS Code Min Version** | ^1.85.0 |
| **License** | MIT |

---

## ✨ Histórico de Versões

| Versão | Data | Mudanças |
|--------|------|----------|
| 1.1.5 | 6 Abr 2026 | Caminhos Portáveis, PathResolver, Multi-localização |
| 1.1.4 | X Abr 2026 | Release anterior |

---

**Status: 🟢 PRONTO PARA PUBLICAR**

```
✅ Código compilado
✅ VSIX gerado
✅ Versão atualizada
✅ Documentação atualizada
✅ Caminhos portáveis funcionando
✅ Pronto para GitHub + VS Code Marketplace
```

Próximo passo: **Publicar nos dois repositórios! 🚀**
