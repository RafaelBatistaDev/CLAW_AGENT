🤖 ClawRafaelIA - Distribuição Minimalista & Funcional

⚡ INSTALAÇÃO RÁPIDA (uma linha):

   python3 INSTALAR.py && source ~/.bashrc

✅ O QUE FAZ:
   • Cria ~/.local/{bin,log,share}
   • Configura variáveis de ambiente
   • Carrega aliases otimizados no ~/.bashrc
   • Valida Google Gemini API
   • Tudo pronto em ~5 segundos

📖 DEPOIS DE INSTALAR:

   source ~/.bashrc
   agent status                 # Ver status da API
   bug seu_arquivo.py           # Encontrar bugs
   refatora seu_codigo.py       # Refatorar
   documenta sua_classe.py      # Documentar
   testa seu_modulo.py          # Criar testes

📁 ARQUIVOS NESTA PASTA:
   • INSTALAR.py               - Script de instalação
   • agents.json               - Config de agentes
   • .claude.json              - Variáveis de ambiente  
   • README.txt                - Este arquivo

📳 ESTRUTURA REAL DO PROJETO:

   ClawRafaelIA/ (Minimalista)
   ├── automation/my_scripts/        ← Seu agente (intacto)
   │   ├── agent.py                  (71 KB - funcional)
   │   └── [ferramentas]
   ├── bin/claw                      ← Entry point único
   ├── config/                       ← Configuração
   ├── docs/                         ← Documentação
   ├── setup-package/                ← você está aqui
   │   ├── INSTALAR.py
   │   └── README.txt
   └── 📄 .md files (essenciais)

🎯 ALIASES CONSOLIDADOS (v1.0)

📝 NOMES EXPRESSIVOS (para scripts/leitura)
   refatora <arquivo>       ✨ Refatora e otimiza código
   documenta <arquivo>      📝 Gera documentação automática
   testa <arquivo>          ✅ Cria testes unitários

⚡ NOMES CURTOS (para terminal interativo)
   bug <arquivo>            🐛 Encontra bugs e problemas
   ref <arquivo>            ✨ Refatora (rápido)
   doc <arquivo>            📝 Documenta (rápido)
   tt <arquivo>             ✅ Testa (rápido)

🔧 COMANDOS PRINCIPAIS

   agent status             Ver status e configuração
   agent-ask "pergunta"     Fazer pergunta ao agent
   agent-reload             Recarregar agent (limpa cache)

💡 DIFERENCIAIS

   ✓ Minimalista - Sem redundâncias (src/, tests/ removidos)
   ✓ Funcional - 100% operacional e testado
   ✓ Expressivo - Aliases descritivos e claros
   ✓ Rápido - Digitação rápida (bug, ref, doc, tt)
   ✓ Inteligente - Cache semântico economiza API
   ✓ Automático - Contexto do projeto carregado automaticamente

🚀 EXEMPLOS DE USO

   # Terminal interativo (use aliases curtos)
   bug meu_script.py
   ref funcao.py
   doc Classe.py
   tt modulo.py

   # Scripts (use nomes expressivos para clareza)
   refatora arquivo.py
   documenta classe.py
   testa suite.py

   # Perguntas diretas
   agent-ask "como fazer X em Python?"
   agent-ask "qual é a melhor prática para Y?"

📚 DOCUMENTAÇÃO COMPLETA

   cat README-MINIMO.md          # Guia minimalista
   cat ~/.local/bin/ALIASES-CONSOLIDADO.txt  # Referência aliases

✨ PRONTO! Seu agente está 100% funcional.

