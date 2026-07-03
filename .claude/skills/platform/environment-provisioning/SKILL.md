---
name: environment-provisioning
description: >-
  Provisiona entornos reproducibles y efímeros (dev/stg/prod, preview per-PR) por código, con paridad entre entornos, aislamiento de datos y teardown automático de los efímeros para controlar coste. Úsala para "provisiona un entorno", "entorno efímero", "preview environment", "levanta staging".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
metadata:
  type: skill
  tier: t2
  domain: platform
  owner: qintess-platform
  version: 1.0.0
---

# Skill: Environment provisioning

Crea entornos reproducibles por código, con paridad y ciclo de vida controlado.

## Principio rector

> Un entorno se levanta y se destruye con un comando, desde código. Los efímeros mueren solos (coste); los datos de prod nunca se copian a no-prod sin anonimizar (GDPR).

## Reglas

- **Reproducibilidad**: mismo IaC/overlay → mismo entorno; nada manual.
- **Paridad**: dev/stg/prod difieren solo en escala y datos, no en topología.
- **Efímeros**: preview por PR con `teardown` automático (TTL) para no acumular coste.
- **Aislamiento de datos**: no-prod usa datos sintéticos o **anonimizados**; nunca PAN/PII real (PCI/GDPR).
- **Baseline**: cada entorno hereda el baseline seguro de `iac-generation` y las policies GitOps.

## Workflow

```
1. Definir el entorno como overlay/módulo parametrizado (nombre, escala, datos)
2. Provisionar vía IaC:  plan -> (aprobación si prod) -> apply en no-prod
3. Sembrar datos sintéticos/anonimizados; nunca copiar prod sin anonimizar
4. Efímeros: registrar TTL y teardown automático
5. Registrar el entorno (owner, coste, expiración) para trazabilidad
```

## Anti-Patterns (Never Do)

- Nunca copies datos de producción a no-prod sin anonimizar (GDPR/PCI).
- Nunca dejes entornos efímeros sin teardown (fuga de coste y superficie).
- Nunca hagas que stg y prod diverjan en topología (bugs que solo aparecen en prod).
- Nunca provisiones prod sin `plan` revisado y aprobación humana.
