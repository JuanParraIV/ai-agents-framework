---
name: rollback
description: >-
  Diseña y ejecuta un rollback probado y trazable ante el fallo de un release: redeploy de la versión previa inmutable, reversibilidad de migraciones de datos, feature flags, evaluación del blast radius y registro de evidencia. En producción requiere aprobación humana. Úsala para "rollback", "revertir el release", "vuelve a la versión anterior".
allowed-tools: Read, Write, Edit, Bash
metadata:
  type: skill
  tier: t2
  domain: devops
  owner: qintess-release
  version: 1.0.0
---

# Skill: Rollback

Devuelve el sistema a un estado bueno conocido, de forma segura y auditable.

## Principio rector

> El rollback se prueba ANTES de necesitarlo. Un rollback no probado es un incidente en potencia. Prefiere revertir a un estado inmutable previo antes que parchear en caliente.

## Estrategia

- **Artefacto**: redeploy de la **versión previa inmutable** (misma que ya pasó gates); nunca re-build de emergencia.
- **Datos**: solo migraciones **reversibles** (expand/contract); si una migración es destructiva, el rollback es forward-fix, no revert — decláralo.
- **Feature flags**: si el cambio está detrás de un flag, apagar el flag es el rollback más rápido y seguro.
- **Blast radius**: evaluar alcance (usuarios, dinero, datos) antes de actuar; despliegue progresivo facilita el corte.

## Workflow

```
1. Detectar el fallo (SLO/health/errores) y decidir: rollback vs forward-fix
2. PROD -> obtener aprobación humana y registrar motivo + impacto (no autónomo)
3. Ejecutar: apagar flag / redeploy de la versión previa / revertir migración reversible
4. Verificar salud post-rollback (health checks, SLO, smoke)
5. Registrar evidencia (qué, cuándo, quién aprobó, resultado) y abrir postmortem sin culpa
```

## Anti-Patterns (Never Do)

- Nunca hagas rollback en prod sin aprobación y sin registrar motivo/impacto.
- Nunca reviertas una migración destructiva sin plan de datos (pérdida irreversible).
- Nunca "arregles en caliente" en el servidor saltándote el pipeline y los gates.
- Nunca cierres el incidente sin verificar salud y sin postmortem.
