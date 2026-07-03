---
name: capacity-planning
description: >-
  Analiza tendencias de uso (tráfico, CPU/memoria, storage, conexiones) para dimensionar recursos con margen, anticipar límites y planificar escalado antes de que el SLO sufra. Considera picos estacionales y de negocio. Úsala para "capacity planning", "dimensionamiento", "escalado", "proyección de recursos".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
metadata:
  type: skill
  tier: t2
  domain: sre
  owner: qintess-sre
  version: 1.0.0
---

# Skill: Capacity planning

Asegura que hay capacidad para el crecimiento y los picos, antes de que el usuario lo note.

## Principio rector

> La capacidad se planifica con datos de tendencia, no cuando ya está saturado. Dimensiona para el pico esperado + margen, no para el promedio.

## Qué analizar

- **Tendencias**: tráfico, latencia, CPU/memoria, storage, conexiones a BD/pools — con horizonte (semanas/meses).
- **Picos**: estacionales (fin de mes, nómina, campañas) y de negocio; dimensionar para el peor caso realista.
- **Límites**: cuotas cloud, límites de conexiones, throughput de dependencias; identificar el cuello de botella.
- **Headroom**: margen objetivo (p.ej. 30–40%) antes de escalar; ligar el disparo al SLO/error budget.

## Workflow

```
1. Extraer series temporales de uso y su tendencia (telemetría)
2. Proyectar demanda futura incluyendo picos conocidos
3. Identificar el recurso que satura primero (cuello de botella)
4. Recomendar escalado (horizontal/vertical/autoscaling) con umbrales
5. Documentar el plan; los cambios de infra van por /iac-generation + PR
```

## Anti-Patterns (Never Do)

- Nunca dimensiones para el promedio: los incidentes ocurren en el pico.
- Nunca ignores los límites de las dependencias (el cuello puede no ser tuyo).
- Nunca escales a ciegas sin identificar el recurso que realmente satura.
- Nunca dejes el autoscaling sin límite superior (sorpresa de coste).
