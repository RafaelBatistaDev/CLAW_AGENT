/**
 * InlineCompletionProvider - Coração da extensão
 * 
 * Fluxo:
 * 1. Usuário para de digitar (debounce 500ms)
 * 2. Extension coleta contexto (últimas 10 linhas)
 * 3. Envia para AgentManager
 * 4. AgentManager chama agent.py subset (gasta pouco token)
 * 5. Sugestão retorna para o editor (cinza)
 * 6. User pressiona Tab para aceitar (ou Esc para descartar)
 */

import * as vscode from 'vscode';
import { AgentManager } from './agentManager';
import { TokenCache } from './tokenCache';
import { Logger } from './logger';

export class InlineCompletionProvider implements vscode.InlineCompletionItemProvider {
    private agentManager: AgentManager;
    private tokenCache: TokenCache;
    private logger: Logger;
    private debounceMs: number;
    private maxTokens: number;
    private debounceTimers: Map<string, NodeJS.Timeout> = new Map();

    constructor(
        agentManager: AgentManager,
        tokenCache: TokenCache,
        logger: Logger,
        debounceMs: number,
        maxTokens: number
    ) {
        this.agentManager = agentManager;
        this.tokenCache = tokenCache;
        this.logger = logger;
        this.debounceMs = debounceMs;
        this.maxTokens = maxTokens;
    }

    async provideInlineCompletionItems(
        document: vscode.TextDocument,
        position: vscode.Position,
        _context: vscode.InlineCompletionContext,
        token: vscode.CancellationToken
    ): Promise<vscode.InlineCompletionItem[] | vscode.InlineCompletionList> {
        // Verificar se está habilitado
        const enabled = vscode.workspace.getConfiguration('clawrafaelia').get('enabled', true);
        if (!enabled) {
            return [];
        }

        // Limpar timer anterior (debounce)
        const docKey = document.uri.toString();
        if (this.debounceTimers.has(docKey)) {
            clearTimeout(this.debounceTimers.get(docKey)!);
        }

        return new Promise((resolve) => {
            // Aguardar debounce delay antes de fazer requisição
            const timer = setTimeout(async () => {
                try {
                    // Cancelation check
                    if (token.isCancellationRequested) {
                        return resolve([]);
                    }

                    // ════════════════════════════════════════════════════════════════════════════════
                    // 1. COLETAR CONTEXTO DO DOCUMENTO
                    // ════════════════════════════════════════════════════════════════════════════════

                    const lineNum = position.line;

                    // Pegar últimas 10 linhas para contexto
                    const startLine = Math.max(0, lineNum - 10);
                    const textBefore = document.getText(
                        new vscode.Range(
                            new vscode.Position(startLine, 0),
                            position
                        )
                    );

                    // Detectar linguagem do arquivo
                    const languageId = document.languageId;
                    const fileName = document.fileName;

                    // ════════════════════════════════════════════════════════════════════════════════
                    // 2. VERIFICAR CACHE (ZERO API CALL)
                    // ════════════════════════════════════════════════════════════════════════════════

                    const cacheKey = `${languageId}:${textBefore}`;
                    const cached = this.tokenCache.get(cacheKey);
                    if (cached) {
                        this.logger.debug(`💾 Cache hit para ${fileName}`);
                        return resolve([new vscode.InlineCompletionItem(cached)]);
                    }

                    // ════════════════════════════════════════════════════════════════════════════════
                    // 3. CHAMAR AGENT.PY (COM FALLBACK)
                    // ════════════════════════════════════════════════════════════════════════════════

                    this.logger.info(`🔄 Solicitando sugestão para ${fileName} (${languageId})`);

                    const suggestion = await this.agentManager.suggest(
                        textBefore,
                        languageId,
                        fileName,
                        this.maxTokens,
                        token
                    );

                    if (!suggestion || token.isCancellationRequested) {
                        return resolve([]);
                    }

                    // ════════════════════════════════════════════════════════════════════════════════
                    // 4. ARMAZENAR EM CACHE E RETORNAR
                    // ════════════════════════════════════════════════════════════════════════════════

                    this.tokenCache.set(cacheKey, suggestion);
                    this.logger.debug(`✅ Sugestão entregue: ${suggestion.substring(0, 50)}...`);

                    resolve([new vscode.InlineCompletionItem(suggestion)]);
                } catch (error) {
                    const errorMsg = error instanceof Error ? error.message : String(error);
                    this.logger.warn(`⚠️  Erro ao gerar sugestão: ${errorMsg}`);
                    resolve([]);
                }
            }, this.debounceMs);

            this.debounceTimers.set(docKey, timer);
        });
    }
}
