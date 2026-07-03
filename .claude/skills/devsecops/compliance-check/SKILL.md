---
name: compliance-check
description: >-
  Verifica que un cambio cumple los controles regulatorios del banco (PCI-DSS, SOX, GDPR, DORA) mapeando el diff a requisitos concretos y señalando evidencia faltante. No sustituye a un auditor; prepara el terreno y falla cerrado ante violaciones claras. Úsala para "compliance check", "cumple PCI", "revisa cumplimiento", "mapea a SOX/GDPR".
allowed-tools: Read, Grep, Glob
metadata:
  type: skill
  tier: t2
  domain: devsecops
  owner: qintess-devsecops
  version: 1.0.0
---

# Skill: Compliance check (PCI-DSS / SOX / GDPR / DORA)

Mapea el cambio a los controles regulatorios y detecta violaciones o evidencia ausente.

## Principio rector

> Fail-closed: si el cambio toca datos de tarjeta/PII o un control financiero y no puedes evidenciar el cumplimiento, márcalo y escala a Compliance.

## Workflow

```
1. Clasificar el cambio: ¿toca PAN/CVV, PII, dinero, controles de acceso, cambios en prod?
2. Mapear a requisitos aplicables (ver tabla)
3. Verificar la evidencia esperada en el diff (enmascarado, cifrado, audit trail, SoD)
4. Reportar: control -> estado (cumple / falta evidencia / viola) -> acción
```

## Mapa de controles

| Área del cambio | Regulación | Qué exigir en el diff |
|-----------------|-----------|------------------------|
| Datos de tarjeta | PCI-DSS Req 3/6 | PAN enmascarado/tokenizado, CVV nunca almacenado, cifrado, sin PAN en logs |
| Autorización / cambios | SOX | SoD (no self-approve), audit trail de la operación, change ref (JIRA) |
| Datos personales | GDPR | minimización, base legal, retención, residencia, derecho de borrado |
| Resiliencia / prod | DORA | rollback, monitoreo, gestión de incidentes, dependencias de terceros |
| Secretos / acceso | ISO 27001 | Vault, least privilege, rotación, sin credenciales en claro |

## Anti-Patterns (Never Do)

- Nunca declares "cumple" sin la evidencia concreta en el cambio: cita el archivo/control.
- Nunca trates el cumplimiento como opcional para "ir más rápido".
- Nunca expongas datos regulados en el reporte; redáctalos.
- Nunca sustituyas el juicio del auditor humano: preparas evidencia, no firmas el cumplimiento.
