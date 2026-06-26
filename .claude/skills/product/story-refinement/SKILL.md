---
name: story-refinement
description: >-
  Transforma issues crudos de JIRA (bugs, feature requests, epics) en User Stories estructuradas con Acceptance Criteria en Gherkin y sub-tasks [BDD]/[DEV]/[QA]. Úsala para "refinar backlog", "refine issues", "crear historias de usuario", "story refinement".
allowed-tools: Read, Grep, Glob, mcp__atlassian__jira_get_issue, mcp__atlassian__jira_search, mcp__atlassian__jira_create_issue, mcp__atlassian__jira_update_issue, mcp__atlassian__jira_add_comment, mcp__atlassian__jira_create_issue_link
---

# Skill: Story Refinement

Convierte input ambiguo en historias **testables por QA** e **implementables por Dev**, con el Gherkin AC como contrato.

## Workflow

```
1. Leer el/los issue(s) de JIRA (por key o JQL)
2. Analizar: quién (rol), qué, por qué, edge cases, dependencias, riesgos
3. Si el feature es grande (>8 pts), dividir en historias sprint-sized
4. Escribir la User Story (As a / I want / So that) + Gherkin AC (mín. 3 escenarios)
5. Añadir sección "Out of Scope" para evitar scope creep
6. Estimar story points (Fibonacci)
7. Crear la historia en estado AI-draft con labels ai-generated + needs-review
8. Crear sub-tasks [BDD], [DEV], [QA] y enlazar al issue origen
9. Reportar resumen con links
```

## Plantilla de historia

```
As a <rol>
I want <capacidad>
So that <valor de negocio>

Acceptance Criteria (Gherkin):
  Scenario: <happy path>
    Given ... When ... Then ...
  Scenario: <edge case>
  Scenario: <error / validación>

Out of Scope:
  - ...
Story Points: <Fibonacci>
```

## Calidad

- Gherkin sintácticamente válido (parseable por Cucumber).
- Mínimo 3 escenarios: happy path, edge case, error.
- Sin detalles de implementación en el AC (comportamiento, no código).
- Completable en 1 sprint (split si >8 pts).

## Anti-Patterns (Never Do)

- Nunca crear historias sin Gherkin AC.
- Nunca incluir detalles técnicos en el AC ("usa React", "llama a API X").
- Nunca asignar la historia a personas (decisión humana).
- Nunca cerrar/borrar issues existentes; siempre enlazar.
- Nunca crear duplicados (buscar en JIRA primero).
