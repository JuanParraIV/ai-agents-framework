---
name: release-orchestration
description: >-
  Orquesta una liberación: calcula la versión SemVer desde Conventional Commits, genera changelog/release notes con las JIRA keys, crea el tag firmado y el GitHub release apuntando al artefacto inmutable, y abre el change request (CAB) para producción. Úsala para "release", "libera la versión", "changelog", "tag y publica".
allowed-tools: Read, Write, Edit, Bash
metadata:
  type: skill
  tier: t2
  domain: devops
  owner: qintess-release
  version: 1.0.0
---

# Skill: Release orchestration

Convierte un artefacto aprobado en una liberación versionada, documentada y trazable.

## Principio rector

> La versión es un contrato inmutable. Se deriva de los commits (no se inventa), se firma, y para prod espera la aprobación CAB — no se asume.

## Versionado (SemVer desde Conventional Commits)

```
feat!  / BREAKING CHANGE  -> major
feat                      -> minor
fix / perf / sec          -> patch
docs/chore/test/refactor  -> no cambian versión de prod por sí solos
```

## Workflow

```
1. Precondición: gates F2+F3 verdes y artefacto firmado + SBOM (si no, STOP)
2. Rango de commits desde el último tag:  git describe --tags --abbrev=0 .. HEAD
3. Calcular la nueva versión SemVer según los tipos de commit del rango
4. Generar changelog agrupado (feat/fix/sec) incluyendo las JIRA keys de cada commit
5. Tag firmado:  git tag -s vX.Y.Z -m "release vX.Y.Z (Jira: ...)"
6. GitHub release:  gh release create vX.Y.Z --notes-file CHANGELOG-vX.Y.Z.md  (adjuntar SBOM)
7. Producción -> abrir change request/CAB y ESPERAR aprobación registrada
8. Registrar trazabilidad release ↔ artefacto ↔ commit ↔ JIRA
```

## Anti-Patterns (Never Do)

- Nunca publiques una versión que ya existe (no re-tag, no sobrescribir el release).
- Nunca generes el changelog a mano ignorando los commits: debe reflejar el rango real.
- Nunca crees el release de un artefacto reconstruido fuera del pipeline aprobado.
- Nunca marques el release a prod como hecho sin la aprobación CAB registrada.
