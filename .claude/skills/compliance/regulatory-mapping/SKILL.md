---
name: regulatory-mapping
description: >-
  Mapea los controles del sistema/framework a los requisitos regulatorios (PCI-DSS, SOX, GDPR, DORA, ISO 27001) produciendo una matriz control↔requisito con estado (cubierto/parcial/gap) y la evidencia que lo respalda. Solo lectura. Úsala para "mapeo regulatorio", "cumple PCI/SOX/GDPR", "matriz de controles", "gap de cumplimiento".
allowed-tools: Read, Grep, Glob, Bash
metadata:
  type: skill
  tier: t2
  domain: compliance
  owner: qintess-compliance
  version: 1.0.0
---

# Skill: Regulatory mapping

Traduce la regulación en una matriz verificable de controles y su evidencia.

## Principio rector

> "Cumplimos PCI" no es una afirmación auditable; "el requisito 3.2 se cumple con estos controles y esta evidencia" sí lo es. Cada requisito se ata a un control concreto y su prueba.

## Marco de mapeo

| Regulación | Foco | Controles del framework a evidenciar |
|-----------|------|--------------------------------------|
| **PCI-DSS** | Datos de tarjeta | secret-scan, enmascarado de PAN, CVV no almacenado, cifrado, SBOM, RBAC |
| **SOX** | Integridad financiera | SoD (no self-approve), audit trail, change mgmt, branch protection |
| **GDPR** | Datos personales | minimización, anonimización en no-prod, retención, residencia |
| **DORA** | Resiliencia operativa | SLOs, error budgets, rollback, runbooks, postmortems, gestión de terceros |
| **ISO 27001** | Seguridad de la info | RBAC, least privilege, gestión de secretos, trazabilidad |

## Workflow

```
1. Seleccionar la regulación y los requisitos en alcance
2. Para cada requisito, localizar el/los control(es) del framework que lo cubren
3. Verificar la evidencia del control (hooks, gates CI, audit trail, docs, PRs)
4. Estado por requisito: cubierto / parcial / gap (con la evidencia o su ausencia)
5. Reportar la matriz y priorizar los gaps por riesgo. NO remediar (derivar al dueño)
```

## Anti-Patterns (Never Do)

- Nunca marques un requisito como cubierto sin señalar la evidencia concreta.
- Nunca mapees de forma genérica: ata cada requisito a un control real y su prueba.
- Nunca ocultes un gap para "quedar bien": el gap no reportado es el que sanciona el regulador.
