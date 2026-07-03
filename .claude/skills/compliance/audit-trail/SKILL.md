---
name: audit-trail
description: >-
  Verifica el audit trail del framework (audit/*.jsonl emitido por el hook PostToolUse): completitud (toda acción significativa registrada), integridad del esquema, redacción de inputs y ausencia de secretos/PAN, y retención. Solo lectura. Úsala para "verifica el audit trail", "revisa la traza", "auditoría de acciones", "completitud del log".
allowed-tools: Read, Grep, Glob, Bash
metadata:
  type: skill
  tier: t2
  domain: compliance
  owner: qintess-compliance
  version: 1.0.0
---

# Skill: Audit trail verification

Verifica que el registro inmutable de acciones (GOVERNANCE §3) es completo, íntegro y no filtra datos.

## Principio rector

> Un control sin traza es un control no auditable. La verificación es de solo lectura: se comprueba, no se completa (rellenar un hueco a mano sería fraude de auditoría).

## Qué verificar (sobre audit/*.jsonl y el histórico)

- **Completitud**: cada acción significativa (commit, PR, deploy, transición JIRA, cambio de infra) tiene su registro.
- **Esquema**: campos obligatorios presentes (timestamp, operator, action, target, result, jira); `inputs_redacted: true`.
- **Redacción / no filtración**: ningún registro contiene secretos, PAN/CVV ni PII (patrones + Luhn).
- **Gates**: acciones con gate (§2) llevan `approver` y `gate` poblados.
- **Retención**: la política (≥1 año SOX/PCI) se cumple para el periodo auditado.

## Workflow

```
1. Localizar los registros del periodo:  ls audit/*.jsonl
2. Validar esquema y campos obligatorios (jq/grep); contar acciones por tipo
3. Cruzar con el histórico git/PRs: ¿hay acciones significativas sin registro? -> gap
4. Escanear los registros por secretos/PAN/PII -> cualquier hallazgo es CRÍTICO
5. Reportar completitud, integridad, gaps y hallazgos. NO modificar el trail
```

## Anti-Patterns (Never Do)

- Nunca edites/añadas registros al trail: solo lectura (integridad de auditoría).
- Nunca asumas completitud sin cruzar contra el histórico real (git/PRs/deploys).
- Nunca ignores un secreto/PAN en un registro: es un hallazgo crítico, no una nota.
