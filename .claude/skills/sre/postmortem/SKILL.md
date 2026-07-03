---
name: postmortem
description: >-
  Redacta postmortems sin culpa tras un incidente: timeline factual, impacto, causa raíz (5 whys / contributing factors), qué funcionó y qué no, y acciones correctivas con dueño y fecha. Foco en sistemas y procesos, nunca en personas. Úsala para "postmortem", "análisis post-incidente", "root cause", "lecciones aprendidas".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
metadata:
  type: skill
  tier: t2
  domain: sre
  owner: qintess-sre
  version: 1.0.0
---

# Skill: Postmortem (sin culpa)

Convierte un incidente en aprendizaje organizacional accionable.

## Principio rector

> Sin culpa: las personas actuaron razonablemente con la información que tenían. Si el sistema permitió el fallo, el arreglo es del sistema/proceso. Culpar mata la honestidad y repite el incidente.

## Estructura

- **Resumen**: qué pasó, impacto (usuarios/dinero/datos/tiempo), severidad.
- **Timeline**: factual, con timestamps (detección → mitigación → recuperación).
- **Causa raíz y factores contribuyentes**: 5 whys / análisis; normalmente son varios.
- **Qué funcionó / qué no**: detección, respuesta, runbooks, comunicación.
- **Acciones correctivas**: cada una con **dueño, fecha y ticket**; prevenir la clase de fallo, no solo la instancia.

## Workflow

```
1. Reconstruir el timeline con la telemetría y los canales del incidente
2. Analizar causa raíz y factores contribuyentes (sin señalar personas)
3. Extraer acciones concretas (dueño + fecha + JIRA) que ataquen la causa
4. Revisión del postmortem con el equipo; publicarlo como aprendizaje compartido
5. Seguir las acciones hasta cierre; versionar el documento
```

## Anti-Patterns (Never Do)

- Nunca atribuyas la causa a "error humano" y pares ahí: pregunta por qué el sistema lo permitió.
- Nunca cierres el postmortem sin acciones con dueño y fecha.
- Nunca dejes las acciones sin seguimiento (postmortem que no cambia nada).
- Nunca uses el documento para sancionar: rompe la cultura sin culpa.
