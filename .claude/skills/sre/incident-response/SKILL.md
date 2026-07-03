---
name: incident-response
description: >-
  Coordina la respuesta a incidentes: detección, severidad, roles (incident commander, comms, ops), triage, mitigación con gate humano, comunicación a stakeholders y cierre con verificación. La mitigación en prod requiere aprobación del incident commander. Úsala para "incidente", "outage", "respuesta a incidente", "mitiga el fallo".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
metadata:
  type: skill
  tier: t2
  domain: sre
  owner: qintess-sre
  version: 1.0.0
---

# Skill: Incident response

Lleva un incidente de la detección a la recuperación de forma ordenada, comunicada y auditable.

## Principio rector

> Primero restaurar el servicio, luego entender la causa (eso es el postmortem). Cada acción en prod se registra y la aprueba el incident commander. Comunicar pronto y seguido reduce el daño.

## Roles y severidad

- **Roles**: Incident Commander (decide), Comms (informa), Ops (ejecuta). Uno no hace los tres.
- **Severidad**: SEV1 (impacto crítico/dinero/datos) … SEV3 (menor). La severidad fija el tempo y a quién se escala.

## Workflow

```
1. Declarar el incidente y su severidad; asignar Incident Commander
2. Triage: alcance, blast radius, servicios/usuarios/dinero afectados (usar telemetría)
3. Mitigar (con aprobación del IC): rollback / feature flag / scaling / failover
4. Comunicar a stakeholders con cadencia según severidad (estado, impacto, ETA)
5. Verificar recuperación (SLO/health) antes de declarar resuelto
6. Abrir SIEMPRE un /postmortem sin culpa con timeline y acciones
```

## Anti-Patterns (Never Do)

- Nunca ejecutes una mitigación de impacto en prod sin aprobación del IC.
- Nunca improvises si existe un runbook para ese fallo: úsalo.
- Nunca declares resuelto sin verificar la recuperación con datos.
- Nunca omitas el postmortem "porque ya se arregló".
