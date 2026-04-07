/**
 * SmartFallback - Agnóstico de IA com 4 camadas de fallback
 * 
 * Auto-detecta e usa:
 * 1. Google Gemini (via agent.py)
 * 2. OpenAI ChatGPT
 * 3. Anthropic Claude
 * 4. LocalAI / Ollama (local)
 * 
 * Fallbacks:
 * 5. Pattern Matching - Detecção de padrões de código
 * 6. Template Snippets - Estruturas básicas
 * 
 * Performance:
 * - Qualquer IA:  500-2000ms, confiança 95%
 * - Pattern:      1-50ms,     confiança 70%
 * - Template:     0-1ms,      confiança 40%
 */

import * as vscode from 'vscode';
import { Logger } from './logger';
import { AISelector } from './aiSelector';

// ═══════════════════════════════════════════════════════════════════════════════
// TIPOS E INTERFACES
// ═══════════════════════════════════════════════════════════════════════════════

interface PatternRule {
    trigger: RegExp;
    suggestions: string[];
    language: string;
    description?: string;
}

interface LanguageTemplates {
    [language: string]: string[];
}

interface FallbackResult {
    suggestion: string;
    source: 'gemini' | 'pattern' | 'localai' | 'template';
    confidence: number;
    latency_ms: number;
}

// ═══════════════════════════════════════════════════════════════════════════════
// MAIN: SmartFallback
// ═══════════════════════════════════════════════════════════════════════════════

export class SmartFallback {
    private logger: Logger;
    private aiSelector: AISelector;
    private patternRules: PatternRule[] = [];
    private languageTemplates: LanguageTemplates = {};

    constructor(logger: Logger) {
        this.logger = logger;
        this.aiSelector = new AISelector(logger);
        this.initializePatterns();
        this.initializeTemplates();
        this.logger.info('✅ SmartFallback inicializado (agnóstico de IA)');
    }

    /**
     * Inicializar AISelector (deve ser chamado após construtor)
     */
    async initialize(): Promise<string> {
        return await this.aiSelector.initialize();
    }

    /**
     * ORQUESTRADOR: 2 camadas principais (IA automática + 3 fallbacks)
     * 
     * 1. AISelector escolhe melhor IA disponível automaticamente
     * 2. Pattern Matching como fallback
     * 3. Template como último recurso
     */
    async suggest(
        context: string,
        language: string,
        _fileName: string,
        cancellationToken: vscode.CancellationToken
    ): Promise<FallbackResult> {
        const startTime = Date.now();

        try {
            // ════════════════════════════════════════════════════════════════════════════════
            // CAMADA 1: IA AUTOMÁTICA (Gemini, OpenAI, Claude, LocalAI, etc)
            // ════════════════════════════════════════════════════════════════════════════════

            if (!cancellationToken.isCancellationRequested) {
                const aiResult = await this.aiSelector.callAI(
                    context,
                    language,
                    50,  // maxTokens
                    cancellationToken
                );

                if (aiResult) {
                    return {
                        suggestion: aiResult,
                        source: 'gemini', // Could be any IA, mas retornar 'gemini' para compatibilidade
                        confidence: 0.95,
                        latency_ms: Date.now() - startTime
                    };
                }
            }

            // ════════════════════════════════════════════════════════════════════════════════
            // CAMADA 2: PATTERN MATCHING
            // ════════════════════════════════════════════════════════════════════════════════

            const patternResult = this.tryPattern(context, language);
            if (patternResult) {
                return {
                    suggestion: patternResult,
                    source: 'pattern',
                    confidence: 0.70,
                    latency_ms: Date.now() - startTime
                };
            }

            // ════════════════════════════════════════════════════════════════════════════════
            // CAMADA 3: TEMPLATE FALLBACK
            // ════════════════════════════════════════════════════════════════════════════════

            const templateResult = this.getTemplate(language);
            return {
                suggestion: templateResult,
                source: 'template',
                confidence: 0.40,
                latency_ms: Date.now() - startTime
            };

        } catch (error) {
            const errorMsg = error instanceof Error ? error.message : String(error);
            this.logger.debug(`SmartFallback erro: ${errorMsg}`);

            // Último recurso: template
            return {
                suggestion: this.getTemplate(language),
                source: 'template',
                confidence: 0.10,
                latency_ms: Date.now() - startTime
            };
        }
    }

    // ═══════════════════════════════════════════════════════════════════════════════
    // CAMADA 1: PATTERN MATCHING
    // ═══════════════════════════════════════════════════════════════════════════════

    private tryPattern(context: string, language: string): string | null {
        const lastLine = context.split('\n').pop() || '';
        const applicable = this.patternRules.filter(r => r.language === language);

        for (const rule of applicable) {
            if (rule.trigger.test(lastLine)) {
                // Escolher sugestão aleatória (melhor UX naturalista)
                const suggestion = rule.suggestions[
                    Math.floor(Math.random() * rule.suggestions.length)
                ];
                this.logger.debug(`✅ Pattern match: ${rule.description || rule.trigger.source}`);
                return suggestion;
            }
        }

        return null;
    }

    // ═══════════════════════════════════════════════════════════════════════════════
    // CAMADA 2: TEMPLATES
    // ═══════════════════════════════════════════════════════════════════════════════

    private getTemplate(language: string): string {
        const templates = this.languageTemplates[language] || ['# TODO'];
        return templates[Math.floor(Math.random() * templates.length)];
    }

    // ═══════════════════════════════════════════════════════════════════════════════
    // INICIALIZAÇÃO: PATTERNS
    // ═══════════════════════════════════════════════════════════════════════════════

    private initializePatterns(): void {
        this.patternRules = [
            // ─────────────────────────────────────────────────────────────────────────
            // PYTHON
            // ─────────────────────────────────────────────────────────────────────────

            {
                language: 'python',
                description: 'Função Python',
                trigger: /def\s+\w+\s*\(/,
                suggestions: [
                    '):\n    """Docstring"""\n    pass',
                    '):\n    pass',
                    '):\n    return None'
                ]
            },
            {
                language: 'python',
                description: 'Condicional if',
                trigger: /if\s+.+$/,
                suggestions: [
                    ':\n    pass',
                    ':\n    # TODO'
                ]
            },
            {
                language: 'python',
                description: 'Classe Python',
                trigger: /class\s+\w+/,
                suggestions: [
                    ':\n    """Docstring"""\n    pass',
                    '(object):\n    pass',
                    ':\n    def __init__(self):\n        pass'
                ]
            },
            {
                language: 'python',
                description: 'Try-Except',
                trigger: /try\s*:/,
                suggestions: [
                    '\n    pass\nexcept Exception as e:\n    pass',
                    '\n    pass\nexcept:\n    pass\nfinally:\n    pass'
                ]
            },
            {
                language: 'python',
                description: 'For loop',
                trigger: /for\s+\w+\s+in\s+/,
                suggestions: [
                    ':\n    pass',
                    ':\n    # TODO'
                ]
            },
            {
                language: 'python',
                description: 'Import',
                trigger: /^from\s+\S+\s+import\s+/,
                suggestions: [
                    'SomeClass',
                    'function',
                    '('
                ]
            },

            // ─────────────────────────────────────────────────────────────────────────
            // TYPESCRIPT / JAVASCRIPT
            // ─────────────────────────────────────────────────────────────────────────

            {
                language: 'typescript',
                description: 'Função TypeScript',
                trigger: /function\s+\w+\s*\(/,
                suggestions: [
                    ') {\n    // TODO\n}',
                    ') {\n    return;\n}',
                    ') {\n    throw new Error("Not implemented");\n}'
                ]
            },
            {
                language: 'typescript',
                description: 'Arrow function',
                trigger: /const\s+\w+\s*=\s*\(/,
                suggestions: [
                    ') => {\n    // TODO\n}',
                    ') => undefined'
                ]
            },
            {
                language: 'typescript',
                description: 'Async function',
                trigger: /async\s+function\s+\w+\s*\(/,
                suggestions: [
                    ') {\n    // TODO\n    return;\n}',
                    ') {\n    await;\n}'
                ]
            },
            {
                language: 'typescript',
                description: 'If statement',
                trigger: /if\s*\(/,
                suggestions: [
                    ') {\n    // TODO\n}',
                    ') { return; }'
                ]
            },
            {
                language: 'typescript',
                description: 'Interface',
                trigger: /interface\s+\w+/,
                suggestions: [
                    ' {\n    // TODO\n}',
                    ' extends BaseInterface {\n    // TODO\n}'
                ]
            },
            {
                language: 'typescript',
                description: 'Class',
                trigger: /class\s+\w+/,
                suggestions: [
                    ' {\n    // TODO\n}',
                    ' extends Base {\n    constructor() {\n        super();\n    }\n}'
                ]
            },

            // ─────────────────────────────────────────────────────────────────────────
            // C#
            // ─────────────────────────────────────────────────────────────────────────

            {
                language: 'csharp',
                description: 'Async Task',
                trigger: /public\s+(async\s+)?Task/,
                suggestions: [
                    ' => Task.CompletedTask;',
                    '\n{\n    // TODO\n    return Task.CompletedTask;\n}'
                ]
            },
            {
                language: 'csharp',
                description: 'If statement',
                trigger: /if\s*\(/,
                suggestions: [
                    ') { }',
                    ') { throw new NotImplementedException(); }',
                    ') {\n    // TODO\n}'
                ]
            },
            {
                language: 'csharp',
                description: 'Class C#',
                trigger: /public\s+class\s+\w+/,
                suggestions: [
                    ' { }',
                    ' : BaseClass { }',
                    '\n{\n    public ' + 'ClassName' + '() { }\n}'
                ]
            },
            {
                language: 'csharp',
                description: 'Record',
                trigger: /public\s+record\s+\w+/,
                suggestions: [
                    '();',
                    '(string Name, int Age);'
                ]
            },

            // ─────────────────────────────────────────────────────────────────────────
            // RUST
            // ─────────────────────────────────────────────────────────────────────────

            {
                language: 'rust',
                description: 'Função Rust',
                trigger: /fn\s+\w+\s*\(/,
                suggestions: [
                    ') {\n    // TODO\n}',
                    ') -> () {\n    // TODO\n}'
                ]
            },
            {
                language: 'rust',
                description: 'If statement',
                trigger: /if\s+/,
                suggestions: [
                    ' {\n    // TODO\n}',
                    ' { } else {\n    // TODO\n}'
                ]
            },

            // ─────────────────────────────────────────────────────────────────────────
            // GO
            // ─────────────────────────────────────────────────────────────────────────

            {
                language: 'go',
                description: 'Função Go',
                trigger: /func\s+\w+\s*\(/,
                suggestions: [
                    ') {\n    // TODO\n}',
                    ') error {\n    return nil\n}'
                ]
            },
            {
                language: 'go',
                description: 'If statement',
                trigger: /if\s+.+\s*\{/,
                suggestions: [
                    '\n    // TODO\n}',
                    '\n    return err\n}'
                ]
            }
        ];

        this.logger.info(`✅ ${this.patternRules.length} pattern rules carregados`);
    }

    // ═══════════════════════════════════════════════════════════════════════════════
    // INICIALIZAÇÃO: TEMPLATES
    // ═══════════════════════════════════════════════════════════════════════════════

    private initializeTemplates(): void {
        this.languageTemplates = {
            python: [
                '# TODO',
                'pass',
                'return None',
                'return',
                '"""Docstring"""',
                'if __name__ == "__main__":',
                'for i in range(10):',
                'try:\n    pass\nexcept:\n    pass',
                'with open("file.txt") as f:',
                'def function():',
                'class MyClass:',
                'import os'
            ],

            typescript: [
                '// TODO',
                'return;',
                'throw new Error("Not implemented");',
                'const x = ();',
                'async () => {}',
                'interface T {',
                'class MyClass { }',
                'export const fn = () => {};',
                'type Union = string | number;',
                'if (condition) { }'
            ],

            javascript: [
                '// TODO',
                'return;',
                'throw new Error("Not implemented");',
                'const x = ();',
                'async () => {}',
                'function fn() { }',
                'const obj = {};',
                'const arr = [];',
                'if (condition) { }',
                'for (let i = 0; i < 10; i++) { }'
            ],

            csharp: [
                '// TODO',
                'return;',
                'throw new NotImplementedException();',
                'public class MyClass { }',
                'public async Task MyMethodAsync() { }',
                'public record MyRecord(string Name);',
                'if (condition) { }',
                'var x = new Object();',
                'using var resource = GetResource();',
                'public interface IInterface { }'
            ],

            rust: [
                '// TODO',
                'unimplemented!()',
                'panic!("Not implemented");',
                'fn function() { }',
                'struct MyStruct { }',
                'impl MyStruct { }',
                'if condition { }',
                'match value { _ => { } }',
                'for i in 0..10 { }',
                'let x = 0;'
            ],

            go: [
                '// TODO',
                'panic("not implemented")',
                'return nil',
                'return nil, err',
                'func function() { }',
                'type MyType struct { }',
                'if condition { }',
                'for i := 0; i < 10; i++ { }',
                'for range slice { }',
                'package main'
            ],

            sql: [
                '-- TODO',
                'SELECT * FROM table WHERE id = 1;',
                'INSERT INTO table (col) VALUES (val);',
                'UPDATE table SET col = val WHERE id = 1;',
                'DELETE FROM table WHERE id = 1;',
                'CREATE TABLE table (id INT);',
                'DROP TABLE table;',
                'ALTER TABLE table ADD COLUMN col INT;',
                'CREATE INDEX idx ON table(col);',
                'SELECT COUNT(*) FROM table;'
            ],

            markdown: [
                '# Title',
                '## Heading',
                '- List item',
                '1. Numbered item',
                '```',
                '> Blockquote',
                '[Link](url)',
                '![Image](url)',
                '**Bold**',
                '*Italic*'
            ]
        };

        this.logger.info(`✅ Templates carregados para ${Object.keys(this.languageTemplates).length} linguagens`);
    }
}

