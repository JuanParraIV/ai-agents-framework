---
name: pipeline-generation
description: >-
  Genera o actualiza pipelines CI/CD (GitHub Actions, GitLab CI, Jenkins) reproducibles con los gates de calidad (F2) y seguridad (F3) cableados como pasos que bloquean. Secretos vía OIDC/Vault, acciones fijadas por SHA, permisos mínimos, deploy a prod tras gate humano. Úsala para "genera el pipeline", "ci/cd", "workflow", "actualiza el pipeline".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
metadata:
  type: skill
  tier: t2
  domain: devops
  owner: qintess-devops
  version: 1.0.0
---

# Skill: Pipeline generation (CI/CD con gates)

Produce el pipeline como código que **hace obligatorios** los gates definidos en fases previas.

## Principio rector

> El pipeline no re-define los gates: los invoca. Reutiliza los comandos ya existentes en el repo (suite BDD, `scripts/smoke_test.py`, `scripts/security_gate.sh`, gitleaks) para que la fuente de verdad sea una sola.

## Etapas y gates (orden estricto)

```
build    -> instalar deps fijadas (lockfile), compilar de forma reproducible
test     -> [GATE F2] behave (BDD verde) · cobertura · smoke test del framework
security -> [GATE F3] sast · sca · secret-scan · container-scan · iac-scan · security_gate.sh
package  -> construir imagen/artefacto + SBOM (CycloneDX)
publish  -> subir a repo inmutable, firmado y versionado (solo si todo lo anterior pasó)
deploy   -> no-prod: automático · PROD: environment protegido con aprobación humana
```

## Reglas de seguridad del pipeline

- **Secretos**: OIDC hacia el cloud / Vault / secret store del CI. Nunca en claro ni en `env:` commiteado.
- **Pinning**: acciones/orbs/imágenes por **SHA/digest**, no por tag móvil.
- **Permisos**: token con `permissions:` mínimos (default read; write solo donde se necesita).
- **Aislamiento**: credenciales de publicación/deploy solo en su etapa, no en build/test.
- **Reproducibilidad**: misma entrada → mismo artefacto; sin `curl | bash` de fuentes móviles.

## Workflow

```
1. Detectar plataforma CI y stack (lockfiles, Dockerfile, IaC)
2. Reutilizar los gates existentes del repo como pasos del pipeline
3. Generar el pipeline con las etapas y gates arriba; prod como environment protegido
4. Lint/validación (actionlint / gitlab-ci lint) y, si se puede, dry-run
5. Abrir PR con el pipeline; nunca push directo a rama protegida
```

## Anti-Patterns (Never Do)

- Nunca marques un gate de test/seguridad como `continue-on-error`.
- Nunca dupliques la lógica de un gate en el pipeline: invoca el script fuente única.
- Nunca concedas `permissions: write-all` por comodidad.
- Nunca automatices el deploy a prod sin un environment con required reviewers.
