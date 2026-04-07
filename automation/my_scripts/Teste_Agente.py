#!/usr/bin/env python3
"""
CLAW - Agent Profissional com Google Gemini AI + Contexto de Projeto
Versão: 2.0.0 (Python 3)

Um assistente de IA que ajuda com:
- Análise de código e debugging
- Sugestões de melhoria
- Refatoração automática
- Documentação
- Testes

Uso: ./automation/my_scripts/agent.py [comando] [opções]
"""

import os
import sys
import json
import subprocess
import time
import urllib.parse
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Tuple, Dict
import hashlib
from difflib import unified_diff
import signal

# === CONFIGURAÇÃO ===
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / ".claude.json"
HOME = Path.home().resolve()
CACHE_DIR = HOME / ".claw" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

VERSION = "2.0.0"

# === CORES ANSI ===
class Colors:
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    CYAN = '\033[0;36m'
    BOLD = '\033[1m'
    NC = '\033[0m'

# ══════════════════════════════════════════════════════════════════════════════
# CARREGAMENTO DE CONTEXTO (.md FILES)
# ══════════════════════════════════════════════════════════════════════════════

class ProjectContext:
    """Gerencia carregamento de contexto a partir de arquivos .md do projeto"""
    
    # Prioridade de leitura dos arquivos .md
    PRIORITY_FILES = [
        "CLAUDE.md", "GEMINI.md", "AGENTE.md", "AGENT.md",
        "PHILOSOPHY.md", "STANDARDS.md", "DEVELOPMENT.md",
        "QUICKSTART.md", "README.md", "INDEX.md", "SUMMARY.md",
        "ROADMAP.md", "CHANGELOG.md"
    ]
    
    # Padrões a ignorar
    IGNORE_PATTERNS = [
        "node_modules", ".git", "vendor", "dist", "build",
        "target", "__pycache__", ".venv", "venv"
    ]
    
    CACHE_FILE = CACHE_DIR / "context_cache.txt"
    TIMESTAMP_FILE = CACHE_DIR / "context_timestamp.txt"
    FILES_FILE = CACHE_DIR / "context_files.txt"
    MAX_CHARS = 200000
    CACHE_TTL = 3600  # 1 hora
    
    def __init__(self):
        self.context = ""
        self.files_loaded = []
        self.is_loaded = False
    
    def _should_ignore(self, path: str) -> bool:
        """Verifica se caminho deve ser ignorado"""
        for pattern in self.IGNORE_PATTERNS:
            if pattern in path:
                return True
        return False
    
    def _load_from_cache(self) -> bool:
        """Tenta carregar contexto do cache (válido por 1 hora)"""
        if not self.CACHE_FILE.exists() or not self.TIMESTAMP_FILE.exists():
            return False
        
        try:
            age = time.time() - int(self.TIMESTAMP_FILE.read_text().strip())
            if age < self.CACHE_TTL:
                self.context = self.CACHE_FILE.read_text()
                
                # Restaurar lista de arquivos
                if self.FILES_FILE.exists():
                    self.files_loaded = self.FILES_FILE.read_text().strip().split('\n')
                    self.files_loaded = [f for f in self.files_loaded if f]
                
                # Fallback: parsear "📄 ARQUIVO:" se array vazio
                if not self.files_loaded:
                    for line in self.context.split('\n'):
                        if '📄 ARQUIVO:' in line:
                            parts = line.split('📄 ARQUIVO:')
                            if len(parts) > 1:
                                self.files_loaded.append(parts[1].strip())
                
                cache_age_min = age // 60
                print(f"  {Colors.GREEN}⚡ Cache carregado ({cache_age_min}min atrás) — "
                      f"{len(self.files_loaded)} arquivos .md{Colors.NC}", file=sys.stderr)
                return True
        except Exception as e:
            print(f"  {Colors.YELLOW}Erro ao carregar cache: {e}{Colors.NC}", file=sys.stderr)
            return False
        
        return False
    
    def load(self) -> None:
        """Carrega todos os arquivos .md do projeto"""
        if self.is_loaded:
            return
        
        # Tentar cache
        if self._load_from_cache():
            self.is_loaded = True
            return
        
        print(f"  {Colors.BLUE}📚 Carregando documentação do projeto...{Colors.NC}", file=sys.stderr)
        
        context_buffer = ""
        files_loaded = []
        total_chars = 0
        
        # FASE 1: Arquivos prioritários
        for fname in self.PRIORITY_FILES:
            fpath = PROJECT_ROOT / fname
            if fpath.exists() and fpath.stat().st_size > 0:
                try:
                    content = fpath.read_text(errors='ignore')
                    fsize = len(content)
                    
                    if total_chars + fsize > self.MAX_CHARS:
                        remaining = self.MAX_CHARS - total_chars
                        content = content[:remaining] + "\n[... truncado ...]"
                    
                    context_buffer += f"\n{'─'*60}\n📄 ARQUIVO: {fname}\n{'─'*60}\n{content}\n"
                    total_chars += fsize
                    files_loaded.append(fname)
                    
                    if total_chars >= self.MAX_CHARS:
                        break
                except Exception as e:
                    print(f"  Erro ao ler {fname}: {e}", file=sys.stderr)
                    continue
        
        # FASE 2: Demais arquivos .md
        if total_chars < self.MAX_CHARS:
            try:
                for fpath in sorted(PROJECT_ROOT.rglob("*.md")):
                    if fpath.name.startswith('.'):
                        continue
                    if self._should_ignore(str(fpath)):
                        continue
                    if fpath.name in files_loaded:
                        continue
                    
                    try:
                        content = fpath.read_text(errors='ignore')
                        if not content.strip():
                            continue
                        
                        fsize = len(content)
                        if total_chars + fsize > self.MAX_CHARS:
                            remaining = self.MAX_CHARS - total_chars
                            if remaining < 200:
                                break
                            content = content[:remaining] + "\n[... truncado ...]"
                        
                        rel_path = str(fpath.relative_to(PROJECT_ROOT))
                        context_buffer += f"\n{'─'*60}\n📄 ARQUIVO: {rel_path}\n{'─'*60}\n{content}\n"
                        total_chars += fsize
                        files_loaded.append(rel_path)
                        
                        if total_chars >= self.MAX_CHARS:
                            break
                    except Exception:
                        continue
            except Exception:
                pass
        
        self.context = context_buffer
        self.files_loaded = files_loaded
        self.is_loaded = True
        
        # Salvar em cache
        self.CACHE_FILE.write_text(self.context)
        self.TIMESTAMP_FILE.write_text(str(int(time.time())))
        self.FILES_FILE.write_text('\n'.join(files_loaded))
        
        count = len(files_loaded)
        print(f"  {Colors.GREEN}✅ {count} arquivo(s) .md carregado(s) — {total_chars} chars{Colors.NC}",
              file=sys.stderr)
        for f in files_loaded:
            print(f"     {Colors.CYAN}·{Colors.NC} {f}", file=sys.stderr)
        print("", file=sys.stderr)
    
    def get_block(self) -> str:
        """Retorna bloco de contexto formatado para injetar no prompt"""
        self.load()
        
        if not self.context:
            return ""
        
        return f"""
================================================================================
CONTEXTO COMPLETO DO PROJETO
(Documentação lida automaticamente dos arquivos .md)
================================================================================
{self.context}
================================================================================
INSTRUÇÕES DE USO DO CONTEXTO:
- Respeite as convenções, filosofias e padrões descritos acima
- Priorize CLAUDE.md / GEMINI.md / AGENTE.md como diretrizes principais
- Use README, PHILOSOPHY, STANDARDS para entender o projeto
- Mantenha consistência com o estilo e decisões já documentadas
================================================================================
"""
    
    def show_status(self) -> None:
        """Mostra status do contexto carregado"""
        self.load()
        count = len(self.files_loaded)
        if count > 0:
            print(f"  {Colors.GREEN}📚 Contexto:{Colors.NC} {count} arquivos .md ativos")
        else:
            print(f"  {Colors.YELLOW}⚠️  Nenhum .md encontrado em:{Colors.NC} {PROJECT_ROOT}")

# ══════════════════════════════════════════════════════════════════════════════
# CLIENTE DE API GEMINI
# ══════════════════════════════════════════════════════════════════════════════

class GeminiClient:
    """Cliente para API Google Gemini"""
    
    API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    TIMEOUT = 60
    
    def __init__(self):
        self.api_key = self._load_api_key()
    
    def _load_api_key(self) -> str:
        """Carrega chave de API do config"""
        try:
            if CONFIG_FILE.exists():
                config = json.loads(CONFIG_FILE.read_text())
                if "google" in config:
                    return config["google"]
        except Exception:
            pass
        return ""
    
    def is_configured(self) -> bool:
        """Verifica se API está configurada"""
        return bool(self.api_key and self.api_key.startswith("AIzaSy"))
    
    def call(self, prompt: str, model: str = "gemini-2.0-flash") -> str:
        """Faz chamada à API Gemini"""
        if not self.is_configured():
            raise RuntimeError("API Google não configurada!")
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"maxOutputTokens": 2000, "temperature": 0.7}
        }
        
        try:
            import subprocess
            temp_file = f"/tmp/api_request_{os.getpid()}.json"
            Path(temp_file).write_text(json.dumps(payload))
            
            result = subprocess.run(
                [
                    "curl", "-s", "--max-time", str(self.TIMEOUT),
                    "--connect-timeout", "10",
                    f"{self.API_URL.format(model=model)}?key={self.api_key}",
                    "-H", "Content-Type: application/json",
                    "-d", f"@{temp_file}"
                ],
                capture_output=True,
                text=True,
                timeout=self.TIMEOUT + 5
            )
            
            Path(temp_file).unlink(missing_ok=True)
            return result.stdout
        except subprocess.TimeoutExpired:
            raise RuntimeError("Timeout na chamada à API")
        except Exception as e:
            raise RuntimeError(f"Erro na chamada à API: {e}")
    
    @staticmethod
    def extract_text(response: str) -> str:
        """Extrai texto da resposta da API"""
        try:
            data = json.loads(response)
            if "candidates" in data:
                for candidate in data["candidates"]:
                    if "content" in candidate:
                        for part in candidate["content"].get("parts", []):
                            if "text" in part:
                                return part["text"]
            
            # Verificar se há erro
            if "error" in data:
                error_msg = data["error"].get("message", "Erro desconhecido")
                if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                    return "ERROR_QUOTA"
                return f"ERROR_{error_msg}"
        except json.JSONDecodeError:
            pass
        
        return ""

# ══════════════════════════════════════════════════════════════════════════════
# BUSCA NA WEB
# ══════════════════════════════════════════════════════════════════════════════

class WebSearch:
    """Busca na web usando Wikipedia e Google"""
    
    @staticmethod
    def urlencode(text: str) -> str:
        """Encoda URL em português"""
        try:
            return urllib.parse.quote(text, safe='')
        except Exception:
            return text.replace(' ', '+')
    
    @staticmethod
    def search(query: str, limit: int = 3) -> str:
        """Busca na Wikipedia"""
        encoded = WebSearch.urlencode(query)
        url = f"https://pt.wikipedia.org/w/api.php?action=query&list=search&srsearch={encoded}&srlimit={limit}&format=json"
        
        try:
            result = subprocess.run(
                ["curl", "-s", "--max-time", "10", url],
                capture_output=True,
                text=True,
                timeout=15
            )
            
            if result.returncode != 0:
                return f"🔗 Google IA: https://www.google.com/search?q={encoded}&udm=50"
            
            data = json.loads(result.stdout)
            search_results = data.get("query", {}).get("search", [])
            
            if not search_results:
                return f"🔗 Google IA: https://www.google.com/search?q={encoded}&udm=50"
            
            output = "\n"
            for idx, item in enumerate(search_results[:3], 1):
                title = item["title"]
                snippet = item["snippet"]
                # Remove tags HTML
                for tag in ['<span class="searchmatch">', '</span>', '<b>', '</b>']:
                    snippet = snippet.replace(tag, '')
                snippet = ' '.join(snippet.split()).strip()
                
                output += f"  [{idx}] {title}\n"
                output += f"      {snippet[:150]}{'...' if len(snippet) > 150 else ''}\n\n"
            
            output += "  🔗 LINKS:\n"
            for idx, item in enumerate(search_results[:3], 1):
                title = item["title"]
                output += f"  [{idx}] https://pt.wikipedia.org/wiki/{title.replace(' ', '_')}\n"
            
            return output
        except Exception:
            return f"🔗 Google IA: https://www.google.com/search?q={encoded}&udm=50"

# ══════════════════════════════════════════════════════════════════════════════
# FALLBACK E APRENDIZADO LOCAL
# ══════════════════════════════════════════════════════════════════════════════

class LocalAI:
    """Sistema de sugestões locais + aprendizado automático"""
    
    LEARNING_FILE = CACHE_DIR / "learn_patterns.txt"
    
    @staticmethod
    def detect_scope(original_path: str, modified_path: str) -> str:
        """Detecta escopo de mudança: SINGLE_LINE, BLOCK ou FULL_FILE"""
        try:
            orig_lines = Path(original_path).read_text().count('\n') if Path(original_path).exists() else 0
            mod_lines = Path(modified_path).read_text().count('\n') if Path(modified_path).exists() else 0
            
            # Contar diferenças
            diff_count = 0
            try:
                orig = Path(original_path).read_text().split('\n') if Path(original_path).exists() else []
                mod = Path(modified_path).read_text().split('\n') if Path(modified_path).exists() else []
                for line in unified_diff(orig, mod):
                    if line.startswith('<') or line.startswith('>'):
                        diff_count += 1
            except Exception:
                pass
            
            if diff_count <= 2:
                return "SINGLE_LINE"
            elif diff_count <= 20:
                return "BLOCK"
            else:
                return "FULL_FILE"
        except Exception:
            return "FULL_FILE"
    
    @staticmethod
    def suggest(file_path: str, cmd_type: str, scope: str) -> str:
        """Gera sugestão adaptada ao escopo"""
        suggestions = {
            "SINGLE_LINE": "MELHORIA (1 Linha): Simplificar expressão, melhorar legibilidade, adicionar validação",
            "BLOCK": "REFATORAÇÃO (Bloco): Extrair função, consolidar lógica duplicada, melhorar nomes",
            "FULL_FILE": "REFATORAÇÃO (Arquivo): Separar responsabilidades, consolidar duplicações, aplicar padrões"
        }
        return suggestions.get(scope, suggestions["FULL_FILE"])
    
    @staticmethod
    def register(action: str, cmd_type: str, filename: str, scope: str) -> None:
        """Registra feedback para aprendizado"""
        LocalAI.LEARNING_FILE.parent.mkdir(parents=True, exist_ok=True)
        timestamp = int(time.time())
        line = f"{action}:{cmd_type}:{filename}:{scope}:{timestamp}\n"
        LocalAI.LEARNING_FILE.write_text(LocalAI.LEARNING_FILE.read_text() + line, encoding='utf-8')

class SmartFallback:
    """Fallback inteligente quando API falha"""
    
    @staticmethod
    def improve(file_path: str, cmd_type: str) -> bool:
        """Oferece sugestão inteligente local quando API falha"""
        print(f"  {Colors.YELLOW}⚠️  API esgotada. Ativando modo inteligente local...{Colors.NC}")
        
        try:
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                return False
            
            filename = file_path_obj.name
            basename = file_path_obj.stem
            ext = file_path_obj.suffix
            
            # Backup imediato
            backup_path = Path(f"/tmp/{basename}_original_backup_{os.getpid()}{ext}")
            backup_path.write_text(file_path_obj.read_text())
            
            # Detectar escopo
            file_lines = file_path_obj.read_text().count('\n')
            if file_lines < 50:
                scope = "SINGLE_LINE"
            elif file_lines < 200:
                scope = "BLOCK"
            else:
                scope = "FULL_FILE"
            
            # Gerar sugestão
            suggestion = LocalAI.suggest(file_path, cmd_type, scope)
            
            # Criar arquivo com sugestões
            improved_path = Path(f"/tmp/{basename}_improved_full_{os.getpid()}{ext}")
            header = f"{'#' if ext in ['.py', '.sh'] else '//'} " + "=" * 70 + "\n"
            header += f"{'#' if ext in ['.py', '.sh'] else '//'} 💡 SUGESTÕES INTELIGENTES LOCAIS [{scope}]\n"
            header += f"{'#' if ext in ['.py', '.sh'] else '//'} {suggestion}\n"
            header += f"{'#' if ext in ['.py', '.sh'] else '//'} " + "=" * 70 + "\n\n"
            
            improved_path.write_text(header + file_path_obj.read_text())
            
            # Abrir em VS Code se disponível
            try:
                subprocess.run(["code", str(improved_path)], timeout=2, capture_output=True)
            except Exception:
                pass
            
            # Mostrar sugestão
            print(f"\n{Colors.CYAN}┌{'─'*60}┐{Colors.NC}")
            print(f"{Colors.CYAN}│{Colors.NC}  {Colors.GREEN}🧠 SUGESTÕES INTELIGENTES [{scope}]{Colors.NC}")
            print(f"{Colors.CYAN}└{'─'*60}┘{Colors.NC}\n")
            print(f"  {suggestion}\n")
            
            # Menu de ação
            print(f"{Colors.CYAN}┌{'─'*60}┐{Colors.NC}")
            print(f"{Colors.CYAN}│{Colors.NC}  {Colors.YELLOW}? AÇÃO{Colors.NC}")
            print(f"{Colors.CYAN}└{'─'*60}┘{Colors.NC}\n")
            
            scope_msg = {
                "SINGLE_LINE": "Aplicar sugestão de melhoria (1 linha)? (s/n)",
                "BLOCK": "Aplicar sugestões de refatoração (bloco)? (s/n)",
                "FULL_FILE": "Aplicar refatoração completa do arquivo? (s/n)"
            }
            
            print(f"{Colors.YELLOW}{scope_msg.get(scope, 'Aplicar mudanças? (s/n)')}{Colors.NC}")
            response = input().strip().lower()
            
            clean_path = Path(f"/tmp/{basename}_improved_clean_{os.getpid()}{ext}")
            
            if response in ['s', 'sim', 'y', 'yes']:
                print(f"\n{Colors.CYAN}┌{'─'*60}┐{Colors.NC}")
                print(f"{Colors.CYAN}│{Colors.NC}  {Colors.GREEN}✅ {scope.replace('_', ' ').upper()}{Colors.NC}")
                print(f"{Colors.CYAN}└{'─'*60}┘\n{Colors.NC}")
                
                # Copiar versão melhorada (sem header)
                improved_text = improved_path.read_text()
                lines = improved_text.split('\n')
                # Pular header
                start = 0
                for i, line in enumerate(lines):
                    if "=" * 70 in line and i > 2:
                        start = i + 1
                        break
                
                clean_path.write_text('\n'.join(lines[start:]))
                
                # Backup permanente
                file_path_obj.write_text(f"{file_path_obj.read_text()}.bak")
                
                # Copiar versão melhorada
                file_path_obj.write_text(clean_path.read_text())
                
                print(f"{Colors.GREEN}✅ Mudanças aplicadas com sucesso!{Colors.NC}")
                print(f"{Colors.BLUE}📂 Backup: {file_path}.bak{Colors.NC}\n")
                
                # Registrar aprendizado
                LocalAI.register("ACCEPTED", cmd_type, filename, scope)
                learning_count = len(LocalAI.LEARNING_FILE.read_text().strip().split('\n'))
                print(f"{Colors.BLUE}🧠 Padrão [{scope}] salvo para auto-aprendizado ({learning_count} registros){Colors.NC}\n")
                
                return True
            else:
                print(f"\n{Colors.CYAN}┌{'─'*60}┐{Colors.NC}")
                print(f"{Colors.CYAN}│{Colors.NC}  {Colors.YELLOW}⏭️  SUGESTÕES REJEITADAS{Colors.NC}")
                print(f"{Colors.CYAN}└{'─'*60}┘\n{Colors.NC}")
                
                print(f"{Colors.BLUE}📂 Arquivo original mantido intacto{Colors.NC}")
                LocalAI.register("REJECTED", cmd_type, filename, scope)
                print(f"{Colors.BLUE}🧠 Feedback [{scope}] registrado para melhoria{Colors.NC}\n")
                
                return False
        except Exception as e:
            print(f"{Colors.RED}❌ Erro no fallback: {e}{Colors.NC}")
            return False

# ══════════════════════════════════════════════════════════════════════════════
# PROMPTS
# ══════════════════════════════════════════════════════════════════════════════

class PromptBuilder:
    """Constrói prompts para diferentes tipos de análise"""
    
    @staticmethod
    def get_project_info() -> Tuple[str, str]:
        """Detecta linguagem e framework do projeto"""
        lang, framework = "desconhecida", "nenhum"
        
        if (PROJECT_ROOT / "Cargo.toml").exists():
            return "Rust", "Cargo"
        elif (PROJECT_ROOT / "package.json").exists():
            return "JavaScript/TypeScript", "Node.js"
        elif (PROJECT_ROOT / "pyproject.toml").exists() or (PROJECT_ROOT / "setup.py").exists():
            return "Python", "Python"
        elif (PROJECT_ROOT / ".csproj").exists() or (PROJECT_ROOT / "pom.xml").exists():
            return "C#/.NET", ".NET"
        elif (PROJECT_ROOT / "go.mod").exists():
            return "Go", "Go"
        
        return lang, framework
    
    @staticmethod
    def build(action: str, file_path: str, content: str, context_block: str) -> str:
        """Constrói prompt para ação específica"""
        lang, framework = PromptBuilder.get_project_info()
        
        base = f"""{context_block}
Você é um assistente profissional de desenvolvimento de software.

CONTEXTO DO PROJETO:
- Linguagem: {lang}
- Framework: {framework}
- Arquivo: {file_path}
"""
        
        if action == "analyze":
            return base + f"""
TAREFA:
Analise o código fornecido e:
1. Identifique possíveis bugs ou issues de segurança
2. Sugira melhorias de performance
3. Verifique boas práticas conforme padrões do projeto
4. Aponte problemas de legibilidade

Seja conciso, profissional e alinhado com a filosofia do projeto.

CÓDIGO A ANALISAR:
```
{content}
```

ANÁLISE:
"""
        
        elif action == "improve":
            return base + f"""
TAREFA:
Refatore o código mantendo a mesma funcionalidade:
1. Melhore legibilidade conforme padrões do projeto
2. Aplique design patterns descritos na documentação
3. Otimize performance
4. Adicione type hints/annotations se aplicável

RETORNE O CÓDIGO COMPLETO, do início ao fim.
MANTENHA TODOS os aliases, caminhos e comandos EXATAMENTE como estão.

CÓDIGO ATUAL:
```
{content}
```

CÓDIGO REFATORADO:
```
"""
        
        elif action == "document":
            return base + f"""
TAREFA:
Crie documentação clara e consistente:
1. Docstrings para funções
2. Explicação de algoritmos complexos
3. Exemplos de uso alinhados com o projeto
4. Mantenha tom e estilo da documentação existente

CÓDIGO:
```
{content}
```

DOCUMENTAÇÃO:
"""
        
        elif action == "test":
            return base + f"""
TAREFA:
Crie casos de teste abrangentes:
1. Testes unitários
2. Casos edge
3. Tratamento de erros
4. Mock de dependências se necessário
5. Siga padrões de teste do projeto

CÓDIGO A TESTAR:
```
{content}
```

TESTES:
```
"""
        
        return base

# ══════════════════════════════════════════════════════════════════════════════
# AUTO-IMPROVE
# ══════════════════════════════════════════════════════════════════════════════

class AutoImprove:
    """Refatora automaticamente resultados"""
    
    @staticmethod
    def improve_result(result: str, cmd_type: str, context_block: str, gemini: GeminiClient) -> str:
        """Refatora resultado automaticamente"""
        if len(result) < 100:
            return result
        
        print(f"{Colors.YELLOW}🔧 Refatorando resultado automaticamente...{Colors.NC}")
        
        prompt = f"""{context_block}

Você é um especialista em otimização e refinamento de saídas.

RESULTADO ORIGINAL:
```
{result}
```

TAREFA:
Melhore este resultado mantendo os mesmos conceitos:
1. Melhore clareza e legibilidade
2. Organize melhor a informação se necessário
3. Corrija erros gramaticais
4. Mantenha brevidade mas garantindo completude
5. Siga padrões de formatação do projeto

RESULTADO MELHORADO:
(sem marcação de código, apenas o texto refatorado)
"""
        
        try:
            api_response = gemini.call(prompt)
            improved = GeminiClient.extract_text(api_response)
            
            if len(improved) < 50 or improved.startswith("ERROR_"):
                return result
            
            # Comparação
            print(f"\n{Colors.BLUE}📊 COMPARAÇÃO (Original vs Melhorado):{Colors.NC}")
            print(f"{Colors.BLUE}{Colors.BOLD}{'─'*60}{Colors.NC}")
            
            # Mostrar diff simples
            orig_lines = result.split('\n')[:5]
            impr_lines = improved.split('\n')[:5]
            print(f"{Colors.YELLOW}Original:{Colors.NC}")
            for line in orig_lines:
                print(f"  {line}")
            print(f"\n{Colors.GREEN}Melhorado:{Colors.NC}")
            for line in impr_lines:
                print(f"  {line}")
            
            print(f"{Colors.BLUE}{Colors.BOLD}{'─'*60}{Colors.NC}")
            print(f"{Colors.YELLOW}Aceitar mudanças? (y/n){Colors.NC}")
            
            response = input().strip().lower()
            if response in ['y', 'yes', 's', 'sim']:
                print(f"{Colors.GREEN}✅ Mudanças aplicadas!{Colors.NC}")
                return improved
        except Exception as e:
            print(f"{Colors.YELLOW}Erro ao refatorar: {e}{Colors.NC}")
        
        return result

# ══════════════════════════════════════════════════════════════════════════════
# COMANDOS PRINCIPAIS
# ══════════════════════════════════════════════════════════════════════════════

def cmd_analyze(file_path: str, context: ProjectContext, gemini: GeminiClient) -> None:
    """Analisa arquivo"""
    file_obj = Path(file_path)
    if not file_obj.exists():
        print(f"{Colors.RED}❌ Arquivo não encontrado: {file_path}{Colors.NC}")
        sys.exit(1)
    
    print(f"{Colors.CYAN}📊 Analisando: {file_path}{Colors.NC}")
    context.show_status()
    
    content = file_obj.read_text()
    prompt = PromptBuilder.build("analyze", file_path, content, context.get_block())
    
    print(f"{Colors.YELLOW}🔄 Processando com IA + contexto do projeto...{Colors.NC}")
    
    try:
        response = gemini.call(prompt)
        result = GeminiClient.extract_text(response)
        
        if result.startswith("ERROR_QUOTA") or not result:
            SmartFallback.improve(file_path, "analyze")
            return
        
        print(f"\n{Colors.CYAN}┌{'─'*60}┐{Colors.NC}")
        print(f"{Colors.CYAN}│{Colors.NC}  {Colors.GREEN}✅ ANÁLISE{Colors.NC}")
        print(f"{Colors.CYAN}└{'─'*60}┘{Colors.NC}\n")
        print(f"{Colors.GREEN}{result}{Colors.NC}\n")
        
        # Auto-improve
        print(f"{Colors.YELLOW}Deseja melhorar esta análise automaticamente? (y/n){Colors.NC}")
        if input().strip().lower() in ['y', 'yes', 's', 'sim']:
            AutoImprove.improve_result(result, "analyze", context.get_block(), gemini)
    
    except Exception as e:
        print(f"{Colors.RED}❌ Erro: {e}{Colors.NC}")
        SmartFallback.improve(file_path, "analyze")

def cmd_improve(file_path: str, context: ProjectContext, gemini: GeminiClient) -> None:
    """Refatora arquivo"""
    file_obj = Path(file_path)
    if not file_obj.exists():
        print(f"{Colors.RED}❌ Arquivo não encontrado: {file_path}{Colors.NC}")
        sys.exit(1)
    
    print(f"{Colors.CYAN}🔧 Refatorando: {file_path}{Colors.NC}")
    context.show_status()
    
    content = file_obj.read_text()
    prompt = PromptBuilder.build("improve", file_path, content, context.get_block())
    
    print(f"{Colors.YELLOW}🔄 Processando melhorias com IA...{Colors.NC}")
    
    try:
        response = gemini.call(prompt)
        result = GeminiClient.extract_text(response)
        
        if not result or len(result) < 100:
            print(f"{Colors.RED}❌ Erro: resposta inválida{Colors.NC}")
            SmartFallback.improve(file_path, "improve")
            return
        
        # Mostrar diff
        print(f"\n{Colors.BLUE}💡 SUGESTÃO DE MUDANÇA:{Colors.NC}")
        print(f"{Colors.GRAY}{'─'*60}{Colors.NC}")
        
        # Criar arquivo temporário para diff
        temp_file = Path(f"/tmp/suggestion_{file_obj.name}")
        temp_file.write_text(result)
        
        try:
            subprocess.run(
                ["diff", "--color=always", "-u", file_path, str(temp_file)],
                timeout=5
            )
        except Exception:
            print(result[:500] + "..." if len(result) > 500 else result)
        
        print(f"{Colors.GRAY}{'─'*60}{Colors.NC}")
        print(f"{Colors.YELLOW}Deseja aplicar estas mudanças? (y/n){Colors.NC}")
        
        if input().strip().lower() in ['y', 'yes', 's', 'sim']:
            backup_path = Path(f"{file_path}.bak")
            backup_path.write_text(file_obj.read_text())
            file_obj.write_text(result)
            print(f"{Colors.GREEN}✅ Sucesso! Backup criado: {backup_path}{Colors.NC}")
        else:
            print(f"{Colors.RED}❌ Mudança descartada{Colors.NC}")
        
        temp_file.unlink(missing_ok=True)
    
    except Exception as e:
        print(f"{Colors.RED}❌ Erro: {e}{Colors.NC}")
        SmartFallback.improve(file_path, "improve")

def cmd_document(file_path: str, context: ProjectContext, gemini: GeminiClient) -> None:
    """Documenta arquivo"""
    file_obj = Path(file_path)
    if not file_obj.exists():
        print(f"{Colors.RED}❌ Arquivo não encontrado: {file_path}{Colors.NC}")
        sys.exit(1)
    
    print(f"{Colors.CYAN}📝 Documentando: {file_path}{Colors.NC}")
    context.show_status()
    
    content = file_obj.read_text()
    prompt = PromptBuilder.build("document", file_path, content, context.get_block())
    
    print(f"{Colors.YELLOW}🔄 Processando com IA...{Colors.NC}")
    
    try:
        response = gemini.call(prompt)
        result = GeminiClient.extract_text(response)
        
        if result.startswith("ERROR_QUOTA") or not result:
            SmartFallback.improve(file_path, "document")
            return
        
        print(f"\n{Colors.CYAN}┌{'─'*60}┐{Colors.NC}")
        print(f"{Colors.CYAN}│{Colors.NC}  {Colors.GREEN}✅ DOCUMENTAÇÃO{Colors.NC}")
        print(f"{Colors.CYAN}└{'─'*60}┘{Colors.NC}\n")
        print(f"{Colors.GREEN}{result}{Colors.NC}\n")
        
        print(f"{Colors.YELLOW}Deseja melhorar esta documentação? (y/n){Colors.NC}")
        if input().strip().lower() in ['y', 'yes', 's', 'sim']:
            AutoImprove.improve_result(result, "document", context.get_block(), gemini)
    
    except Exception as e:
        print(f"{Colors.RED}❌ Erro: {e}{Colors.NC}")
        SmartFallback.improve(file_path, "document")

def cmd_test(file_path: str, context: ProjectContext, gemini: GeminiClient) -> None:
    """Cria testes"""
    file_obj = Path(file_path)
    if not file_obj.exists():
        print(f"{Colors.RED}❌ Arquivo não encontrado: {file_path}{Colors.NC}")
        sys.exit(1)
    
    print(f"{Colors.CYAN}🧪 Criando testes: {file_path}{Colors.NC}")
    context.show_status()
    
    content = file_obj.read_text()
    prompt = PromptBuilder.build("test", file_path, content, context.get_block())
    
    print(f"{Colors.YELLOW}🔄 Processando com IA...{Colors.NC}")
    
    try:
        response = gemini.call(prompt)
        result = GeminiClient.extract_text(response)
        
        if result.startswith("ERROR_QUOTA") or not result:
            SmartFallback.improve(file_path, "test")
            return
        
        print(f"\n{Colors.CYAN}┌{'─'*60}┐{Colors.NC}")
        print(f"{Colors.CYAN}│{Colors.NC}  {Colors.GREEN}✅ TESTES UNITÁRIOS{Colors.NC}")
        print(f"{Colors.CYAN}└{'─'*60}┘{Colors.NC}\n")
        print(f"{Colors.GREEN}{result}{Colors.NC}\n")
        
        print(f"{Colors.YELLOW}Deseja melhorar estes testes? (y/n){Colors.NC}")
        if input().strip().lower() in ['y', 'yes', 's', 'sim']:
            AutoImprove.improve_result(result, "test", context.get_block(), gemini)
    
    except Exception as e:
        print(f"{Colors.RED}❌ Erro: {e}{Colors.NC}")
        SmartFallback.improve(file_path, "test")

def cmd_ask(question: str, context: ProjectContext, gemini: GeminiClient) -> None:
    """Responde pergunta"""
    if not question:
        print(f"{Colors.RED}❌ Pergunta vazia!{Colors.NC}")
        sys.exit(1)
    
    print(f"\n{Colors.CYAN}┌{'─'*60}┐{Colors.NC}")
    print(f"{Colors.CYAN}│{Colors.NC}  {Colors.YELLOW}❓ PERGUNTA{Colors.NC}")
    print(f"{Colors.CYAN}└{'─'*60}┘{Colors.NC}")
    print(f"  {Colors.YELLOW}{question}{Colors.NC}")
    context.show_status()
    
    print(f"  {Colors.BLUE}🔍 Pesquisando na web...{Colors.NC}")
    web_results = WebSearch.search(question, 5)
    
    prompt = f"""{context.get_block()}

Você é um assistente profissional que responde com contexto do projeto.

PERGUNTA: {question}

RESULTADOS DA WEB:
{web_results}

Responda em português de forma clara, estruturada e alinhada com os padrões do projeto.
"""
    
    print(f"{Colors.YELLOW}🤖 Processando com IA + Pesquisa Web...{Colors.NC}")
    
    try:
        response = gemini.call(prompt)
        result = GeminiClient.extract_text(response)
        
        if not result:
            print(f"\n{Colors.CYAN}┌{'─'*60}┐{Colors.NC}")
            print(f"{Colors.CYAN}│{Colors.NC}  {Colors.BLUE}🌐 RESULTADOS DA WEB{Colors.NC}")
            print(f"{Colors.CYAN}└{'─'*60}┘{Colors.NC}\n")
            print(f"{web_results}\n")
            return
        
        print(f"\n{Colors.CYAN}┌{'─'*60}┐{Colors.NC}")
        print(f"{Colors.CYAN}│{Colors.NC}  {Colors.GREEN}✅ RESPOSTA{Colors.NC}")
        print(f"{Colors.CYAN}└{'─'*60}┘{Colors.NC}\n")
        print(f"{Colors.GREEN}{result}{Colors.NC}\n")
        
        print(f"{Colors.YELLOW}Deseja melhorar esta resposta? (y/n){Colors.NC}")
        if input().strip().lower() in ['y', 'yes', 's', 'sim']:
            AutoImprove.improve_result(result, "ask", context.get_block(), gemini)
    
    except Exception as e:
        print(f"{Colors.RED}❌ Erro: {e}{Colors.NC}")

def cmd_search(query: str, context: ProjectContext, gemini: GeminiClient) -> None:
    """Pesquisa na web"""
    if not query:
        print(f"{Colors.RED}❌ Consulta vazia!{Colors.NC}")
        sys.exit(1)
    
    print(f"{Colors.CYAN}🔍 Pesquisando: {query}{Colors.NC}")
    web_results = WebSearch.search(query, 5)
    
    print(f"{Colors.GREEN}📰 Resultados da Web:{Colors.NC}")
    print("─" * 60)
    print(web_results[:500])
    print("─" * 60)
    
    prompt = f"""{context.get_block()}

Você é um assistente que pesquisa e responde em português.

CONSULTA: {query}

RESULTADOS DA WEB:
{web_results}

Responda de forma clara, estruturada e com fontes quando possível.
"""
    
    print(f"{Colors.YELLOW}🤖 Processando com IA + Pesquisa Web...{Colors.NC}")
    
    try:
        response = gemini.call(prompt)
        result = GeminiClient.extract_text(response)
        
        if not result or result.startswith("ERROR_QUOTA"):
            print(f"{Colors.GREEN}✅ Modo ECONOMIA ativado{Colors.NC}\n")
            print(f"{Colors.CYAN}┌{'─'*60}┐{Colors.NC}")
            print(f"{Colors.CYAN}│{Colors.NC}  {Colors.BLUE}🌐 RESULTADOS DA WEB{Colors.NC}")
            print(f"{Colors.CYAN}└{'─'*60}┘{Colors.NC}\n")
            print(f"{web_results}\n")
            return
        
        print(f"\n{Colors.CYAN}┌{'─'*60}┐{Colors.NC}")
        print(f"{Colors.CYAN}│{Colors.NC}  {Colors.GREEN}✅ RESPOSTA{Colors.NC}")
        print(f"{Colors.CYAN}└{'─'*60}┘{Colors.NC}\n")
        print(f"{Colors.GREEN}{result}{Colors.NC}\n")
        
        print(f"{Colors.YELLOW}Deseja melhorar esta resposta? (y/n){Colors.NC}")
        if input().strip().lower() in ['y', 'yes', 's', 'sim']:
            AutoImprove.improve_result(result, "search", context.get_block(), gemini)
    
    except Exception as e:
        print(f"{Colors.RED}❌ Erro: {e}{Colors.NC}")

def cmd_research(question: str, context: ProjectContext, gemini: GeminiClient) -> None:
    """Pesquisa profunda"""
    if not question:
        print(f"{Colors.RED}❌ Pergunta vazia!{Colors.NC}")
        sys.exit(1)
    
    print(f"{Colors.CYAN}🔬 Pesquisa Profunda: {question}{Colors.NC}")
    web_results = WebSearch.search(question, 10)
    
    prompt = f"""{context.get_block()}

Você é um assistante de pesquisa profunda com acesso ao contexto completo do projeto.

PERGUNTA: {question}

DADOS DE PESQUISA WEB:
{web_results}

Responda em português com:
1. Resposta clara e estruturada
2. Contexto do projeto quando relevante
3. Informações verificadas com fontes
4. Limitações ou pontos de incerteza
5. Sugestões de próximos passos
"""
    
    print(f"{Colors.YELLOW}🔄 Processando pesquisa avançada...{Colors.NC}")
    
    try:
        response = gemini.call(prompt)
        result = GeminiClient.extract_text(response)
        
        if not result or result.startswith("ERROR_QUOTA"):
            print(f"\n{Colors.CYAN}┌{'─'*60}┐{Colors.NC}")
            print(f"{Colors.CYAN}│{Colors.NC}  {Colors.BLUE}🌐 RESULTADOS DA WEB{Colors.NC}")
            print(f"{Colors.CYAN}└{'─'*60}┘{Colors.NC}\n")
            print(f"{web_results}\n")
            return
        
        print(f"\n{Colors.CYAN}┌{'─'*60}┐{Colors.NC}")
        print(f"{Colors.CYAN}│{Colors.NC}  {Colors.GREEN}📊 RESULTADO DA PESQUISA{Colors.NC}")
        print(f"{Colors.CYAN}└{'─'*60}┘{Colors.NC}\n")
        print(f"{Colors.GREEN}{result}{Colors.NC}\n")
        
        print(f"{Colors.YELLOW}Deseja melhorar esta resposta? (y/n){Colors.NC}")
        if input().strip().lower() in ['y', 'yes', 's', 'sim']:
            AutoImprove.improve_result(result, "research", context.get_block(), gemini)
    
    except Exception as e:
        print(f"{Colors.RED}❌ Erro: {e}{Colors.NC}")

def cmd_context(context: ProjectContext) -> None:
    """Lista contexto carregado"""
    print(f"\n{Colors.CYAN}┌{'─'*60}┐{Colors.NC}")
    print(f"{Colors.CYAN}│{Colors.NC}  {Colors.BLUE}📚 CONTEXTO DO PROJETO{Colors.NC}")
    print(f"{Colors.CYAN}└{'─'*60}┘{Colors.NC}\n")
    
    context.load()
    count = len(context.files_loaded)
    
    if count > 0:
        print(f"  {Colors.GREEN}{count} arquivo(s) .md carregados:{Colors.NC}\n")
        for i, f in enumerate(context.files_loaded, 1):
            print(f"  {Colors.CYAN}[{i}]{Colors.NC} {f}")
        print(f"\n  {Colors.BLUE}Raiz do projeto:{Colors.NC} {PROJECT_ROOT}\n")
    else:
        print(f"  {Colors.YELLOW}⚠️  Nenhum arquivo .md encontrado{Colors.NC}\n")

def cmd_status() -> None:
    """Mostra status do agente"""
    gemini = GeminiClient()
    print(f"\n{Colors.CYAN}{'═'*70}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}🤖 CLAW_RAFAEL_IA - v{VERSION} (Python 3){Colors.NC}")
    print(f"{Colors.CYAN}{'═'*70}{Colors.NC}\n")
    print(f"  {Colors.YELLOW}API GOOGLE{Colors.NC}      ● ", end="")
    print(Colors.GREEN + "CONFIGURADA" + Colors.NC if gemini.is_configured() else Colors.RED + "NÃO CONFIGURADA" + Colors.NC)
    print(f"  {Colors.GREEN}MODO OPERAÇÃO{Colors.NC}   ● {Colors.CYAN}Economia Web + IA + Contexto .md{Colors.NC}")
    print(f"  {Colors.CYAN}LINGUAGENS{Colors.NC}      ● {Colors.YELLOW}Rust, Python, JS, C#, Go, Ruby, PHP, Java, C++{Colors.NC}")
    print(f"  {Colors.CYAN}CAPACIDADES{Colors.NC}     ● {Colors.YELLOW}Análise, Refatoração, Documentação, Testes, Contexto{Colors.NC}\n")
    print(f"{Colors.CYAN}{'═'*70}{Colors.NC}")
    print(f"\n{Colors.CYAN}🚀 COMANDOS DISPONÍVEIS{Colors.NC}\n")
    print(f"  {Colors.YELLOW}python3 agent.py analyze <arquivo>{Colors.NC}   - Analisa com contexto")
    print(f"  {Colors.YELLOW}python3 agent.py improve <arquivo>{Colors.NC}   - Refatora com padrões")
    print(f"  {Colors.YELLOW}python3 agent.py document <arquivo>{Colors.NC}  - Documenta")
    print(f"  {Colors.YELLOW}python3 agent.py test <arquivo>{Colors.NC}      - Cria testes")
    print(f"  {Colors.YELLOW}python3 agent.py ask \"PERGUNTA\"{Colors.NC}    - Responde confiável")
    print(f"  {Colors.YELLOW}python3 agent.py search \"CONSULTA\"{Colors.NC} - Pesquisa web")
    print(f"  {Colors.YELLOW}python3 agent.py research \"PERGUNTA\"{Colors.NC} - Pesquisa profunda")
    print(f"  {Colors.YELLOW}python3 agent.py context{Colors.NC}             - Lista arquivos")
    print(f"\n")

def cmd_help() -> None:
    """Mostra ajuda"""
    print(f"\n{Colors.CYAN}{'═'*70}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}🤖 AGENTE PROFISSIONAL v{VERSION} - Python 3{Colors.NC}")
    print(f"{Colors.CYAN}{'═'*70}{Colors.NC}\n")
    print(f"{Colors.YELLOW}Com Contexto Completo do Projeto:{Colors.NC}")
    print(f"O agente lê TODOS os arquivos .md automaticamente e usa em cada decisão.\n")
    print(f"{Colors.YELLOW}ORDEM DE LEITURA (prioridade):{Colors.NC}")
    print(f"  1. CLAUDE.md / GEMINI.md / AGENTE.md  ← Instruções")
    print(f"  2. PHILOSOPHY.md / STANDARDS.md       ← Filosofia")
    print(f"  3. DEVELOPMENT.md / QUICKSTART.md     ← Como desenvolver")
    print(f"  4. README.md / INDEX.md               ← Visão geral")
    print(f"  5. Todos os demais .md                ← Contexto extra\n")
    print(f"{Colors.YELLOW}COMANDOS:{Colors.NC}")
    print(f"  analyze FILE      - Analisa código")
    print(f"  improve FILE      - Refatora código")
    print(f"  document FILE     - Documenta")
    print(f"  test FILE         - Cria testes")
    print(f"  ask PERGUNTA      - Responde com contexto")
    print(f"  search CONSULTA   - Web + IA + contexto")
    print(f"  research PERGUNTA - Pesquisa profunda")
    print(f"  context           - Lista .md carregados")
    print(f"  status            - Status completo")
    print(f"  help              - Esta mensagem\n")
    print(f"{Colors.YELLOW}EXEMPLOS:{Colors.NC}")
    print(f"  python3 agent.py ask 'qual é a filosofia deste projeto'")
    print(f"  python3 agent.py analyze src/main.rs")
    print(f"  python3 agent.py improve src/utils.py")
    print(f"\n")

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    """Entry point principal"""
    if len(sys.argv) < 2:
        cmd_help()
        sys.exit(0)
    
    # Crear config se não existir
    if not CONFIG_FILE.exists():
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_FILE.write_text('{"google": "${GOOGLE_GEMINI_API_KEY}", "note": "Replace with your actual API key"}')
    
    cmd = sys.argv[1]
    args = sys.argv[2:] if len(sys.argv) > 2 else []
    
    context = ProjectContext()
    gemini = GeminiClient()
    
    try:
        if cmd == "analyze":
            if not args:
                print(f"{Colors.RED}❌ Uso: agent.py analyze <arquivo>{Colors.NC}")
                sys.exit(1)
            cmd_analyze(args[0], context, gemini)
        
        elif cmd == "improve":
            if not args:
                print(f"{Colors.RED}❌ Uso: agent.py improve <arquivo>{Colors.NC}")
                sys.exit(1)
            cmd_improve(args[0], context, gemini)
        
        elif cmd == "document":
            if not args:
                print(f"{Colors.RED}❌ Uso: agent.py document <arquivo>{Colors.NC}")
                sys.exit(1)
            cmd_document(args[0], context, gemini)
        
        elif cmd == "test":
            if not args:
                print(f"{Colors.RED}❌ Uso: agent.py test <arquivo>{Colors.NC}")
                sys.exit(1)
            cmd_test(args[0], context, gemini)
        
        elif cmd == "ask":
            question = " ".join(args)
            cmd_ask(question, context, gemini)
        
        elif cmd == "search":
            query = " ".join(args)
            cmd_search(query, context, gemini)
        
        elif cmd == "research":
            question = " ".join(args)
            cmd_research(question, context, gemini)
        
        elif cmd == "context":
            cmd_context(context)
        
        elif cmd == "status":
            cmd_status()
        
        elif cmd in ["help", "--help", "-h"]:
            cmd_help()
        
        else:
            print(f"{Colors.RED}❌ Comando desconhecido: {cmd}{Colors.NC}")
            cmd_help()
            sys.exit(1)
    
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⏸️  Operação cancelada pelo usuário{Colors.NC}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}❌ Erro: {e}{Colors.NC}")
        sys.exit(1)

if __name__ == "__main__":
    main()













































