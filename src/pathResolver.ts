/**
 * pathResolver.ts - Resolve caminhos portáveis para qualquer usuário
 *
 * Estratégia:
 * 1. Expandir ~ para homedir() do usuário
 * 2. Procurar agent.py em localizações conhecidas
 * 3. Usar caminhos relativos quando possível
 */

import { homedir } from 'os';
import { join } from 'path';
import { existsSync } from 'fs';
import { Logger } from './logger';

export class PathResolver {
    private static logger: Logger;

    /**
     * Inicializar logger (opcional)
     */
    static setLogger(logger: Logger): void {
        this.logger = logger;
    }

    /**
     * Expandir caminho com ~ para homedir do usuário
     * 
     * Exemplos:
     * "~/OneDrive/ClawRafaelIA/automation/my_scripts/agent.py"
     *   →  "/home/user/OneDrive/ClawRafaelIA/automation/my_scripts/agent.py"
     * 
     * "/absoluto/caminho" → "/absoluto/caminho" (sem mudança)
     */
    static expandPath(pathStr: string): string {
        if (!pathStr) return '';
        
        if (pathStr.startsWith('~')) {
            return join(homedir(), pathStr.slice(1));
        }
        
        return pathStr;
    }

    /**
     * Encontrar agent.py usando várias estratégias
     *
     * Procura em:
     * 1. Configuração do usuário (se existir)
     * 2. ~/.local/bin/agent.py (RECOMENDADO)
     * 3. ~/bin/agent.py
     * 4. /usr/local/bin/agent.py
     * 5. ~/.claw/agent.py
     * 6. Retorna null se não encontrar
     */
    static findAgentPy(configuredPath?: string): string | null {
        const candidates: string[] = [];

        // 1. Se houver caminho configurado, tentar expandir
        if (configuredPath) {
            const expanded = this.expandPath(configuredPath);
            candidates.push(expanded);
        }

        // 2-5. Localizações padrão em bin (portável para qualquer usuário)
        const home = homedir();
        candidates.push(
            join(home, '.local/bin/agent.py'),
            join(home, 'bin/agent.py'),
            '/usr/local/bin/agent.py',
            join(home, '.claw/agent.py'),
        );

        // 5. Procurar e retornar o primeiro que existe
        for (const candidate of candidates) {
            if (existsSync(candidate)) {
                this.log(`✅ agent.py encontrado: ${candidate}`);
                return candidate;
            }
        }

        this.log(`❌ agent.py não encontrado em nenhuma localização conhecida`);
        this.log(`Tentadas: ${candidates.join(', ')}`);
        return null;
    }

    /**
     * Validar se um caminho é portável (sem usuário hardcoded)
     * 
     * Retorna false se contiver:
     * - "/home/recifecrypto"
     * - "/home/username"
     * - Caminhos Windows com drive letters
     */
    static isPortable(pathStr: string): boolean {
        // Verificar padrões de usuários específicos
        const userPatterns = [
            /\/home\/[a-zA-Z0-9_\-]+\//,  // /home/username/
            /C:\\Users\\[a-zA-Z0-9_\-]+\\/,  // C:\Users\username\
            /\/Users\/[a-zA-Z0-9_\-]+\//, // /Users/username/ (macOS)
        ];

        for (const pattern of userPatterns) {
            if (pattern.test(pathStr)) {
                return false;
            }
        }

        return true;
    }

    /**
     * Converter caminho absoluto para portável (com ~)
     */
    static makePortable(pathStr: string): string {
        const home = homedir();
        
        if (pathStr.startsWith(home)) {
            return '~' + pathStr.slice(home.length);
        }

        return pathStr;
    }

    /**
     * Logging helper
     */
    private static log(message: string): void {
        if (this.logger) {
            if (message.includes('✅')) this.logger.info(message);
            else if (message.includes('❌')) this.logger.error(message);
            else this.logger.debug(message);
        }
    }
}
