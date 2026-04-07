# 👋 Bem-vindo ao CLAW!

**Sua extensão de código com IA está pronta para trabalhar!**

---

## ⚡ 3 Passos para Começar

### **1️⃣ Abra um arquivo de código**

Qualquer arquivo: Python (`.py`), TypeScript (`.ts`), Java (`.java`), C# (`.cs`), etc.

```python
# create_file.py
def hello_world():
    print("Hello, ")
    # Pause aqui por 500ms...
```

### **2️⃣ Comece a digitar e pausa**

CLAW aguarda você parar de digitar por **500ms** para sugerir:

```python
def hello_world():
    print("Hello, ")
    # ⏳ Aguardando 500ms...
    # 💡 Sugestão aparecerá em CINZA
```

### **3️⃣ Escolha sua ação**

```
Tab  = Aceitar sugestão ✅
Esc  = Rejeitar ❌
↑↓   = Próxima/anterior
```

---

## 🎮 Atalhos Principais

| Tecla | Ação |
|-------|------|
| **Tab** | ✅ Aceitar sugestão |
| **Esc** | ❌ Rejeitar |
| **Ctrl+Alt+C** | 🔄 Ativar/Desativar |

---

## ⚙️ Primeira Configuração (Opcional)

Pressione **Ctrl+,** e procure por `clawrafaelia`:

```json
{
  "clawrafaelia.enabled": true,           // Ativar/desativar
  "clawrafaelia.debounceMs": 500,         // Tempo de espera
  "clawrafaelia.maxTokens": 150           // Tamanho da sugestão
}
```

---

## 📖 Documentação Completa

Quer saber mais? Abra:

👉 **[USER-GUIDE.md](USER-GUIDE.md)** — Guia completo com exemplos
👉 **[QUICK-START.md](QUICK-START.md)** — Setup rápido
👉 **[ARCHITECTURE.md](ARCHITECTURE.md)** — Como funciona

---

## 💡 Exemplo Rápido

### **Python**
```python
def calculate_total(items):
    total = 0
    for item in items:
        total +=  # ← CLAW sugere: item['price']
```

### **TypeScript**
```typescript
interface User {
    id: number;
    name: string;
    email:  // ← CLAW sugere: string;
}
```

### **C#**
```csharp
public async Task<User> GetUserAsync(int id)
{
    // ← CLAW sugere:
    var user = await _context.Users.FindAsync(id);
    return user ?? throw new NotFoundException();
}
```

---

## 🔧 Verificar Status

Pressione **Ctrl+Shift+P** e execute:

```
CLAW: Show Status
```

Mostra:
- ✅ Agent status (API conectada?)
- ✅ Cache size (quantas sugestões armazenadas)
- ✅ Version

---

## 🆘 Algo Não Funciona?

### **Sugestões não aparecem?**
1. Abra arquivo code (`.py`, `.ts`, `.js`, etc.)
2. Comece a digitar
3. **Aguarde 500ms** (não digita muito rápido)
4. Check: `Ctrl+Shift+P` → `CLAW: Show Status`

### **Sugestões lentas?**
Aumente o debounce em Settings:
```json
"clawrafaelia.debounceMs": 1000
```

### **Precisa de ajuda?**
📧 Email: rafaelbatistadev@outlook.com.br  
🐙 GitHub: [Abrir issue](https://github.com/RafaelBatistaDev/CLAW---Sugest-es-Inline-com-IA/issues)

---

## 🌟 Linguagens Suportadas

✅ Python
✅ TypeScript/JavaScript
✅ C# (.NET)
✅ Java
✅ Rust
✅ Go
✅ Ruby
✅ PHP
✅ C++
✅ SQL
✅ E mais!

---

## 🚀 Próximos Passos

1. **Abra um arquivo de codigo**
2. **Comece a digitar** (experimente!)
3. **Leia [USER-GUIDE.md](USER-GUIDE.md)** para mais dicas
4. **Configure em Settings** se quiser customizar

---

## 👨‍💻 Desenvolvido por

**Rafael Batista** - C# Developer  
🐙 [@RafaelBatistaDev](https://github.com/RafaelBatistaDev)

---

## 📜 Licença

MIT - Use livremente!

---

**Pronto para começar?** 🎉  
Abra um arquivo e comece a digitar!
