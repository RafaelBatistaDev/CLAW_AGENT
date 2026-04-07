#!/bin/bash

################################################################################
# ACTIVATE.sh - Script de Ativação do Agente CLAW_RAFAEL_IA
#
# Este script ativa o agente para uso global no terminal.
# Copie e cole este arquivo em qualquer PC e execute:
#   bash ACTIVATE.sh
#
# Funcionalidades:
# - Detecta o local do projeto automaticamente
# - Cria alias 'agent' para uso imediato
# - Configura variáveis de ambiente
# - Valida a instalação
# - Suporta bash e zsh
#
################################################################################

set -e

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# Variáveis globais
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"
AGENT_SCRIPT="$PROJECT_ROOT/automation/my_scripts/agent.py"
CONFIG_DIR="${HOME}/.claw/config"
CONFIG_FILE="${CONFIG_DIR}/.claude.json"
SHELL_CONFIG=""

################################################################################
# FUNÇÕES
################################################################################

print_banner() {
    clear
    echo -e "${MAGENTA}"
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║       🚀 ATIVAÇÃO DO AGENTE CLAW_RAFAEL_IA                 ║"
    echo "║                                                           ║"
    echo "║  Preparando seu agente de IA para uso global no terminal ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_step() {
    echo -e "${CYAN}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

validate_project() {
    print_step "Validando estrutura do projeto..."
    
    if [[ ! -f "$AGENT_SCRIPT" ]]; then
        print_error "Agent não encontrado em: $AGENT_SCRIPT"
        exit 1
    fi
    
    if [[ ! -x "$AGENT_SCRIPT" ]]; then
        chmod +x "$AGENT_SCRIPT"
        print_success "Permissões de execução adicionadas"
    fi
    
    print_success "Estrutura do projeto validada"
    print_info "Localização: $PROJECT_ROOT"
}

setup_config_dir() {
    print_step "Configurando diretório de configuração..."
    
    mkdir -p "$CONFIG_DIR"
    print_success "Diretório criado: $CONFIG_DIR"
    
    if [[ ! -f "$CONFIG_FILE" ]]; then
        print_warning "Arquivo de configuração não encontrado"
        create_config_template
    else
        print_success "Arquivo de configuração encontrado"
    fi
}

create_config_template() {
    print_step "Criando arquivo de configuração..."
    
    cat > "$CONFIG_FILE" << 'EOF'
{
  "project": {
    "name": "ClawRafaelIA",
    "description": "Agente de IA com detecção automática de linguagem",
    "version": "1.0.0"
  },
  "api": {
    "google": {
      "key": "${GOOGLE_GEMINI_API_KEY}",
      "model": "gemini-2.0-flash",
      "maxTokens": 2000
    }
  },
  "agent": {
    "autodetect": true,
    "supportedLanguages": [
      "python", "javascript", "typescript", "rust", "go", "csharp", "java", "cpp"
    ],
    "features": {
      "analyze": true,
      "improve": true,
      "document": true,
      "test": true
    }
  }
}
EOF
    
    print_success "Template de configuração criado"
    print_warning "IMPORTANTE: Configure sua chave Google Gemini em:"
    echo -e "${CYAN}  $CONFIG_FILE${NC}"
}

detect_shell() {
    print_step "Detectando shell..."
    
    if [[ -f "$HOME/.zshrc" ]]; then
        SHELL_CONFIG="$HOME/.zshrc"
        print_success "Detectado: zsh"
    elif [[ -f "$HOME/.bashrc" ]]; then
        SHELL_CONFIG="$HOME/.bashrc"
        print_success "Detectado: bash"
    elif [[ -f "$HOME/.bash_profile" ]]; then
        SHELL_CONFIG="$HOME/.bash_profile"
        print_success "Detectado: bash profile"
    else
        print_error "Nenhum arquivo de configuração de shell encontrado"
        exit 1
    fi
}

create_alias() {
    print_step "Criando alias 'agent'..."
    
    local alias_line="alias agent='python3 $AGENT_SCRIPT'"
    
    # Verificar se alias já existe
    if grep -q "alias agent=" "$SHELL_CONFIG" 2>/dev/null; then
        print_warning "Alias 'agent' já existe em $SHELL_CONFIG"
        print_step "Atualizando alias..."
        
        # Remover alias antigo
        sed -i.bak "/alias agent=/d" "$SHELL_CONFIG"
        rm -f "${SHELL_CONFIG}.bak"
    fi
    
    # Adicionar alias novo
    echo "" >> "$SHELL_CONFIG"
    echo "# Agente CLAW_RAFAEL_IA (Python 3) - Ativado em $(date +%Y-%m-%d)" >> "$SHELL_CONFIG"
    echo "export CLAWRAFAELIA_HOME='$PROJECT_ROOT'" >> "$SHELL_CONFIG"
    echo "export PATH=\"\$PATH:$PROJECT_ROOT/automation/my_scripts\"" >> "$SHELL_CONFIG"
    echo "$alias_line" >> "$SHELL_CONFIG"
    
    print_success "Alias Python 3 criado com sucesso"
}

test_installation() {
    print_step "Testando instalação..."
    
    if ! command -v python3 &> /dev/null; then
        print_error "python3 não encontrado (necessário)"
        return 1
    fi
    
    # Testar se agent.py funciona
    if python3 "$AGENT_SCRIPT" help &> /dev/null; then
        print_success "Agent.py (Python 3) está funcional"
    else
        print_warning "Não foi possível verificar agent.py completamente"
    fi
}

print_summary() {
    echo ""
    echo -e "${MAGENTA}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${MAGENTA}║                  ✓ ATIVAÇÃO CONCLUÍDA!                   ║${NC}"
    echo -e "${MAGENTA}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    echo -e "${GREEN}📋 Resumo da Instalação:${NC}"
    echo -e "  ${CYAN}Projeto:${NC}      $PROJECT_ROOT"
    echo -e "  ${CYAN}Shell:${NC}        $SHELL_CONFIG"
    echo -e "  ${CYAN}Config:${NC}       $CONFIG_FILE"
    echo -e "  ${CYAN}Alias:${NC}        agent"
    echo ""
    
    echo -e "${YELLOW}⚠️  PRÓXIMOS PASSOS:${NC}"
    echo ""
    echo "1. Recarregue seu shell:"
    echo -e "   ${CYAN}source $SHELL_CONFIG${NC}"
    echo ""
    echo "2. Configure sua chave Google Gemini:"
    echo -e "   ${CYAN}nano $CONFIG_FILE${NC}"
    echo "   (Substitua 'COLOQUE_SUA_CHAVE_AQUI' pela sua chave real)"
    echo ""
    echo "3. Teste o agente:"
    echo -e "   ${CYAN}agent status${NC}"
    echo ""
    
    echo -e "${GREEN}💡 Uso Rápido:${NC}"
    echo -e "  ${CYAN}agent analyze arquivo.py${NC}     # Analisar código"
    echo -e "  ${CYAN}agent improve arquivo.rs${NC}     # Melhorar código"
    echo -e "  ${CYAN}agent document arquivo.ts${NC}   # Documentar"
    echo -e "  ${CYAN}agent test arquivo.js${NC}       # Gerar testes"
    echo -e "  ${CYAN}agent help${NC}                   # Ver ajuda completa"
    echo ""
    
    echo -e "${BLUE}📚 Documentação:${NC}"
    echo -e "  • AGENTE.md - Guia completo do agente"
    echo -e "  • PRIMEIRO-USO.md - Primeiros passos"
    echo -e "  • CLAUDE.md - Configurações avançadas"
    echo ""
}

print_transfer_instructions() {
    echo ""
    echo -e "${MAGENTA}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${MAGENTA}║             📦 COMO TRANSFERIR PARA OUTRO PC             ║${NC}"
    echo -e "${MAGENTA}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    echo -e "${YELLOW}Para usar em outro PC:${NC}"
    echo ""
    echo "1. Copie toda a pasta ClawRafaelIA para o novo PC"
    echo ""
    echo "2. Abra um terminal no novo PC"
    echo ""
    echo "3. Execute este script:"
    echo -e "   ${CYAN}bash /caminho/para/ClawRafaelIA/ACTIVATE.sh${NC}"
    echo ""
    echo "4. O script fará todo o resto automaticamente!"
    echo ""
}

main() {
    print_banner
    
    print_step "Iniciando processo de ativação..."
    echo ""
    
    # Executar validações e setup
    validate_project
    echo ""
    
    setup_config_dir
    echo ""
    
    detect_shell
    echo ""
    
    create_alias
    echo ""
    
    test_installation
    echo ""
    
    # Imprimir resumo
    print_summary
    print_transfer_instructions
    
    echo -e "${GREEN}🎉 Seu agente está pronto para uso!${NC}"
    echo ""
    echo -e "${CYAN}Execute agora:${NC} ${YELLOW}source $SHELL_CONFIG${NC}"
    echo ""
}

# Executar main
main
