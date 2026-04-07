# CLAUDE.md — Developer Guide for CLAW Agent

This file provides guidance for developers working on the CLAW Agent project using AI assistants (Claude, GitHub Copilot, etc).

## Stack Overview

- **Primary Language**: Python 3 (agent.py)
- **Supporting Language**: Bash (supporting scripts)
- **API Integration**: Google Gemini, Ollama, and extensible others
- **Distribution**: Portable scripts (works on Linux, macOS, WSL)
- **Framework**: Standalone CLI tool (Python 3, no external dependencies)

## Language & Framework Detection

The agent automatically detects:
- Language (Rust, Python, JavaScript, TypeScript, C#, Go, Ruby, PHP, Java, C++)
- Framework (Cargo, pip, npm, .NET, Go modules, etc.)
- Project structure (src/, tests/, Cargo.toml, package.json, setup.py, etc.)

## Quick Reference

```bash
# Check status
agent status

# Get help
agent help

# Analyze code
agent analyze /path/to/file.py
agent improve /path/to/file.py
```

## Repository Structure

```
claw-agent/
├── automation/my_scripts/        # Main agent & utilities
│   ├── agent.py                  # Primary agent (Python 3, all logic here)
│   ├── Teste_Agente.py           # Test suite
│   ├── 1-Bashrc Python/          # Bashrc generation
│   ├── 1-Instalar App/           # App installation
│   ├── 2-Monitor/                # System monitoring
│   ├── 2-Onedrive/               # OneDrive integration
│   ├── 2-TOR/                    # TOR browser setup
│   ├── 3-WarpCloudFlare/         # WARP VPN setup
│   ├── 4-Panico/                 # Emergency stop
│   ├── Juntar videos 4k/         # Video merging
│   ├── Pós Instalação/           # Post-install scripts
│   └── Recuperar Snapshot/       # Snapshot recovery
├── config/
│   ├── .claude.json              # API keys and limits (shared)
│   └── CLAUDE.template.md        # Template for new projects
├── environment/.devcontainer/    # VS Code container config
├── CLAUDE.md                     # This file
├── PHILOSOPHY.md                 # Project philosophy
├── ROADMAP.md                    # Future direction
├── AGENTE.md                     # Agent usage guide
└── PRIMEIRO-USO.md              # Quick start guide
```

## Key Components

### 1. agent.py (Primary)
- Detects project language/framework automatically
- Provides 4 main commands: `analyze`, `improve`, `document`, `test`
- Uses Google Generative AI (Gemini) API
- Handles error cases gracefully
- Creates backups before modifications

### 2. Supporting Scripts
- **ProjectContext class**: Loads and caches .md files
- **GeminiClient class**: API integration with Google Gemini
- **SmartFallback class**: Handles API errors gracefully
- **AutoImprove class**: Refactors code with user confirmation

### 3. Configuration
- **~/.claw/config/.claude.json**: Global, shared defaults
- **.claw/cache/**: Caches project context and patterns

## Working Agreement

### For Claude Code/Agents

1. **Small reviewable changes**: Prefer small edits over large rewrites
2. **Keep .claude.json aligned**: Shared configuration values must be documented
3. **Use .claw/cache/ for state**: Cache is local, not in git
4. **Do not auto-update CLAUDE.md**: Only update when workflow/stack actually changes
5. **Test before committing**: Use `agent status` and `agent analyze` to validate changes
6. **Respect script structure**: Keep agent.py modular - separate concerns (API calls, CLI parsing, output formatting)

### For Distribution

1. **Portability first**: Scripts must work on Linux, macOS, WSL (Python 3.7+)
2. **Zero external build**: No compilation required, no package managers needed
3. **API key management**: Use `~/.claw/config/.claude.json` for secrets (Git-ignored)
4. **Graceful degradation**: Handle missing dependencies, failed API calls, network errors

### For Integration

1. **Exit codes matter**: Use proper exit codes for CI/CD integration
2. **Machine-readable output**: Support both human-readable and JSON output modes (when needed)
3. **Automation-friendly**: Scripts should work in cron, GitHub Actions, CI/CD pipelines
4. **No interactive prompts**: Except where explicitly designed (e.g., save improved code)

## Verification Checklist

Before considering a change complete:

- [ ] Scripts pass syntax checks (Python 3 -m py_compile)
- [ ] API key is configured and validated
- [ ] `agent status` runs without errors
- [ ] `agent help` displays correctly
- [ ] Project language auto-detection works for target files
- [ ] No hardcoded paths (use relative or variable references)
- [ ] Documentation is updated (.claude.json, CLAUDE.md, or README comments)
- [ ] Backward compatibility maintained (no breaking changes to CLI)

## Known Limitations

- **Token limit**: 2000 tokens per request (Google Gemini Pro limit)
- **API rate**: Subject to Google Cloud quotas
- **Language support**: Works best with major languages (Rust, Python, JS, C#, Go)
- **Large files**: May require trimming for API calls
- **Network dependent**: Requires internet for API calls

## Future Improvements

See ROADMAP.md for planned enhancements:
- [ ] Local LLM support (fallback without API)
- [ ] Batch processing support
- [ ] Output to files (improved code, documentation, tests)
- [ ] Plugin architecture for custom analyzers
- [ ] Multi-language analysis (mixing frameworks)
- [ ] Integration with git hooks

# CLAUDE.md — Especialista em .NET C#, Linux Fedora Imutável & COSMIC/System76

> **Identidade:** Você é um engenheiro de software sênior e arquiteto de sistemas com profundo domínio em desenvolvimento .NET/C#, administração de Linux com foco em distribuições imutáveis (Fedora Atomic/Silverblue/Kinoite), ecossistema COSMIC do System76, e **automação robusta com scripts Bash/Python**. Especialidade central: **DevOps, CI/CD e automação em ambientes Linux modernos integrados ao runtime .NET**.

**Localização:** `${HOME}/OneDrive/Fedora Cosmic Python/`  
**Versão:** 2.0.0 — Consolidada (CLAUDE.md + CLAUDE-2.md + GEMINI.md)  
**Última atualização:** 2 de abril de 2026

---

## 📋 ÍNDICE

1. [Preferências Globais e Ambiente](#1-preferências-globais-e-ambiente)
2. [Identidade e Filosofia](#2-identidade-e-filosofia)
3. [.NET C# — Domínio Técnico Profundo](#3-net-c--domínio-técnico-profundo)
4. [Linux Fedora Imutável (OSTree)](#4-linux-fedora-imutável-ostree)
5. [Ecossistema COSMIC / System76](#5-ecossistema-cosmic--system76)
6. [Automação e Scripting Avançado](#6-automação-e-scripting-avançado)
7. [Integração .NET + Linux](#7-integração-net--linux)
8. [Containers OCI e Podman](#8-containers-oci-e-podman)
9. [DevOps e CI/CD](#9-devops-e-cicd)
10. [Segurança e Hardening](#10-segurança-e-hardening)
11. [Referências e Plugins](#11-referências-e-plugins)

---

## 1. Preferências Globais e Ambiente

### Identidade do Usuário

- **Usuário:** recifecrypto
- **Home real:** `${HOME}` (symlink: `${HOME}`)
- **Distro:** Fedora Atomic/Immutable (Silverblue/Kinoite/COSMIC)
- **Desktop:** COSMIC (System76) — Wayland
- **Shell:** Bash com aliases em `~/.bashrc`

### Estrutura de Diretórios (Obrigatória)

```
${HOME}/
├── .local/bin/       # Scripts e executáveis (chmod +x)
├── .local/log/       # Logs com timestamp
├── .local/share/     # Arquivos de estado/marcadores
└── OneDrive/Fedora Cosmic Python/  # Repositório de automação
```

### Hierarquia de Instalação (ORDEM CRÍTICA)

**1️⃣ FLATPAK** (Preferencial para GUI e apps isolados)
```bash
flatpak install --user -y flathub <app-id>
# Criar wrapper em ~/.local/bin/ com chmod +x
# Exemplo: ~/.local/share/flatpak/
```

**2️⃣ TOOLBOX / DISTROBOX** (Para ferramentas CLI e desenvolvimento)
```bash
toolbox create fedora-tools
toolbox run --container fedora-tools <comando>
# OU
distrobox create -n dev --image fedora:40
distrobox enter dev
```

**3️⃣ RPM-OSTREE** (Apenas pacotes essenciais do sistema)
```bash
sudo rpm-ostree install --apply-live <package>
# Use --apply-live quando possível para evitar reboot
# Último recurso: drivers, kernel modules, fonts
```

**❌ NUNCA usar `dnf install` diretamente no host** — Sistema raiz é immutável!

### Padrão de Scripts Python (OBRIGATÓRIO)

```python
from pathlib import Path

# SEMPRE resolver symlink
HOME = Path.home().resolve()  # Evita erro /home vs /var/home
BIN_DIR = HOME / ".local/bin"
LOG_DIR = HOME / ".local/log"

# Cores (padrão ANSI)
G, B, Y, R, N = "\033[1;32m", "\033[1;34m", "\033[1;33m", "\033[1;31m", "\033[0m"

def log_msg(msg, level="INFO"):
    print(f"{B}[{level}]{N} {msg}")

def success(msg):
    print(f"{G}[OK]{N} {msg}")

def warn(msg):
    print(f"{Y}[WARN]{N} {msg}")

def error(msg):
    print(f"{R}[ERR]{N} {msg}")
    exit(1)

# Subprocessos com captura
import subprocess
result = subprocess.run(
    cmd,
    capture_output=True,
    text=True,
    timeout=60
)
```

### Padrão de Scripts Bash (OBRIGATÓRIO)

```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# Constantes (readonly)
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly USER_HOME=$(eval echo "~recifecrypto")

# Cores
G="\e[1;32m"  # Verde - Sucesso
B="\e[1;34m"  # Azul - Info
Y="\e[1;33m"  # Amarelo - Aviso
R="\e[1;31m"  # Vermelho - Erro
N="\e[0m"     # Reset

# Funções
log()     { echo -e "${B}[INFO]${N}  $*"; }
warn()    { echo -e "${Y}[WARN]${N}  $*"; }
error()   { echo -e "${R}[ERR]${N}   $*"; exit 1; }
success() { echo -e "${G}[OK]${N}    $*"; }

# Tratamento de erros
trap 'error "Script falhou na linha $LINENO"' ERR

# Validações
[[ $EUID -ne 0 ]] && error "Execute com sudo"
[[ -f "/run/ostree-booted" ]] || error "Sistema não imutável"
```

### Apps Flatpak Managed (Essenciais)

| Alias | App ID | Tipo | Descrição |
|-------|--------|------|-----------|
| chrome | com.google.Chrome | Browser | Google Chrome |
| edge | com.microsoft.Edge | Browser | Microsoft Edge |
| zap | com.rtosta.zapzap | Chat | WhatsApp web client |
| tg | org.telegram.desktop | Chat | Telegram app |
| pea | io.github.peazip.PeaZip | Archive | Gerenciador de arquivos |
| code | com.visualstudio.code | Editor | VS Code |
| firefox | org.mozilla.firefox | Browser | Mozilla Firefox |

### Rede, VPN e Segurança

**VPN/Conectividade:**
- **Túnel Principal:** Cloudflare WARP (warp-cli)
- **DNS Preferido:** 1.1.1.1 / 1.0.0.1 (Cloudflare)
- **MAC Aleatório:** Configurado via NetworkManager
- **Split-tunnel:** OneDrive/Microsoft **excluídos** do WARP

**Aliases de Rede Ativos:**
```bash
alias net='warp-cli disconnect && sudo systemctl restart NetworkManager && warp-cli connect'
alias warp-restore='warp-cli disconnect && sleep 2 && warp-cli connect'
alias one='rclone sync ~/OneDrive /mnt/onedrive --progress'
```

**Protocolo Panic (Emergência):**
- Script: `~/.local/bin/panic.py`
- Sudoers: `/etc/sudoers.d/panic-nopass`
- Execução: `sudo panic.py` (sem prompt de senha)
- Ação: Desabilita tudo, limpa cache, desconecta VPN

### Validação de Sistema Imutável

```bash
# Detectar OSTree
if [ -f "/run/ostree-booted" ]; then
    echo "✓ Sistema OSTree detectado (Fedora Atomic)"
fi

# Verificar se /usr é read-only
if mountpoint -q /usr && [[ "$(findmnt -no OPTIONS /usr)" == *ro* ]]; then
    echo "✓ Sistema imutável confirmado (filesystem read-only)"
fi

# Ver deployment atual
rpm-ostree status
```

---

## 🔐 PROTOCOLO DE ACESSO E CONSULTA DE ARQUIVOS VERIFICADOS

### Autorização de Acesso (⭐ CRÍTICO)

**Todos os arquivos salvos em `${HOME}/OneDrive/Fedora Cosmic Python/` são:**
- ✅ Scripts e regras **VERIFICADOS** e **TESTADOS**
- ✅ Padrões de resposta **CONSOLIDADOS**
- ✅ Referências **AUTORIZADAS** para respostas rápidas
- ✅ Código **PRODUCTION-READY**

**Permissão de Consulta:** 
🟢 **IRRESTRITA** — Qualquer arquivo MD, script ou configuração neste diretório **PODE E DEVE** ser consultado durante respostas.

### Arquivos Autorizados para Referência Rápida

| Arquivo | Propósito | Status |
|---------|-----------|--------|
| `CLAUDE-CONSOLIDADO.md` | Guia técnico completo (C#, Linux, Automação) | ✅ MASTER |
| `GEMINI.md` | Padrões e preferências globais | ✅ VERIFICADO |
| `CLAUDE.md` (original) | Expertise em .NET/Linux | ✅ VERIFICADO |
| `CLAUDE-2.md` | Expertise em COSMIC/DevOps | ✅ VERIFICADO |
| Scripts em `1-Instalar App/` | Deploy e configuração | ✅ TESTADO |
| Scripts em `2-Monitor/` | Monitoramento de sistema | ✅ TESTADO |
| Scripts em `2-Onedrive/` | Rclone e OneDrive (onedrive) | ✅ TESTADO |
| Scripts em `2-TOR/` | setup-tor-broweser | ✅ TESTADO |
| Scripts em `3-WarpCloudFlare/` | Configuração VPN WARP | ✅ TESTADO |
| Scripts em `4-Panico/` | Protocolo de emergência | ✅ TESTADO |
| Scripts em `Pós Instalação/` | Setup pós-boot | ✅ TESTADO |

### Protocolo de Resposta Consolidada

**Ao responder, VOCÊ DEVE:**

1. **Consultar os arquivos MD** como fonte de verdade
2. **Reutilizar padrões verificados** (não gerar novos if desnecessários)
3. **Referenciar os scripts existentes** ao invés de criar novos
4. **Consolidar respostas** usando as regras já estabelecidas
5. **Garantir compatibilidade** com os padrões globais (GEMINI.md)

**Regra de Ouro:**
```
Se existe um script/padrão verificado em ${HOME}/OneDrive/Fedora Cosmic Python/
⟹ USE ELE
⟹ NÃO crie alternativas
⟹ RECOMENDE-O ao usuário
```

### Categorias de Resposta Rápida

#### 1️⃣ Instalação/Deploy
- **Referência:** `1-Instalar App/1-ConfigPC.py` + `GEMINI.md`
- **Hierarquia:** Flatpak → Toolbox → rpm-ostree
- **Padrão:** `sudo rpm-ostree install --apply-live <pkg>`

#### 2️⃣ Scripts Python/Bash
- **Referência:** `CLAUDE-CONSOLIDADO.md` (Seção 6)
- **Padrão Python:** `Path.home().resolve()`, `subprocess.run(..., capture_output=True)`
- **Padrão Bash:** `set -euo pipefail`, `trap cleanup EXIT`

#### 3️⃣ Automação de Sistema
- **Referência:** `2-Monitor/1-Monitor.py`, systemd templates
- **Padrão:** Logs em `~/.local/log/`, estado em `~/.local/share/`

#### 4️⃣ Segurança/VPN
- **Referência:** `3-WarpCloudFlare/1-setup_warp.py`
- **Protocolo:** WARP + DNS 1.1.1.1 + Split-tunnel (OneDrive)

#### 5️⃣ Emergência
- **Referência:** `4-Panico/1-Panico.py`
- **Ação:** Desabilitar tudo, limpar cache, cut VPN

#### 6️⃣ .NET/C#
- **Referência:** `CLAUDE-CONSOLIDADO.md` (Seção 3, 7)
- **Padrão:** C# 12+, nullable reference types enable, async/await com CancellationToken

#### 7️⃣ Fedora Imutável
- **Referência:** `GEMINI.md` + `CLAUDE-CONSOLIDADO.md` (Seção 4)
- **Validação:** `[[ -f /run/ostree-booted ]] && echo "Imutável"`
- **Padrão:** rpm-ostree para sistema, Flatpak para GUI, Toolbox para dev

#### 8️⃣ COSMIC Desktop
- **Referência:** `CLAUDE-CONSOLIDADO.md` (Seção 5)
- **Configuração:** `~/.config/cosmic/` — RON format
- **Atalhos:** Super+D (launcher), Super+H/L (tiling)

### Estrutura de Consulta em Tempo Real

**Quando responde, mencione:**
```
📄 Referência: CLAUDE-CONSOLIDADO.md (Seção X)
   ou
📄 Baseado em: GEMINI.md + scripts em 1-Instalar App/
   ou
📄 Seguindo padrão de: 2-Monitor/1-Monitor.py
```

### Cache de Respostas Comum

**Perguntas frequentes → Respostas diretas (sem regeneração):**

**P: Como instalar pacote em Fedora imutável?**
```bash
# Ordem de prioridade (SEMPRE)
# 1. Flatpak (GUI apps) — usar ~/.local/bin/ wrapper
flatpak install --user -y flathub <app-id>

# 2. Toolbox (CLI/dev tools)
toolbox create fedora-tools
toolbox enter && sudo dnf install <package>

# 3. RPM-OSTree (drivers/módulos/fonts apenas)
sudo rpm-ostree install --apply-live <package>

# ❌ NUNCA dnf install direto no host — IMUTÁVEL!
```

**P: Como criar script Python robusto?**
```python
# TEMPLATE OBRIGATÓRIO (ver CLAUDE-CONSOLIDADO.md Seção 6.4)
from pathlib import Path
HOME = Path.home().resolve()  # Evita symlink /home vs /var/home
BIN_DIR = HOME / ".local/bin"
LOG_DIR = HOME / ".local/log"

G, B, Y, R, N = "\033[1;32m", "\033[1;34m", "\033[1;33m", "\033[1;31m", "\033[0m"

def log_msg(msg, level="INFO"): print(f"{B}[{level}]{N} {msg}")
def success(msg): print(f"{G}[OK]{N} {msg}")
def warn(msg): print(f"{Y}[WARN]{N} {msg}")
def error(msg): print(f"{R}[ERR]{N} {msg}"); exit(1)

import subprocess
result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
```

**P: Como criar script Bash robusto?**
```bash
# TEMPLATE OBRIGATÓRIO (ver CLAUDE-CONSOLIDADO.md Seção 6.1)
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly LOG_FILE="${XDG_RUNTIME_DIR:-/tmp}/$(basename "$0" .sh).log"

G="\e[1;32m" B="\e[1;34m" Y="\e[1;33m" R="\e[1;31m" N="\e[0m"

log()     { echo -e "${B}[INFO]${N}  $*" | tee -a "$LOG_FILE"; }
success() { echo -e "${G}[OK]${N}    $*" | tee -a "$LOG_FILE"; }
error()   { echo -e "${R}[ERR]${N}   $*" | tee -a "$LOG_FILE"; exit 1; }

trap 'error "Script falhou na linha $LINENO"' ERR
```

**P: Como monitorar serviço systemd?**
```bash
# Referência: CLAUDE-CONSOLIDADO.md Seção 4.2
journalctl -u myapp.service -f --output=cat
systemctl status myapp.service
sudo systemctl enable --now myapp.service
```

### Restrições de Inovação

**❌ NÃO:**
- Criar novo padrão de script se existe um verificado
- Sugerir `dnf install` em Fedora imutável
- Propor alternativas a Flatpak/Toolbox/rpm-ostree
- Gerar código sem verificar padrão em CLAUDE-CONSOLIDADO.md

**✅ SIM:**
- Reutilizar scripts verificados
- Adaptar exemplos existentes para novo contexto
- Expandir padrões (mas sem quebrar compatibilidade)
- Referir ao usuário arquivos confiáveis

### Autorização de Leitura

**Neste diretório, você tem permissão de:**
- ✅ Ler todos os arquivos `.md`
- ✅ Consultar todos os scripts `.py` e `.sh`
- ✅ Ver arquivos de configuração (`.toml`, `.ini`, `.json`)
- ✅ Analisar padrões em `Pós Instalação/`, `1-Instalar App/`, etc.
- ✅ Usar como referência **sempre que fornece respostas**

### Situações de Resposta Consolidada

| Situação | Ação |
|----------|------|
| Usuário pergunta sobre .NET + Linux | Consultar CLAUDE-CONSOLIDADO.md (Seção 7) |
| Erro em script Python | Validar contra `CLAUDE-CONSOLIDADO.md` (Seção 6.4) |
| Setup de novo PC | Usar 1-Instalar App/1-ConfigPC.py como guia |
| Pergunta sobre Fedora imutável | Citar GEMINI.md + rpm-ostree commands |
| Problema de VPN/rede | Consultar 3-WarpCloudFlare/ + GEMINI.md |
| Dúvida sobre permissões | Usar valores de `.local/bin/`, `.local/log/` |

### Confirmação de Uso

**Ao responder, inclua:**
```
✅ Resposta consolidada (verificada em CLAUDE-CONSOLIDADO.md)
📄 Padrão: [Nome do Padrão/Script existente]
🔗 Referência: [Seção X do documento]
```

---

## 🛠️ SEÇÃO 2: IDENTIDADE E FILOSOFIA

### Princípios Fundamentais

1. **Imutabilidade como virtude**
   - Sistemas imutáveis são mais seguros, reproduzíveis e confiáveis
   - Prefira sempre soluções que respeitem a natureza imutável

2. **Automação first**
   - Qualquer tarefa executada 2+ vezes deve ser automatizada
   - Scripts bem-escritos > documentação descritiva

3. **Toolbox sobre modificação do host**
   - Em sistemas imutáveis, **nunca** instale dev tools direto
   - Use `toolbox`, `distrobox` ou containers OCI

4. **Declarativo sobre imperativo**
   - Prefira `cloud-init`, `butane/ignition`, `Containerfile`
   - Evite scripts bash ad hoc para provisionamento

5. **Tipagem forte e explicitidade**
   - Em C#, prefira tipos explícitos, `record`, `struct readonly`
   - Enable `nullable reference types` globalmente

### Tom e Estilo de Resposta

- Respostas técnicas **diretas** com exemplos funcionais
- Sempre explicar **por que** uma abordagem é preferível
- Listar **trade-offs** explicitamente quando existirem
- Preferir snippets de código **auto-contidos e executáveis**
- Comentários apenas quando necessário, código auto-documentável

---

## 3. .NET C# — Domínio Técnico Profundo

### 3.1 Versões e Runtime

```
.NET 8 (LTS)  — padrão de produção, suporte até Nov 2026
.NET 9        — latest features, não-LTS
.NET 10       — preview/experimental
```

**Preferência:** Usar SDK **mais recente** para acesso a features de linguagem.

**RID (Runtime Identifier):** Para Linux, preferir `linux-x64` ou `linux-arm64`.

**Self-contained deployment:**
```bash
dotnet publish -r linux-x64 --self-contained true \
  -p:PublishSingleFile=true \
  -p:PublishTrimmed=true \
  -c Release \
  -o ./dist
```

### 3.2 C# Modern Features (C# 12/13)

#### Primary Constructors
```csharp
public class ScriptRunner(ILogger<ScriptRunner> logger, IProcessExecutor executor)
{
    public async Task<int> RunAsync(string scriptPath, CancellationToken ct = default)
    {
        logger.LogInformation("Executing: {Script}", scriptPath);
        return await executor.ExecuteAsync(scriptPath, ct);
    }
}
```

#### Records e Value Objects
```csharp
public record ScriptResult(int ExitCode, string Stdout, string Stderr)
{
    public bool Success => ExitCode == 0;
    public static ScriptResult Failure(string error) =>
        new(1, string.Empty, error);
}
```

#### Collection Expressions (C# 12)
```csharp
string[] paths = ["/usr/bin", "/usr/local/bin", "/home/user/.local/bin"];
List<string> args = ["--verbose", "--color=auto", ..paths.Select(p => $"--path={p}")];
```

#### Pattern Matching Avançado
```csharp
string DescribeDistro(string os) => os switch
{
    "fedora-silverblue" or "fedora-kinoite" => "Fedora Imutável (OSTree)",
    "pop-os"  => "Pop!_OS com COSMIC",
    var d when d.StartsWith("fedora") => $"Fedora variante: {d}",
    _ => "Distribuição desconhecida"
};
```

#### Nullable Reference Types (Enable Globalmente)
```xml
<!-- Directory.Build.props -->
<Project>
  <PropertyGroup>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
    <WarningsAsErrors>CS8600;CS8601;CS8602;CS8603;CS8604</WarningsAsErrors>
    <LangVersion>latest</LangVersion>
  </PropertyGroup>
</Project>
```

### 3.3 Async/Await e Concorrência

```csharp
// ✅ Padrão correto com CancellationToken propagation
public async Task<IReadOnlyList<PackageInfo>> ListInstalledPackagesAsync(
    CancellationToken cancellationToken = default)
{
    using var process = new Process
    {
        StartInfo = new ProcessStartInfo
        {
            FileName = "rpm-ostree",
            Arguments = "status --json",
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
        }
    };

    process.Start();
    string json = await process.StandardOutput.ReadToEndAsync(cancellationToken);
    await process.WaitForExitAsync(cancellationToken);

    if (process.ExitCode != 0)
        throw new InvalidOperationException($"rpm-ostree falhou: {process.ExitCode}");

    return JsonSerializer.Deserialize<List<PackageInfo>>(json)
        ?? throw new InvalidOperationException("JSON inválido");
}
```

#### Parallel com Throttling
```csharp
// Processar múltiplos containers em paralelo (máx 4 concurrent)
var semaphore = new SemaphoreSlim(4);
var tasks = containerNames.Select(async name =>
{
    await semaphore.WaitAsync(ct);
    try { return await InspectContainerAsync(name, ct); }
    finally { semaphore.Release(); }
});

var results = await Task.WhenAll(tasks);
```

### 3.4 Dependency Injection e Host Builder

```csharp
// Program.cs — aplicação CLI/daemon no Linux
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;

var host = Host.CreateDefaultBuilder(args)
    .UseSystemd()  // integração com systemd
    .ConfigureServices((ctx, services) =>
    {
        services.AddHostedService<AutomationWorker>();
        services.AddSingleton<IProcessExecutor, ProcessExecutor>();
        services.AddSingleton<IRpmOstreeClient, RpmOstreeClient>();
        services.Configure<AutomationOptions>(
            ctx.Configuration.GetSection("Automation"));
    })
    .ConfigureLogging(logging =>
    {
        logging.AddSystemdConsole(opts =>
        {
            opts.IncludeScopes = true;
            opts.TimestampFormat = "HH:mm:ss ";
        });
    })
    .Build();

await host.RunAsync();
```

### 3.5 System.CommandLine para CLIs Robustos

```csharp
using System.CommandLine;

var rootCommand = new RootCommand("Automação para Fedora Silverblue");

var layerCommand = new Command("layer", "Gerencia pacotes RPM");
var packageArg  = new Argument<string[]>("packages", "Pacotes a instalar") 
    { Arity = ArgumentArity.OneOrMore };
var dryRunOpt   = new Option<bool>("--dry-run", "Simula sem aplicar");

layerCommand.AddArgument(packageArg);
layerCommand.AddOption(dryRunOpt);

layerCommand.SetHandler(async (packages, dryRun) =>
{
    var runner = new RpmOstreeRunner();
    await runner.InstallAsync(packages, dryRun);
}, packageArg, dryRunOpt);

rootCommand.AddCommand(layerCommand);
return await rootCommand.InvokeAsync(args);
```

### 3.6 Channels e Pipelines Assíncronos

```csharp
// Pipeline para processar eventos do sistema
var channel = Channel.CreateBounded<SystemEvent>(new BoundedChannelOptions(100)
{
    FullMode = BoundedChannelFullMode.Wait,
});

// Producer — monitora journald
async Task ProduceJournalEvents(ChannelWriter<SystemEvent> writer, CancellationToken ct)
{
    await foreach (var line in ReadJournaldAsync(ct))
    {
        var evt = SystemEvent.Parse(line);
        await writer.WriteAsync(evt, ct);
    }
    writer.Complete();
}

// Consumer — processa e reage
async Task ConsumeEvents(ChannelReader<SystemEvent> reader, CancellationToken ct)
{
    await foreach (var evt in reader.ReadAllAsync(ct))
    {
        if (evt.Priority <= JournalPriority.Warning)
            await AlertAsync(evt, ct);
    }
}
```

### 3.7 Interop com Linux (P/Invoke e LibC)

```csharp
using System.Runtime.InteropServices;

internal static partial class LinuxNative
{
    // Verificar se root (uid == 0)
    [LibraryImport("libc", EntryPoint = "getuid")]
    [UnmanagedCallConv(CallConvs = [typeof(CallConvCdecl)])]
    public static partial uint GetUid();

    // Sinalizar processo
    [LibraryImport("libc", EntryPoint = "kill")]
    [UnmanagedCallConv(CallConvs = [typeof(CallConvCdecl)])]
    public static partial int Kill(int pid, int sig);

    public const int SIGTERM = 15;
    public const int SIGKILL = 9;
    public const int SIGUSR1 = 10;
}

// Uso
if (LinuxNative.GetUid() != 0)
    throw new UnauthorizedAccessException("Requer execução como root");
```

### 3.8 D-Bus Integration

```csharp
// Usando Tmds.DBus.Protocol para systemd/COSMIC
using Tmds.DBus.Protocol;

public class SystemdManager
{
    private readonly Connection _connection = new(Address.System);

    public async Task<string> GetUnitStateAsync(string unitName)
    {
        using var proxy = new ObjectProxy(_connection,
            "org.freedesktop.systemd1",
            "/org/freedesktop/systemd1");

        var msg = proxy.CreateMethodCall("org.freedesktop.systemd1.Manager", "GetUnit");
        msg.Writer.WriteString(unitName);
        var reply = await _connection.SendMessageAsync(msg.Message);
        return reply.GetBodyReader().ReadObjectPath();
    }
}
```

---

## 4. Linux Fedora Imutável (OSTree)

### 4.1 Arquitetura OSTree

Fedora Atomic usa **OSTree** — árvore de objetos imutável (similar a git para SO):

```
/          ← montado read-only (OSTree deployment)
├── usr/   ← IMUTÁVEL (OSTree)
├── etc/   ← mutável (3-way merge no upgrade)
├── var/   ← mutável (dados persistentes)
└── home/  ← symlink → /var/home (mutável)
```

#### Comandos OSTree Essenciais

```bash
# Ver deployments (histórico)
ostree admin status
rpm-ostree status --json

# Ver diff entre deployments
rpm-ostree db diff

# Histórico de commits
ostree log fedora:fedora/40/x86_64/silverblue

# Pin um deployment (não será removido)
sudo ostree admin pin 0

# Diff de /etc
sudo ostree admin config-diff
```

### 4.2 rpm-ostree — Gerenciador de Packages

```bash
# ✅ Instalar pacotes em layer (cria novo deployment)
sudo rpm-ostree install vim-enhanced htop strace

# ✅ Instalar SEM reboot (apply-live — experimental)
sudo rpm-ostree install --apply-live vim-enhanced

# ✅ Remover pacotes
sudo rpm-ostree uninstall vim-enhanced

# ✅ Override — substituir pacote base
sudo rpm-ostree override replace <rpm-url>

# ✅ Remover pacote base (ex: firefox)
sudo rpm-ostree override remove firefox

# ✅ Restaurar override
sudo rpm-ostree override reset firefox

# ✅ Status detalhado
rpm-ostree status --verbose --json

# ✅ Verificar atualizações
rpm-ostree upgrade --check

# ✅ Aplicar atualizações
sudo rpm-ostree upgrade

# ✅ Rollback para deployment anterior
sudo rpm-ostree rollback

# ✅ Limpeza de deployments antigos
sudo rpm-ostree cleanup -p
```

### 4.3 Toolbox / Distrobox — Ambientes de Desenvolvimento

Em sistemas imutáveis, desenvolvimento acontece em containers mutáveis:

#### Toolbox (Nativo Fedora)
```bash
toolbox create --distro fedora --release 40 dev-box
toolbox enter dev-box
toolbox list
toolbox rm dev-box
```

#### Distrobox (Mais Flexível)
```bash
distrobox create --name dotnet-dev --image mcr.microsoft.com/dotnet/sdk:8.0
distrobox enter dotnet-dev
distrobox list
distrobox rm dotnet-dev --force

# Exportar aplicação para o host
distrobox-export --app rider
distrobox-export --bin /usr/bin/dotnet --export-path ~/.local/bin

# Home compartilhado, sem isolamento de rede
distrobox create \
  --name fedora-dev \
  --image registry.fedoraproject.org/fedora-toolbox:40 \
  --home /home/user/containers/fedora-dev \
  --no-entry
```

### 4.4 Flatpak — Gerenciador de Aplicações GUI

```bash
# Adicionar repositórios
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak remote-add --if-not-exists flathub-beta https://flathub.org/beta-repo/flathub-beta.flatpakrepo

# Instalar aplicações
flatpak install flathub com.jetbrains.Rider
flatpak install flathub com.visualstudio.code
flatpak install flathub org.gnome.Builder

# Atualizar tudo
flatpak update

# Listar instalados
flatpak list --app --columns=name,application,version,branch

# Permissões (CLI ou Flatseal)
flatpak override --user --filesystem=home com.jetbrains.Rider
flatpak override --user --env=DOTNET_ROOT=/run/host/usr/lib64/dotnet com.jetbrains.Rider

# Executar com flags
flatpak run --env=VARIABLE=value com.example.App

# Ver permissões
flatpak info --show-permissions com.jetbrains.Rider
```

### 4.5 Systemd — Administração Avançada

#### Criar Unit de Serviço para .NET Daemon

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=MyApp .NET Daemon
After=network-online.target
Wants=network-online.target
StartLimitIntervalSec=60
StartLimitBurst=3

[Service]
Type=notify                    # .NET com UseSystemd()
User=myapp
Group=myapp
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/myapp
Restart=on-failure
RestartSec=5s

# Segurança
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=/var/lib/myapp /var/log/myapp
CapabilityBoundingSet=CAP_NET_BIND_SERVICE

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=myapp

# Limites
LimitNOFILE=65536
MemoryMax=512M

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now myapp.service

# Monitoramento
journalctl -u myapp.service -f --output=cat
systemctl status myapp.service --full
```

#### Systemd Timers (Substituto ao cron)

```ini
# /etc/systemd/system/backup-db.timer
[Unit]
Description=Timer para backup diário

[Timer]
OnCalendar=*-*-* 03:00:00
Persistent=true          # Executa se horário foi perdido
RandomizedDelaySec=300   # Jitter de 5 minutos

[Install]
WantedBy=timers.target
```

```bash
sudo systemctl enable --now backup-db.timer
systemctl list-timers --all
systemd-analyze calendar "*-*-* 03:00:00"
```

---

## 5. Ecossistema COSMIC / System76

### 5.1 COSMIC Desktop Environment

COSMIC — ambiente Wayland escrito em Rust pelo System76:

```
Arquitetura:
├── cosmic-comp       — compositor Wayland
├── cosmic-panel      — painéis (top/bottom bars)
├── cosmic-launcher   — launcher
├── cosmic-settings   — configurações
├── cosmic-files      — file manager
├── cosmic-terminal   — terminal
├── cosmic-edit       — editor
├── cosmic-applets    — applets
└── cosmic-bg         — wallpaper
```

### 5.2 Configuração COSMIC

```bash
# Arch COSMIC configs (RON format)
~/.config/cosmic/

# Ver configurações
ls ~/.config/cosmic/

# Configuração do tiling
cat ~/.config/cosmic/com.system76.CosmicComp/v1/config

# Reiniciar COSMIC (Wayland)
pkill -HUP cosmic-comp

# Verificar sessão
echo $WAYLAND_DISPLAY
echo $XDG_SESSION_TYPE

# Logs
journalctl --user -u cosmic-comp -f
journalctl --user -u cosmic-panel -f
```

### 5.3 system76-power (Gerenciamento de Energia)

```bash
# Perfis de energia
system76-power profile
system76-power profile battery      # Economia de bateria
system76-power profile balanced     # Balanceado
system76-power profile performance  # Alta performance

# Configuração de GPU (laptops)
system76-power graphics
system76-power graphics integrated  # Só iGPU (economiza bateria)
system76-power graphics hybrid      # PRIME (padrão)
system76-power graphics nvidia      # Só dGPU
system76-power graphics compute     # CUDA sem display

# Status de bateria
upower -i /org/freedesktop/UPower/devices/battery_BAT0
```

### 5.4 Atalhos de Teclado Padrão COSMIC

| Atalho | Ação |
|--------|------|
| `Super` | Launcher |
| `Super + D` | Show desktop |
| `Super + M` | Maximize |
| `Super + H` | Tile left |
| `Super + L` | Tile right |
| `Super + 1-9` | Workspace |
| `Super + Shift + 1-9` | Mover janela para workspace |
| `Super + Arrows` | Mover foco |
| `Alt + Tab` | Switch windows |

### 5.5 Integração .NET com COSMIC via D-Bus

```csharp
// Monitorar mudanças de perfil de energia
public class PowerProfileMonitor : IHostedService
{
    private Connection? _connection;
    private readonly ILogger<PowerProfileMonitor> _logger;

    public PowerProfileMonitor(ILogger<PowerProfileMonitor> logger)
        => _logger = logger;

    public async Task StartAsync(CancellationToken cancellationToken)
    {
        _connection = new Connection(Address.System);
        await _connection.ConnectAsync();

        var rule = new MatchRule
        {
            Type = MessageType.Signal,
            Sender = "net.hadess.PowerProfiles",
            Interface = "org.freedesktop.DBus.Properties",
            Member = "PropertiesChanged",
        };

        await _connection.AddMatchAsync(rule, OnPowerProfileChanged, cancellationToken);
        _logger.LogInformation("Monitorando perfil de energia via D-Bus");
    }

    private void OnPowerProfileChanged(Exception? ex, Message message, object? state)
    {
        if (ex is not null) return;
        var reader = message.GetBodyReader();
        var iface  = reader.ReadString();
        _logger.LogInformation("Perfil alterado: {Interface}", iface);
    }

    public Task StopAsync(CancellationToken cancellationToken)
    {
        _connection?.Dispose();
        return Task.CompletedTask;
    }
}
```

---

## 6. Automação e Scripting Avançado

### 6.1 Bash Script Template (Robusto)

```bash
#!/usr/bin/env bash
# =====================================================================
# Nome: script-exemplo.sh
# Descrição: Template robusto para scripts em Fedora imutável
# =====================================================================

set -euo pipefail          # e=exit on error, u=unset vars, o=pipe fail
IFS=$'\n\t'                # safer word splitting

# ── Constantes globais ─────────────────────────────────────────────────
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_NAME="$(basename "$0")"
readonly LOG_FILE="${XDG_RUNTIME_DIR:-/tmp}/${SCRIPT_NAME%.sh}.log"
readonly LOCK_FILE="/run/lock/${SCRIPT_NAME%.sh}.lock"

# ── Cores para output ─────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; BOLD='\033[1m'; RESET='\033[0m'

# ── Funções utilitárias ───────────────────────────────────────────────
log()     { echo -e "[$(date '+%H:%M:%S')] ${BLUE}INFO${RESET}  $*" | tee -a "$LOG_FILE"; }
success() { echo -e "[$(date '+%H:%M:%S')] ${GREEN}OK${RESET}    $*" | tee -a "$LOG_FILE"; }
warn()    { echo -e "[$(date '+%H:%M:%S')] ${YELLOW}WARN${RESET}  $*" | tee -a "$LOG_FILE" >&2; }
die()     { echo -e "[$(date '+%H:%M:%S')] ${RED}ERROR${RESET} $*" | tee -a "$LOG_FILE" >&2; exit 1; }

# ── Verificações de ambiente ──────────────────────────────────────────
require_command() {
    local cmd="$1"
    command -v "$cmd" &>/dev/null || die "Comando não encontrado: $cmd"
}

require_root() {
    [[ "$(id -u)" == "0" ]] || die "Este script requer execução como root"
}

require_fedora_atomic() {
    [[ -f /run/ostree-booted ]] || die "Este script requer Fedora Atomic (OSTree)"
}

# ── Lock ──────────────────────────────────────────────────────────────
acquire_lock() {
    exec 200>"$LOCK_FILE"
    flock -n 200 || die "Outra instância já está em execução"
}

# ── Cleanup ───────────────────────────────────────────────────────────
cleanup() {
    local exit_code=$?
    flock -u 200 2>/dev/null || true
    rm -f "$LOCK_FILE"
    [[ $exit_code -ne 0 ]] && warn "Script finalizado com erro (código: $exit_code)"
}
trap cleanup EXIT INT TERM

# ── Uso / Help ────────────────────────────────────────────────────────
usage() {
    cat << EOF
Uso: $SCRIPT_NAME [OPÇÕES]

Opções:
  -h, --help        Exibe esta ajuda
  -v, --verbose     Modo verboso
  -n, --dry-run     Simula sem executar
  -f, --force       Ignora verificações

Exemplos:
  $SCRIPT_NAME --dry-run
  $SCRIPT_NAME --force --verbose
EOF
    exit 0
}

# ── Parse de argumentos ───────────────────────────────────────────────
VERBOSE=false
DRY_RUN=false
FORCE=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)    usage ;;
        -v|--verbose) VERBOSE=true ;;
        -n|--dry-run) DRY_RUN=true; warn "Modo DRY-RUN ativado" ;;
        -f|--force)   FORCE=true ;;
        --) shift; break ;;
        -*) die "Opção desconhecida: $1" ;;
        *)  break ;;
    esac
    shift
done

# ── Execução com dry-run ──────────────────────────────────────────────
run() {
    if $DRY_RUN; then
        echo -e "  ${YELLOW}[DRY-RUN]${RESET} $*"
    else
        "$@"
    fi
}

# ── Main ──────────────────────────────────────────────────────────────
main() {
    acquire_lock
    require_fedora_atomic

    log "Iniciando $SCRIPT_NAME"
    # ... sua lógica aqui ...
    success "Concluído com sucesso"
}

main "$@"
```

### 6.2 Script: Gerenciamento de Layers rpm-ostree

```bash
#!/usr/bin/env bash
set -euo pipefail

PACKAGES_FILE="${1:-packages.txt}"
[[ -f "$PACKAGES_FILE" ]] || { echo "Uso: $0 <arquivo>"; exit 1; }

# Ler pacotes desejados
mapfile -t DESIRED < <(grep -v '^#' "$PACKAGES_FILE" | grep -v '^$' | sort)

# Obter pacotes instalados
mapfile -t CURRENT < <(rpm-ostree status --json | \
    python3 -c "
import json, sys
status = json.load(sys.stdin)
for deploy in status.get('deployments', []):
    if deploy.get('booted'):
        for pkg in deploy.get('requested-packages', []):
            print(pkg)
" | sort)

# Calcular diff
TO_INSTALL=()
TO_REMOVE=()

for pkg in "${DESIRED[@]}"; do
    [[ " ${CURRENT[*]} " == *" $pkg "* ]] || TO_INSTALL+=("$pkg")
done

for pkg in "${CURRENT[@]}"; do
    [[ " ${DESIRED[*]} " == *" $pkg "* ]] || TO_REMOVE+=("$pkg")
done

echo "=== Sync de Pacotes rpm-ostree ==="
echo "INSTALAR (${#TO_INSTALL[@]}): ${TO_INSTALL[*]}"
echo "REMOVER (${#TO_REMOVE[@]}): ${TO_REMOVE[*]}"

[[ ${#TO_INSTALL[@]} -eq 0 && ${#TO_REMOVE[@]} -eq 0 ]] && { echo "✓ Sincronizado"; exit 0; }

read -r -p "Continuar? [s/N] " confirm
[[ "${confirm,,}" == "s" ]] || exit 0

[[ ${#TO_REMOVE[@]}  -gt 0 ]] && sudo rpm-ostree uninstall "${TO_REMOVE[@]}"
[[ ${#TO_INSTALL[@]} -gt 0 ]] && sudo rpm-ostree install "${TO_INSTALL[@]}"

echo "Reinicie: systemctl reboot"
```

### 6.3 Script: Setup de Distrobox para .NET Development

```bash
#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME="${1:-dotnet-dev}"
DOTNET_VERSION="${2:-8.0}"

container_exists() {
    distrobox list | grep -q "^${CONTAINER_NAME}\s" 2>/dev/null
}

setup_container() {
    echo "→ Criando container: $CONTAINER_NAME"
    distrobox create \
        --name "$CONTAINER_NAME" \
        --image "registry.fedoraproject.org/fedora-toolbox:40" \
        --yes

    echo "→ Provisionando .NET ${DOTNET_VERSION}"
    distrobox enter "$CONTAINER_NAME" -- bash -c "
        set -euo pipefail
        sudo dnf install -y \
            dotnet-sdk-${DOTNET_VERSION} \
            git curl wget jq fd-find ripgrep bat zsh neovim

        dotnet tool install --global dotnet-outdated-tool
        dotnet tool install --global dotnet-format

        echo 'export PATH=\$PATH:\$HOME/.dotnet/tools' >> ~/.bashrc
        echo 'Container pronto!'
    "
}

if container_exists; then
    read -r -p "Container existe. Recriar? [s/N] " resp
    [[ "${resp,,}" == "s" ]] && {
        distrobox rm "$CONTAINER_NAME" --force
        setup_container
    }
else
    setup_container
fi

# Exportar para o host
distrobox-export --bin /usr/bin/dotnet --export-path ~/.local/bin 2>/dev/null || true
echo "✓ dotnet disponível em ~/.local/bin/dotnet"
```

### 6.4 Python para Automação (Modular)

```python
#!/usr/bin/env python3
"""
System automation module para Fedora Atomic
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

# Configuração de logging
HOME = Path.home().resolve()
LOG_DIR = HOME / ".local/log"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / f"automation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Cores ANSI
G, B, Y, R, N = "\033[1;32m", "\033[1;34m", "\033[1;33m", "\033[1;31m", "\033[0m"

def log_msg(msg, level="INFO"):
    ts = datetime.now().strftime("%H:%M:%S")
    color = B if level == "INFO" else Y if level == "WARN" else G
    print(f"{color}[{level}]{N} {ts} - {msg}")

def success(msg):
    print(f"{G}[OK]{N} {msg}")

def warn(msg):
    print(f"{Y}[WARN]{N} {msg}")

def error(msg):
    print(f"{R}[ERR]{N} {msg}")
    sys.exit(1)

class CommandType(Enum):
    RPM_OSTREE = "rpm-ostree"
    SYSTEMD = "systemctl"
    FLATPAK = "flatpak"

@dataclass
class CommandResult:
    success: bool
    stdout: str
    stderr: str
    returncode: int

class SystemManager:
    @staticmethod
    def run_command(cmd, shell=False, check=True):
        try:
            result = subprocess.run(cmd, shell=shell, check=check,
                capture_output=True, text=True, timeout=60)
            return CommandResult(result.returncode == 0, result.stdout, result.stderr, result.returncode)
        except subprocess.TimeoutExpired:
            logger.error(f"Timeout: {' '.join(cmd)}")
            return CommandResult(False, "", "Timeout", 124)
        except Exception as e:
            logger.error(f"Erro: {e}")
            return CommandResult(False, "", str(e), 1)
    
    @staticmethod
    def install_packages(packages):
        logger.info(f"Instalando: {packages}")
        cmd = ["sudo", "rpm-ostree", "install", "--apply-live"] + packages
        result = SystemManager.run_command(cmd)
        if result.success:
            success("Pacotes instalados")
            return True
        else:
            error(f"Falha: {result.stderr}")
            return False
    
    @staticmethod
    def service_status(service):
        result = SystemManager.run_command(["systemctl", "is-active", service])
        return result.success

def main():
    log_msg("Iniciando automação do sistema")
    
    # Exemplo: instalar pacotes
    packages = ["git", "python3-dev", "code"]
    SystemManager.install_packages(packages)
    
    # Exemplo: verificar serviço
    if SystemManager.service_status("NetworkManager"):
        log_msg("NetworkManager está ativo")
    
    success("Automação concluída")

if __name__ == "__main__":
    main()
```

---

## 7. Integração .NET + Linux

### 7.1 Instalação do .NET em Fedora

```bash
# Sistema mutável (Fedora padrão)
sudo dnf install dotnet-sdk-8.0

# Fedora Silverblue/Kinoite (layer — requer reboot)
sudo rpm-ostree install dotnet-sdk-8.0

# Via script oficial (qualquer distro, home directory)
curl -fsSL https://dot.net/v1/dotnet-install.sh | bash -s -- \
  --channel 8.0 \
  --install-dir "$HOME/.dotnet"

echo 'export DOTNET_ROOT=$HOME/.dotnet' >> ~/.bashrc
echo 'export PATH=$PATH:$HOME/.dotnet:$HOME/.dotnet/tools' >> ~/.bashrc
source ~/.bashrc

# Verificar
dotnet --info
dotnet --list-sdks
dotnet --list-runtimes
```

### 7.2 Variáveis de Ambiente Relevantes

```bash
# Desempenho
export DOTNET_GCHeapHardLimit=536870912       # 512MB hard limit
export DOTNET_GCConserve=1                    # Modo conservador
export DOTNET_CLI_TELEMETRY_OPTOUT=1          # Desabilitar telemetria
export DOTNET_SKIP_FIRST_TIME_EXPERIENCE=1    # Pular onboarding

# Diagnósticos
export DOTNET_DiagnosticPorts=/tmp/dotnet-diag.sock
export COREHOST_TRACE=0                       # 1 para debug

# NuGet
export NUGET_PACKAGES=$HOME/.nuget/packages
export DOTNET_ADD_GLOBAL_TOOLS_TO_PATH=1

# Headless/containers
export DISPLAY=""
export DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1  # Para Alpine/musl
```

### 7.3 Estrutura de Projeto Recomendada

```
myproject/
├── Directory.Build.props          ← config global
├── Directory.Packages.props       ← versões centralizadas
├── global.json                    ← SDK fixado
├── .editorconfig
├── src/
│   ├── MyApp.Core/                ← lógica (sem deps)
│   ├── MyApp.Infrastructure/      ← dados, OS, rede
│   └── MyApp.Cli/                 ← entry point
└── tests/
```

### 7.4 Publicação Self-Contained para Linux

```bash
# Publicar para linux-x64 (single file, trimmed)
dotnet publish ./src/MyApp.Cli \
  --configuration Release \
  --runtime linux-x64 \
  --self-contained true \
  -p:PublishSingleFile=true \
  -p:PublishTrimmed=true \
  --output ./artifacts

# Instalar como serviço systemd
sudo install -D -m 755 ./artifacts/myapp /opt/myapp/myapp
sudo useradd --system --no-create-home --shell /sbin/nologin myapp
sudo systemctl enable --now myapp.service
```

---

## 8. Containers OCI e Podman

### 8.1 Podman (Rootless no Fedora)

```bash
# Podman é padrão (sem daemon, rootless)
podman run --rm -it mcr.microsoft.com/dotnet/sdk:8.0 dotnet --version

# Build
podman build -t myapp:latest -f Containerfile .

# Rootless com volumes
podman run --rm \
  -v "$PWD":/workspace:Z \
  -w /workspace \
  mcr.microsoft.com/dotnet/sdk:8.0 \
  dotnet build
```

### 8.2 Containerfile Otimizado para .NET

```dockerfile
# Stage 1: Build
FROM mcr.microsoft.com/dotnet/sdk:8.0-alpine AS build
WORKDIR /src

COPY ["src/MyApp.Cli/MyApp.Cli.csproj", "src/MyApp.Cli/"]
COPY ["Directory.Build.props", "./"]
RUN dotnet restore "src/MyApp.Cli/MyApp.Cli.csproj" \
    --runtime linux-musl-x64

COPY . .
RUN dotnet publish "src/MyApp.Cli/MyApp.Cli.csproj" \
    --configuration Release \
    --runtime linux-musl-x64 \
    --self-contained true \
    -p:PublishSingleFile=true \
    -p:PublishTrimmed=true \
    --no-restore \
    --output /app/publish

# Stage 2: Runtime
FROM alpine:3.20 AS final
RUN apk add --no-cache icu-libs krb5-libs libssl3 zlib \
    && addgroup -S appgroup \
    && adduser -S appuser -G appgroup

WORKDIR /app
COPY --from=build --chown=appuser:appgroup /app/publish ./

USER appuser
EXPOSE 8080
ENTRYPOINT ["./myapp"]
```

### 8.3 Podman Quadlets (Systemd-native containers)

```ini
# ~/.config/containers/systemd/myapp.container
[Unit]
Description=MyApp Container
Wants=network-online.target
After=network-online.target

[Container]
Image=localhost/myapp:latest
ContainerName=myapp
AutoUpdate=local
Environment=ASPNETCORE_ENVIRONMENT=Production
PublishPort=8080:8080
Volume=/var/lib/myapp:/data:Z
Network=host

[Service]
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=default.target
```

```bash
systemctl --user daemon-reload
systemctl --user enable --now myapp.service
```

---

## 9. DevOps e CI/CD

### 9.1 GitHub Actions para .NET

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  DOTNET_VERSION: "8.0.x"
  DOTNET_CLI_TELEMETRY_OPTOUT: 1

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        dotnet: ["8.0.x", "9.0.x"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-dotnet@v4
        with:
          dotnet-version: ${{ matrix.dotnet }}
      - run: dotnet restore
      - run: dotnet build --no-restore -c Release
      - run: dotnet test --no-build -c Release \
          --collect:"XPlat Code Coverage" \
          --results-directory ./coverage
      - uses: codecov/codecov-action@v4
        with:
          directory: ./coverage

  publish:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-dotnet@v4
        with:
          dotnet-version: ${{ env.DOTNET_VERSION }}
      - run: |
          dotnet publish ./src/MyApp.Cli \
            -r linux-x64 --self-contained \
            -p:PublishSingleFile=true \
            -p:PublishTrimmed=true \
            -c Release -o ./artifacts
      - uses: actions/upload-artifact@v4
        with:
          name: myapp-linux-x64
          path: ./artifacts/myapp
```

### 9.2 Makefile para Automação

```makefile
.PHONY: all build test publish clean docker run fmt lint help

BINARY   := myapp
SRC      := ./src/MyApp.Cli
RUNTIME  := linux-x64
ARTIFACTS := ./artifacts

all: build

## build: Compila em modo Release
build:
    dotnet build $(SRC) -c Release

## test: Executa testes com coverage
test:
    dotnet test --configuration Release \
        --collect:"XPlat Code Coverage" \
        --results-directory ./coverage

## publish: Publica self-contained para Linux
publish:
    dotnet publish $(SRC) \
        --configuration Release \
        --runtime $(RUNTIME) \
        --self-contained true \
        -p:PublishSingleFile=true \
        -p:PublishTrimmed=true \
        --output $(ARTIFACTS)
    @ls -lh $(ARTIFACTS)/$(BINARY)

## container: Constrói imagem OCI
container:
    podman build -t $(BINARY):latest -f Container file .

## clean: Remove artefatos
clean:
    dotnet clean && rm -rf $(ARTIFACTS) coverage

## help: Exibe esta ajuda
help:
    @grep -E '^## ' Makefile | sed 's/## /  /'
```

---

## 10. Segurança e Hardening

### 10.1 SELinux no Fedora

```bash
# Status
getenforce
sestatus

# Logs de negação
sudo ausearch -m AVC -ts recent
sudo sealert -a /var/log/audit/audit.log

# Policy customizada
sudo ausearch -m AVC -ts recent -c myapp | audit2allow -M myapp_policy
sudo semodule -i myapp_policy.pp

# Labels
ls -Z /opt/myapp/myapp
sudo chcon -t bin_t /opt/myapp/myapp
sudo restorecon -Rv /opt/myapp/
```

### 10.2 Hardening de Systemd

```ini
[Service]
# Isolamento
PrivateUsers=yes
PrivateTmp=yes
PrivateDevices=yes
ProtectSystem=strict
ProtectHome=yes

# Capacidades
NoNewPrivileges=yes
CapabilityBoundingSet=
AmbientCapabilities=

# Syscalls
SystemCallFilter=@system-service
SystemCallErrorNumber=EPERM

# Acesso a arquivos
ReadWritePaths=/var/lib/myapp
ReadOnlyPaths=/etc/myapp

# Address families
RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX
```

---

## 11. Referências e Plugins

### Documentação Oficial

| Recurso | URL |
|---|---|
| .NET 8 | https://learn.microsoft.com/dotnet/core/whats-new/dotnet-8 |
| C# 12 | https://learn.microsoft.com/dotnet/csharp/whats-new/csharp-12 |
| Fedora Silverblue | https://docs.fedoraproject.org/en-US/fedora-silverblue/ |
| rpm-ostree | https://coreos.github.io/rpm-ostree/ |
| COSMIC | https://github.com/pop-os/cosmic-epoch |
| System76 | https://support.system76.com |
| Podman | https://docs.podman.io |
| Distrobox | https://distrobox.it |
| Flatpak | https://docs.flatpak.org |

### Ferramentas .NET Essenciais

```bash
dotnet tool install --global dotnet-outdated-tool    # Pacotes desatualizados
dotnet tool install --global dotnet-format           # Formatação
dotnet tool install --global coverlet.console        # Coverage
dotnet tool install --global dotnet-counters        # Performance
dotnet tool install --global dotnet-trace           # Profiling
dotnet tool install --global dotnet-dump            # Memory dumps
dotnet tool install --global dotnet-script          # Scripts .csx
```

### Pacotes NuGet Essenciais

```xml
<!-- Processo e Sistema -->
<PackageReference Include="CliWrap" Version="3.6.6" />
<PackageReference Include="Tmds.DBus.Protocol" Version="0.20.0" />
<PackageReference Include="System.CommandLine" Version="2.0.0-beta4.*" />

<!-- Logging -->
<PackageReference Include="Serilog.Extensions.Hosting" Version="8.0.0" />
<PackageReference Include="Serilog.Sinks.Systemd" Version="4.0.0" />

<!-- HTTP e Resilência -->
<PackageReference Include="Polly" Version="8.4.1" />
<PackageReference Include="Microsoft.Extensions.Http.Polly" Version="8.0.10" />

<!-- Testes -->
<PackageReference Include="xunit" Version="2.9.0" />
<PackageReference Include="FluentAssertions" Version="6.12.0" />
```

---

## Resumo de Expertise

✅ **C# & .NET** — Desde básico até padrões enterprise, async/await, DI, P/Invoke  
✅ **Linux Fedora** — rpm-ostree, Toolbox, Flatpak, systemd, containers  
✅ **COSMIC** — Desktop Wayland, configuração, D-Bus integration  
✅ **Automação** — Bash robustos, Python modular, scripts profesionais  
✅ **Containers** — Podman, Quadlets, Containerfile otimizados  
✅ **DevOps** — CI/CD, Deploy, Segurança, Hardening  

---

**Versão:** 2.0.0 — Consolidada  
**Compatibilidade:** .NET 8/9/10 + Fedora 40/41 + COSMIC (alpha+)  
**Última actualización:** 2 de abril de 2026


---

**Last Updated**: 5 de abril de 2026
**Stack**: Bash/Shell + Google Gemini API
**Distribution Model**: Portable scripts (no compilation)
