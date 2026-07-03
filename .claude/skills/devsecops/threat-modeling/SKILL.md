---
name: threat-modeling
description: >-
  Modelado de amenazas STRIDE sobre el diseño de un cambio con superficie nueva (endpoint, flujo de datos, integración, límite de confianza). Identifica amenazas, controles existentes/faltantes y riesgo residual, mapeando a los datos sensibles del banco. Úsala para "threat model", "modelado de amenazas", "STRIDE", "analiza el riesgo del diseño".
allowed-tools: Read, Grep, Glob
metadata:
  type: skill
  tier: t2
  domain: devsecops
  owner: qintess-devsecops
  version: 1.0.0
---

# Skill: Threat modeling (STRIDE)

Análisis de amenazas a nivel de **diseño** (no de línea de código) para cambios que introducen superficie nueva.

## Principio rector

> Piensa como atacante sobre los límites de confianza. Un control ausente en un flujo que toca dinero o PAN es un hallazgo, aunque el código "funcione".

## Workflow

```
1. Dibujar el flujo del cambio: actores, entradas, almacenes de datos, límites de confianza
2. Clasificar los datos que cruzan cada límite (PAN, PII, credenciales, dinero)
3. Aplicar STRIDE por elemento/flujo:
     Spoofing        -> ¿authn en cada límite?
     Tampering       -> ¿integridad de datos/mensajes?
     Repudiation     -> ¿audit trail de la operación?
     Info Disclosure -> ¿cifrado, minimización, enmascarado?
     Denial of Svc   -> ¿rate limiting, timeouts, límites?
     Elevation       -> ¿authz least-privilege, sin escalada?
4. Para cada amenaza: control existente / faltante y riesgo residual (Alto/Medio/Bajo)
5. Salida: tabla de amenazas priorizadas + controles recomendados como AC de seguridad
```

## Anti-Patterns (Never Do)

- Nunca asumas que un control existe sin verlo en el código/diseño.
- Nunca ignores el repudio/auditoría en operaciones financieras (requisito SOX).
- Nunca entregues una lista genérica de STRIDE: átala a los flujos y datos reales del cambio.
