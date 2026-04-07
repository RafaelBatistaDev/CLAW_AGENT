/**
 * TokenCache - Cache inteligente de sugestões
 * 
 * Estratégia ZERO API:
 * - Armazenar sugestões em cache local (SQLite mínimalista)
 * - Similaridade semântica para reusar sugestões parecidas
 * - Economizar 100% de API calls para contextos similares
 */

import { join } from 'path';
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';

interface CacheEntry {
    context: string;
    suggestion: string;
    timestamp: number;
    hits: number;
}

export class TokenCache {
    private cache: Map<string, CacheEntry> = new Map();
    private cacheFilePath: string;
    private maxEntries: number = 500;
    private similarityThreshold: number = 0.75; // 75% similar = reusar

    constructor(globalStorageUri: string) {
        this.cacheFilePath = join(globalStorageUri, 'claw-suggestions-cache.json');
        this.loadFromDisk();
    }

    /**
     * Obter sugestão do cache
     * Usa similaridade semântica ao invés de match exato
     */
    get(context: string): string | null {
        // Buscar match exato primeiro
        if (this.cache.has(context)) {
            const entry = this.cache.get(context)!;
            entry.hits++;
            return entry.suggestion;
        }

        // Buscar sugestão similar (80%+)
        let bestMatch: CacheEntry | null = null;
        let bestScore = 0;

        for (const entry of this.cache.values()) {
            const similarity = this.calculateSimilarity(context, entry.context);
            if (similarity > this.similarityThreshold && similarity > bestScore) {
                bestScore = similarity;
                bestMatch = entry;
            }
        }

        if (bestMatch) {
            bestMatch.hits++;
            return bestMatch.suggestion;
        }

        return null;
    }

    /**
     * Armazenar sugestão em cache
     */
    set(context: string, suggestion: string): void {
        // Não cachecar sugestões muito curtas ou vazias
        if (!suggestion || suggestion.trim().length < 3) {
            return;
        }

        this.cache.set(context, {
            context,
            suggestion,
            timestamp: Date.now(),
            hits: 0
        });

        // Cleanup se exceder limite
        if (this.cache.size > this.maxEntries) {
            this.pruneCache();
        }

        // Salvar no disco (async)
        setImmediate(() => this.saveToDisk());
    }

    /**
     * Limpar cache
     */
    clear(): void {
        this.cache.clear();
        try {
            writeFileSync(this.cacheFilePath, JSON.stringify({}));
        } catch (e) {
            // Ignorar erro
        }
    }

    /**
     * Obter estatísticas do cache
     */
    getStats(): string {
        let totalHits = 0;
        for (const entry of this.cache.values()) {
            totalHits += entry.hits;
        }

        return `${this.cache.size} entries, ${totalHits} hits`;
    }

    /**
     * Calcular similaridade entre dois strings
     * Algoritmo: Jaccard similarity (simples mas eficaz)
     */
    private calculateSimilarity(str1: string, str2: string): number {
        // Tokenizar em palavras/tokens
        const tokens1 = new Set(str1.toLowerCase().split(/\W+/));
        const tokens2 = new Set(str2.toLowerCase().split(/\W+/));

        // Jaccard: |intersection| / |union|
        const intersection = new Set([...tokens1].filter(x => tokens2.has(x)));
        const union = new Set([...tokens1, ...tokens2]);

        return union.size > 0 ? intersection.size / union.size : 0;
    }

    /**
     * Remover entradas menos usadas quando cache está cheio
     * FIFO + LRU (Frequency-based)
     */
    private pruneCache(): void {
        // Ordenar por hits (descendente) e depois por timestamp (ascendente)
        const sorted = Array.from(this.cache.entries())
            .sort(([, a], [, b]) => {
                if (a.hits !== b.hits) {
                    return b.hits - a.hits; // Mais recentes first
                }
                return a.timestamp - b.timestamp; // Antigos first
            });

        // Remover 20% das piores entradas
        const toRemove = Math.ceil(this.maxEntries * 0.2);
        for (let i = sorted.length - 1; i >= sorted.length - toRemove; i--) {
            this.cache.delete(sorted[i][0]);
        }
    }

    /**
     * Carregar cache do disco
     */
    private loadFromDisk(): void {
        try {
            if (!existsSync(this.cacheFilePath)) {
                return;
            }

            const data = readFileSync(this.cacheFilePath, 'utf-8');
            const obj = JSON.parse(data);

            for (const [key, value] of Object.entries(obj)) {
                if (
                    value &&
                    typeof value === 'object' &&
                    'suggestion' in value &&
                    'timestamp' in value
                ) {
                    this.cache.set(key, value as CacheEntry);
                }
            }
        } catch (e) {
            // Ignorar erro de parse (cache corrompido)
        }
    }

    /**
     * Salvar cache no disco
     */
    private saveToDisk(): void {
        try {
            // Garantir diretório existe
            const dir = this.cacheFilePath.substring(0, this.cacheFilePath.lastIndexOf('/'));
            mkdirSync(dir, { recursive: true });

            // Converter Map para Object
            const obj: Record<string, CacheEntry> = {};
            for (const [key, value] of this.cache.entries()) {
                obj[key] = value;
            }

            writeFileSync(this.cacheFilePath, JSON.stringify(obj, null, 2));
        } catch (e) {
            // Ignorar erro de escrita
        }
    }
}
