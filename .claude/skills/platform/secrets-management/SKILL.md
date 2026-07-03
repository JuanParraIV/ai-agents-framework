---
name: secrets-management
description: >-
  Gestiona secretos con Vault / External Secrets Operator / KMS: inyección por referencia (nunca en claro), rotación, least privilege de acceso, y cifrado en tránsito y reposo. La rotación y el acceso a secretos son acciones con gate humano/auditoría. Úsala para "gestiona secretos", "vault", "external secrets", "rota credenciales", "kms".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
metadata:
  type: skill
  tier: t2
  domain: platform
  owner: qintess-platform
  version: 1.0.0
---

# Skill: Secrets management (Vault/ESO/KMS)

Los secretos viven en un gestor dedicado; el resto del sistema los referencia, nunca los contiene.

## Principio rector

> Un secreto en el repo, el manifiesto o el estado de Terraform es un secreto comprometido. Se inyecta por referencia desde Vault/ESO en runtime, con acceso mínimo y rotación.

## Reglas

- **Nunca en claro**: ni en código, IaC, manifiestos, ConfigMaps, `.tfstate`, logs o el contexto.
- **Referencia, no valor**: ESO/Vault Agent inyecta en runtime; el repo solo guarda la **referencia**.
- **Least privilege**: cada workload accede solo a sus secretos (políticas Vault/roles por app).
- **Rotación**: periódica y ante sospecha; rotación/acceso quedan **auditados** (gate humano — GOVERNANCE §2).
- **Cifrado**: en tránsito (TLS) y reposo; para GitOps usar SOPS/Sealed Secrets si el secreto debe versionarse cifrado.
- **PCI-DSS**: CVV nunca se almacena; PAN cifrado/tokenizado.

## Workflow

```
1. Modelar el secreto en Vault/KMS con su política de acceso mínima
2. Configurar la inyección: ESO (ExternalSecret) o Vault Agent/CSI; el manifiesto solo referencia
3. Definir la rotación (TTL/lease) y el proceso de rotación auditado
4. Verificar que no hay secretos en claro en el diff (secret-scan)  [gate F3]
5. Acceso/rotación en prod -> aprobación humana registrada
```

## Anti-Patterns (Never Do)

- Nunca commitees un secreto, ni "de prueba", ni cifrado débilmente.
- Nunca des acceso amplio a todo el árbol de secretos; políticas por app.
- Nunca dejes secretos en variables de entorno logueables o en el `.tfstate`.
- Nunca rotes/accedas a secretos de prod sin aprobación y sin dejar traza.
