---
name: helm-chart
description: >-
  Crea y parametriza charts de Helm versionados, con values seguros por defecto, plantillas que heredan el hardening de K8s, y validación (helm lint / template / kubeconform). Úsala para "helm chart", "empaqueta en helm", "values.yaml", "parametriza el deploy".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
metadata:
  type: skill
  tier: t2
  domain: platform
  owner: qintess-platform
  version: 1.0.0
---

# Skill: Helm chart

Empaqueta el despliegue como chart reutilizable, versionado y seguro por defecto.

## Principio rector

> Los `values` por defecto deben ser los seguros; el que quiera relajar seguridad lo hace explícito. El chart se versiona (SemVer) igual que el código.

## Estructura y reglas

- `Chart.yaml` con **versión** (chart) y **appVersion** claras; SemVer.
- `values.yaml` con defaults seguros: recursos, probes, `securityContext`, réplicas ≥2, imagen por digest.
- Plantillas que heredan el hardening de `k8s-manifest` (no reinventar el checklist).
- Sin secretos en `values`; usar referencias a `Secret`/ESO. Parametrizar por entorno con `values-<env>.yaml`.
- Documentar cada value en `README`/`values.schema.json`.

## Workflow

```
1. helm create / editar plantillas heredando el hardening K8s
2. helm lint
3. helm template . -f values-<env>.yaml | kubeconform -strict
4. Versionar el chart (bump SemVer); publicar en el repo de charts (OCI/immutable)
5. Encauzar por GitOps; PR con el diff renderizado
```

## Anti-Patterns (Never Do)

- Nunca dejes defaults inseguros (root, sin límites, réplica única) en `values.yaml`.
- Nunca metas secretos en `values`; usa `Secret`/ESO.
- Nunca republiques la misma versión del chart (inmutabilidad).
- Nunca uses `latest` para la imagen del chart de prod.
