---
name: chaos-testing
description: >-
  Diseña y ejecuta experimentos de ingeniería del caos controlados (fallo de instancia, latencia, partición de red, agotamiento de recursos) para validar resiliencia, con hipótesis, blast radius acotado y plan de aborto. Nunca en prod sin autorización. Úsala para "chaos", "chaos engineering", "prueba de resiliencia", "game day".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
metadata:
  type: skill
  tier: t2
  domain: sre
  owner: qintess-sre
  version: 1.0.0
---

# Skill: Chaos testing

Valida que el sistema aguanta el fallo, inyectándolo de forma controlada antes de que ocurra solo.

## Principio rector

> El caos es un experimento científico, no vandalismo: hipótesis, radio de impacto acotado y botón de aborto. En prod, solo con autorización y observabilidad suficiente para ver el efecto.

## Método

- **Hipótesis**: "si falla X, el sistema se degrada así y el SLO se mantiene porque Y".
- **Blast radius**: empezar pequeño (una instancia, un % de tráfico); crecer solo si la hipótesis se sostiene.
- **Steady state**: definir la métrica de normalidad antes; el experimento compara contra ella.
- **Abort**: condición y mecanismo de parada inmediata; nunca sin él.
- **Entorno**: primero no-prod; prod solo con autorización, ventana y observabilidad.

## Experimentos típicos

Fallo de instancia/pod, latencia/errores inyectados en dependencias, partición de red, agotamiento de CPU/memoria/disco, caída de zona.

## Workflow

```
1. Definir hipótesis y steady state (métrica de normalidad)
2. Acotar blast radius y definir la condición/mecanismo de aborto
3. Ejecutar en no-prod; observar vs steady state
4. Prod: solo con autorización registrada, ventana y monitoreo activo
5. Documentar hallazgos -> acciones de resiliencia (runbooks, límites, retries)
```

## Anti-Patterns (Never Do)

- Nunca lances un experimento sin hipótesis ni mecanismo de aborto.
- Nunca corras chaos en prod sin autorización y sin observabilidad para ver el impacto.
- Nunca empieces con un blast radius grande: crece gradualmente.
- Nunca ejecutes sin haber definido el steady state contra el que comparar.
