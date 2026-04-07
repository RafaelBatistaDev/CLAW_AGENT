# 🚀 Release Automation Guide

Script automated para criar releases da extensão CLAW.

---

## 📋 Como Usar

### **Uso Básico**

```bash
cd ~/OneDrive/ClawRafaelIA/vscode-extension
bash release.sh
```

### **Processo Automático**

O script automaticamente:

1. ✅ Detecta versão atual em `package.json`
2. ✅ Pergunta pela nova versão (semântico: X.Y.Z)
3. ✅ **Compila** TypeScript
4. ✅ **Empacota** .vsix
5. ✅ **Cria commit** com mensagem
6. ✅ **Cria tag** Git (vX.Y.Z)
7. ✅ **Faz push** para GitHub (branch + tag)
8. ✅ **Gera instruções** para GitHub Release

---

## 🎯 Exemplo Prático

```bash
$ bash release.sh

[INFO]  CLAW Release Automation
[INFO]  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[INFO]  Versão atual: 1.0.1

Nova versão (atual: 1.0.1): 1.0.2

[INFO]  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[INFO]  Plano de release:
[INFO]    • Versão: 1.0.1 → 1.0.2
[INFO]    • Compilar & Empacotar
[INFO]    • Git commit & tag
[INFO]    • Push para GitHub
[INFO]  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Continuar? [s/N] s

[INFO]  1️⃣  Atualizando package.json...
[OK]    Versão atualizada para 1.0.2

[INFO]  2️⃣  Compilando TypeScript...
[OK]    Compilação concluída

[INFO]  3️⃣  Empacotando .vsix...
[OK]    Arquivo criado: clawrafaelia-suggestions-1.0.2.vsix

[INFO]  4️⃣  Criando commit...
[OK]    Commit criado

[INFO]  5️⃣  Criando tag...
[OK]    Tag v1.0.2 criada

[INFO]  6️⃣  Fazendo push para GitHub...
[OK]    Push concluído

[INFO]  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[OK]    Release v1.0.2 pronta para publicar!
[INFO]  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Próximos passos (manual no GitHub):

1️⃣  Acesse a URL:
   https://github.com/RafaelBatistaDev/CLAW---Sugest-es-Inline-com-IA/releases/new

2️⃣  Preencha:
   Tag version: v1.0.2
   Release title: CLAW v1.0.2

3️⃣  Upload do arquivo:
   /home/recifecrypto/OneDrive/ClawRafaelIA/vscode-extension/clawrafaelia-suggestions-1.0.2.vsix

4️⃣  Clique 'Publish release'
```

---

## 🔧 O que o Script Faz

### 1️⃣ **Detecção de Versão**
Lê versão atual de `package.json`:
```bash
grep '"version"' package.json | sed 's/.*"\([^"]*\)".*/\1/'
```

### 2️⃣ **Validação de Entrada**
- Valida formato semântico (X.Y.Z)
- Impede versão duplicada
- Pede confirmação antes de continuar

### 3️⃣ **Atualização de package.json**
```bash
sed -i "s/\"version\": \".*\"/\"version\": \"$NEW_VERSION\"/" package.json
```

### 4️⃣ **Compilação**
```bash
npm run compile:prod
```

### 5️⃣ **Empacotamento**
```bash
npm run package
```
Cria: `clawrafaelia-suggestions-X.Y.Z.vsix`

### 6️⃣ **Git Commit**
```bash
git commit -m "Bump version to X.Y.Z"
```

### 7️⃣ **Git Tag**
```bash
git tag -a "vX.Y.Z" -m "CLAW vX.Y.Z Release"
```

### 8️⃣ **Git Push**
```bash
git push origin main
git push origin vX.Y.Z
```

---

## ⚙️ Pré-requisitos

- ✅ Bash shell
- ✅ Git com acesso SSH configurado
- ✅ npm/Node.js
- ✅ Acesso de escrita ao repositório
- ✅ TSconfig e webpack.config.js atualizados

---

## 🎯 Versionamento Semântico

Use formato **MAJOR.MINOR.PATCH**:

| Versão | Caso de Uso |
|--------|-----------|
| `1.0.0` → `1.0.1` | Bug fixes, patches pequenos |
| `1.0.1` → `1.1.0` | Novas features (backward compatible) |
| `1.1.0` → `2.0.0` | Mudanças breaking, reescritas |

---

## 🆘 Troubleshooting

### "Erro de compilação"
```bash
npm run compile:prod
# Verifique erros TypeScript antes de usar release.sh
```

### "Git push falhou"
```bash
git config --list | grep credential
# Certifique-se de ter SSH key configurada
# ou credenciais HTTPS salvas
```

### "npm run package falhou"
```bash
rm -rf dist/ node_modules/
npm install
npm run package
```

### "Script não é executável"
```bash
chmod +x release.sh
```

---

## 📚 Fluxo Completo de Release

1. **Local — Script Automático:**
   ```bash
   bash release.sh
   ```

2. **Local — Modificações:**
   ```bash
   # Script faz tudo automaticamente!
   ```

3. **GitHub — Manual:**
   - Visite: https://github.com/RafaelBatistaDev/CLAW---Sugest-es-Inline-com-IA/releases/new
   - Tag: `vX.Y.Z`
   - Upload: `.vsix`
   - Publish

4. **VS Code Marketplace — Opcional:**
   ```bash
   vsce publish --packagePath clawrafaelia-suggestions-X.Y.Z.vsix
   ```

---

## 📝 Git Commits Gerados

Exemplo para versão `1.0.2`:

```
Commit:  9ff8743
Message: Bump version to 1.0.2

Tag:     v1.0.2
Message: CLAW v1.0.2 Release
```

---

## 🔒 Segurança

- ✅ Script valida entrada (não aceita strings malformadas)
- ✅ Git tag impede duplicação
- ✅ Confirmação antes de continuar
- ✅ Set -e garante saída em erro
- ✅ Sem escrita em arquivos desnecessários

---

## 🚀 Próximas Iterações

Futuras melhorias:
- [ ] Auto-criar GitHub Release via API
- [ ] Auto-publicar no Marketplace
- [ ] Changelog gerado automaticamente
- [ ] Testes antes de build
- [ ] Integração com GitHub Actions

---

**Última atualização:** 6 de abril de 2026  
**Autor:** Rafael Batista (@RafaelBatistaDev)
