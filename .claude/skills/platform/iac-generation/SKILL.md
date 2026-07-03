---
name: iac-generation
description: >-
  Genera y modifica Infrastructure-as-Code (Terraform/Pulumi) con baseline seguro por defecto (cifrado en reposo/tránsito, least privilege, sin recursos públicos, estado remoto cifrado). Valida con fmt/validate/plan y escaneo tfsec/checkov; el `apply` a prod es gate humano. Úsala para "terraform", "pulumi", "genera la infra", "recursos cloud".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
metadata:
  type: skill
  tier: t2
  domain: platform
  owner: qintess-platform
  version: 1.0.0
---

# Skill: IaC generation (Terraform/Pulumi)

Declara infraestructura reproducible y segura por defecto; propone cambios vía `plan`, nunca `apply` directo a prod.

## Principio rector

> Seguro por defecto y dry-run. El recurso nace cifrado, privado y con least privilege; abrirlo requiere justificación. El `plan` es el gate: se revisa antes de aplicar.

## Baseline obligatorio

- **Cifrado**: en reposo (KMS) y en tránsito (TLS); nunca desactivado.
- **Acceso**: least privilege en IAM/roles; sin `*:*`; sin recursos públicos por defecto.
- **Estado**: backend remoto **cifrado** con locking y control de acceso (nunca estado local commiteado).
- **Secretos**: desde Vault/KMS (data sources), nunca literales en el código ni en variables.
- **Trazabilidad**: tags de propietario, entorno, coste y clasificación de datos.

## Workflow

```
1. terraform fmt + validate  (o pulumi preview)
2. Aplicar el baseline seguro al recurso nuevo/modificado
3. Escaneo:  tfsec .  |  checkov -d .   [gate F3: sin High/Critical]
4. terraform plan -out=plan.tfplan   (revisión humana obligatoria antes de apply)
5. Abrir PR con el plan adjunto; prod -> aprobación humana/CAB
```

## Anti-Patterns (Never Do)

- Nunca ejecutes `apply`/`destroy` a prod sin `plan` revisado y aprobación.
- Nunca dejes el `terraform.tfstate` en el repo ni en un backend sin cifrar.
- Nunca pongas secretos en `variables.tf`/`.tfvars` en claro.
- Nunca silencies un hallazgo de tfsec/checkov sin justificación registrada.
