---
name: evidence-collection
description: >-
  Reúne evidencia de auditoría trazable de punta a punta (requisito↔historia↔código↔test↔seguridad↔deploy↔audit trail) para un release o control, ensamblando un paquete de evidencia para el auditor/regulador. Solo lectura; la evidencia se reúne, no se fabrica. Úsala para "recolecta evidencia", "paquete de auditoría", "trazabilidad requisito a deploy", "evidencia para el regulador".
allowed-tools: Read, Grep, Glob, Bash
metadata:
  type: skill
  tier: t2
  domain: compliance
  owner: qintess-compliance
  version: 1.0.0
---

# Skill: Evidence collection

Reconstruye y ensambla la cadena de evidencia que demuestra que un cambio siguió el proceso controlado.

## Principio rector

> Trazabilidad completa o no hay evidencia. Cada eslabón (requisito → deploy) debe enlazar con el siguiente por su JIRA key/commit/PR. La evidencia se reúne de fuentes reales; si un eslabón falta, es un hallazgo, no se inventa.

## Cadena de trazabilidad a reconstruir

```
Requisito (JIRA)  ->  Historia + AC Gherkin  ->  .feature (contrato)  ->  código + tests verdes
   ->  revisión de seguridad (F3)  ->  gates CI (F2+F3) verdes  ->  artefacto firmado + SBOM
   ->  release + change approval  ->  deploy  ->  registros del audit trail
```

## Workflow

```
1. Fijar el alcance: un release / control / periodo, con su JIRA key
2. Para cada eslabón, localizar la evidencia:
     JIRA (historia/AC), .feature, PR + review, resultados de CI, SBOM/firma,
     release + aprobación, audit/*.jsonl del deploy
3. Enlazar los eslabones por JIRA key / commit / PR; detectar eslabones faltantes (gaps)
4. Ensamblar el paquete de evidencia (índice + referencias), con datos regulados redactados
5. Reportar la cadena completa y los gaps. NO modificar artefactos ni el trail
```

## Anti-Patterns (Never Do)

- Nunca fabriques ni edites evidencia: se reúne de fuentes reales (git/JIRA/CI/trail).
- Nunca presentes una cadena con eslabones sin enlazar como si estuviera completa.
- Nunca incluyas PAN/CVV/PII sin redactar en el paquete de evidencia.
- Nunca modifiques el artefacto o el trail para "cerrar" un gap.
