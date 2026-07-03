---
name: slo-management
description: >-
  Define SLIs (latencia, disponibilidad, error rate, correctness) y SLOs con error budgets y una política clara de consumo del budget. Convierte objetivos de negocio en umbrales medibles. Úsala para "slo", "sli", "error budget", "define objetivos de fiabilidad".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
metadata:
  type: skill
  tier: t2
  domain: sre
  owner: qintess-sre
  version: 1.0.0
---

# Skill: SLO management

Traduce "el servicio debe ser fiable" en SLIs medibles, SLOs con umbral y error budgets con política.

## Principio rector

> Un SLO sin error budget es un deseo. El budget es lo que permite decidir objetivamente entre lanzar features o estabilizar.

## Definición

- **SLI**: métrica del usuario (p.ej. % de requests < 300ms; % de respuestas 2xx/3xx; correctness de transacciones).
- **SLO**: objetivo sobre el SLI en una ventana (p.ej. 99.9% disponibilidad / 28 días).
- **Error budget**: 100% − SLO. Define qué se puede "gastar" en fallos/cambios.
- **Política de budget**: al agotarse → congelar features y priorizar fiabilidad; con budget sano → más velocidad.

## Workflow

```
1. Identificar el customer journey crítico y su SLI (lo que el usuario percibe)
2. Fijar el SLO con negocio (realista, no 100%); definir la ventana
3. Calcular el error budget y su política de consumo
4. Instrumentar el SLI (ver /observability-setup) y crear el burn-rate alert
5. Documentar el SLO como código/versionado; PR contra main
```

## Anti-Patterns (Never Do)

- Nunca fijes SLO al 100%: no deja margen para cambios y es inalcanzable.
- Nunca midas SLIs de infra (CPU) como si fueran de usuario: mide la experiencia.
- Nunca definas un SLO sin política de qué hacer al agotar el budget.
- Nunca cambies el SLO para "cumplir" en vez de arreglar el servicio.
