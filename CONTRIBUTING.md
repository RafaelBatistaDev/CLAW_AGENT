# 🤝 Contributing to CLAW VS Code Extension

Obrigado por se interessar em contribuir! Este documento explica como fazer isso.

## 🚀 Quick Start para Contribuidores

```bash
# 1. Fork do projeto (GitHub)
# 2. Clone seu fork
git clone https://github.com/your-username/clawrafaelia-extension.git
cd vscode-extension

# 3. Instalar dependências
npm install

# 4. Começar desenvolvimento
npm run dev

# 5. Em outra aba, rodar testes
npm test

# 6. Fazer commit & push
git add .
git commit -m "fix: descrever mudança"
git push origin feature-branch

# 7. Abrir Pull Request no GitHub
```

---

## 📋 Tipos de Contribuições

### 🐛 Reportar Bugs

**Onde reportar:** GitHub Issues → `New Issue` → `Bug Report`

**Informações essenciais:**

```markdown
### Descrição
[Descreva o problema em 1-2 frases]

### Passos para Reproduzir
1. Abrir arquivo .py
2. Digitar "def foo"
3. Pausar por 500ms
4. Nada acontece

### Comportamento Esperado
Sugestão deveria aparecer em cinza

### Informações do Sistema
- OS: [Linux/macOS/Windows]
- VS Code version: [1.85+]
- Extension version: [latest]
- Python version: [3.9+]

### Logs
[Copie o resultado de: Ctrl+Shift+P → CLAW: Show Status]
```

---

### ✨ Sugerir Features

**Onde:** GitHub Discussions ou Issues → `Feature Request`

**Template:**

```markdown
### Descrição do Feature
[O que você gostaria que a extensão fizesse?]

### Caso de Uso
[Quando você usaria isso?]

### Solução Proposta
[Como você implementaria? (opcional)]

### Alternativas Consideradas
[Havia outras formas? (opcional)]
```

---

### 💻 Contribuir Código

**Prioridade (comece por aqui):**

| Prioridade | Tipo | Exemplos |
|-----------|------|----------|
| 🔴 Alta | Core fixes | Debounce bug, cache corruption |
| 🟠 Média | Features | New language support, config option |
| 🟡 Baixa | Polish | Log formatting, comment clarity |
| 🟢 Documentação | Docs | README update, code comments |

---

## 🏗️ Estrutura do Projeto

```
vscode-extension/
├── src/
│   ├── extension.ts              # Entry point
│   ├── inlineCompletionProvider.ts  # Core logic
│   ├── agentManager.ts           # Agent communication
│   ├── tokenCache.ts             # Caching
│   └── logger.ts                 # Logging
├── test/                         # Unit tests
├── dist/                         # Compiled (auto-generated)
├── package.json                  # Manifest
├── tsconfig.json                 # TypeScript config
├── webpack.config.js             # Bundler
└── .eslintrc.json               # Linter rules
```

---

## 🛠️ Development Workflow

### 1. Setup Local

```bash
# Clone
git clone https://github.com/your-username/clawrafaelia-extension.git

# Install
cd vscode-extension
npm install

# Compile once
npm run compile

# Watch mode (auto-compile on save)
npm run dev
```

### 2. Fazer Mudança

**Exemplo: Adicionar suporte para Dart**

```typescript
// src/extension.ts
const LANGUAGE_PATTERNS = [
  // ... existing patterns ...
  '**/*.dart',  // ← Add Dart
];
```

### 3. Testar

```bash
# Rodar testes
npm test

# Manual testing in VS Code
1. F5 (Run & Debug)
2. Opens new VS Code window
3. Create .dart file and test
4. Check Output → CLAW Debug Log
```

### 4. Lint & Format

```bash
# Check style
npm run lint

# Auto-fix
npm run lint -- --fix

# Format (Prettier)
npm run format
```

### 5. Commitamento

```bash
# Follow Conventional Commits
git commit -m "feat: adicionar suporte para Dart"
# ou
git commit -m "fix: cache não persiste após restart"
# ou
git commit -m "docs: atualizar README"
```

---

## 📝 Commit Message Convention

Seguimos [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: adicionar novo feature
fix: corrigir bug
docs: atualizar documentação
style: formatação, sem mudança funcional
refactor: reescrever código sem mudar comportamento
perf: melhoria de performance
test: adicionar/atualizar testes
chore: mudanças de build, deps, etc
```

**Exemplos:**

```bash
git commit -m "feat: adicionar suporte para Go"
git commit -m "fix: debounce não funciona em múltiplos documentos"
git commit -m "docs: adicionar exemplo de cache"
git commit -m "perf: otimizar Jaccard similarity"
```

---

## 🧪 Testing

### Executar Testes

```bash
npm test                 # All tests
npm test -- --watch     # Watch mode
npm test -- --coverage  # With coverage
```

### Estrutura de Testes

```
test/
├── tokenCache.test.ts
├── agentManager.test.ts
└── utils.test.ts
```

### Exemplo de Test

```typescript
// test/tokenCache.test.ts
import { TokenCache } from '../src/tokenCache';

describe('TokenCache', () => {
  let cache: TokenCache;
  
  beforeEach(() => {
    cache = new TokenCache();
  });
  
  test('should cache similar context', () => {
    cache.put('def hello', 'print()');
    
    const result = cache.lookup('def hel');  // Similar
    expect(result?.suggestion).toBe('print()');
  });
  
  test('should not cache dissimilar context', () => {
    cache.put('def hello', 'print()');
    
    const result = cache.lookup('class Foo');  // Dissimilar
    expect(result).toBeNull();
  });
});
```

### Ao Submeter PR: Checklist

- [ ] Código compila sem erros (`npm run compile`)
- [ ] Testes passam (`npm test`)
- [ ] Lint passa (`npm run lint`)
- [ ] Commit messages seguem convention
- [ ] README atualizado (se needed)
- [ ] CHANGELOG entry (se feature/fix major)

---

## 📚 Code Style

### TypeScript Style Guide

```typescript
// ✅ GOOD: Explicit types
async function suggest(
  context: string,
  language: string,
  maxTokens: number
): Promise<SuggestionResult> { }

// ❌ BAD: Any types
async function suggest(context: any, lang: any): any { }

// ✅ GOOD: Named imports
import { InlineCompletionItem } from 'vscode';

// ❌ BAD: Star imports (except for namespaces)
import * as everything from 'vscode';

// ✅ GOOD: Descriptive names
const debounceDelayMs = 500;
const agent = new AgentManager();

// ❌ BAD: Single letter or vague names
const d = 500;
const a = new AgentManager();

// ✅ GOOD: Early returns
if (!context) return null;
const result = processContext(context);
return result;

// ❌ BAD: Deep nesting
if (context) {
  if (language) {
    const result = processContext(context);
    return result;
  }
}
```

### ESLint Rules

Checked with `.eslintrc.json`:

```json
{
  "quotes": ["error", "double"],          // Double quotes
  "semi": ["error", "always"],            // Semicolons required
  "indent": ["error", 2],                 // 2-space indent
  "@typescript-eslint/no-explicit-any": "error"  // No any type
}
```

---

## 🔧 Adding a New Feature

### Example: Add language support for Kotlin

**Step 1: Add to language patterns**

```typescript
// src/extension.ts
const LANGUAGE_PATTERNS = [
  // ... existing ...
  '**/*.kt',  // ← Add Kotlin
];
```

**Step 2: Add Kotlin suggestions in fallback**

```typescript
// src/agentManager.ts
private generateLocalSuggestion(payload): SuggestionResult {
  const patterns = {
    // ... existing ...
    kotlin: [
      'fun ',
      'return',
      'println()',
      'val ',
    ],
  };
  // ... rest of logic
}
```

**Step 3: Test**

```bash
# Create test file
echo 'fun hello() {}' > test.kt

# Open in VS Code
code test.kt

# Type something and test suggestions
```

**Step 4: Update README**

```markdown
### Supported Languages

- Python
- TypeScript/JavaScript
- C#
- Rust
- Go
- Ruby
- PHP
- Java
- C++
- **Kotlin** ← New!
```

**Step 5: Commit**

```bash
git add src/extension.ts src/agentManager.ts README.md
git commit -m "feat: add Kotlin language support"
```

---

## 🚨 Common Issues & Solutions

### Issue: "npm install" fails

**Solution:**
```bash
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

### Issue: TypeScript compilation error

**Solution:**
```bash
npm run compile

# If still broken, check tsconfig.json
cat tsconfig.json | grep -A5 '"strict"'
```

### Issue: Eslint showing errors

**Solution:**
```bash
npm run lint -- --fix  # Auto-fix
npm run format         # Format code
```

### Issue: Test failures

**Solution:**
```bash
npm test -- test/file.test.ts  # Run single test
npm test -- --verbose          # More details
```

---

## 📤 Submitting a Pull Request

### Before Submitting

```bash
# 1. Update from main
git fetch origin
git rebase origin/main

# 2. Test everything
npm run compile
npm test
npm run lint

# 3. Commit
git commit -m "fix: resolver issue #123"

# 4. Push
git push origin feature-branch
```

### PR Template (auto-filled on GitHub)

```markdown
## Description
[What does this PR do?]

## Related Issue
Fixes #[issue number]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
[How did you test this?]

## Checklist
- [ ] Code compiles
- [ ] Tests pass
- [ ] Lint passes
- [ ] Commit messages follow convention
- [ ] README updated (if needed)
```

### PR Review Process

1. **Automated checks:**
   - GitHub Actions runs tests/lint
   - Coverage reports generated
   - Netlify preview (docs)

2. **Maintainer review:**
   - Code quality
   - Design decisions
   - Test coverage
   - Documentation

3. **Feedback:**
   - "Request changes" → Make updates
   - "Comment" → Address concerns
   - "Approve" → Ready to merge

4. **Merge:**
   - Maintainer merges to main
   - Auto-deployed to marketplace

---

## 🔓 Code of Conduct

**TL;DR:** Be respectful, helpful, and constructive.

- ✅ Welcome diversity and different perspectives
- ✅ Assume good intent
- ✅ Be patient and kind
- ✅ Focus on the code, not the person
- ❌ No harassment, discrimination, or abuse
- ❌ No spam or promotional content

---

## 📞 Getting Help

### Debugging

```typescript
// Enable debug logging
// Settings → clawrafaelia.logLevel → debug

// Check logs
Ctrl+Shift+P → Output → CLAW Debug Log
```

### Questions?

1. **Existing issue?** Search GitHub Issues
2. **Docs?** Check README.md, ARCHITECTURE.md, QUICK-START.md
3. **Still stuck?** Open GitHub Discussion

### Useful Links

- **VS Code API:** https://code.visualstudio.com/api
- **TypeScript:** https://www.typescriptlang.org/docs
- **Conventional Commits:** https://www.conventionalcommits.org
- **ESLint:** https://eslint.org/docs/rules

---

## 🎓 Learning Path

### Beginner (New to VS Code extensions)

1. Read: QUICK-START.md
2. Read: ARCHITECTURE.md (high-level)
3. Task: Add comment to code
4. Task: Fix typo in README
5. Task: Update version number

### Intermediate (Comfortable with extension basics)

1. Task: Add new language to patterns
2. Task: Adjust debounce timing
3. Task: Improve error handling
4. Task: Update fallback suggestions

### Advanced (Deep knowledge of codebase)

1. Task: Optimize Jaccard algorithm
2. Task: Add configuration option
3. Task: Implement new caching strategy
4. Task: Add telemetry/analytics

---

## 🎉 Recognition

Contributors are recognized in:

- `CONTRIBUTORS.md` file
- GitHub releases notes
- VS Code marketplace changelog

Thank you! 🙏

---

## 📝 License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT or Apache 2.0, specify in LICENSE file).

---

**Happy contributing!** 🚀
