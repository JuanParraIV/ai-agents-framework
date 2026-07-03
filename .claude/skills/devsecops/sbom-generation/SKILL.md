---
name: sbom-generation
description: >-
  Genera el SBOM (Software Bill of Materials) en formato CycloneDX o SPDX del artefacto/imagen con syft/cdxgen, base para trazabilidad de componentes, correlación con CVEs y cumplimiento (PCI/regulador). Úsala para "sbom", "bill of materials", "genera el SBOM", "inventario de dependencias".
allowed-tools: Read, Grep, Glob, Bash
metadata:
  type: skill
  tier: t2
  domain: devsecops
  owner: qintess-devsecops
  version: 1.0.0
---

# Skill: SBOM generation (CycloneDX/SPDX)

Produce el inventario firmable de componentes del artefacto liberado — requisito de trazabilidad y cumplimiento.

## Principio rector

> Un release sin SBOM es un release sin inventario: no puedes responder "¿nos afecta esta CVE?" sin él. Genera SBOM por release y consérvalo como evidencia.

## Workflow

```
1. Identificar el artefacto: imagen, filesystem o manifiestos de dependencias
2. Generar el SBOM:
     - Imagen/fs:  syft <target> -o cyclonedx-json > sbom.cdx.json
     - Node:       cdxgen -o sbom.cdx.json
3. Verificar completitud: componentes, versiones, licencias, hashes
4. (Opcional) correlacionar con CVEs: grype sbom:sbom.cdx.json
5. Adjuntar el SBOM al release y registrarlo como evidencia (retención según política)
```

## Anti-Patterns (Never Do)

- Nunca liberes a prod sin SBOM del artefacto final (no del código fuente suelto).
- Nunca edites el SBOM a mano para "limpiar" componentes: refleja la realidad del artefacto.
- Nunca omitas licencias: son parte del inventario y del riesgo legal.
