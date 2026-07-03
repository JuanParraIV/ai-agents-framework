---
name: sca-scan
description: >-
  Análisis de composición de software (SCA): detecta dependencias con CVEs conocidos, licencias problemáticas y paquetes no confiables, priorizando las dependencias nuevas o actualizadas en el diff. Falla cerrado ante vulnerabilidades High/Critical explotables. Úsala para "sca", "dependencias vulnerables", "snyk", "audita las dependencias".
allowed-tools: Read, Grep, Glob, Bash
metadata:
  type: skill
  tier: t2
  domain: devsecops
  owner: qintess-devsecops
  version: 1.0.0
---

# Skill: SCA scan (dependencias)

Revisa las dependencias, con foco en las **añadidas/actualizadas** en el diff del manifiesto/lockfile.

## Principio rector

> Fail-closed: CVE High/Critical con path de explotación → BLOCK. Prioriza lo que el cambio introduce sobre la deuda preexistente (repórtala aparte).

## Workflow

```
1. Detectar el ecosistema por manifiesto: requirements*.txt/pyproject, package.json, pom.xml, go.mod
2. Ver qué dependencias toca el diff (git diff del lockfile/manifest)
3. Ejecutar el escáner disponible:
     - Snyk:      snyk test --severity-threshold=high
     - Python:    pip-audit
     - Node:      npm audit --audit-level=high
     - Java:      mvn org.owasp:dependency-check-maven:check
4. Cruzar hallazgos con las dependencias del diff; clasificar por severidad y explotabilidad
5. Proponer versión fija segura; reportar CVE, severidad y fix. Veredicto BLOCK/COMMENT/PASS
```

## Anti-Patterns (Never Do)

- Nunca inventes CVEs ni severidades; cita el identificador real (CVE/GHSA).
- Nunca marques PASS si no había escáner disponible: dilo explícitamente.
- Nunca fijes una dependencia a un rango abierto (`^`, `~`) en un fix de seguridad.
- Nunca ignores una transitria vulnerable asumiendo que "no se usa" sin verificar el path.
