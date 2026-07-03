# audit/ — Audit trail (TB-3)

Registros **append-only** que emite el hook `PostToolUse` (`.claude/hooks/audit_log.py`)
por cada acción significativa de un agente. Implementa `GOVERNANCE.md §3` y el guardrail
"todo auditable" de `CLAUDE.md`.

- Formato: **JSON Lines**, un archivo por día → `audit/YYYY-MM-DD.jsonl`.
- Los `.jsonl` **no se versionan** (`.gitignore`): son traza local. En un banco real
  estos eventos se envían a un **almacén inmutable** (WORM/SIEM) con retención
  **≥ 1 año** (SOX/PCI). Este directorio es el punto de emisión, no el de retención.

## Qué se registra (acción significativa)

- Escritura de archivos: `Edit`, `Write`, `MultiEdit`, `NotebookEdit`.
- Bash mutante: `git commit/push/checkout -b/tag`, `gh pr create/merge`, `docker build`,
  `terraform apply/plan`, `kubectl apply`, `helm install/upgrade`.
- MCP de **escritura**: `jira_create/update/transition/add_comment`, GitHub create/merge/push…
- **No** se registran lecturas (`Read`, `Grep`, `Glob`, git status/diff/log, MCP `get_/search/list`).

## Esquema del registro

```json
{
  "timestamp": "2026-07-02T14:03:11+00:00",
  "operator": "juan@banco.example",     // AUDIT_OPERATOR o git user.email
  "agent": null,                         // AUDIT_AGENT si la orquestación lo fija
  "skill": null,                         // AUDIT_SKILL idem
  "action": "open_pull_request",
  "target": "org/repo#PR-482",           // redactado (**** ante posibles secretos)
  "jira": "SCRUM-5",                     // inferido de input o de la rama
  "inputs_redacted": true,               // nunca se almacena el input crudo
  "result": "success",                   // success | error | unknown
  "approver": null,                      // se completa en acciones con gate humano
  "gate": null,
  "tool": "Bash"
}
```

`operator/agent/skill` se enriquecen vía variables de entorno cuando la orquestación las
conoce; si no, quedan `null` (no se inventan — auditoría honesta).

## Nota

El hook es **fail-open**: nunca bloquea el flujo. Si no puede escribir, avisa por stderr y
continúa. El bloqueo es responsabilidad de los hooks `PreToolUse` (ver `docs/CI-AND-HOOKS.md`).
