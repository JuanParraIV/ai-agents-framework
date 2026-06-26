# RUNBOOK-F1 — Ejecutar el flujo issue→story→.feature→PR

Runbook operativo para **cerrar el exit criterion de Fase 1**: un issue real recorre
`issue → story → .feature → PR` con el **gate BDD** funcionando. Asume que F0 está hecho
y que los agentes/skills de F1 existen (`product-analyst`, `qa-bdd-engineer`, `developer`).

> Cumple los guardrails de [`../CLAUDE.md`](../CLAUDE.md): ramas `feature/*`, nunca merge
> propio, story siempre en `AI-draft` para revisión humana, `.feature` inmutable tras Dev.

---

## 0. Pre-flight (entorno y MCP)

Claude Code expande `${VAR}` **al arrancar**; si lanzas `claude` sin el `.env` cargado,
el MCP de JIRA recibe el literal `${JIRA_URL}` y el de GitHub no levanta. Para evitarlo:

```bash
cd ~/Documents/DevOps/ai-agents-framework
direnv allow          # ya ejecutado; carga .env al entrar al directorio
# (fallback sin direnv:  set -a; source .env; set +a)
claude                # relánzalo en esta shell, con el entorno cargado
```

Dentro de Claude Code, verifica:

```
/mcp        →  atlassian  ✓ connected   |   github  ✓ connected
```

Prueba de humo (debe devolver datos reales, no errores `Invalid URL '${JIRA_URL}'`):

```
> lista mis proyectos de JIRA
```

> ⚠️ Si `github` no conecta: el endpoint `api.githubcopilot.com/mcp/` requiere un token
> con acceso válido. Confirma `GITHUB_TOKEN` y los scopes (Contents/PR/Issues = RW) según
> [`MCP-SETUP.md`](./MCP-SETUP.md) §3.2.

### Inputs que necesitas decidir antes de empezar

| Input | Para qué | Ejemplo |
|-------|----------|---------|
| **Project key de JIRA** | dónde vive el issue/story/sub-tasks | `PROJ` |
| **Issue crudo de origen** | el bug/feature request a refinar | `PROJ-101` |
| **Repo destino del código** | dónde van `.feature`, steps y el PR | `org/repo` |

---

## 1. Product — issue → User Story (+ Gherkin AC + sub-tasks)

```
> refinar el issue PROJ-101 en una User Story
```

El agente `product-analyst`:
- lee el issue crudo, escribe la story con **AC en Gherkin** (≥3 escenarios),
- la crea en estado **`AI-draft`** con labels `ai-generated` + `needs-review`,
- crea sub-tasks `[BDD]`, `[DEV]`, `[QA]` y enlaza la story al issue de origen.

**✅ Checkpoint 1:** existe la story en `AI-draft` con Gherkin AC y 3 sub-tasks enlazadas.

### 🔒 GATE HUMANO 1 — revisión de la story
Un humano revisa la story `AI-draft`. Si es correcta, la transiciona a `Ready` (o el
estado equivalente "listo para BDD"). **El pipeline no avanza sin esta aprobación.**

---

## 2. QA — story → `.feature` + step skeletons (contrato inmutable)

```
> generate BDD tests for PROJ-XXX     (la story creada en el paso 1)
```

El agente `qa-bdd-engineer`:
- detecta el framework BDD del repo destino (behave / Cucumber-JVM / Cucumber.js / pytest-bdd),
- genera el `.feature` (1 Feature por story, tag `@PROJ-XXX`, 1 escenario por AC),
- genera **step definitions skeleton** (`pending` / `NotImplementedError` / `PendingException`),
- corre **dry-run** (gate: 0 undefined, 0 ambiguous) y abre PR con los artefactos,
- transiciona **solo** el sub-task `[BDD] → Done` y comenta ubicaciones.

**✅ Checkpoint 2:** `.feature` + steps en el repo, dry-run verde, `[BDD]` en `Done`.

### 🔒 GATE BDD (automático, lo impone el agente Dev)
A partir de aquí el `.feature` es **inmutable**. El agente `developer` rehúsa arrancar
si no se cumple: existe `.feature` **y** existen step defs **y** `[BDD]` está en `Done`.

---

## 3. Dev — `.feature` → código → PR (make tests pass)

```
> implement story PROJ-XXX
```

El agente `developer`:
- **verifica el gate BDD** (STOP si falla),
- crea rama `feature/PROJ-XXX-descripcion`,
- implementa código + rellena los step skeletons **sin tocar el `.feature`**,
- corre la suite BDD hasta que **todos los escenarios pasan**,
- commitea (Conventional Commits + `Jira: PROJ-XXX`) y abre **PR (no mergea)**,
- transiciona `[DEV] → In Review` y comenta el link del PR + escenarios en verde.

Límites de PR: ≤15 archivos, ≤500 líneas añadidas (si se excede, pide split).

**✅ Checkpoint 3:** PR abierto desde `feature/*`, suite BDD verde, `[DEV]` en `In Review`.

### 🔒 GATE HUMANO 2 — revisión y merge del PR
Un humano (≠ autor) revisa y mergea el PR. **Ningún agente mergea su propio trabajo (SOX).**

---

## 4. Verificación del exit criterion de Fase 1

- [ ] Issue crudo refinado a story con Gherkin AC (`product-analyst`).
- [ ] Story creada en `AI-draft` y aprobada por humano (Gate 1).
- [ ] `.feature` + step skeletons generados; dry-run verde; `[BDD] = Done` (`qa-bdd-engineer`).
- [ ] Gate BDD respetado: Dev solo arrancó con `[BDD]` en `Done`.
- [ ] Código implementado, suite BDD verde, **PR abierto sin merge** (`developer`).
- [ ] Trazabilidad: issue ↔ story ↔ sub-tasks ↔ rama ↔ PR, todo con la JIRA key.

Con todos marcados, **Fase 1 queda cerrada** y habilita Fase 2 (Quality Engineering).

---

Documentos relacionados: [`README.md`](../README.md) · [`ARCHITECTURE.md`](./ARCHITECTURE.md) ·
[`GOVERNANCE.md`](./GOVERNANCE.md) · [`MCP-SETUP.md`](./MCP-SETUP.md)
</content>
</invoke>
