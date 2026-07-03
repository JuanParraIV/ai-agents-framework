# CI & Hooks — Gates forzados (TB-2)

Implementación de **TB-2** del [`TO-BE`](./TO-BE.md): convertir los guardrails de
[`../CLAUDE.md`](../CLAUDE.md) y [`GOVERNANCE.md`](./GOVERNANCE.md) de *texto en prompts*
a **mecanismos que no se pueden saltar**. Tres capas de defensa:

| Capa | Dónde | Qué fuerza | Bloqueo |
|------|-------|------------|---------|
| Hooks de Claude Code | `.claude/settings.json` → `.claude/hooks/` | `.feature` inmutable · secret-scan pre-commit | exit 2 (deny) |
| Git hook | `.githooks/pre-commit` | `.feature` inmutable · secret-scan | exit 1 |
| CI | `.github/workflows/ci.yml` | gate BDD (dry-run + suite) · gitleaks | job falla |

Defensa en profundidad: el hook de Claude protege el flujo del **agente**; el git hook
protege cualquier commit **humano/otra herramienta**; el CI es la **red final** en el PR.

---

## 1. Hooks de Claude Code

Configurados en `.claude/settings.json` (`hooks.PreToolUse`):

- **`protect_feature.py`** — matcher `Edit|Write|MultiEdit|NotebookEdit`. Bloquea (exit 2)
  cualquier intento de **modificar** un `.feature` existente (Edit/MultiEdit, o Write que
  sobrescribe). **Permite** crear uno nuevo (Write a ruta inexistente → lo hace QA).
  Enforcement de `CLAUDE.md §1.5` (contrato BDD inmutable).
- **`secret_scan.py`** — matcher `Bash`. Si el comando es `git commit`, escanea las líneas
  **añadidas** del diff staged y bloquea (exit 2) ante private keys, tokens (AWS/GitHub/Slack),
  credenciales genéricas, CVV o **PAN validado por Luhn**. Nunca imprime el valor, solo la
  categoría. Enforcement de `CLAUDE.md §2/§5`.

> Los hooks se activan solos al abrir Claude Code en el repo (leen `$CLAUDE_PROJECT_DIR`).

## 2. Git hook (a nivel git, fuera del agente)

`.githooks/pre-commit` aplica los **mismos** controles a cualquier `git commit`. Actívalo
una vez por clon:

```bash
git config core.hooksPath .githooks
```

Reutiliza `secret_scan.py --staged` y bloquea `.feature` modificados
(`git diff --cached --diff-filter=M -- '*.feature'`).

## 3. CI (GitHub Actions)

`.github/workflows/ci.yml`, en cada `pull_request` y push a `main`/`develop`:

- **`bdd-gate`**: `behave --dry-run` (falla si hay steps sin enlazar → 0 undefined) y
  `behave` (la suite debe estar 100% verde).
- **`secret-scan`**: `gitleaks detect --redact --exit-code 1` sobre el histórico.

## 4. Branch protection (paso de admin — no automatizable sin permisos)

El CI no basta: hay que **exigirlo** para mergear y cerrar el bucle SoD/SOX
(`GOVERNANCE.md §2`). En GitHub → *Settings → Branches → Add rule* para `main` y `develop`:

- ✅ Require a pull request before merging · **Require approvals: 1** (revisor ≠ autor).
- ✅ Require status checks to pass → `bdd-gate`, `secret-scan`.
- ✅ Require branches to be up to date · ✅ Do not allow bypass.

Equivalente por CLI (requiere token admin del repo):

```bash
gh api -X PUT repos/OWNER/REPO/branches/main/protection \
  -F required_pull_request_reviews.required_approving_review_count=1 \
  -F 'required_status_checks.contexts[]=bdd-gate' \
  -F 'required_status_checks.contexts[]=secret-scan' \
  -F required_status_checks.strict=true \
  -F enforce_admins=true -F restrictions=
```

---

## 5. Verificación (todo probado localmente)

| Test | Resultado esperado | ✅ |
|------|--------------------|----|
| Edit sobre `.feature` existente | bloqueado (exit 2) | ✅ |
| Write de `.feature` nuevo | permitido (exit 0) | ✅ |
| Edit de código normal | permitido (exit 0) | ✅ |
| `git commit` con secreto staged | bloqueado | ✅ |
| `git commit` limpio | permitido | ✅ |
| `behave --dry-run` | exit 0 (0 undefined) | ✅ |
| `behave` | 9/9 escenarios verdes | ✅ |

Con esto se cumple el **criterio 2 de §3 del TO-BE** (cada control tiene un mecanismo que
lo impone), salvo la branch protection que requiere un admin del repo (§4).

---

Relacionados: [`TO-BE.md`](./TO-BE.md) · [`CLAUDE.md`](../CLAUDE.md) · [`GOVERNANCE.md`](./GOVERNANCE.md) · [`RUNBOOK-F1.md`](./RUNBOOK-F1.md)
