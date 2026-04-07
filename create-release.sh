#!/usr/bin/env bash
# ====================================================================
# GitHub Release Automation Script
# Cria automaticamente releases no GitHub CLI
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

# ── Verificações ───────────────────────────────────────────────────
log "Verificando requisitos..."

command -v gh &> /dev/null || die "GitHub CLI (gh) não encontrado. Instale: https://cli.github.com"
command -v git &> /dev/null || die "Git não encontrado"

# ── Detectar Info do Repositório ───────────────────────────────────
REPO=$(git remote get-url origin 2>/dev/null | sed 's|.*:\(.*\)\.git|\1|' || echo "")
[[ -z "$REPO" ]] && die "Não é um repositório git válido"

OWNER=$(echo "$REPO" | cut -d'/' -f1)
REPO_NAME=$(echo "$REPO" | cut -d'/' -f2)

log "Repositório detectado: $OWNER/$REPO_NAME"

# ── Obter tags ─────────────────────────────────────────────────────
log "Obtendo versão atual..."

LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")

log "Última tag: $LATEST_TAG"
log "Procurando por novas tags..."

# Verificar se há tag não publicada
UNPUBLISHED_TAGS=$(git tag -l | while read tag; do
  if ! gh release view "$tag" &> /dev/null 2>&1; then
    echo "$tag"
  fi
done) || true

if [[ -z "$UNPUBLISHED_TAGS" ]]; then
  die "Nenhuma tag não publicada encontrada"
fi

log "Tags não publicadas found:"
echo "$UNPUBLISHED_TAGS"

echo ""
read -r -p "$(printf '%b' "${B}Qual tag publicar? ${N}")" VERSION_TO_RELEASE

# ── Validar Tag ────────────────────────────────────────────────────
if ! git rev-list "$VERSION_TO_RELEASE" &> /dev/null; then
  die "Tag $VERSION_TO_RELEASE não existe"
fi

log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log "Release: $VERSION_TO_RELEASE"
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ── Coletar Informações ────────────────────────────────────────────
read -r -p "$(printf '%b' "${B}Título da release: ${N}")" RELEASE_TITLE

read -r -p "$(printf '%b' "${B}Descrição (deixe em branco para padrão): ${N}")" RELEASE_BODY || true

# Descrição padrão
if [[ -z "$RELEASE_BODY" ]]; then
  RELEASE_BODY="🎉 Release $VERSION_TO_RELEASE

Mudanças nesta versão:
- Novos recursos
- Melhorias
- Bug fixes

Para detalhes completos, veja o [changelog](../../CHANGELOG.md)"
fi

# ── Procurar por arquivos .vsix ────────────────────────────────────
log ""
log "Procurando por artefatos .vsix..."

VSIX_FILE=$(find . -name "*.vsix" -type f 2>/dev/null | head -1)

if [[ -n "$VSIX_FILE" ]]; then
  log "Encontrado: $VSIX_FILE"
  INCLUDE_ASSETS=true
else
  warn "Nenhum arquivo .vsix encontrado"
  INCLUDE_ASSETS=false
fi

echo ""
read -r -p "$(printf '%b' "${Y}Incluir como pre-release? [s/N] ${N}")" IS_PRERELEASE || true
PRERELEASE_FLAG=""
if [[ "${IS_PRERELEASE,,}" == "s" ]]; then
  PRERELEASE_FLAG="--prerelease"
fi

# ── Confirmação ────────────────────────────────────────────────────
log ""
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log "Resumo:"
log "  Repositório: $OWNER/$REPO_NAME"
log "  Tag: $VERSION_TO_RELEASE"
log "  Título: $RELEASE_TITLE"
if $INCLUDE_ASSETS; then
  log "  Assets: $VSIX_FILE"
fi
if [[ -n "$PRERELEASE_FLAG" ]]; then
  log "  Pre-release: Sim"
fi
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

read -r -p "$(printf '%b' "${Y}Continuar? [s/N] ${N}")" CONFIRM || true
[[ "${CONFIRM,,}" == "s" ]] || { log "Cancelado"; exit 0; }

# ── Criar Release ──────────────────────────────────────────────────
log "Criando release no GitHub..."

# Build command
GH_CMD="gh release create $VERSION_TO_RELEASE"
GH_CMD="$GH_CMD --title='$RELEASE_TITLE'"
GH_CMD="$GH_CMD --notes='$RELEASE_BODY'"

if [[ -n "$PRERELEASE_FLAG" ]]; then
  GH_CMD="$GH_CMD $PRERELEASE_FLAG"
fi

if $INCLUDE_ASSETS && [[ -f "$VSIX_FILE" ]]; then
  GH_CMD="$GH_CMD '$VSIX_FILE'"
fi

# Execute
eval "$GH_CMD" || die "Falha ao criar release"

success "Release $VERSION_TO_RELEASE criada com sucesso!"

log ""
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
success "URL da release:"
echo "${B}https://github.com/$OWNER/$REPO_NAME/releases/tag/$VERSION_TO_RELEASE${N}"
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
