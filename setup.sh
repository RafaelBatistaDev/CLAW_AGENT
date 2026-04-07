#!/usr/bin/env bash
# 🚀 SETUP RÁPIDO — CLAW VS Code Extension
# Instala e configura a extensão automaticamente
# 
# Uso:
#   bash setup.sh                    # Setup completo
#   bash setup.sh --dev              # Modo desenvolvimento (watch)
#   bash setup.sh --package          # Empacotar .vsix para release

set -euo pipefail

# Cores
G="\033[0;32m"
B="\033[0;34m"
Y="\033[1;33m"
R="\033[0;31m"
N="\033[0m"

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="${1:-install}"

echo -e "${B}╔════════════════════════════════════════════════════════════════╗${N}"
echo -e "${B}║${N}  🚀 CLAW VS Code Extension - Setup Automático"
echo -e "${B}║${N}  Modo: ${Y}${MODE}${N}"
echo -e "${B}╚════════════════════════════════════════════════════════════════╝${N}"
echo ""

# ════════════════════════════════════════════════════════════════════════════════
# 1. VALIDAR AMBIENTE
# ════════════════════════════════════════════════════════════════════════════════

echo -e "${B}📋 Validando ambiente...${N}"

# Verificar Node.js
if ! command -v node &> /dev/null; then
    echo -e "${R}❌ Node.js não encontrado. Instale em: https://nodejs.org${N}"
    exit 1
fi
NODE_VERSION=$(node -v)
echo -e "${G}✅ Node.js:${N} $NODE_VERSION"

# Verificar npm
if ! command -v npm &> /dev/null; then
    echo -e "${R}❌ npm não encontrado${N}"
    exit 1
fi
NPM_VERSION=$(npm -v)
echo -e "${G}✅ npm:${N} $NPM_VERSION"

# Verificar VS Code
if command -v code &> /dev/null; then
    VS_CODE_VERSION=$(code --version 2>/dev/null | head -1)
    echo -e "${G}✅ VS Code:${N} $VS_CODE_VERSION"
else
    echo -e "${Y}⚠️  VS Code não encontrado no PATH${N}"
    echo -e "${Y}   (Pode instalar depois manualmente)${N}"
fi

# Verificar agent.py
AGENT_PATH="$HOME/OneDrive/ClawRafaelIA/automation/my_scripts/agent.py"
if [ -f "$AGENT_PATH" ]; then
    echo -e "${G}✅ agent.py:${N} encontrado em $AGENT_PATH"
else
    echo -e "${R}❌ agent.py não encontrado em $AGENT_PATH${N}"
    echo -e "${Y}   (Extension funcionará com fallback local)${N}"
fi

echo ""

# ════════════════════════════════════════════════════════════════════════════════
# 2. INSTALAR DEPENDÊNCIAS
# ════════════════════════════════════════════════════════════════════════════════

echo -e "${B}📦 Instalando dependências...${N}"

# Criar .npmrc para aceitar permissões
if [ ! -f "$DIR/.npmrc" ]; then
    echo "audit=false" > "$DIR/.npmrc"
fi

cd "$DIR"
npm install 2>/dev/null || {
    echo -e "${R}❌ Erro ao instalar dependências${N}"
    exit 1
}

echo -e "${G}✅ Dependências instaladas${N}"
echo ""

# ════════════════════════════════════════════════════════════════════════════════
# 3. COMPILAR
# ════════════════════════════════════════════════════════════════════════════════

echo -e "${B}🔨 Compilando TypeScript...${N}"

npm run compile 2>/dev/null || {
    echo -e "${R}❌ Erro ao compilar${N}"
    exit 1
}

echo -e "${G}✅ Compilação completa${N}"
echo ""

# ════════════════════════════════════════════════════════════════════════════════
# 4. AÇÕES ESPECÍFICAS DO MODO
# ════════════════════════════════════════════════════════════════════════════════

case "$MODE" in
    --dev|dev)
        echo -e "${B}⌚ Modo DESENVOLVIMENTO (watch mode)${N}"
        echo -e "${Y}Pressione Ctrl+C para parar${N}"
        npm run dev
        ;;
    
    --package|package)
        echo -e "${B}📦 Empacotando para release...${N}"
        npm run compile:prod 2>/dev/null
        npm run package 2>/dev/null || {
            echo -e "${Y}⚠️  vsce não instalado globalmente${N}"
            echo -e "${Y}   Instale com: npm install -g vsce${N}"
        }
        
        VSIX_FILE=$(ls -t "$DIR"/*.vsix 2>/dev/null | head -1)
        if [ -f "$VSIX_FILE" ]; then
            echo -e "${G}✅ Pacote criado:${N} $VSIX_FILE"
        fi
        ;;
    
    --install|install|default)
        echo -e "${B}📥 Instalando extensão no VS Code...${N}"
        
        if command -v code &> /dev/null; then
            # Criar vsix temporário
            npm run package >/dev/null 2>&1 || true
            
            VSIX_FILE=$(ls -t "$DIR"/*.vsix 2>/dev/null | head -1)
            if [ -f "$VSIX_FILE" ]; then
                code --install-extension "$VSIX_FILE" 2>/dev/null || {
                    echo -e "${Y}⚠️  Instalação automática falhou${N}"
                    echo -e "${Y}   Instale manualmente: code --install-extension $VSIX_FILE${N}"
                }
                echo -e "${G}✅ Extensão instalada${N}"
            else
                echo -e "${Y}⚠️  .vsix não gerado${N}"
                echo -e "${Y}   Execute: npm run package${N}"
            fi
        else
            echo -e "${Y}⚠️  VS Code não encontrado${N}"
            echo -e "${Y}   Após instalar VS Code, execute:${N}"
            echo -e "${Y}   code --install-extension ./clawrafaelia-suggestions.vsix${N}"
        fi
        ;;
    
    *)
        echo -e "${R}❌ Modo desconhecido: $MODE${N}"
        echo -e "Usos:"
        echo -e "  bash setup.sh              # Install (padrão)"
        echo -e "  bash setup.sh --dev        # Desenvolvimento (watch)"
        echo -e "  bash setup.sh --package    # Empacotar para release"
        exit 1
        ;;
esac

echo ""
echo -e "${B}╔════════════════════════════════════════════════════════════════╗${N}"
echo -e "${B}║${N}  ${G}✅ Setup completado!${N}"
echo -e "${B}║${N}"
echo -e "${B}║${N}  📖 Próximos passos:"
echo -e "${B}║${N}     1. Abra VS Code"
echo -e "${B}║${N}     2. Vá para Extensions (Ctrl+Shift+X)"
echo -e "${B}║${N}     3. Procure por 'CLAW'"
echo -e "${B}║${N}     4. Clique Install"
echo -e "${B}║${N}"
echo -e "${B}║${N}  ⚙️  Configurar em Settings:"
echo -e "${B}║${N}     Ctrl+, → clawrafaelia"
echo -e "${B}║${N}"
echo -e "${B}║${N}  💻 Começar a digitar em qualquer arquivo!"
echo -e "${B}╚════════════════════════════════════════════════════════════════╝${N}"
