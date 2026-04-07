# CLAUDE.md - Guia de Regras para Novos Projetos

Este arquivo fornece orientações para Claude ao trabalhar com código neste repositório.

## 🎯 Stack Detectado

Ajuste conforme necessário para seu projeto:

```
- Linguagens: [Rust/Python/TypeScript/etc]
- Frameworks: [.NET/Flask/React/Vue/etc]
- Package Manager: [Cargo/pip/npm/etc]
```

## ✅ Verificação

Antes de mergear código para produção, execute:

```bash
# Formatação
cargo fmt
# ou
python -m black .

# Linting
cargo clippy --workspace --all-targets -- -D warnings
# ou
python -m pylint src/

# Testes
cargo test --workspace
# ou
python -m pytest tests/
```

## 📁 Estrutura do Repositório

```
.
├── src/              # Código-fonte principal
├── tests/            # Testes unitários e integração
├── .claude.json      # Configuração de API e limites
├── .claude/          # Overrides locais e settings específicos da máquina
├── .devcontainer/    # Containerização para VS Code
└── CLAUDE.md         # Este arquivo
```

### Convenções

- **Commits pequenos e review-friendly**: Um commit = uma feature ou fix claro
- **Manter .claude.json sincronizado**: Valores shared entre máquinas
- **Usar .claude/settings.local.json para overrides**: Configurações específicas locais
- **Não sobrescrever CLAUDE.md automaticamente**: Atualize intencionalmente quando workflows mudam

## 🔄 Fluxo de Trabalho

1. **Planejamento**: Descrever claramente o que precisa ser feito
2. **Execução**: Múltiplos agentes trabalham em paralelo
3. **Review**: Testes passam, código é revisado
4. **Merge**: Quando aprovado, integrar na main
5. **Feedback**: Loops de retry se necessário

## 🚨 Panic Protocol

Se algo quebrar em produção:

```bash
./automation/my_scripts/panic.sh "[descrição do problema]"
```

Isso:
- Para a execução imediata
- Notifica via Discord/Slack
- Cria issue no GitHub
- Rollback automático (se configurado)

## 📊 Status Check

Antes de iniciar novo trabalho:

```bash
./automation/my_scripts/status.sh
```

Mostra:
- Estado dos testes
- Cobertura de código
- Issues abertas
- Dependências desatualizadas
- Ambiente configurado

## 🔐 Segurança

- Nunca commitar chaves API (use .claude/settings.local.json)
- Validar inputs em todos os entrypoints
- Rodar `cargo audit` regularmente (Rust)
- Manter dependencies atualizadas
- Usar signed commits quando possível

## 📝 Documentação

Manter documentação atualizada:
- README.md: Overview e setup
- CLAUDE.md: Guia de desenvolvimento (este)
- Inline comments: Para lógica complexa
- ADRs: Para decisões arquiteturais importantes

## 💡 Dicas para Reutilização

### PC Novo?
```bash
cp ~/ClawRafaelIA/bin/claw /usr/local/bin/
cp ~/.claw/config/.claude.json ~/.claw/config/  # ou seu path
```

### Novo Projeto?
```bash
cp ~/ClawRafaelIA/config/CLAUDE.template.md ./CLAUDE.md
cp -r ~/ClawRafaelIA/environment/.devcontainer ./.devcontainer
claw status  # Valida o ambiente
```

### Novo Ambiente?
```bash
# O .devcontainer já tem tudo pré-configurado
# Abra no VS Code e clique em "Reopen in Container"
```

## 🛠️ Troubleshooting

**Problema: `claw` command not found**
- Solução: `sudo cp ~/ClawRafaelIA/bin/claw /usr/local/bin && chmod +x /usr/local/bin/claw`

**Problema: Ambiente quebrou**
- Solução: `./automation/my_scripts/repair.sh`

**Problema: Testes falhando**
- Solução: `cargo clean && cargo test` (ou equivalente)

## 📚 Referências

- [Claw Code Philosophy](https://github.com/seu-usuario/claw-code-parity)
- [OmX - oh-my-codex](https://github.com/Yeachan-Heo/oh-my-codex)
- [clawhip - Event Router](https://github.com/Yeachan-Heo/clawhip)
- [OmO - oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent)
