# 🤖 AGENTE — Guia Completo dos 4 Comandos

**Como usar o ClawRafaelIA para analisar, melhorar, documentar e testar código automáticamente.**  
Data: 6 de abril de 2026 | Versão: 1.0.0

---

## ⚡ OS 4 COMANDOS PRINCIPAIS

### 1️⃣ **analyze** — Detectar Bugs e Problemas

**O que faz:** Encontra bugs, vulnerabilidades de segurança, ineficiências e melhores práticas não seguidas.

```bash
agent analyze <arquivo>
```

**Exemplo:**
```bash
agent analyze src/main.py
agent analyze config.json
agent analyze schema.sql
```

**Saída esperada:**
```
📊 Analisando: src/main.py
  📚 Carregando contexto do projeto... ✅ 2 .md carregados

🐛 BUGS ENCONTRADOS (2):
  • Line 42: Unwrap sem error handling
  • Line 87: Possível integer overflow

🚀 MELHORIAS SUGERIDAS (3):
  • Usar Result<T> em vez de Option<T>
  • Cache regex compilation
  • Adicionar type hints (PEP 484)

✅ Boas Práticas:
  • Código está bem estruturado
  • Segue padrões do projeto (STANDARDS.md)
  • Documentação adequada
```

**Quando usar:** Antes de submeter PR, refatoração grande, ou revisar código novo.

---

### 2️⃣ **improve** — Refatorar e Otimizar

**O que faz:** Refatora código para melhorar qualidade, performance e legibilidade.

```bash
agent improve <arquivo>
```

**Exemplo:**
```bash
agent improve src/utils.py
agent improve package.json
agent improve main.rs
```

**Saída esperada:**
```
📊 Refatorando: src/utils.py
  📚 Contexto: 2 arquivos .md

🔧 VERSÃO ORIGINAL:
  def process(data):
      return filter(lambda x: x > 0, data)

🚀 VERSÃO MELHORADA:
  def process(data: List[int]) -> List[int]:
      """Filter positive values from data."""
      return [x for x in data if x > 0]

✨ MELHORIAS APLICADAS:
  ✓ Type hints adicionados
  ✓ List comprehension mais eficiente
  ✓ Docstring adiccionada
  ✓ Mais legível e Pythônico

💾 Salvar resultado? (y/n) 
```

**Quando usar:** Otimizar código, refatoração antes de merge, ou melhorar legibilidade.

---

### 3️⃣ **document** — Gerar Documentação Automática

**O que faz:** Cria documentação completa (Markdown) para funções, classes e módulos.

```bash
agent document <arquivo>
```

**Exemplo:**
```bash
agent document src/api/handlers.ts
agent document database/models.py
agent document lib/utils.go
```

**Saída esperada:**
```
📝 Documentando: src/api/handlers.ts

## Module: handlers

### `getUserById(id: string): User`
- **Descrição:** Obtém usuário por ID único
- **Parâmetros:**
  - `id` (string): ID do usuário
- **Retorno:** User object com dados completos
- **Exceções:** UserNotFound se ID não existir
- **Exemplo:**
  ```typescript
  const user = await getUserById("123");
  console.log(user.name); // "João"
  ```

### `updateUser(id: string, data: Partial<User>): Promise<User>`
...

💾 Salvar documentação? (y/n)
```

**Quando usar:** Documentar novo código, gerar README, ou criar API docs.

---

### 4️⃣ **test** — Criar Testes Unitários

**O que faz:** Gera testes unitários automáticos para cobertura de código.

```bash
agent test <arquivo>
```

**Exemplo:**
```bash
agent test src/calculator.py
agent test lib/math.js
agent test src/User.cs
```

**Saída esperada:**
```
🧪 Gerando Testes: src/calculator.py

import pytest
from src.calculator import add, subtract, multiply

class TestCalculator:
    def test_add_positive_numbers(self):
        assert add(2, 3) == 5
    
    def test_add_negative_numbers(self):
        assert add(-2, -3) == -5
    
    def test_add_zero(self):
        assert add(0, 5) == 5
    
    def test_subtract_positive(self):
        assert subtract(5, 3) == 2
    
    def test_divide_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            divide(10, 0)

💾 Salvar testes em tests/test_calculator.py? (y/n)
```

**Quando usar:** Aumentar cobertura de testes, novo código, ou antes de merge para produção.

---

## 📊 REFERÊNCIA RÁPIDA

| Comando | Detecta | Melhora | Documenta | Testa |
|---------|---------|---------|-----------|-------|
| **analyze** | ✅ Bugs, vulnerabilidades, ineficiências | — | — | — |
| **improve** | — | ✅ Refatora, otimiza | — | — |
| **document** | — | — | ✅ Gera docs Markdown | — |
| **test** | — | — | — | ✅ Cria testes |

---

## 🌍 LINGUAGENS SUPORTADAS

**Suporte automático para 10+ linguagens:**

| Linguagem | analyze | improve | document | test |
|-----------|---------|---------|----------|------|
| Python | ✅ | ✅ | ✅ | ✅ |
| JavaScript/TypeScript | ✅ | ✅ | ✅ | ✅ |
| Rust | ✅ | ✅ | ✅ | ✅ |
| Go | ✅ | ✅ | ✅ | ✅ |
| C# / .NET | ✅ | ✅ | ✅ | ✅ |
| Java | ✅ | ✅ | ✅ | ✅ |
| C/C++ | ✅ | ✅ | ✅ | ✅ |
| PHP | ✅ | ✅ | ✅ | ✅ |
| Ruby | ✅ | ✅ | ✅ | ✅ |
| SQL | ✅ | ✅ | ✅ | — |

---

## 💡 EXEMPLOS PRÁTICOS

### Cenário 1: Revisar código antes de PR

```bash
# Verificar qualidade
agent analyze src/main.py

# Refatorar
agent improve src/main.py

# Gerar documentação
agent document src/main.py

# Criar testes
agent test src/main.py

# Commit!
git add src/
git commit -m "Melhoria: refatoração + testes + docs"
```

### Cenário 2: Documentar projeto legado

```bash
# Para cada arquivo:
for file in src/*.py; do
    agent document "$file"
done

# Resultado: documentação completa!
```

### Cenário 3: Aumentar cobertura de testes

```bash
# Ver o que precisa de testes
agent analyze src/utils.py

# Gerar testes automaticamente
agent test src/utils.py

# Executar
pytest tests/test_utils.py -v
```

---

## ⚙️ CONFIGURAÇÃO

### Arquivo: `~/.claw/config/.claude.json`

```json
{
  "api": {
    "google_gemini_api_key": "${GOOGLE_GEMINI_API_KEY}no",
    "model": "gemini-2.0-flash",
    "timeout": 60
  },
  "limits": {
    "max_daily_requests": 1000,
    "max_tokens_per_request": 2000
  }
}
```

✅ **Já vem pré-configurado!** (Google Gemini, chave válida)

---

## 🎯 DICAS E TRUQUES

### Análise de múltiplos arquivos

```bash
# Analisar todos os arquivos Python
for file in src/**/*.py; do
    agent analyze "$file"
done
```

### Melhorar com contexto do projeto

Coloque seus padrões em `STANDARDS.md` para o agente entender:

```markdown
# STANDARDS.md

## Nossas práticas de codificação

- Use type hints em todas funções Python
- Limite linhas a 100 caracteres
- Use comments em inglês
- TDD (Test-Driven Development)
```

Agora o agente considera isso ao analisar!

### Automação: Analisar antes de commit

Adicione a `~/.bashrc`:

```bash
commit-safe() {
    for file in $(git diff --cached --name-only); do
        agent analyze "$file" || return 1
    done
    git commit "$@"
}
```

Use: `commit-safe -m "Minha mudança"`

---

## ❓ FAQ

**P: Quanto custa usar o agente?**  
R: Grátis! Usa API do Google Gemini com limite de 1000 requisições/dia.

**P: E se passar do limite?**  
R: Cria um arquivo `.backup` automático antes de falhar. Roda testes locais.

**P: Posso confiar nos testes gerados?**  
R: São um bom ponto de partida! Sempre revise e adicione casos edge.

**P: Funciona offline?**  
R: Análise sim (usa regras locais). Outros comandos precisam da API.

**P: Quais arquivos são suportados?**  
R: Qualquer tipo de arquivo de código (extensão automática).

**P: Posso usar em CI/CD?**  
R: Sim! Veja [DEVELOPMENT.md](DEVELOPMENT.md) para GitHub Actions.

---

## 🚀 PRÓXIMOS PASSOS

1. **Comece agora:** `agent analyze seu_arquivo.py`
2. **Leia mais:** [INDEX.md](INDEX.md) — Mapa completo
3. **Contribua:** [DEVELOPMENT.md](DEVELOPMENT.md)
4. **Dúvidas?** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**Status:** 100% Funcional  
**Última atualização:** 6 de abril de 2026  
**Suporte:** Ver [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
