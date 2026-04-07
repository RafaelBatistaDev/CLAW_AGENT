/**
 * AIProbe - Detector inteligente de IAs disponíveis
 * 
 * Testa em paralelo:
 * - Gemini (via agent.py)
 * - OpenAI (API key)
 * - Claude/Anthropic (API key)
 * - LocalAI/Ollama (endpoint HTTP)
 * 
 * Resultado: Array de IAs disponíveis com prioridade
 */

import { Logger } from './logger';
import { execSync } from 'child_process';
import * as path from 'path';
import * as fs from 'fs';
import { homedir } from 'os';

// ═══════════════════════════════════════════════════════════════════════════════
// TIPOS
// ═══════════════════════════════════════════════════════════════════════════════

export interface AIProbeResult {
    provider: 'gemini' | 'openai' | 'claude' | 'localai' | 'ollama' | 'none';
    name: string;
    available: boolean;
    latency_ms: number;
    endpoint?: string;
    apiKey?: string;
    model?: string;
    priority: number; // 1=highest, 5=lowest
}

// ═══════════════════════════════════════════════════════════════════════════════
// MAIN: AIProbe
// ═══════════════════════════════════════════════════════════════════════════════

export class AIProbe {
    private logger: Logger;
    private probeCache: Map<string, AIProbeResult> = new Map();
    private cacheExpirationMs: number = 300000; // 5 minutos
    private lastProbeTime: number = 0;

    constructor(logger: Logger) {
        this.logger = logger;
    }

    /**
     * MAIN: Detectar IAs disponíveis
     * Executa em paralelo, retorna em ordem de prioridade
     */
    async detectAvailableAIs(): Promise<AIProbeResult[]> {
        // Verificar cache
        if (Date.now() - this.lastProbeTime < this.cacheExpirationMs) {
            const cached = Array.from(this.probeCache.values())
                .filter(r => r.available)
                .sort((a, b) => a.priority - b.priority);

            if (cached.length > 0) {
                this.logger.debug(`✅ Usando cache de IAs (${cached.length} disponíveis)`);
                return cached;
            }
        }

        // Testar em paralelo
        const probes = await Promise.allSettled([
            this.probeGemini(),
            this.probeOpenAI(),
            this.probeClaude(),
            this.probeLocalAI(),
            this.probeOllama()
        ]);

        const results: AIProbeResult[] = [];

        probes.forEach((probe) => {
            if (probe.status === 'fulfilled' && probe.value) {
                results.push(probe.value);
                this.probeCache.set(probe.value.provider, probe.value);
            }
        });

        this.lastProbeTime = Date.now();

        // Ordenar por prioridade
        const sorted = results
            .filter(r => r.available)
            .sort((a, b) => a.priority - b.priority);

        const summary = sorted
            .map(r => `${r.name}(${r.latency_ms}ms)`)
            .join(', ');

        this.logger.info(`🔍 IAs detectadas: ${summary || 'NENHUMA'}`);

        return sorted;
    }

    /**
     * PROBE: Gemini (via agent.py)
     */
    private async probeGemini(): Promise<AIProbeResult | null> {
        const startTime = Date.now();

        try {
            // Verificar se agent.py existe
            const agentPaths = [
                path.join(homedir(), 'OneDrive/ClawRafaelIA/automation/my_scripts/agent.py'),
                path.join(homedir(), 'ClawRafaelIA/automation/my_scripts/agent.py'),
                '/opt/claw/agent.py'
            ];

            let agentPath: string | null = null;
            for (const p of agentPaths) {
                if (fs.existsSync(p)) {
                    agentPath = p;
                    break;
                }
            }

            if (!agentPath) {
                return null;
            }

            // Executar agent status
            const result = execSync(`python3 "${agentPath}" status 2>&1`, {
                timeout: 3000,
                encoding: 'utf-8'
            });

            const isConfigured = result.includes('API Google: Configurada') ||
                               result.includes('gemini') ||
                               result.includes('configurado');

            if (!isConfigured) {
                return null;
            }

            return {
                provider: 'gemini',
                name: '🔷 Google Gemini',
                available: true,
                latency_ms: Date.now() - startTime,
                endpoint: 'agent.py local',
                model: 'gemini-2.0-flash',
                priority: 1 // Prioridade máxima
            };

        } catch (error) {
            return null;
        }
    }

    /**
     * PROBE: OpenAI
     */
    private async probeOpenAI(): Promise<AIProbeResult | null> {
        const startTime = Date.now();

        try {
            // Verificar API key
            const apiKey = process.env.OPENAI_API_KEY ||
                          this.readConfigValue('OPENAI_API_KEY') ||
                          this.readConfigValue('openai.apiKey');

            if (!apiKey) {
                return null;
            }

            // Health check
            const response = await this.fetchWithTimeout(
                'https://api.openai.com/v1/models',
                {
                    headers: {
                        'Authorization': `Bearer ${apiKey}`,
                        'User-Agent': 'CLAW-Extension/1.0'
                    }
                },
                2000
            );

            if (!response.ok) {
                return null;
            }

            const latency = Date.now() - startTime;

            return {
                provider: 'openai',
                name: '🟢 OpenAI ChatGPT',
                available: true,
                latency_ms: latency,
                endpoint: 'https://api.openai.com/v1',
                apiKey: '***', // Não retornar chave real
                model: 'gpt-4o-mini',
                priority: 2
            };

        } catch (error) {
            return null;
        }
    }

    /**
     * PROBE: Claude (Anthropic)
     */
    private async probeClaude(): Promise<AIProbeResult | null> {
        const startTime = Date.now();

        try {
            const apiKey = process.env.ANTHROPIC_API_KEY ||
                          this.readConfigValue('ANTHROPIC_API_KEY') ||
                          this.readConfigValue('claude.apiKey');

            if (!apiKey) {
                return null;
            }

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
                        model: 'claude-opus',
                        max_tokens: 1,
                        messages: [{ role: 'user', content: 'hi' }]
                    })
                },
                2000
            );

            if (!response.ok) {
                return null;
            }

            return {
                provider: 'claude',
                name: '🔴 Anthropic Claude',
                available: true,
                latency_ms: Date.now() - startTime,
                endpoint: 'https://api.anthropic.com/v1',
                apiKey: '***',
                model: 'claude-3-sonnet',
                priority: 3
            };

        } catch (error) {
            return null;
        }
    }

    /**
     * PROBE: LocalAI (Ollama, vLLM, LM Studio, etc)
     */
    private async probeLocalAI(): Promise<AIProbeResult | null> {
        const startTime = Date.now();

        const endpoints = [
            process.env.LOCALAI_ENDPOINT || 'http://localhost:8000',
            'http://localhost:5000',    // LM Studio
            'http://127.0.0.1:5000',
            'http://localhost:11434',   // Ollama (default)
            'http://127.0.0.1:11434'
        ];

        for (const endpoint of endpoints) {
            try {
                const response = await this.fetchWithTimeout(
                    `${endpoint}/v1/models`,
                    { method: 'GET', timeout: 1000 },
                    1000
                );

                if (response.ok) {
                    const data: any = await response.json();
                    const modelName = data.data?.[0]?.id || 'mistral-7b';

                    return {
                        provider: 'localai',
                        name: '🟡 LocalAI (Offline)',
                        available: true,
                        latency_ms: Date.now() - startTime,
                        endpoint: endpoint,
                        model: modelName,
                        priority: 4 // Menor prioridade que APIs cloud
                    };
                }
            } catch (error) {
                // Tentar próximo endpoint
                continue;
            }
        }

        return null;
    }

    /**
     * PROBE: Ollama (específico)
     */
    private async probeOllama(): Promise<AIProbeResult | null> {
        const startTime = Date.now();

        try {
            const response = await this.fetchWithTimeout(
                'http://localhost:11434/api/tags',
                { method: 'GET' },
                1000
            );

            if (response.ok) {
                const data: any = await response.json();
                const models = data.models || [];

                if (models.length === 0) {
                    return null;
                }

                const modelName = models[0]?.name || 'mistral:7b';

                return {
                    provider: 'ollama',
                    name: '🟣 Ollama (Local)',
                    available: true,
                    latency_ms: Date.now() - startTime,
                    endpoint: 'http://localhost:11434',
                    model: modelName,
                    priority: 5
                };
            }

        } catch (error) {
            return null;
        }

        return null;
    }

    // ═══════════════════════════════════════════════════════════════════════════════
    // HELPERS
    // ═══════════════════════════════════════════════════════════════════════════════

    /**
     * Fetch com timeout
     */
    private async fetchWithTimeout(
        url: string,
        options: RequestInit & { timeout?: number },
        defaultTimeout: number
    ): Promise<Response> {
        const timeout = options.timeout || defaultTimeout;
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), timeout);

        try {
            const opts = { ...options };
            delete (opts as any).timeout;
            return await fetch(url, { ...opts, signal: controller.signal });
        } finally {
            clearTimeout(timeoutId);
        }
    }

    /**
     * Ler configuração de arquivo
     */
    private readConfigValue(key: string): string | undefined {
        try {
            const configPath = path.join(homedir(), '.claw/config/.claude.json');

            if (!fs.existsSync(configPath)) {
                return undefined;
            }

            const content = fs.readFileSync(configPath, 'utf-8');
            const config = JSON.parse(content);

            // Suportar notação de ponto: "openai.apiKey"
            return key.split('.').reduce((obj: any, k: string) => obj?.[k], config);

        } catch (error) {
            return undefined;
        }
    }

    /**
     * Clear cache (teste)
     */
    clearCache(): void {
        this.probeCache.clear();
        this.lastProbeTime = 0;
    }
}
