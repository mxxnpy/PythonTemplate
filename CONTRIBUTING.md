# Contribuindo

## Padrão de Commits

Este projeto utiliza **Conventional Commits** para manter um histórico de commits limpo e padronizado.

### Formato

```
type(scope): description
```

### Types

| Type | Descrição |
|------|-----------|
| `feat` | Nova funcionalidade |
| `fix` | Correção de bug |
| `chore` | Tarefas de manutenção |
| `docs` | Documentação |
| `style` | Formatação (sem mudança de código) |
| `refactor` | Refatoração de código |
| `test` | Adição ou correção de testes |
| `ci` | Mudanças de CI/CD |
| `perf` | Melhorias de performance |
| `build` | Mudanças no build |
| `revert` | Reverter commit anterior |

### Scope (Opcional)

O scope indica qual parte do código foi alterada:

- Nome do arquivo: `logger.py`, `config.py`
- Módulo: `api`, `core`, `domain`
- Funcionalidade: `auth`, `users`, `database`

### Exemplos

```bash
# nova funcionalidade
feat(api): add health check endpoint
feat(auth): implement JWT authentication

# correção de bug
fix(database): resolve connection timeout
fix(api): handle null response

# manutenção
chore(deps): update dependencies
chore(logger): add newline at end of file

# documentação
docs(readme): add installation guide
docs(api): update endpoint documentation

# formatação
style(core): fix indentation
style: apply ruff formatting

# refatoração
refactor(handlers): simplify error handling
refactor: rename routes to controllers

# testes
test(api): add integration tests
test(specs): add specification tests

# CI/CD
ci: add commit lint check
ci(docker): optimize build cache

# performance
perf(database): add query caching
perf(api): implement response compression

# build
build: update dockerfile
build(deps): add new dependency
```

### Git Hooks (Opcional)

Para validar commits localmente antes do push, você pode usar o `pre-commit`:

```bash
pip install pre-commit
pre-commit install --hook-type commit-msg
```

