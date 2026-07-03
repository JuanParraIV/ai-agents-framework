---
name: k8s-manifest
description: >-
  Genera manifiestos de Kubernetes endurecidos: requests/limits, liveness/readiness probes, securityContext (non-root, readOnlyRootFilesystem, drop capabilities), NetworkPolicies, y sin secretos en claro. Valida con kubeconform/kubectl --dry-run. Úsala para "manifiestos k8s", "deployment", "kubernetes yaml", "hardening de pods".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
metadata:
  type: skill
  tier: t2
  domain: platform
  owner: qintess-platform
  version: 1.0.0
---

# Skill: K8s manifest (endurecido)

Genera manifiestos production-ready con seguridad y fiabilidad por defecto.

## Principio rector

> Un pod sin límites, sin probes y corriendo como root es un incidente latente. El manifiesto nace endurecido; relajar un control exige justificación.

## Checklist obligatorio

- **Recursos**: `requests` y `limits` de CPU/memoria (evita noisy-neighbor y OOM sorpresa).
- **Salud**: `livenessProbe` + `readinessProbe` (y `startupProbe` si arranca lento).
- **securityContext**: `runAsNonRoot`, `readOnlyRootFilesystem`, `allowPrivilegeEscalation: false`, `drop: [ALL]` capabilities.
- **Red**: `NetworkPolicy` por defecto deny; abrir solo lo necesario.
- **Secretos**: referencias a `Secret`/ESO, nunca valores en el manifiesto ni en `env` en claro.
- **Disponibilidad**: `PodDisruptionBudget`, `topologySpreadConstraints`/anti-affinity para réplicas.
- **Imagen**: por **digest**, `imagePullPolicy` coherente; no `latest`.

## Workflow

```
1. Generar el manifiesto con el checklist aplicado
2. Validar:  kubeconform -strict  |  kubectl apply --dry-run=server
3. (Opcional) checkov --framework kubernetes  [gate F3]
4. Encauzar por GitOps (no kubectl apply directo a prod); PR con el diff
```

## Anti-Patterns (Never Do)

- Nunca despliegues sin requests/limits ni sin probes.
- Nunca corras como root ni con `privileged: true` salvo necesidad justificada.
- Nunca pongas secretos en `env`/ConfigMap en claro.
- Nunca uses `kubectl apply` directo a prod: pasa por GitOps.
