---
name: implement-from-bdd
description: >-
  Implementa código de producción + step definitions pendientes para hacer pasar los BDD tests definidos por QA, sin tocar los .feature. Respeta el BDD-First Gate. Úsala para "implement story", "implementar historia", "make tests pass", "implement BDD".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, mcp__atlassian__jira_get_issue, mcp__atlassian__jira_update_issue, mcp__atlassian__jira_add_comment, mcp__atlassian__jira_transition_issue
---

# Skill: Implement from BDD

QA define el QUÉ (el contrato `.feature`); tú implementas el CÓMO. El `.feature` es inmutable.

## BDD-First Gate (HARD REQUIREMENT)

Antes de escribir código, verifica TODO:

```
- Existe el .feature de la historia
- Existen los step definitions (aunque sean skeleton)
- El sub-task [BDD] en Jira está "Done"
```

Si algo falla -> STOP. Reporta: "Cannot implement: BDD tests not ready."

## Workflow

```
1. Verificar el BDD-First Gate (STOP si falla)
2. Leer .feature + step skeletons (la especificación) y la historia
3. Detectar patrones del codebase: lenguaje, framework, estructura, convenciones
4. Crear feature branch (feature/PROJ-XXX-desc)
5. Implementar código de producción + step definitions pendientes
6. Ejecutar el suite BDD; iterar hasta que TODOS los escenarios pasen
7. Self-check contra límites de PR (≤15 archivos, ≤500 líneas añadidas)
8. Commit (Conventional Commits + Jira key) y abrir PR (sin mergear)
9. JIRA: [DEV] sub-task -> In Review + comentario con link del PR y nº de escenarios verdes
```

## Code Standards

- Seguir patrones existentes del proyecto; inyección de dependencias.
- Manejo de errores en todas las llamadas externas; sin valores hardcodeados.
- Implementar solo lo que el AC exige (sin over-engineering); diff mínimo y revisable.

## Anti-Patterns (Never Do)

- Nunca modificar los .feature para facilitar la implementación.
- Nunca empezar si el BDD-First Gate falla.
- Nunca saltar manejo de errores para pasar tests más rápido.
- Nunca implementar más allá de lo que el AC especifica.
- Nunca pushear a ramas protegidas (main/develop) ni mergear tu propio PR.
- Nunca commitear secretos o credenciales.
- Si te atascas tras 3 iteraciones, pide guía humana.
