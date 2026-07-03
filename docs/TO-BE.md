# TO-BE — De diseño documentado a controles forzados y probados

Estado objetivo del **AI Agents Framework** para que sea *100% exitoso*. Este documento
parte del AS-IS real del repo (no del diseño ideal) y define **qué falta y en qué orden**
para cruzar la brecha entre "arquitectura excelente" y "pipeline que demostrablemente
produce software bancario bajo controles auditables".

> Alinea con los guardrails de [`../CLAUDE.md`](../CLAUDE.md), el plano por fases de
> [`ARCHITECTURE.md`](./ARCHITECTURE.md) y el modelo de gobierno de [`GOVERNANCE.md`](./GOVERNANCE.md).
> Complementa (no reemplaza) el roadmap F0–F7; se enfoca en **cerrar F1 con evidencia**
> antes de expandir a F3–F7.

---

## 1. Diagnóstico AS-IS (medido, no aspiracional)

El framework hoy es **~90% documentación excelente y ~10% ejecutable**. El diseño es de
nivel profesional; la evidencia de que *funciona* es casi nula.

| Señal | Realidad medida | Estado |
|-------|-----------------|--------|
| Flujo end-to-end probado | Solo existe `.feature` + skeleton (SCRUM-1). Nunca se implementó código. | ❌ |
| Código de producción | No hay `src/`, `tests/`, ni salida real del agente `developer`. | ❌ |
| Suite BDD ejecutable | `behave` no está instalado; los steps lanzan `NotImplementedError`. | ❌ |
| CI / gates automáticos | No hay `.github/workflows`. Los gates son texto en prompts, no mecanismos. | ❌ |
| Audit trail | Es un esquema JSON documentado. Nada emite registros. | ❌ |
| Secret-scan | CLAUDE.md dice "asume que corre" — no hay hook que lo ejecute. | ❌ |
| Agentes | 4 de 10 existen (`product-analyst`, `qa-bdd-engineer`, `developer`, `test-generator`). | 🟡 |
| Skills | ~7 de ~40 construidas (F1–F3 core). | 🟡 |
| Gobierno (F0) | `CLAUDE.md`, `GOVERNANCE.md`, `settings.json`, `.gitignore`, `.env.example`. | ✅ |

**Riesgo central:** los controles de gobierno (SoD, gates humanos, fail-closed, RBAC)
están **descritos pero no forzados**. Nada mecánico impide violarlos — solo la buena
voluntad del prompt. En un banco, **un control no auditable es un control que no existe**.

---

## 2. El principio del TO-BE

> No faltan más fases. Falta **cerrar la brecha entre lo documentado y lo mecánicamente
> demostrable**. Cada control debe ser *inejecutable de saltar* y cada acción debe dejar
> *traza verificable*.

Regla de priorización: **probar antes que expandir**. Construir 6 agentes más antes de
demostrar que F1 funciona multiplica deuda no verificada (el riesgo de "deriva entre
skills y agentes" que la propia arquitectura lista).

---

## 3. Definición de "100% exitoso" (criterio medible)

El framework triunfa cuando se puede afirmar, con **evidencia ejecutable**:

1. **Flujo real verde**: un issue recorre `issue → story → .feature → PR con suite verde`,
   sin más intervención que los 2 gates humanos definidos en `RUNBOOK-F1`.
2. **Gates forzados**: cada control de `GOVERNANCE.md` tiene un **mecanismo que lo impone**
   (hook de Claude Code o job de CI), no solo un párrafo.
3. **Auditoría emitida**: cada acción significativa de un agente produce un **registro de
   audit trail** verificable (no un esquema teórico).
4. **Integridad del framework**: un CI propio valida que agentes ↔ skills ↔ MCP no tienen
   referencias rotas.

**Baseline actual: 0 de 4 cumplidos.**

---

## 4. Iniciativas del TO-BE (orden por valor)

### TB-1 — Probar F1 de punta a punta con una historia real  `[máxima prioridad]`
Cerrar el exit criterion que el propio [`RUNBOOK-F1`](./RUNBOOK-F1.md) define, usando **SCRUM-1**:
- Instalar `behave`; implementar el código de la transferencia con el agente `developer`.
- Dejar los **9 escenarios en verde** (happy path, saldo insuficiente, monto inválido,
  misma cuenta, cuenta ajena, idempotencia, rollback atómico, precisión decimal).
- Abrir **PR sin merge** desde `feature/*`, con `[DEV] → In Review`.
- **Por qué primero:** convierte todo el andamiaje en un pipeline que *demostrablemente*
  produce software. Es la pieza que hoy falta y la que da credibilidad a lo demás.
- **Exit:** `behave` corre; 9/9 escenarios verdes; PR abierto; criterio 1 de §3 cumplido.

### TB-2 — Forzar los gates con mecanismos, no con prompts
Los guardrails de `CLAUDE.md` deben ser inejecutables de saltar:
- **Hooks de Claude Code** (`.claude/settings.json`):
  - `PreToolUse` que bloquee edición de `*.feature` (contrato inmutable, `CLAUDE.md` §1.5).
  - `PreToolUse`/pre-commit que ejecute **secret-scan real** (el "asume que corre" debe correr).
- **CI en `.github/workflows`**: gate BDD (dry-run `0 undefined`), secret-scan (gitleaks),
  bloqueo de merge si la suite no está verde.
- **Branch protection** real en `main`/`develop`/`release/*` (revisor ≠ autor → SoD/SOX).
- **Exit:** intentar saltar un gate falla mecánicamente; criterio 2 de §3 cumplido.

### TB-3 — Audit trail que realmente emita registros
Convertir el esquema de `GOVERNANCE.md` §3 en un **hook `PostToolUse`** que escriba
`audit/*.jsonl` en cada acción significativa (campos: `timestamp`, `operator`, `agent`,
`skill`, `action`, `target`, `jira`, `inputs_redacted`, `result`, `approver`, `gate`).
- **Por qué:** sin traza emitida no se pasa una auditoría SOX/PCI.
- **Exit:** cada acción de agente deja un registro; criterio 3 de §3 cumplido.

### TB-4 — Sanear la fricción operativa ya conocida
- **MCP de GitHub:** hoy usa `api.githubcopilot.com/mcp/` (el propio `RUNBOOK-F1` admite el
  "si no conecta…"). Evaluar el server oficial de GitHub o `gh` CLI como fallback; un MCP
  inestable rompe el paso `.feature → PR`.
- **Smoke test del framework:** script que valide que cada agente referencia skills/MCP que
  existen (previene la deriva agentes↔skills).
- **Exit:** `/mcp` conecta de forma reproducible; el smoke test pasa; criterio 4 de §3 cumplido.

### TB-5 — Expandir F3 → F7 (solo tras TB-1…TB-4)
Con F1 probado y los controles forzados, expandir por valor bancario:
- **F3 `security-reviewer`** (siguiente por valor): `sast/sca/secret/container/iac-security/compliance`.
- Luego F4 (`devops-pipeline`), F5 (`platform-engineer`), F6 (`sre-agent`), F7 (`compliance-auditor`).
- Cada componente nuevo hereda TB-2/TB-3 (gate forzado + traza) desde su nacimiento.

---

## 5. Mapa iniciativa → criterio de éxito → fase

| Iniciativa | Cierra criterio §3 | Fase | Depende de |
|-----------|--------------------|------|------------|
| TB-1 Flujo F1 verde | 1 | F1 | — |
| TB-2 Gates forzados | 2 | F0/F1 | — (potencia TB-1) |
| TB-3 Audit trail emitido | 3 | F0/F7 | TB-2 (hooks) |
| TB-4 Fricción operativa | 4 | F1 | — |
| TB-5 Expansión F3–F7 | (mantiene 1–4) | F3–F7 | TB-1…TB-4 |

---

## 6. Secuencia recomendada

```
TB-1 (SCRUM-1 verde) ──▶ TB-2 (hooks + CI + branch protection) ──▶ TB-3 (audit jsonl)
        │                                                                    │
        └──────────────── TB-4 (MCP GitHub + smoke test) ───────────────────┘
                                        │
                                        ▼
                          TB-5 (F3 security → F4 → F5 → F6 → F7)
```

El camino más corto a los 4 criterios: **implementar SCRUM-1 y verlo verde**, luego cablear
hooks + CI, luego emitir el audit trail. Todo lo demás se construye sobre esa base probada.

---

Documentos relacionados: [`README.md`](../README.md) · [`CLAUDE.md`](../CLAUDE.md) ·
[`ARCHITECTURE.md`](./ARCHITECTURE.md) · [`ARCHITECTURE-DETAILED.md`](./ARCHITECTURE-DETAILED.md) ·
[`GOVERNANCE.md`](./GOVERNANCE.md) · [`RUNBOOK-F1.md`](./RUNBOOK-F1.md)
