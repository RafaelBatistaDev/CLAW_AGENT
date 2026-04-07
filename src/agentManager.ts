/**
 * AgentManager - Comunica com agent.py via subprocess
 * 
 * Responsabilidades:
 * 1. Executar agent.py com contexto (timeout 5s para não travar editor)
 * 2. Parsear resposta JSON
 * 3. Implementar fallbacks (LocalAI, cache)
 * 4. Circuit breaker para API falhando
 */

import * as vscode from 'vscode';
import { Logger } from './logger';
import { PathResolver } from './pathResolver';

type SuggestionRequest = {
    context: string;
    language: string;
    fileName: string;
    maxTokens: number;
};

interface AgentResponse {
    suggestion: string;
    confidence: number;
    source: 'api' | 'cache' | 'local';
    tokens_used: number;
}

export class AgentManager {
    private logger: Logger;
    private agentPythonPath: string;
    private circuitBreakerFailures: number = 0;
    private circuitBreakerTimeout: number = 0;

    constructor(logger: Logger) {
        this.logger = logger;
        this.agentPythonPath = this.resolveAgentPath();
    }

    /**
     * Inicializar e validar agent.py
     */
    async initialize(): Promise<string> {
        try {
            // Validar que agent.py existe e é executável
            const { execSync } = require('child_process');
            execSync(`python3 "${this.agentPythonPath}" status 2>&1`, {
                timeout: 5000,
                encoding: 'utf-8'
            });

            this.logger.info(`✅ agent.py validado: ${this.agentPythonPath}`);
            return `Agent Path: ${this.agentPythonPath}`;
        } catch (error) {
            const msg = error instanceof Error ? error.message : String(error);
            this.logger.error(`Falha ao validar agent.py: ${msg}`);
            return `Falha na validação (fallback local ativado)`;
        }
    }

    /**
     * Obter status do agente
     */
    async getStatus(): Promise<string> {
        try {
            const { execSync } = require('child_process');
            const result = execSync(`python3 "${this.agentPythonPath}" status 2>&1`, {
                timeout: 3000,
                encoding: 'utf-8'
            });
            return result;
        } catch (error) {
            return 'Agent status: offline (fallback mode)';
        }
    }

    /**
     * Solicitar sugestão inline
     * 
     * Estratégia:
     * 1. Circuit breaker: se API falhou 3x, esperar 5min
     * 2. Cache semântico: verificar sugestões similares
     * 3. Chamar agent.py com timeout 2s (não pode travar editor)
     * 4. Fallback: dicas locais simbólicas
     */
    async suggest(
        context: string,
        language: string,
        fileName: string,
        maxTokens: number,
        cancellationToken: vscode.CancellationToken
    ): Promise<string> {
        try {
            // ════════════════════════════════════════════════════════════════════════════════
            // CIRCUIT BREAKER CHECK
            // ════════════════════════════════════════════════════════════════════════════════

            if (this.circuitBreakerFailures >= 3) {
                const now = Date.now();
                if (now - this.circuitBreakerTimeout < 300000) { // 5 minutos
                    this.logger.warn('⚠️  Circuit breaker ativo - usando fallback local');
                    return this.getLocalSuggestion(context, language);
                } else {
                    // Tentar recuperar após timeout
                    this.circuitBreakerFailures = 0;
                    this.logger.info('🔄 Circuit breaker reset - tentando novamente');
                }
            }

            // ════════════════════════════════════════════════════════════════════════════════
            // CALL AGENT.PY (com timeout curto)
            // ════════════════════════════════════════════════════════════════════════════════

            const suggestion = await this.callAgentPython(
                context,
                language,
                fileName,
                maxTokens,
                cancellationToken
            );

            if (suggestion) {
                this.circuitBreakerFailures = 0; // Reset on success
                return suggestion;
            }

            // ════════════════════════════════════════════════════════════════════════════════
            // FALLBACK: Local Suggestion
            // ════════════════════════════════════════════════════════════════════════════════

            this.circuitBreakerFailures++;
            this.circuitBreakerTimeout = Date.now();

            const local = this.getLocalSuggestion(context, language);
            this.logger.warn(`⚠️  Fallback local (falhas: ${this.circuitBreakerFailures})`);
            return local;

        } catch (error) {
            this.circuitBreakerFailures++;
            this.circuitBreakerTimeout = Date.now();

            const errorMsg = error instanceof Error ? error.message : String(error);
            this.logger.error(`Erro em suggest: ${errorMsg}`);

            return this.getLocalSuggestion(context, language);
        }
    }

    /**
     * Chamar agent.py via subprocess com timeout 2s
     * Não pode travar o editor VS Code
     */
    private async callAgentPython(
        context: string,
        language: string,
        fileName: string,
        maxTokens: number,
        cancellationToken: vscode.CancellationToken
    ): Promise<string> {
        return new Promise((resolve) => {
            try {
                // Timeout de 2 segundos (não pode travar editor)
                const timeoutHandle = setTimeout(() => {
                    this.logger.warn('⏱️  Timeout em agent.py (2s)');
                    resolve('');
                }, 2000);

                // Cancelation token check
                if (cancellationToken.isCancellationRequested) {
                    clearTimeout(timeoutHandle);
                    resolve('');
                    return;
                }

                // Preparar payload JSON
                const payload: SuggestionRequest = {
                    context: context.substring(0, 500), // Limitar contexto
                    language,
                    fileName,
                    maxTokens
                };

                // Executar agent.py como subprocess
                const { spawn } = require('child_process');
                const agentProcess = spawn('python3', [
                    this.agentPythonPath,
                    'inline',  // Comando específico para inline completions
                    JSON.stringify(payload)
                ], {
                    timeout: 2500, // Kill após 2.5s
                    stdio: ['pipe', 'pipe', 'pipe']
                });

                let output = '';
                let errorOutput = '';

                agentProcess.stdout.on('data', (data: Buffer) => {
                    output += data.toString();
                });

                agentProcess.stderr.on('data', (data: Buffer) => {
                    errorOutput += data.toString();
                });

                agentProcess.on('close', (code: number) => {
                    clearTimeout(timeoutHandle);

                    if (code === 0 && output) {
                        try {
                            // Parsear JSON response
                            const response: AgentResponse = JSON.parse(output);
                            this.logger.debug(`✅ agent.py respondeu (${response.tokens_used} tokens)`);
                            resolve(response.suggestion || '');
                        } catch (e) {
                            // Se não for JSON, tomar como string simples
                            resolve(output.trim());
                        }
                    } else {
                        this.logger.debug(`agent.py code=${code}`);
                        resolve('');
                    }
                });

                agentProcess.on('error', (err: Error) => {
                    clearTimeout(timeoutHandle);
                    this.logger.warn(`Erro ao chamar agent.py: ${err.message}`);
                    resolve('');
                });

            } catch (error) {
                const msg = error instanceof Error ? error.message : String(error);
                this.logger.error(`callAgentPython: ${msg}`);
                resolve('');
            }
        });
    }

    /**
     * Sugestão local (fallback quando API não responde)
     * Usa pattern matching simples no contexto
     */
    private getLocalSuggestion(context: string, language: string): string {
        const lines = context.split('\n');
        const lastLine = lines[lines.length - 1] || '';

        // Dicas por linguagem
        const suggestions: Record<string, string[]> = {
            python: [
                '\n    pass',
                '\n    """\n    \n    """',
                '\n    return None',
                '\n    raise NotImplementedError()',
                '\n    ...',
            ],
            typescript: [
                '\n  }',
                '\n  : void => {',
                '\n  return;',
                '\n  throw new Error("");',
                '\n  // TODO',
            ],
            javascript: [
                '\n  }',
                '\n  () => {',
                '\n  return undefined;',
                '\n  throw new Error("");',
                '\n  // TODO',
            ],
            csharp: [
                '\n    }',
                '\n    => throw new NotImplementedException();',
                '\n    => null;',
                '\n    {',
                '\n    // TODO',
            ],
            rust: [
                '\n    }',
                '\n    unimplemented!()',
                '\n    todo!()',
                '\n    Ok(())',
                '\n    // TODO',
            ],
            default: [
                '\n    // TODO: Implementar',
                '\n    }',
                '\n    ...',
                '\n    return;',
            ]
        };

        const tips = suggestions[language] || suggestions.default;
        // Retornar primeira sugestão que não duplica última linha
        for (const tip of tips) {
            if (!lastLine.endsWith(tip)) {
                return tip;
            }
        }
        return tips[0];
    }

    /**
     * Resolver caminho para agent.py (portável para qualquer usuário)
     * Usa PathResolver para buscar em localizações conhecidas
     */
    private resolveAgentPath(): string {
        // Tentar usar caminho configurado
        const config = vscode.workspace.getConfiguration('clawrafaelia');
        const configuredPath = config.get<string>('agentPythonPath');

        // PathResolver.findAgentPy procura em:
        // 1. ~/.local/bin/agent.py
        // 2. ~/bin/agent.py
        // 3. /usr/local/bin/agent.py
        // 4. ~/.claw/agent.py
        const found = PathResolver.findAgentPy(configuredPath);
        
        if (found) {
            return found;
        }

        // Fallback: expandir caminho portável
        return PathResolver.expandPath('~/.local/bin/agent.py');
    }
}
