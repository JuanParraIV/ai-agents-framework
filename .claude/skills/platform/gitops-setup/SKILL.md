---
name: gitops-setup
description: >-
  Configura GitOps (ArgoCD/Flux) para que el repositorio sea la única fuente de verdad del estado desplegado: Applications/Kustomizations, sync policies, detección de drift y reconciliación. Prod con sync manual (gate humano). Úsala para "gitops", "argocd", "flux", "reconciliación", "fuente de verdad".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
metadata:
  type: skill
  tier: t2
  domain: platform
  owner: qintess-platform
  version: 1.0.0
---

# Skill: GitOps setup (ArgoCD/Flux)

Hace de Git la fuente de verdad: lo desplegado = lo declarado en el repo, con reconciliación automática y drift visible.

## Principio rector

> Si la consola difiere de Git, Git gana. GitOps convierte "quién cambió qué en prod" en un historial de commits auditable — el sueño del regulador.

## Reglas

- **Fuente única**: el clúster refleja el repo; sin cambios manuales (self-heal revierte el drift).
- **Sync policy**: no-prod puede auto-sync; **prod con sync manual** (aprobación humana) o con ventana.
- **App-of-apps / Kustomize overlays** por entorno; separación clara dev/stg/prod.
- **Drift detection**: alertar cuando el estado real diverge del declarado.
- **Rollback**: revertir el commit → ArgoCD/Flux reconcilia al estado previo.

## Workflow

```
1. Definir Application (ArgoCD) o Kustomization (Flux) apuntando al path/rama del repo
2. Configurar sync policy: auto+self-heal en no-prod; manual/aprobado en prod
3. Estructurar overlays por entorno (kustomize/helm values)
4. Activar drift detection y notificaciones
5. Validar reconciliación en no-prod antes de prod; PR con la config
```

## Anti-Patterns (Never Do)

- Nunca hagas `kubectl apply` manual a prod: rompe la fuente de verdad.
- Nunca actives auto-sync sin self-heal en prod sin gate humano.
- Nunca guardes secretos en claro en el repo GitOps: usa SOPS/ESO/Sealed Secrets.
- Nunca ignores un drift persistente: investiga y reconcilia o corrige el repo.
