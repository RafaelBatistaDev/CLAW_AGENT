#!/bin/bash

################################################################################
# INSTALLATION GUIDE - ClawRafaelIA Template
# Leia este arquivo após clonar/copiar o template
################################################################################

cat << 'EOF'

╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                     🦞 ClawRafaelIA v1.0.0 - Tutorial                       ║
║                                                                              ║
║  Template reutilizável para novos projetos e máquinas em 30 segundos        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

📍 INSTALAÇÃO:  git clone <repo> && cd claw-agent

ESTRUTURA:
├── bin/                              Binários compilados
│   └── claw                          Execução Claw (placeholder)
│
├── config/                           Configurações e templates
│   ├── .claude.json                  Chaves de API e limites
│   └── CLAUDE.template.md            Guia de regras para projetos
│
├── automation/my_scripts/            Scripts de automação
│   ├── setup.sh                      Setup inicial
│   ├── status.sh                     Verificação de saúde
│   ├── panic.sh                      Emergency stop
│   └── repair.sh                     Reparo automático
│
└── environment/.devcontainer/        Container VS Code
    ├── devcontainer.json             Configuração container
    └── Dockerfile                    Imagem Docker


═══════════════════════════════════════════════════════════════════════════════
PASSO 1️⃣: Configuração Inicial (AGORA)
═══════════════════════════════════════════════════════════════════════════════

a) Editar chaves de API:

   vim ~/.claw/config/.claude.json

   Substituir os placeholders:
   - "your-api-key-here"       → sk-ant-XXXX...
   - "your-github-token-here"  → ghp_XXXX...

   (Criar pasta se não existir: mkdir -p ~/.claw/config)


b) Instalar em /usr/local/bin (opcional agora):

   sudo cp bin/claw /usr/local/bin/
   chmod +x /usr/local/bin/claw


═══════════════════════════════════════════════════════════════════════════════
PASSO 2️⃣: Usar em um Novo Projeto (quando necessário)
═══════════════════════════════════════════════════════════════════════════════

EXEMPLO: Iniciar um projeto .NET 10

   cd ~/projects/meu-projeto-dotnet

   # Copiar estrutura Claw
   cp config/CLAUDE.template.md ./CLAUDE.md
   cp -r environment/.devcontainer ./.devcontainer
   cp -r automation ./.

   # Personalizar CLAUDE.md:
   vim ./CLAUDE.md
   # - Trocar "Languages: [Rust/Python/TypeScript/etc]" → "Languages: C#"
   # - Trocar "Frameworks: [...]" → "Frameworks: .NET 10"
   # - Trocar comandos de build/test/lint para .NET

   # Validar ambiente:
   ./automation/my_scripts/status.sh

   # Pronto! Começar desenvolvimento


═══════════════════════════════════════════════════════════════════════════════
PASSO 3️⃣: Usar Container VS Code (Docker)
═══════════════════════════════════════════════════════════════════════════════

   1. Clonar projeto (com .devcontainer copiado)
   2. Abrir em VS Code
   3. Pressionar: Ctrl+Shift+P
   4. Digitar: "Reopen in Container"
   5. Aguardar ~2 min (primeira execução)

   O container já virá com:
   ✓ Rust (stable + clippy + rustfmt)
   ✓ Python 3.11 (+ pytest, black, pylint)
   ✓ Git, curl, build-essential
   ✓ Claw configurado


═══════════════════════════════════════════════════════════════════════════════
PASSO 4️⃣: Scripts Disponíveis
═══════════════════════════════════════════════════════════════════════════════

status.sh    → ./automation/my_scripts/status.sh
              Mostra: testes, cobertura, environment, dependências

panic.sh     → ./automation/my_scripts/panic.sh "erro"
              Para execução, notifica Discord/Slack, cria issue GitHub

repair.sh    → ./automation/my_scripts/repair.sh
              Limpa cache, recompila, reinstala dependências

setup.sh     → ./automation/my_scripts/setup.sh
              Instalação inicial do projeto


═══════════════════════════════════════════════════════════════════════════════
PASSO 5️⃣: Variáveis de Ambiente (Opcionais)
═══════════════════════════════════════════════════════════════════════════════

Adicionar ao ~/.bashrc ou ~/.zshrc:

   export ANTHROPIC_API_KEY="sk-ant-..."
   export GITHUB_TOKEN="ghp_..."
   export DISCORD_WEBHOOK="https://discord.com/api/webhooks/..."
   export LOG_LEVEL="debug"  # ou "info", "warn"

Depois recarregar:

   source ~/.bashrc  # ou ~/.zshrc


═══════════════════════════════════════════════════════════════════════════════
CHECKLIST RÁPIDO
═══════════════════════════════════════════════════════════════════════════════

□ Copiei CLAUDE.template.md para novo projeto
□ Copiei .devcontainer para novo projeto
□ Adaptei CLAUDE.md para meu stack (.NET, Python, etc)
□ Configurei .claude.json com minhas chaves
□ Rodei ./automation/my_scripts/status.sh (sucesso!)
□ Pronto para começar


═══════════════════════════════════════════════════════════════════════════════
TROUBLESHOOTING
═══════════════════════════════════════════════════════════════════════════════

P: "claw: command not found"
R: sudo cp bin/claw /usr/local/bin/ && chmod +x /usr/local/bin/claw

P: "status.sh: permission denied"
R: chmod +x automation/my_scripts/*.sh

P: "API key invalid"
R: vim ~/.claw/config/.claude.json
   (procurar por "your-api-key-here" e substituir)

P: "Container não inicia em VS Code"
R: Ctrl+Shift+P > "Dev Containers: Rebuild Container"

P: "Testes falhando"
R: ./automation/my_scripts/repair.sh


═══════════════════════════════════════════════════════════════════════════════
PRÓXIMOS PASSOS
═══════════════════════════════════════════════════════════════════════════════

❶ Leia:     README.md (visão geral)
❷ Setup:    SETUP.md (configuração do início)
❸ Rápido:   QUICKSTART.md (30 segundos)
❹ Exemplo:  Crie um projeto teste e copie a estrutura


═══════════════════════════════════════════════════════════════════════════════
CUSTOMIZAÇÃO
═══════════════════════════════════════════════════════════════════════════════

Adicionar seus próprios scripts:

   1. Criar: automation/my_scripts/seu_script.sh
   2. Chmod: chmod +x automation/my_scripts/seu_script.sh
   3. Documentar em CLAUDE.md

Customizações por projeto:

   1. Copie CLAUDE.template.md → ./CLAUDE.md
   2. Edite ./CLAUDE.md conforme necessário
   3. Crie .claude/settings.local.json para overrides


═══════════════════════════════════════════════════════════════════════════════

Criado: 5 de abril de 2026
Versão: 1.0.0
Última atualização: $(date)

Para mais detalhes, abra: README.md ou SETUP.md

═══════════════════════════════════════════════════════════════════════════════

EOF
