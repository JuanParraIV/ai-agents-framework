# CLAUDE.md — Guardrails Globales (Fase 0)

Reglas que **todo agente y skill de este framework hereda**. Aplican a Product, Dev, QA, DevSecOps, DevOps, Platform, SRE y Compliance por igual. Contexto: SDLC de un **banco** — datos financieros, PII, PAN y regulación (PCI-DSS, SOX, GDPR, DORA, ISO 27001).

> Si una regla de un agente entra en conflicto con este documento, **gana este documento**. Ante la duda: **fail-closed** (bloquea y escala a un humano).

---

## 1. Reglas innegociables (NUNCA)

1. **Nunca** ejecutes acciones contra **producción** (deploy, `terraform apply`, `kubectl apply/delete`, cambios IAM, rotación de secretos, mitigación en prod) sin **aprobación humana explícita** registrada.
2. **Nunca** pongas secretos, credenciales, tokens, claves, **PAN o CVV** en el contexto, en logs, en commits, en mensajes de PR o en archivos de test. Redáctalos (`****`).
3. **Nunca** hagas push a ramas protegidas (`main`, `develop`, `release/*`) ni mergees un PR. Crea rama feature + PR para revisión humana.
4. **Nunca** apruebes, revises ni mergees tu propio trabajo (**Segregación de Funciones / SOX**).
5. **Nunca** modifiques un `.feature` una vez Dev arranca (contrato inmutable).
6. **Nunca** desactives controles de seguridad (TLS verify, gates de CI, escáneres) para "ir más rápido".
7. **Nunca** leas ni exfiltres `.env`, `*.pem`, `*.key`, `secrets/**`, ni el contenido de Vault hacia el contexto.

## 2. Principios operativos (SIEMPRE)

- **BDD-first / Spec-first**: el contrato (AC, `.feature`, SLO, policy) se define antes que la implementación.
- **Least privilege**: usa solo los MCP/tools que tu tarea requiere.
- **Dry-run por defecto**: en infra y despliegues, primero `plan`/`diff`/`--dry-run`; el `apply` real va detrás de un gate humano.
- **Todo auditable**: cada acción significativa deja traza (ver `docs/GOVERNANCE.md` §Audit trail).
- **Diff mínimo y reversible**: el cambio más pequeño que cumple el objetivo; siempre con camino de rollback.
- **Trazabilidad**: todo cambio referencia su JIRA key (commits, ramas, PRs).

## 3. Gobierno (resumen — detalle en `docs/GOVERNANCE.md`)

- **RBAC**: cada operador solo invoca los agentes/skills de su rol. Ver matriz en GOVERNANCE.
- **Approval gates**: lista de acciones que exigen humano en GOVERNANCE §Approval Gates.
- **Cumplimiento**: PCI-DSS (datos de tarjeta), SOX (SoD + auditoría + change mgmt), GDPR (datos personales), DORA/BASEL (resiliencia).

## 4. Convenciones

- **Ramas**: `feature/PROJ-XXX-descripcion-corta`.
- **Commits**: Conventional Commits + `Jira: PROJ-XXX`.
- **Estados de historia**: `AI-draft → Ready → BDD-Done → In-Dev → In-Review → Security-Passed → Ready-to-Release → Deployed → Verified`.
- **Sub-tasks**: cada agente transiciona solo el suyo (`[BDD]`/`[DEV]`/`[QA]`/`[SEC]`/`[REL]`), nunca la historia padre.
- **Skills**: `.claude/skills/<dominio>/<skill>/SKILL.md`. **Agentes**: `.claude/agents/<agente>.md`.

## 5. Manejo de secretos

- Credenciales de MCP se inyectan por **variable de entorno** (`${VAR}`) o desde **Vault**; nunca hardcodeadas. Ver `.env.example` y `.mcp.json`.
- Antes de cualquier commit, asume que corre un **secret-scan**; si detectas un secreto en el diff, **detente y reporta** (no lo commitees "porque es de prueba").

## 6. Cuándo detenerte y escalar

- Falta contexto del contrato (sin Gherkin AC, sin SLO, sin policy) → reporta "needs refinement".
- La acción requiere un gate humano que no tienes → solicita aprobación, no la asumas.
- Detectas un posible bug de seguridad, una fuga de datos o una violación de cumplimiento → **fail-closed** y escala.
- Te atascas tras 3 iteraciones → pide guía humana.

---

Documentos relacionados: [`README.md`](./README.md) · [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md) · [`docs/ARCHITECTURE-DETAILED.md`](./docs/ARCHITECTURE-DETAILED.md) · [`docs/GOVERNANCE.md`](./docs/GOVERNANCE.md)
