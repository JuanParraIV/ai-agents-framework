---
name: iac-security-scan
description: >-
  Escaneo de seguridad de Infrastructure-as-Code (Terraform, CloudFormation, K8s, Helm) con tfsec/checkov: buckets públicos, security groups 0.0.0.0/0, cifrado en reposo desactivado, IAM excesivo, secretos en variables. Falla cerrado ante High/Critical. Úsala para "iac scan", "tfsec", "checkov", "revisa la infra".
allowed-tools: Read, Grep, Glob, Bash
metadata:
  type: skill
  tier: t2
  domain: devsecops
  owner: qintess-devsecops
  version: 1.0.0
---

# Skill: IaC security scan (tfsec/checkov)

Escanea los archivos de IaC tocados por el diff antes de cualquier `plan`/`apply`.

## Principio rector

> Fail-closed: exposición pública de datos o desactivación de cifrado → BLOCK. La infra insegura se corrige en el código IaC, nunca a mano en la consola cloud (drift).

## Workflow

```
1. Detectar IaC en el diff: *.tf, *.yaml (k8s/helm), templates CFN
2. Escanear:
     - Terraform: tfsec .   |   checkov -d .
     - K8s/Helm:  checkov -d . --framework kubernetes,helm
3. Priorizar por severidad y exposición (público > interno)
4. Fix concreto en el recurso IaC (cifrado, políticas, CIDRs, IAM mínimo)
5. Veredicto BLOCK/COMMENT/PASS. Recordar: apply a prod requiere gate humano (GOVERNANCE §2)
```

## Checklist clave (banking)

- Almacenamiento público (S3/GCS/Blob), cifrado en reposo/tránsito desactivado.
- Security groups / NSG con `0.0.0.0/0` en puertos sensibles; ausencia de segmentación.
- IAM con `*:*` o roles demasiado amplios; falta de least privilege.
- Secretos en variables de IaC en claro (deben venir de Vault/KMS).
- Logging/audit de recursos desactivado; sin tags de clasificación de datos.

## Anti-Patterns (Never Do)

- Nunca sugieras `apply` directo a prod: primero `plan`, luego gate humano.
- Nunca silencies una regla (`#tfsec:ignore`, `checkov:skip`) sin justificación registrada.
- Nunca marques PASS si no había escáner disponible: dilo.
