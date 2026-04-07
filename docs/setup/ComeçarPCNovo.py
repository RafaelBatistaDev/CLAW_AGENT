#!/usr/bin/env python3
"""
🤖 SETUP DO AGENTE CLAW_AGENT — Para Novo PC

Este guia explica como ativar o agente em um novo computador.

📋 ANTES DE COMEÇAR:
   ✓ Clone este repositório: git clone <repo> claw-agent
   ✓ Ou copie a pasta para seu computador
   ✓ Certifique-se que Python 3.7+ está instalado (python3 --version)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 SETUP RÁPIDO (3 Passos — 2 Minutos)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PASSO 1: Clonar ou Copiar a Pasta
────────────────────────────────────────────────────────────

Via Git:
  git clone https://github.com/seu-usuario/claw-agent.git
  cd claw-agent

Ou via cópia manual:
  1. Copie a pasta para seu HOME
  2. cd ~/claw-agent (ou onde quer que tenha copiado)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PASSO 2: Executar Script de Ativação
────────────────────────────────────────────────────────────

Abra terminal e execute:

  bash docs/setup/ACTIVATE.sh && source ~/.bashrc

⏱️  Tempo: ~30 segundos

O que faz ACTIVATE.sh:
  ✓ Configura alias 'agent' no ~/.bashrc
  ✓ Cria diretório ~/.claw/config/
  ✓ Cria diretório ~/.claw/cache/
  ✓ Copia configurações padrão

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PASSO 3: Testar o Agente
────────────────────────────────────────────────────────────

Teste rápido (sem usar API):

  agent status
  agent help

Se funcionar: 🎉 Parabéns! Seu agente está ativo!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📖 USANDO O AGENTE — Comandos Principais
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Análise de código:
  agent analyze seu_arquivo.py    # Encontra bugs
  agent improve seu_arquivo.py    # Refatora e melhora
  agent document seu_arquivo.py   # Gera documentação
  agent test seu_arquivo.py       # Cria testes

Perguntas e pesquisa:
  agent ask "sua pergunta aqui"
  agent ask "como fazer X em Python?"

Manutenção:
  agent status                     # Verifica status
  agent help                       # Mostra ajuda completa

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 EDITAR E RECARREGAR agent.py (Para Desenvolvedores)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Se precisar editar agent.py:

  1. Abra no editor:
     code automation/my_scripts/agent.py

  2. Salve (Ctrl+S)

  3. Use normalmente (cache é automático):
     agent analyze seu_arquivo.py

Ou para teste imediato:
  python3 automation/my_scripts/agent.py analyze seu_arquivo.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚙️  CUSTOMIZAÇÃO (Opcional)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Adicione sua chave Google Gemini:

   mkdir -p ~/.claw/config/
   cp config/agents.json.template ~/.claw/config/agents.json
   nano ~/.claw/config/agents.json
   # Substitua ${GOOGLE_GEMINI_API_KEY} pela sua chave real

2. Se a pasta claw-agent está em outro local:

   nano ~/.bashrc
   # Atualize: export CLAW_AGENT_HOME=/seu/caminho/claw-agent
   source ~/.bashrc

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⛔ TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Q: "agent: command not found"
A: Execute: source ~/.bashrc

Q: "Permission denied"
A: chmod +x automation/my_scripts/agent.py

Q: "API lenta ou em branco"
A: Verifique chave em ~/.claw/config/agents.json
   grep GOOGLE_GEMINI ~/.claw/config/agents.json

Q: "Erro de módulo Python"
A: agent.py usa apenas bibliotecas built-in (Python 3.7+)
   python3 --version

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 DOCUMENTAÇÃO COMPLETA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  - README.md .............. Visão geral do projeto
  - SETUP.md ............... Configuração completa
  - QUICKSTART.md .......... Referência rápida
  - docs/examples/ ......... Exemplos práticos

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Tudo pronto! Bom uso! 🚀

Data: 6 de abril de 2026
Versão: agent.py (Python 3)
Status: ✅ PRODUCTION READY

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
agent-reload