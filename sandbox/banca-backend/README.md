# Backend de prueba - API Banca Digital (andamiaje BDD)

Este directorio contiene **solo el andamiaje de tests BDD** (Cucumber.js + TypeScript)
generado por el agente QA BDD a partir de las historias del proyecto JIRA `SCRUM`.

> Los archivos `.feature` son el **contrato inmutable** (Acceptance Criteria en Gherkin).
> Los step definitions son **skeletons**: cada step existe y reporta `pending`.
> La logica de negocio y el codigo de produccion (rutas, handlers, persistencia)
> los implementa el agente **Dev** en la fase `[DEV]`.

## Estructura

```
sandbox/banca-backend/
├── package.json                 scripts de test BDD + devDependencies del harness
├── tsconfig.json
├── cucumber.js                  config de Cucumber.js (ts-node)
└── features/
    ├── *.feature                un feature por historia (@SCRUM-XX)
    ├── support/
    │   └── world.ts             World compartido (estado request/response, sin logica)
    └── step_definitions/
        ├── common.steps.ts      steps genericos reutilizados (auth, status HTTP)
        └── *.steps.ts           steps de dominio por historia
```

## Trazabilidad historia -> feature

| Historia | Feature | Sub-task BDD |
|----------|---------|--------------|
| SCRUM-6  | `authentication.feature`  | SCRUM-13 |
| SCRUM-7  | `user-registration.feature` | SCRUM-15 |
| SCRUM-8  | `account-balance.feature` | SCRUM-17 |
| SCRUM-9  | `account-transactions.feature` | SCRUM-19 |
| SCRUM-10 | `transfers.feature` | SCRUM-21 |
| SCRUM-11 | `user-profile.feature` | SCRUM-23 |
| SCRUM-12 | `health-observability.feature` | SCRUM-25 |

## Como correr los tests BDD

```bash
cd sandbox/banca-backend
npm install
npm run test:bdd        # ejecuta los escenarios (todos pending hasta [DEV])
npm run test:bdd:dry    # dry-run: verifica que 0 steps quedan undefined/ambiguous
```

Mientras los steps sean skeletons, la corrida reporta los escenarios como **pending**
(no como passed). Es el estado esperado: el contrato esta definido, la implementacion
la aporta Dev.

## Datos de prueba

Todos los datos (emails, cuentas `ACC-xxx`, importes) son **ficticios**. Nunca se usan
credenciales, PAN o CVV reales; cualquier PAN se enmascara (`****`).
