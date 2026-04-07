#!/usr/bin/env bash
# ====================================================================
# CLAW Release Automation Script
# Automatiza: version bump → build → tag → push → GitHub Release
# ====================================================================

set -euo pipefail
IFS=$'\n\t'

# ── Cores ──────────────────────────────────────────────────────────
G="\033[1;32m"    # Verde
B="\033[1;34m"    # Azul
Y="\033[1;33m"    # Amarelo
R="\033[1;31m"    # Vermelho
N="\033[0m"       # Reset

# ── Funções de Output ──────────────────────────────────────────────
log()     { echo -e "${B}[INFO]${N}  $*"; }
success() { echo -e "${G}[OK]${N}    $*"; }
warn()    { echo -e "${Y}[WARN]${N}  $*"; }
die()     { echo -e "${R}[ERROR]${N} $*"; exit 1; }

# ── Paths ──────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"
PACKAGE_JSON="$PROJECT_ROOT/package.json"

# ── Verificações Iniciais ──────────────────────────────────────────
[[ -f "$PACKAGE_JSON" ]] || die "package.json não encontrado em $PROJECT_ROOT"
[[ -x "$(command -v git)" ]] || die "git não encontrado"
[[ -x "$(command -v npm)" ]] || die "npm não encontrado"

# ── Detectar Versão Atual ──────────────────────────────────────────
CURRENT_VERSION=$(grep '"version"' "$PACKAGE_JSON" | head -1 | sed 's/.*"version": "\([^"]*\)".*/\1/')

log "CLAW Release Automation"
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log "Versão atual: $CURRENT_VERSION"
log ""

# ── Input: Nova Versão ─────────────────────────────────────────────
read -r -p "$(printf '%b' "${B}Nova versão (atual: $CURRENT_VERSION): ${N}")" NEW_VERSION

# ── Validar Versão ────────────────────────────────────────────────
if [[ ! $NEW_VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    die "Versão inválida! Use formato semântico: X.Y.Z"
fi

if [[ "$NEW_VERSION" == "$CURRENT_VERSION" ]]; then
    die "Nova versão não pode ser igual à atual ($CURRENT_VERSION)"
fi

log ""
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log "Plano de release:"
log "  • Versão: $CURRENT_VERSION → $NEW_VERSION"
log "  • Compilar & Empacotar"
log "  • Git commit & tag"
log "  • Push para GitHub"
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log ""

read -r -p "$(printf '%b' "${Y}Continuar? [s/N] ${N}")" confirm
[[ "${confirm,,}" == "s" ]] || { log "Cancelado"; exit 0; }

echo ""

# ── 1. Atualizar package.json ──────────────────────────────────────
log "1️⃣  Atualizando package.json..."
sed -i.bak "s/\"version\": \".*\"/\"version\": \"$NEW_VERSION\"/" "$PACKAGE_JSON"
rm -f "$PACKAGE_JSON.bak"
success "Versão atualizada para $NEW_VERSION"

# ── 2. Compilar ────────────────────────────────────────────────────
log "2️⃣  Compilando TypeScript..."
npm run compile:prod > /dev/null 2>&1 || die "Compilação falhou"
success "Compilação concluída"

# ── 3. Empacotar ───────────────────────────────────────────────────
log "3️⃣  Empacotando .vsix..."
VSIX_FILE="clawrafaelia-suggestions-$NEW_VERSION.vsix"
npm run package > /dev/null 2>&1 || die "Empacotamento falhou"
success "Arquivo criado: $VSIX_FILE"

# ── 4. Git Commit ──────────────────────────────────────────────────
log "4️⃣  Criando commit..."
git add package.json package-lock.json
git commit -m "Bump version to $NEW_VERSION" > /dev/null 2>&1
success "Commit criado"

# ── 5. Git Tag ─────────────────────────────────────────────────────
log "5️⃣  Criando tag..."
git tag -a "v$NEW_VERSION" -m "CLAW v$NEW_VERSION Release" > /dev/null 2>&1 || die "Falha ao criar tag"
success "Tag v$NEW_VERSION criada"

# ── 6. Git Push ────────────────────────────────────────────────────
log "6️⃣  Fazendo push para GitHub..."
git push origin main > /dev/null 2>&1 || warn "Push de branch falhou (pode estar atualizado)"
git push origin "v$NEW_VERSION" > /dev/null 2>&1 || die "Falha ao fazer push da tag"
success "Push concluído"

echo ""
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
success "Release v$NEW_VERSION pronta para publicar!"
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ── 7. Instruções para GitHub Release ──────────────────────────────
log "📋 Próximos passos (manual no GitHub):"
echo ""
echo "1️⃣  Acesse a URL:"
echo "   ${B}https://github.com/RafaelBatistaDev/CLAW---Sugest-es-Inline-com-IA/releases/new${N}"
echo ""
echo "2️⃣  Preencha:"
echo "   Tag version: v$NEW_VERSION"
echo "   Release title: CLAW v$NEW_VERSION"
echo ""
echo "3️⃣  Upload do arquivo:"
echo "   $(pwd)/$VSIX_FILE"
echo ""
echo "4️⃣  Clique 'Publish release'"
echo ""

# ── 8. Instruções para Marketplace (opcional) ──────────────────────
log "📦 Para publicar no Marketplace (opcional):"
echo ""
echo "   ${B}vsce publish --packagePath $VSIX_FILE${N}"
echo ""
echo "   ⚠️  Requer PAT válido configurado com 'vsce login RafaelBatista'"
echo ""

# ── Resumo ─────────────────────────────────────────────────────────
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log "Resumo:"
log "  ✅ package.json: $CURRENT_VERSION → $NEW_VERSION"
log "  ✅ .vsix: $VSIX_FILE ($(du -h "$VSIX_FILE" | cut -f1))"
log "  ✅ Git tag: v$NEW_VERSION"
log "  ✅ Git push: completado"
log ""
log "  📍 Status: Pronto para GitHub Release"
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
