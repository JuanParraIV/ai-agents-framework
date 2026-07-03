---
name: runbook-generation
description: >-
  Genera runbooks operativos por servicio: síntomas, diagnóstico paso a paso, acciones de mitigación (con su gate), enlaces a dashboards/alertas y criterios de escalado. Ejecutables bajo presión, sin ambigüedad. Úsala para "runbook", "procedimiento operativo", "playbook", "cómo mitigar X".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
metadata:
  type: skill
  tier: t2
  domain: sre
  owner: qintess-sre
  version: 1.0.0
---

# Skill: Runbook generation

Convierte el conocimiento operativo en procedimientos que cualquiera de guardia puede seguir a las 3am.

## Principio rector

> Un runbook se escribe para alguien cansado y bajo presión: pasos concretos, comandos exactos, decisiones claras. Si requiere adivinar, no es un runbook.

## Estructura del runbook

- **Síntoma / alerta que lo dispara** (enlazado desde la alerta).
- **Impacto** y severidad esperada.
- **Diagnóstico**: pasos numerados con qué mirar (dashboard/log/trace) y qué significa.
- **Mitigación**: acciones concretas; marcar cuáles requieren **aprobación** (prod).
- **Escalado**: cuándo y a quién; criterios objetivos.
- **Verificación**: cómo confirmar la recuperación (SLO/health).
- **Enlaces**: dashboard, alerta, arquitectura, postmortems previos.

## Workflow

```
1. Partir de un modo de fallo conocido (o de un postmortem)
2. Escribir diagnóstico y mitigación con comandos exactos y sus gates
3. Enlazar desde la alerta correspondiente (/observability-setup)
4. Validar el runbook en un ejercicio/entorno no-prod
5. Versionar como código; PR contra main; revisar tras cada incidente
```

## Anti-Patterns (Never Do)

- Nunca escribas pasos ambiguos ("revisa si algo va mal"): sé específico.
- Nunca incluyas comandos destructivos sin marcar su gate de aprobación.
- Nunca dejes un runbook sin criterio de verificación de recuperación.
- Nunca dejes que se desactualice: revísalo tras cada incidente que lo use.
