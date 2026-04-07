#!/usr/bin/env python3
"""
🤖 ClawRafaelIA - Setup Automático Completo
Comando único: python3 INSTALAR.py
Tempo: ~5 segundos
Resultado: Agente 100% pronto para usar
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

# Cores (códigos ANSI)
G = "\033[1;32m"   # Verde
B = "\033[1;34m"   # Azul
Y = "\033[1;33m"   # Amarelo
R = "\033[1;31m"   # Vermelho
N = "\033[0m"      # Reset

# Caminhos
HOME = Path.home().resolve()
LOCAL_BIN = HOME / ".local" / "bin"
LOCAL_LOG = HOME / ".local" / "log"
LOCAL_SHARE = HOME / ".local" / "share"
MARKER = LOCAL_SHARE / "claw_setup_complete.marker"
BASHRC = HOME / ".bashrc"

# Script está em setup-package/, parent é raiz projeto
SETUP_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SETUP_DIR.parent
AGENT_PY = PROJECT_ROOT / "automation" / "my_scripts" / "agent.py"

print(f"\n{B}▶ ClawRafaelIA Setup{N}\n")

# 1️⃣ Verificar Python
if sys.version_info < (3, 7):
    print(f"{R}✗ Python 3.7+ necessário{N}\n")
    sys.exit(1)

# 2️⃣ Verificar se já instalado (evitar instalação duplicada)
if MARKER.exists():
    print(f"{G}✓ Já instalado{N}\n")
    sys.exit(0)

# 3️⃣ Criar diretórios
print(f"{B}⋯ Criando diretórios...{N}", end=" ", flush=True)
LOCAL_BIN.mkdir(parents=True, exist_ok=True)
LOCAL_LOG.mkdir(parents=True, exist_ok=True)
LOCAL_SHARE.mkdir(parents=True, exist_ok=True)
print(f"{G}✓{N}")

# 4️⃣ Procurar agent.py
print(f"{B}⋯ Procurando agent.py...{N}", end=" ", flush=True)
if not AGENT_PY.exists():
    # Alternativas
    alternatives = [PROJECT_ROOT / "agent.py"]
    found = False
    for alt in alternatives:
        if alt.exists():
            AGENT_PY = alt
            found = True
            break
    if not found:
        print(f"{R}✗{N}\n  Erro: agent.py não encontrado\n")
        sys.exit(1)
print(f"{G}✓{N}")

# 5️⃣ Criar symlink
print(f"{B}⋯ Criando symlink...{N}", end=" ", flush=True)
agent_link = LOCAL_BIN / "agent"
if agent_link.exists() or agent_link.is_symlink():
    agent_link.unlink()
agent_link.symlink_to(AGENT_PY)
agent_link.chmod(0o755)
print(f"{G}✓{N}")

# 6️⃣ Adicionar alias no bashrc
print(f"{B}⋯ Configurando alias...{N}", end=" ", flush=True)
alias_cmd = f"alias agent='python3 {AGENT_PY}'"

if not BASHRC.exists():
    BASHRC.write_text(f"# ClawRafaelIA\n{alias_cmd}\n")
else:
    content = BASHRC.read_text()
    if "alias agent=" not in content:
        with open(BASHRC, "a") as f:
            f.write(f"\n# ClawRafaelIA ({datetime.now().strftime('%Y-%m-%d')})\n{alias_cmd}\n")
print(f"{G}✓{N}")

# 7️⃣ Criar marker
print(f"{B}⋯ Criando marker...{N}", end=" ", flush=True)
MARKER.write_text(f"Instalado: {datetime.now().isoformat()}\n")
print(f"{G}✓{N}")

# 8️⃣ Pronto!
print(f"\n{G}════════════════════════════════════════{N}")
print(f"{G}✅ PRONTO!{N}")
print(f"{G}════════════════════════════════════════{N}\n")

print(f"{B}Próximos passos:{N}")
print(f"  1. source ~/.bashrc")
print(f"  2. agent status")
print(f"  3. agent analyze arquivo.py\n")
