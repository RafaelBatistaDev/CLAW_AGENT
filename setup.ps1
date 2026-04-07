# 🚀 SETUP RÁPIDO — CLAW VS Code Extension (PowerShell)
# Instala e configura a extensão automaticamente
# 
# Uso:
#   .\setup.ps1                      # Setup completo
#   .\setup.ps1 -Mode "dev"          # Modo desenvolvimento
#   .\setup.ps1 -Mode "package"      # Empacotar para release

param(
    [string]$Mode = "install"
)

# Cores
$G = "`e[0;32m"
$B = "`e[0;34m"
$Y = "`e[1;33m"
$R = "`e[0;31m"
$N = "`e[0m"

function Log { param([string]$Msg, [string]$Level = "INFO")
    $colors = @{
        "INFO" = $B
        "OK"   = $G
        "WARN" = $Y
        "ERR"  = $R
    }
    $color = $colors[$Level]
    Write-Host "$color[$Level]$N $Msg"
}

function Run { param([string[]]$Cmd)
    try {
        $result = & $Cmd[0] $Cmd[1..($Cmd.Length-1)] 2>&1
        return @{success=$?; output=$result}
    } catch {
        return @{success=$false; output=$_.Exception.Message}
    }
}

Clear-Host
Write-Host ""
Write-Host "$B╔════════════════════════════════════════════════════════════════╗$N"
Write-Host "$B║$N  🚀 CLAW VS Code Extension - Setup Automático (PowerShell)"
Write-Host "$B║$N  Modo: $Y$Mode$N"
Write-Host "$B╚════════════════════════════════════════════════════════════════╝$N"
Write-Host ""

# ════════════════════════════════════════════════════════════════════════════════
# 1. VALIDAR AMBIENTE
# ════════════════════════════════════════════════════════════════════════════════

Log "Validando ambiente..." "INFO"

# Node.js
$node_check = Run @("node", "--version")
if ($node_check.success) {
    Log "Node.js: $($node_check.output)" "OK"
} else {
    Log "Node.js não encontrado. Instale em: https://nodejs.org" "ERR"
    exit 1
}

# npm
$npm_check = Run @("npm", "--version")
if ($npm_check.success) {
    Log "npm: $($npm_check.output)" "OK"
} else {
    Log "npm não encontrado" "ERR"
    exit 1
}

# VS Code
$vscode_check = Run @("code", "--version")
if ($vscode_check.success) {
    $vs_version = ($vscode_check.output -split '\n')[0]
    Log "VS Code: $vs_version" "OK"
} else {
    Log "VS Code não encontrado no PATH" "WARN"
    Log "(Pode instalar depois manualmente)" "WARN"
}

# agent.py
$agent_path = "$env:USERPROFILE\OneDrive\ClawRafaelIA\automation\my_scripts\agent.py"
if (Test-Path $agent_path) {
    Log "agent.py: encontrado" "OK"
} else {
    Log "agent.py não encontrado" "WARN"
    Log "(Extension funcionará com fallback local)" "WARN"
}

Write-Host ""

# ════════════════════════════════════════════════════════════════════════════════
# 2. INSTALAR DEPENDÊNCIAS
# ════════════════════════════════════════════════════════════════════════════════

Log "Instalando dependências..." "INFO"

$install_result = Run @("npm", "install")
if ($install_result.success) {
    Log "Dependências instaladas" "OK"
} else {
    Log "Erro ao instalar dependências" "ERR"
    exit 1
}

Write-Host ""

# ════════════════════════════════════════════════════════════════════════════════
# 3. COMPILAR
# ════════════════════════════════════════════════════════════════════════════════

Log "Compilando TypeScript..." "INFO"

$compile_result = Run @("npm", "run", "compile")
if ($compile_result.success) {
    Log "Compilação completa" "OK"
} else {
    Log "Erro ao compilar" "ERR"
    exit 1
}

Write-Host ""

# ════════════════════════════════════════════════════════════════════════════════
# 4. AÇÕES ESPECÍFICAS DO MODO
# ════════════════════════════════════════════════════════════════════════════════

switch ($Mode) {
    "dev" {
        Log "Modo DESENVOLVIMENTO (watch mode)" "WARN"
        Log "Pressione Ctrl+C para parar" "WARN"
        & npm run dev
        break
    }
    
    "package" {
        Log "Empacotando para release..." "INFO"
        $pkg_result = Run @("npm", "run", "package")
        if ($pkg_result.success) {
            $vsix = Get-ChildItem -Path "*.vsix" -ErrorAction SilentlyContinue | Sort-Object CreationTime -Descending | Select-Object -First 1
            if ($vsix) {
                Log "Pacote criado: $($vsix.Name)" "OK"
            }
        }
        break
    }
    
    "install" {
        Log "Instalando extensão no VS Code..." "INFO"
        
        $vscode_installed = (Run @("code", "--version")).success
        if ($vscode_installed) {
            $pkg_result = Run @("npm", "run", "package")
            $vsix = Get-ChildItem -Path "*.vsix" -ErrorAction SilentlyContinue | Sort-Object CreationTime -Descending | Select-Object -First 1
            
            if ($vsix) {
                $install_result = Run @("code", "--install-extension", $vsix.FullName)
                if ($install_result.success) {
                    Log "Extensão instalada" "OK"
                } else {
                    Log "Instalação automática falhou" "WARN"
                    Log "Instale manualmente: code --install-extension $($vsix.FullName)" "WARN"
                }
            } else {
                Log ".vsix não gerado" "WARN"
                Log "Execute: npm run package" "WARN"
            }
        } else {
            Log "VS Code não encontrado" "WARN"
            Log "Após instalar VS Code, execute:" "WARN"
            Log "code --install-extension ./clawrafaelia-suggestions.vsix" "WARN"
        }
        break
    }
    
    default {
        Log "Modo desconhecido: $Mode" "ERR"
        Log "Usos: install (padrão), dev, package" "INFO"
        exit 1
    }
}

Write-Host ""
Write-Host "$B╔════════════════════════════════════════════════════════════════╗$N"
Write-Host "$B║$N  $G✅ Setup completado!$N"
Write-Host "$B║$N"
Write-Host "$B║$N  📖 Próximos passos:"
Write-Host "$B║$N     1. Abra VS Code"
Write-Host "$B║$N     2. Vá para Extensions (Ctrl+Shift+X)"
Write-Host "$B║$N     3. Procure por 'CLAW'"
Write-Host "$B║$N     4. Clique Install"
Write-Host "$B║$N"
Write-Host "$B║$N  ⚙️  Configurar em Settings:"
Write-Host "$B║$N     Ctrl+, → clawrafaelia"
Write-Host "$B║$N"
Write-Host "$B║$N  💻 Começar a digitar em qualquer arquivo!"
Write-Host "$B╚════════════════════════════════════════════════════════════════╝$N"
