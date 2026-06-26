---
name: coverage-gap-analysis
description: >-
  Ejecuta cobertura sobre el código (o el diff), identifica ramas/paths sin cubrir y genera tests dirigidos a esos gaps. Úsala para "coverage gap", "análisis de cobertura", "qué falta por testear", "uncovered paths".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Skill: Coverage Gap Analysis

Encuentra qué NO está cubierto y cierra los gaps con tests dirigidos. Calidad sobre vanity metrics: prioriza ramas críticas (auth, dinero, validación) por encima del porcentaje.

## Workflow

```
1. Detectar la herramienta de coverage del proyecto
2. Ejecutar la suite con cobertura (line + branch)
3. Parsear el reporte; listar archivos/funciones/ramas sin cubrir
4. Priorizar gaps por criticidad de negocio (no solo por % faltante)
5. Generar tests dirigidos a las ramas/paths descubiertos
6. Re-ejecutar; reportar coverage antes→después y gaps residuales (con motivo)
```

## Herramientas de coverage

| Lenguaje | Comando |
|----------|---------|
| Python | `pytest --cov --cov-branch --cov-report=term-missing` |
| JS/TS | `jest --coverage` / `vitest run --coverage` / `c8` |
| Java | JaCoCo (`mvn test jacoco:report`) |
| Go | `go test -coverprofile=cover.out -covermode=count ./...` |
| .NET | `coverlet` / `dotnet test --collect:"XPlat Code Coverage"` |

## Calidad

- Target por defecto 80% line **y** branch sobre el código objetivo.
- Priorizar ramas de seguridad y financieras antes que getters/setters.
- Si un path no se puede cubrir sin tests triviales, dejarlo sin cubrir y explicar por qué.

## Anti-Patterns (Never Do)

- Nunca perseguir 100% con tests triviales o tautológicos.
- Nunca añadir snapshots masivos para inflar el número.
- Nunca modificar el source para "facilitar" la cobertura.
- Nunca reportar cobertura sin haber ejecutado la suite.
