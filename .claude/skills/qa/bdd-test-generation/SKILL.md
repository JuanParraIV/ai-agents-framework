---
name: bdd-test-generation
description: >-
  Genera feature files (.feature) ejecutables y step definitions skeleton (pending) a partir de User Stories de JIRA con Gherkin AC. El .feature es el contrato inmutable QA↔Dev. Úsala para "generate BDD tests", "crear tests BDD", "generar features", "BDD from story".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, mcp__atlassian__jira_get_issue, mcp__atlassian__jira_add_comment, mcp__atlassian__jira_transition_issue
---

# Skill: BDD Test Generation

Convierte el Gherkin AC de una historia en `.feature` ejecutables + step definitions **skeleton**. Las steps quedan `pending` para que Dev las implemente. No escribes aserciones reales.

## Workflow

```
1. Leer la User Story de JIRA (debe tener Gherkin AC)
2. Validar sintaxis Gherkin y mapeo AC↔escenario (1:1)
3. Detectar framework BDD (behave / pytest-bdd / Cucumber-JVM / Cucumber.js)
4. Generar .feature con tag de la JIRA key (@PROJ-123)
5. Generar step skeletons con marcador pending (NotImplementedError / PendingException / 'pending')
6. Dry-run: 0 undefined, 0 ambiguous, 0 parse errors
7. Commit a feature branch + PR para que Dev implemente
8. JIRA: [BDD] sub-task -> Done + comentario con ubicación de archivos
```

## Frameworks y dry-run

| Lenguaje | Framework | Feature dir | Steps dir | Dry-run |
|----------|-----------|-------------|-----------|---------|
| Python | behave | `features/` | `features/steps/` | `behave --dry-run --no-summary` |
| Python | pytest-bdd | `tests/features/` | `tests/step_defs/` | `pytest --collect-only -q` |
| Java | Cucumber-JVM | `src/test/resources/features/` | `src/test/java/.../steps/` | `mvn test -Dcucumber.execution.dry-run=true` |
| JS/TS | Cucumber.js | `features/` | `features/step_definitions/` | `npx cucumber-js --dry-run` |

## Calidad

- 1 Feature por historia, tag con JIRA key; 1:1 escenario↔AC.
- Gherkin declarativo (el *qué*, no el *cómo*): sin selectores, URLs, SQL ni sleeps.
- `Scenario Outline` + `Examples` para variaciones; `Background` para setup compartido.
- Cubrir happy path + casos negativos del AC; si la historia solo trae happy path, marcar el gap en JIRA.

## Anti-Patterns (Never Do)

- Nunca implementar lógica/aserciones reales (solo skeleton pending).
- Nunca meter mecánica de UI en Gherkin (clicks, selectores, waits).
- Nunca inventar escenarios/datos no derivados del AC.
- Nunca generar tests si la historia no tiene Gherkin AC -> "Story needs refinement".
- Nunca commitear con dry-run en rojo o steps undefined/ambiguous.
- Nunca modificar el .feature una vez Dev arranca (contrato inmutable).
