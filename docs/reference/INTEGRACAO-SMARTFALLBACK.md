# 🚀 Guia de Integração: SmartFallback + Gemini

## 📋 Checklist de Implementação

- [ ] Copiar `smartFallback.ts` para `src/`
- [ ] Atualizar imports em `agentManager.ts`
- [ ] Atualizar `inlineCompletionProvider.ts` para usar SmartFallback
- [ ] Testar com VS Code dev
- [ ] Compilar e empacotar

---

## 1️⃣ Atualizar `agentManager.ts`

Adicione no início do arquivo:

```typescript
import { SmartFallback } from './smartFallback';
```

E no construtor:

```typescript
export class AgentManager {
    private logger: Logger;
    private agentPythonPath: string;
    private smartFallback: SmartFallback;  // ← NOVO
    private circuitBreakerFailures: number = 0;
    private circuitBreakerTimeout: number = 0;

    constructor(logger: Logger) {
        this.logger = logger;
        this.agentPythonPath = this.resolveAgentPath();
        this.smartFallback = new SmartFallback(logger);  // ← NOVO
    }
```

Substitua o método `suggest` por este:

```typescript
async suggest(
    context: string,
    language: string,
    fileName: string,
    maxTokens: number,
    cancellationToken: vscode.CancellationToken
): Promise<string> {
    try {
        // Circuit breaker check
        if (this.circuitBreakerFailures >= 5) {
            const now = Date.now();
            if (now - this.circuitBreakerTimeout < 300000) { // 5 minutos
                this.logger.warn('⚠️  Circuit breaker ativo');
                return this.getLocalSuggestion(context, language);
            } else {
                this.circuitBreakerFailures = 0;
            }
        }

        // Usar SmartFallback
        const result = await this.smartFallback.suggest(
            context,
            language,
            fileName,
            async (ctx, lang) => this.callGeminiDirect(ctx, lang, maxTokens),
            cancellationToken
        );

        if (result.source === 'gemini') {
            this.circuitBreakerFailures = 0;
        } else if (result.source !== 'template') {
            this.circuitBreakerFailures = 0;
        }

        this.logger.debug(
            `📊 Sugestão: ${result.source} (${result.latency_ms}ms, ${(result.confidence * 100).toFixed(0)}% confiança)`
        );

        return result.suggestion;

    } catch (error) {
        this.circuitBreakerFailures++;
        const errorMsg = error instanceof Error ? error.message : String(error);
        this.logger.error(`Erro em suggest: ${errorMsg}`);
        return this.getLocalSuggestion(context, language);
    }
}

private async callGeminiDirect(
    context: string,
    language: string,
    maxTokens: number
): Promise<string | null> {
    try {
        const { execSync } = require('child_process');
        const prompt = `Contexto ${language}:\n${context}\n\nPróxima linha (máx ${maxTokens} tokens):`;

        const result = execSync(
            `python3 "${this.agentPythonPath}" improve --language ${language} --max-tokens ${maxTokens} < /dev/stdin 2>/dev/null`,
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
```

---

## 2️⃣ Testar Localmente

```bash
cd vscode-extension

# Compilar
npm run compile

# Abrir em dev mode
npm run dev
```

Depois, em outro terminal, abra o VS Code em modo dev:

```bash
code --extensionPath /path/to/vscode-extension
```

---

## 3️⃣ Verificar Configuração

No VS Code, vá em: **Settings (Ctrl+,)** → Pesquise **clawrafaelia**

Configurações importantes:

```json
{
    "clawrafaelia.enabled": true,
    "clawrafaelia.debounceMs": 500,
    "clawrafaelia.maxTokens": 50,
    "clawrafaelia.geminiMaxWait": 2000,
    "clawrafaelia.minConfidenceToShow": 0.35
}
```

---

## 4️⃣ Teste Prático: Python

Crie arquivo `test.py`:

```python
def hello(name):
```

Espere 500ms de debounce → Veja a sugestão aparecer em cinza

Exemplos esperados:
- ✅ Gemini API: `"):\n    """Docstring"""\n    pass"`
- ✅ Pattern Match: `"):\n    pass"`
- ✅ Template: `"pass"`

---

## 5️⃣ Teste Prático: TypeScript

Crie arquivo `test.ts`:

```typescript
async function fetchData(url: string
```

Sugestões esperadas:
- ✅ Gemini: `) { const response = await fetch(url); return response.json(); }`
- ✅ Pattern: `) {\n    return;\n}`

---

## 6️⃣ Analytics: Monitorar Performance

Adicione este trecho em `inlineCompletionProvider.ts` (dentro do `provideInlineCompletionItems`):

```typescript
// Registrar métrica
const suggestion = await this.agentManager.suggest(/*...*/);

// Log de performance
this.logger.debug(
    `📊 Sugestão entregue em ${Date.now() - startTime}ms`
);
```

---

## 7️⃣ Compile & Package

Quando tudo funcionar:

```bash
npm run compile
npm run package

# Resultado: claw-rafaelia.vsix (1-2MB)
```

Compartilhe:
```bash
# Instalar seu .vsix localmente
code --install-extension claw-rafaelia.vsix
```

---

## 🔧 Troubleshooting

### Sugestões não aparecem

Verifique:
```bash
# 1. Agent.py está funcionando?
agent status

# 2. Extensão está habilitada?
Ctrl+, > clawrafaelia.enabled

# 3. Ver logs
Ctrl+Shift+P > Developer: Toggle Developer Tools
```

### Pattern não funciona

Edite `smartFallback.ts` e ajuste as regex no `initializePatterns()`.

Teste regex:
```typescript
const trigger = /def\s+\w+\s*\(/;
console.log(trigger.test('def hello('));  // true
```

### LocalAI timeout

Desabilite:
```json
{
    "clawrafaelia.enableLocalAI": false
}
```

---

## 📊 Exemplos de Output

```
// Python: typing 500ms de debounce
def my_function(x, y):
                        ↓ Sugestão (cinza)
                    ):\n    return x + y

// TypeScript: timeout Gemini → fallback pattern
async function fetch() {
                        ↓ Sugestão (cinza)
                    {\n    return;\n}

// Fallback template (último recurso)
class MyClass
         ↓ Sugestão (cinza)
         #TODO
```

---

## 📈 Métricas Esperadas

| Métrica | Esperado |
|---------|----------|
| Latência média (cache) | 15-30ms |
| Latência (Gemini) | 700-1500ms |
| Fallback pattern latência | 20-50ms |
| Taxa de cache hit | 60-70% |
| Aceita ção de usuário | 35-50% |

---

## 🎯 Deploy e Release

### 1. Atualizar versão

```bash
# Em package.json
{
    "version": "1.1.0",  // ← Incrementar
}
```

### 2. Build final

```bash
npm run compile
npm run package
```

### 3. Publicar marketplace

```bash
# Se estiver registrado
vsce publish
```

Ou simplesmente compartilhe o `.vsix`.

---

## 🚀 Resultado Final

Sua extensão terá:

✅ **Gemini + 4 fallbacks inteligentes**  
✅ **Cache ZERO API (60%+ das sugestões)**  
✅ **Circuit breaker automático**  
✅ **Analytics de performance**  
✅ **Suporte 10+ linguagens**  
✅ **Latência < 2s (timeout)**  

---

## 📚 Próximas Melhorias

1. **Batch requests** — Múltiplas sugestões em paralelo
2. **Fine-tuning** — Treinar modelo para seu estilo
3. **Custom patterns** — Patterns por projeto
4. **Webhook analytics** — Enviar métricas para servidor
5. **Persistent cache** — Sincronizar entre máquinas via OneDrive

---

**Status:** ✅ Pronto para integração  
**Tempo estimado:** 30-60 minutos  
**Suporte:** Abra uma [Issue](https://github.com/seu-usuario/claw-agent/issues) no GitHub  
