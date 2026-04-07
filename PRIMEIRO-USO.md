# 🚀 PRIMEIRO USO — Comece em 2 Minutos

**Setup rápido + primeira análise do agente.**  
Data: 6 de abril de 2026

---

## ⚡ PASSO 1: Ativar (30 segundos)

```bash
# Carregue configuração
source ~/.bashrc

# Valide instalação
agent status
```

✅ **Pronto!** API está configurada e funcionando.

---

## 🎯 PASSO 2: Primeira Análise (30 segundos)

Crie um arquivo de teste:

```bash
# Python
cat > test.py << 'EOF'
def calculate_total(items):
    total = 0
    for item in items:
        total = total + item
    return total

result = calculate_total([1, 2, 3])
print(result)
EOF

# Use o agente
agent analyze test.py
```

**Resultado esperado:**
```
📊 Analisando: test.py
📚 Contexto carregado...

✅ Código OK, mas sugestões:
  • Usar sum() built-in em vez de loop
  • Adicionar type hints
  • Usar list comprehension
```

---

## 📖 PASSO 3: Aprender os 4 Comandos (1 minuto)

```bash
# 1. Analisar
agent analyze test.py

# 2. Melhorar
agent improve test.py

# 3. Documentar
agent document test.py

# 4. Testar
agent test test.py
```

Ver [AGENTE.md](AGENTE.md) para detalhes completos.

---

## 🎓 PRÓXIMOS PASSOS

**Agora que sabe usar, explore:**

| Leia | Se você quer |
|------|--------------|
| [INDEX.md](INDEX.md) | Mapa completo (todos os docs) |
| [AGENTE.md](AGENTE.md) | Guia detalhado dos 4 comandos |
| [QUICKSTART.md](QUICKSTART.md) | Referência rápida (3 min) |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Soluções para problemas |
| [PHILOSOPHY.md](PHILOSOPHY.md) | Entender filosofia de design |

---

## ✅ CHECKLIST

- [ ] Execute `source ~/.bashrc`
- [ ] Execute `agent status` ✓
- [ ] Crie arquivo teste
- [ ] Execute `agent analyze teste`
- [ ] Veja os 4 comandos em ação
- [ ] Leia [AGENTE.md](AGENTE.md)

---

**Sucesso!** Ao longo de 2 minutos aprendeu o agente. Explore e divirta-se! 🎉
