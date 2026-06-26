---
name: test-generation
description: >-
  Analiza un archivo/módulo y genera un suite de tests REALES y ejecutables (unit/integration) para el framework detectado, los corre y reporta. Úsala para "genera tests", "generate tests", "crea unit tests", "test this file".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Skill: Test Generation

Genera tests reales con aserciones (a diferencia de los skeletons BDD), los ejecuta y reporta. Nunca modifica el código fuente.

## Workflow

```
1. Detectar lenguaje, test runner y convenciones (naming, dirs) desde manifests
2. Analizar el target: API pública, ramas, edge cases, error paths, dependencias
3. Elegir el nivel más bajo posible (unit > integration)
4. Generar tests AAA (Arrange-Act-Assert), un comportamiento por test, deterministas
5. Mockear dependencias externas (DB, HTTP, FS, time, random); construir fixtures/factories
6. Ejecutar el suite; si un test falla: corregir el test si está mal, o REPORTAR probable bug de source
7. Reportar: tests añadidos, pass/fail, y áreas sin cubrir
```

## Frameworks

| Lenguaje | Unit/Integration | Mocking |
|----------|------------------|---------|
| Python | pytest, unittest | pytest-mock, unittest.mock |
| JS/TS | Jest, Vitest, Mocha | jest.mock, sinon |
| Java | JUnit 5 | Mockito |
| Go | testing + testify | gomock |
| C#/.NET | xUnit, NUnit | Moq |
| Rust | `#[test]` | mockall |

Respeta el naming existente (`test_*.py` vs `*_test.py`, `*.spec.ts` vs `*.test.ts`) y la estructura de directorios.

## Calidad

- Cada test con al menos una aserción significativa; sin tautologías.
- Determinista: sin red real, sin sleeps, sin estado global mutable, sin dependencia de orden.
- Cubrir happy path + boundaries + error/exception paths; parametrizar en vez de copiar.
- Ejecutar antes de reportar; nunca declarar verde sin output de ejecución.

## Anti-Patterns (Never Do)

- Nunca modificar el código fuente para que pase un test.
- Nunca tests sin aserción o que no puedan fallar.
- Nunca red/DB/tiempo/random reales en unit tests.
- Nunca over-mock (que el test solo verifique los mocks).
- Nunca snapshot-everything ni tests triviales para inflar cobertura.
- Nunca borrar tests existentes para poner el suite en verde.
