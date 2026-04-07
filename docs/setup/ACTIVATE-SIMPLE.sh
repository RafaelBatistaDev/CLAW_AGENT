#!/bin/bash

# ========================================================================================
# 🚀 ATIVA AGENTE CLAW_RAFAEL_IA - Script Ultra-Simples (Copiar & Colar)
# ========================================================================================
#
# USO:
# Copie e cole tudo isto no seu terminal para ativar instantaneamente em qualquer PC:
#
#   bash -c "$(curl -fsSL https://seu-repo/activate-simple.sh)"
#
# OU localmente:
#
#   bash ~/ClawRafaelIA/ACTIVATE-SIMPLE.sh
#
# ========================================================================================

set -e

# Detect project location automatically
if [[ -f "./ACTIVATE.sh" ]]; then
    # Running from ClawRafaelIA directory
    PROJECT_ROOT="$(pwd)"
elif [[ -f "$(dirname "$0")/ACTIVATE.sh" ]]; then
    # Running from subdirectory
    PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
elif [[ -f "$HOME/ClawRafaelIA/ACTIVATE.sh" ]]; then
    # Default location
    PROJECT_ROOT="$HOME/ClawRafaelIA"
else
    echo "❌ CLAW_RAFAEL_IA não encontrado!"
    echo "Copie a pasta para: $HOME/ClawRafaelIA"
    exit 1
fi

# Run main activation script
bash "$PROJECT_ROOT/ACTIVATE.sh"
