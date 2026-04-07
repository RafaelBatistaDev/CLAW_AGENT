#!/usr/bin/env bash
# ====================================================================
# 🚀 CLAW v1.1.3 — Quick Publication Commands
# 
# Este script automatiza os passos finais de publicação
# ====================================================================

set -euo pipefail
IFS=$'\n\t'

# ── Cores ──────────────────────────────────────────────────────────
G="\033[1;32m"; B="\033[1;34m"; Y="\033[1;33m"; R="\033[1;31m"; N="\033[0m"

log()     { echo -e "${B}[INFO]${N}  $*"; }
success() { echo -e "${G}[OK]${N}    $*"; }
warn()    { echo -e "${Y}[WARN]${N}  $*"; }
error()   { echo -e "${R}[ERROR]${N} $*"; exit 1; }

# ── Setup ──────────────────────────────────────────────────────────
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VSIX_FILE="$PROJECT_ROOT/clawrafaelia-suggestions-1.1.3.vsix"

# ── Validações ─────────────────────────────────────────────────────
[[ -f "$VSIX_FILE" ]] || error "Arquivo .vsix não encontrado: $VSIX_FILE"
[[ -x "$(command -v vsce)" ]] || error "vsce não encontrado. Execute: npm install -g @vscode/vsce"

# ── Menu ──────────────────────────────────────────────────────────
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🚀 CLAW v1.1.3 — Publicação no VS Code Marketplace        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

cat << 'EOF'
Escolha uma opção:

1️⃣  Status — Verificar configuração atual
2️⃣  Login — Fazer login como RafaelBatista
3️⃣  Publish — Publicar extensão (1.1.3)
4️⃣  Verify — Verificar publicação no Marketplace
5️⃣  Help — Ver documentação completa
0️⃣  Exit — Sair

EOF

read -r -p "$(printf '%b' "${B}Opção [0-5]: ${N}")" choice

case "$choice" in
    1)
        log "Verificando status..."
        echo ""
        vsce ls || warn "Não autenticado. Execute opção 2️⃣ para fazer login"
        success "Status verificado"
        ;;
    
    2)
        log "Fazendo login no VS Code Marketplace..."
        read -r -p "$(printf '%b' "${B}Publicador (padrão: RafaelBatista): ${N}")" publisher
        publisher="${publisher:-RafaelBatista}"
        
        log "Enter seu Personal Access Token quando solicitado..."
        log "(Obtenha em: https://marketplace.visualstudio.com/manage/)"
        echo ""
        
        vsce login "$publisher"
        success "Login realizado como: $publisher"
        ;;
    
    3)
        log "Publicando CLAW v1.1.3..."
        echo ""
        
        # Verificar autenticação
        if ! vsce ls &>/dev/null; then
            error "Não autenticado. Execute opção 2️⃣ primeiro"
        fi
        
        read -r -p "$(printf '%b' "${Y}Confirmar publicação? [s/N] ${N}")" confirm
        [[ "${confirm,,}" == "s" ]] || { warn "Cancelado"; exit 0; }
        
        echo ""
        log "Iniciando publicação..."
        
        # Publicar
        cd "$PROJECT_ROOT"
        vsce publish --packagePath "$VSIX_FILE" || error "Falha na publicação"
        
        echo ""
        success "✅ CLAW v1.1.3 publicado no Marketplace!"
        echo ""
        log "Acesse em:"
        log "  https://marketplace.visualstudio.com/items?itemName=RafaelBatista.clawrafaelia-suggestions"
        echo ""
        ;;
    
    4)
        log "Verificando publicação no Marketplace..."
        echo ""
        
        URL="https://marketplace.visualstudio.com/items?itemName=RafaelBatista.clawrafaelia-suggestions"
        
        if command -v xdg-open &>/dev/null; then
            xdg-open "$URL"
            success "Abrindo no navegador..."
        elif command -v open &>/dev/null; then
            open "$URL"
            success "Abrindo no navegador..."
        else
            log "Abra manualmente:"
            log "  $URL"
        fi
        
        echo ""
        warn "Verifique:"
        warn "  ✓ Versão: 1.1.3"
        warn "  ✓ Data: 6 de Abril de 2026"
        warn "  ✓ Status: Published"
        ;;
    
    5)
        log "Abrindo documentação..."
        cat << 'HELP'

📖 CLAW v1.1.3 — Publicação no Marketplace

┌─ CHECKLIST ──────────────────────────────────────────────────────┐
│ ✅ .vsix gerado: clawrafaelia-suggestions-1.1.3.vsix (1.98 MB)   │
│ ✅ GitHub commit: v1.1.3 Auto-detect IAs, SmartFallback         │
│ ✅ Tag Git: v1.1.3 criada e pushed                              │
│ ⏳ GitHub Release: Criar manualmente (Passo 1)                  │
│ ⏳ Marketplace: Publicar com vsce (Passo 2)                     │
└──────────────────────────────────────────────────────────────────┘

PASSO 1: Criar GitHub Release
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Acesse: https://github.com/.../releases
2. Clique: "Create a new release"
3. Tag: v1.1.3
4. Title: CLAW v1.1.3 — Auto-Detect IAs & Smart Fallback
5. Description: (usar RELEASE-1.1.3.md)
6. Attach: clawrafaelia-suggestions-1.1.3.vsix
7. Publish! ✅

PASSO 2: Publicar no Marketplace
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Option 2: Fazer login
  $ vsce login RafaelBatista
  (Cole seu Personal Access Token)

Option 3: Publicar
  $ vsce publish --packagePath clawrafaelia-suggestions-1.1.3.vsix
  (Requer autenticação do passo anterior)

PASSO 3: Verificar
━━━━━━━━━━━━━━━━
Option 4: Abrir Marketplace
  https://marketplace.visualstudio.com/items?itemName=RafaelBatista.clawrafaelia-suggestions

COMANDOS RÁPIDOS
━━━━━━━━━━━━━━
# Ver status
vsce ls

# Login
vsce login RafaelBatista

# Publicar
cd ~/OneDrive/ClawRafaelIA/vscode-extension
vsce publish --packagePath clawrafaelia-suggestions-1.1.3.vsix

# Info
vsce show RafaelBatista.clawrafaelia-suggestions

DOCUMENTAÇÃO COMPLETA
━━━━━━━━━━━━━━━━━━━━
Veja: PUBLISH-V1.1.3-GUIDE.md

HELP
        ;;
    
    0)
        success "Até logo!"
        exit 0
        ;;
    
    *)
        error "Opção inválida"
        ;;
esac

echo ""
