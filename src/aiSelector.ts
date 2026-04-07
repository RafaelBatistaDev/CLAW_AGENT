/**
 * AISelector - Seletor inteligente de IA
 * 
 * Usa AIProbe para detectar IAs disponíveis
 * Auto-seleciona a melhor com fallback automático
 * Agnóstico: funciona com Gemini, OpenAI, Claude, LocalAI, Ollama
 */

import { Logger } from './logger';
import { AIProbe, AIProbeResult } from './aiProbe';
import { PathResolver } from './pathResolver';
import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
import { homedir } from 'os';

// ═══════════════════════════════════════════════════════════════════════════════
// TIPOS
// ═══════════════════════════════════════════════════════════════════════════════

interface AICall {
    provider: string;
    model: string;
    latency_ms: number;
    success: boolean;
    error?: string;
}

// ═══════════════════════════════════════════════════════════════════════════════
// MAIN: AISelector
// ═══════════════════════════════════════════════════════════════════════════════

export class AISelector {
    private logger: Logger;
    private aiProbe: AIProbe;
    private selectedAI: AIProbeResult | null = null;
    private availableAIs: AIProbeResult[] = [];
    private callHistory: AICall[] = [];
    private failureCount: Map<string, number> = new Map();
    private circuitBreakerThreshold: number = 3;

    constructor(logger: Logger) {
        this.logger = logger;
        this.aiProbe = new AIProbe(logger);
    }

    /**
     * Inicializar: Detectar IAs disponíveis
     */
    async initialize(): Promise<string> {
        try {
            this.logger.info('🔍 Detectando IAs disponíveis...');

            this.availableAIs = await this.aiProbe.detectAvailableAIs();

            if (this.availableAIs.length === 0) {
                this.logger.warn('⚠️  Nenhuma IA detectada (usando fallback local)');
                return 'Fallback mode (patterns + templates)';
            }

            this.selectedAI = this.availableAIs[0];
            this.logger.info(`✅ IA selecionada: ${this.selectedAI.name}`);

            return this.selectedAI.name;

        } catch (error) {
            const errorMsg = error instanceof Error ? error.message : String(error);
            this.logger.error(`Erro ao detectar IAs: ${errorMsg}`);
            return 'Fallback mode (patterns + templates)';
        }
    }

    /**
     * MAIN: Chamar IA selecionada
     * Auto-fallback entre IAs se uma falhar
     */
    async callAI(
        prompt: string,
        language: string,
        maxTokens: number = 50,
        cancellationToken?: vscode.CancellationToken
    ): Promise<string | null> {
        const startTime = Date.now();

        // Verificar se há IA selecionada funcionando
        if (!this.selectedAI || !this.isAIOperational(this.selectedAI.provider)) {
            // Tentar próxima IA disponível
            this.selectedAI = this.findNextworkingAI();

            if (!this.selectedAI) {
                this.logger.debug('⚠️  Nenhuma IA disponível');
                return null;
            }

            this.logger.info(`🔄 Passando para: ${this.selectedAI.name}`);
        }

        try {
            // Cancelation check
            if (cancellationToken?.isCancellationRequested) {
                return null;
            }

            // Chamar a IA selecionada
            const result = await this.callSelectedAI(
                prompt,
                language,
                maxTokens,
                this.selectedAI
            );

            const latency = Date.now() - startTime;

            if (result) {
                // Reset failure count on success
                this.failureCount.set(this.selectedAI.provider, 0);

                this.callHistory.push({
                    provider: this.selectedAI.provider,
                    model: this.selectedAI.model || 'unknown',
                    latency_ms: latency,
                    success: true
                });

                this.logger.debug(
                    `✅ ${this.selectedAI.name}: ${result.substring(0, 40).replace(/\n/g, ' ')}... (${latency}ms)`
                );

                return result;
            }

        } catch (error) {
            const errorMsg = error instanceof Error ? error.message : String(error);
            this.logger.debug(`❌ ${this.selectedAI?.name} falhou: ${errorMsg}`);

            // Incrementar counter de falhas
            const provider = this.selectedAI?.provider || 'unknown';
            const failCount = (this.failureCount.get(provider) || 0) + 1;
            this.failureCount.set(provider, failCount);

            if (failCount >= this.circuitBreakerThreshold) {
                this.logger.warn(`🚫 Circuit breaker ativado para ${provider}`);
            }

            this.callHistory.push({
                provider: provider,
                model: this.selectedAI?.model || 'unknown',
                latency_ms: Date.now() - startTime,
                success: false,
                error: errorMsg
            });
        }

        // Tentar próxima IA
        return this.callAI(prompt, language, maxTokens, cancellationToken);
    }

    /**
     * Chamar a IA selecionada (agnóstico de provider)
     */
    private async callSelectedAI(
        prompt: string,
        language: string,
        maxTokens: number,
        ai: AIProbeResult
    ): Promise<string | null> {
        switch (ai.provider) {
            case 'gemini':
                return this.callGemini(prompt, language, maxTokens);

            case 'openai':
                return this.callOpenAI(prompt, language, maxTokens);

            case 'claude':
                return this.callClaude(prompt, language, maxTokens);

            case 'localai':
            case 'ollama':
                return this.callLocalAI(prompt, language, maxTokens, ai.endpoint || '');

            default:
                return null;
        }
    }

    // ═══════════════════════════════════════════════════════════════════════════════
    // IMPLEMENTAÇÕES POR PROVIDER
    // ═══════════════════════════════════════════════════════════════════════════════

    /**
     * Chamar Gemini (via agent.py)
     */
    private async callGemini(
        prompt: string,
        language: string,
        maxTokens: number
    ): Promise<string | null> {
        try {
            const { execSync } = require('child_process');
            const agentPath = this.findAgentPath();

            if (!agentPath) {
                return null;
            }

            const result = execSync(
                `python3 "${agentPath}" improve --language ${language} --max-tokens ${maxTokens} < /dev/stdin 2>/dev/null`,
                {
                    input: prompt,
                    timeout: 2000,
                    encoding: 'utf-8'
                }
            );

            return result.trim() || null;

        } catch (error) {
            return null;
        }
    }

    /**
     * Chamar OpenAI
     */
    private async callOpenAI(
        prompt: string,
        language: string,
        maxTokens: number
    ): Promise<string | null> {
        try {
            const apiKey = this.getAPIKey('openai');
            if (!apiKey) return null;

            const response = await this.fetchWithTimeout(
                'https://api.openai.com/v1/chat/completions',
                {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${apiKey}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        model: 'gpt-4o-mini',
                        messages: [
                            {
                                role: 'system',
                                content: `Code completion expert in ${language}. Return only code, no explanation.`
                            },
                            { role: 'user', content: prompt }
                        ],
                        max_tokens: maxTokens,
                        temperature: 0.3
                    })
                },
                2000
            );

            if (!response.ok) {
                return null;
            }

            const data: any = await response.json();
            return data.choices?.[0]?.message?.content?.trim() || null;

        } catch (error) {
            return null;
        }
    }

    /**
     * Chamar Claude (Anthropic)
     */
    private async callClaude(
        prompt: string,
        language: string,
        maxTokens: number
    ): Promise<string | null> {
        try {
            const apiKey = this.getAPIKey('claude');
            if (!apiKey) return null;

            const response = await this.fetchWithTimeout(
                'https://api.anthropic.com/v1/messages',
                {
                    method: 'POST',
                    headers: {
                        'x-api-key': apiKey,
                        'anthropic-version': '2023-06-01',
                        'content-type': 'application/json'
                    },
                    body: JSON.stringify({
                        model: 'claude-3-sonnet-20240229',
                        max_tokens: maxTokens,
                        messages: [
                            { role: 'user', content: `${language} code: ${prompt}` }
                        ]
                    })
                },
                2000
            );

            if (!response.ok) {
                return null;
            }

            const data: any = await response.json();
            return data.content?.[0]?.text?.trim() || null;

        } catch (error) {
            return null;
        }
    }

    /**
     * Chamar LocalAI / Ollama
     */
    private async callLocalAI(
        prompt: string,
        language: string,
        maxTokens: number,
        endpoint: string
    ): Promise<string | null> {
        try {
            const response = await this.fetchWithTimeout(
                `${endpoint}/v1/completions`,
                {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        prompt: `${language}:\n${prompt}`,
                        max_tokens: maxTokens,
                        temperature: 0.3,
                        top_p: 0.9
                    })
                },
                1500
            );

            if (!response.ok) {
                return null;
            }

            const data: any = await response.json();
            return data.choices?.[0]?.text?.trim() || null;

        } catch (error) {
            return null;
        }
    }

    // ═══════════════════════════════════════════════════════════════════════════════
    // GERENCIAMENTO DE ESTADO
    // ═══════════════════════════════════════════════════════════════════════════════

    /**
     * Verificar se IA está operacional (não em circuit breaker)
     */
    private isAIOperational(provider: string): boolean {
        const failCount = this.failureCount.get(provider) || 0;
        return failCount < this.circuitBreakerThreshold;
    }

    /**
     * Encontrar próxima IA funcionando
     */
    private findNextworkingAI(): AIProbeResult | null {
        for (const ai of this.availableAIs) {
            if (this.isAIOperational(ai.provider)) {
                return ai;
            }
        }
        return null;
    }

    /**
     * Obter status das IAs
     */
    getStatus(): string {
        if (!this.selectedAI) {
            return '⚠️  Nenhuma IA detectada';
        }

        const stats = {
            selected: this.selectedAI.name,
            totalCalls: this.callHistory.length,
            successRate: this.calculateSuccessRate(),
            avgLatency: this.calculateAvgLatency(),
            availableIAs: this.availableAIs.map(ai => `${ai.name} (${ai.latency_ms}ms)`).join(', ')
        };

        return JSON.stringify(stats, null, 2);
    }

    /**
     * Calcular taxa de sucesso
     */
    private calculateSuccessRate(): string {
        if (this.callHistory.length === 0) return '0%';

        const successes = this.callHistory.filter(c => c.success).length;
        const rate = (successes / this.callHistory.length * 100).toFixed(1);
        return `${rate}%`;
    }

    /**
     * Calcular latência média
     */
    private calculateAvgLatency(): string {
        if (this.callHistory.length === 0) return '0ms';

        const total = this.callHistory.reduce((sum, c) => sum + c.latency_ms, 0);
        const avg = Math.round(total / this.callHistory.length);
        return `${avg}ms`;
    }

    // ═══════════════════════════════════════════════════════════════════════════════
    // HELPERS
    // ═══════════════════════════════════════════════════════════════════════════════

    /**
     * Encontrar agent.py (portável para qualquer usuário)
     */
    private findAgentPath(): string | null {
        return PathResolver.findAgentPy();
    }

    /**
     * Obter API key de forma segura
     */
    private getAPIKey(provider: 'openai' | 'claude'): string | null {
        const envVar = provider === 'openai' ? 'OPENAI_API_KEY' : 'ANTHROPIC_API_KEY';
        const configKey = provider === 'openai' ? 'OPENAI_API_KEY' : 'ANTHROPIC_API_KEY';

        // Tentar env var
        const envKey = process.env[envVar];
        if (envKey) {
            return envKey;
        }

        // Tentar arquivo de config
        try {
            const configPath = path.join(homedir(), '.claw/config/.claude.json');
            if (fs.existsSync(configPath)) {
                const content = fs.readFileSync(configPath, 'utf-8');
                const config = JSON.parse(content);
                return config[configKey] || config[`${provider}.apiKey`];
            }
        } catch (error) {
            // Ignorar erro
        }

        return null;
    }

    /**
     * Fetch com timeout
     */
    private async fetchWithTimeout(
        url: string,
        options: RequestInit,
        timeoutMs: number
    ): Promise<Response> {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

        try {
            return await fetch(url, { ...options, signal: controller.signal });
        } finally {
            clearTimeout(timeoutId);
        }
    }
}
