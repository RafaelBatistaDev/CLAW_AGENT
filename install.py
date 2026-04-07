#!/usr/bin/env python3
"""
🚀 CLAW VS Code Extension - Auto Installer
Instala a extensão CLAW automaticamente no VS Code
"""

import os
import sys
import subprocess
import json
import platform
from pathlib import Path
from typing import Optional

# Cores ANSI
G = "\033[0;32m"
B = "\033[0;34m"
Y = "\033[1;33m"
R = "\033[0;31m"
N = "\033[0m"

class ExtensionInstaller:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.platform = platform.system()
        self.home = Path.home()
        self.agent_path = self.home / "OneDrive" / "ClawRafaelIA" / "automation" / "my_scripts" / "agent.py"
        
    def log(self, msg: str, level: str = "INFO"):
        """Exibir mensagem com timestamp"""
        colors = {
            "INFO": B,
            "OK": G,
            "WARN": Y,
            "ERROR": R,
        }
        color = colors.get(level, B)
        print(f"{color}[{level}]{N} {msg}")
    
    def run(self, cmd: list, silent: bool = False) -> tuple[bool, str]:
        """Executar comando e retornar (success, output)"""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            return (result.returncode == 0, result.stdout.strip())
        except subprocess.TimeoutExpired:
            if not silent:
                self.log(f"Timeout: {' '.join(cmd)}", "WARN")
            return (False, "Timeout")
        except Exception as e:
            if not silent:
                self.log(f"Erro: {e}", "ERROR")
            return (False, str(e))
    
    def check_node(self) -> bool:
        """Verificar se Node.js está instalado"""
        self.log("Verificando Node.js...", "INFO")
        success, version = self.run(["node", "--version"], silent=True)
        if success:
            self.log(f"Node.js {version} encontrado", "OK")
            return True
        else:
            self.log("Node.js não encontrado", "WARN")
            self.log("Instale em: https://nodejs.org", "WARN")
            return False
    
    def check_npm(self) -> bool:
        """Verificar se npm está instalado"""
        self.log("Verificando npm...", "INFO")
        success, version = self.run(["npm", "--version"], silent=True)
        if success:
            self.log(f"npm {version} encontrado", "OK")
            return True
        else:
            self.log("npm não encontrado", "WARN")
            return False
    
    def check_vscode(self) -> bool:
        """Verificar se VS Code está instalado"""
        self.log("Verificando VS Code...", "INFO")
        
        # Diferentes locais dependendo do SO
        vscode_paths = {
            "Linux": ["/usr/bin/code", "/snap/bin/code"],
            "Darwin": ["/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"],
            "Windows": ["C:\\Program Files\\Microsoft VS Code\\bin\\code.cmd"],
        }
        
        paths = vscode_paths.get(self.platform, [])
        for path in paths:
            if Path(path).exists():
                self.log(f"VS Code encontrado em {path}", "OK")
                return True
        
        # Tentar comando direto
        success, _ = self.run(["code", "--version"], silent=True)
        if success:
            self.log("VS Code encontrado no PATH", "OK")
            return True
        
        self.log("VS Code não encontrado", "WARN")
        self.log("Instale em: https://code.visualstudio.com", "WARN")
        return False
    
    def check_agent_py(self) -> bool:
        """Verificar se agent.py existe"""
        self.log("Verificando agent.py...", "INFO")
        if self.agent_path.exists():
            self.log(f"agent.py encontrado em {self.agent_path}", "OK")
            return True
        else:
            self.log(f"agent.py não encontrado em {self.agent_path}", "WARN")
            self.log("Extension funcionará com fallback local", "WARN")
            return False
    
    def install_dependencies(self) -> bool:
        """Instalar dependências npm"""
        self.log("Instalando dependências...", "INFO")
        
        os.chdir(self.project_dir)
        success, output = self.run(["npm", "install"])
        
        if success:
            self.log("Dependências instaladas", "OK")
            return True
        else:
            self.log("Erro ao instalar dependências", "ERROR")
            return False
    
    def compile(self) -> bool:
        """Compilar TypeScript"""
        self.log("Compilando TypeScript...", "INFO")
        
        os.chdir(self.project_dir)
        success, output = self.run(["npm", "run", "compile"])
        
        if success:
            self.log("Compilação completada", "OK")
            return True
        else:
            self.log("Erro ao compilar", "ERROR")
            return False
    
    def package(self) -> Optional[str]:
        """Empacotar extensão em .vsix"""
        self.log("Empacotando extensão...", "INFO")
        
        os.chdir(self.project_dir)
        success, output = self.run(["npm", "run", "package"])
        
        if success:
            # Procurar .vsix mais recente
            vsix_files = list(self.project_dir.glob("*.vsix"))
            if vsix_files:
                latest = max(vsix_files, key=os.path.getctime)
                self.log(f"Pacote criado: {latest.name}", "OK")
                return str(latest)
        
        self.log("Erro ao empacotar", "ERROR")
        return None
    
    def install_in_vscode(self, vsix_path: str) -> bool:
        """Instalar extensão no VS Code"""
        self.log(f"Instalando extensão {Path(vsix_path).name} no VS Code...", "INFO")
        
        success, _ = self.run(["code", "--install-extension", vsix_path])
        
        if success:
            self.log("Extensão instalada com sucesso", "OK")
            return True
        else:
            self.log("Erro ao instalar extensão", "ERROR")
            self.log(f"Tente manualmente: code --install-extension {vsix_path}", "WARN")
            return False
    
    def run_setup(self):
        """Executar setup completo"""
        print("")
        print(f"{B}╔════════════════════════════════════════════════════════════════╗{N}")
        print(f"{B}║{N}  🚀 CLAW VS Code Extension - Auto Installer")
        print(f"{B}║{N}  Platform: {self.platform}")
        print(f"{B}╚════════════════════════════════════════════════════════════════╝{N}")
        print("")
        
        # Validar ambiente
        has_node = self.check_node()
        has_npm = self.check_npm()
        has_vscode = self.check_vscode()
        has_agent = self.check_agent_py()
        print("")
        
        # Se não tem node/npm, não podemos continuar
        if not (has_node and has_npm):
            self.log("Prerequisitos não atendidos", "ERROR")
            self.log("Instale Node.js + npm de https://nodejs.org", "WARN")
            return False
        
        # Se não tem VS Code, aviso mas continua
        if not has_vscode:
            self.log("VS Code não encontrado - será necessário instalá-lo", "WARN")
            print("")
        
        # Instalar e compilar
        if not self.install_dependencies():
            return False
        
        if not self.compile():
            return False
        
        # Empacotar
        vsix_path = self.package()
        if not vsix_path:
            return False
        
        print("")
        
        # Instalar no VS Code se encontrado
        if has_vscode:
            self.install_in_vscode(vsix_path)
        else:
            self.log("VS Code não encontrado", "WARN")
            self.log(f"Para instalar manualmente, execute:", "INFO")
            self.log(f"  code --install-extension {vsix_path}", "INFO")
            print("")
        
        # Success
        print("")
        print(f"{B}╔════════════════════════════════════════════════════════════════╗{N}")
        print(f"{B}║{N}  {G}✅ Setup completado!{N}")
        print(f"{B}║{N}")
        print(f"{B}║{N}  📖 Próximos passos:")
        print(f"{B}║{N}     1. Abra VS Code")
        print(f"{B}║{N}     2. Vá para Extensions (Ctrl+Shift+X)")
        print(f"{B}║{N}     3. Procure por 'CLAW'")
        print(f"{B}║{N}     4. Clique Install")
        print(f"{B}║{N}")
        print(f"{B}║{N}  ⚙️  Configurar em Settings:")
        print(f"{B}║{N}     Ctrl+, → clawrafaelia")
        print(f"{B}║{N}")
        print(f"{B}║{N}  💻 Começar a digitar em qualquer arquivo!")
        print(f"{B}║{N}")
        print(f"{B}║{N}  📚 Documentação: {self.project_dir}/README.md")
        print(f"{B}╚════════════════════════════════════════════════════════════════╝{N}")
        
        return True

def main():
    """Entry point"""
    installer = ExtensionInstaller()
    success = installer.run_setup()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
