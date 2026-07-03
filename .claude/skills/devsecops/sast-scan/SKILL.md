---
name: sast-scan
description: >-
  Análisis estático de seguridad (SAST) sobre los archivos del diff con Semgrep. Detecta inyección, cripto débil, deserialización insegura, secretos, patrones inseguros por lenguaje. Clasifica por severidad y falla cerrado ante High/Critical. Úsala para "sast", "análisis estático", "semgrep scan", "escanea el código".
allowed-tools: Read, Grep, Glob, Bash, mcp__semgrep__semgrep_scan
metadata:
  type: skill
  tier: t2
  domain: devsecops
  owner: qintess-devsecops
  version: 1.0.0
---

# Skill: SAST scan (Semgrep)

Ejecuta SAST **solo sobre los archivos cambiados** del PR/branch (señal/ruido) y reporta hallazgos accionables.

## Principio rector

> Fail-closed: High/Critical → BLOCK. No silencies una regla sin justificación registrada; un `nosemgrep` sin motivo es una desviación de control.

## Workflow

```
1. Delimitar el diff: git diff --name-only --merge-base origin/<base>
2. Ejecutar Semgrep sobre esos archivos:
     - MCP: mcp__semgrep__semgrep_scan (si está configurado), o
     - CLI: semgrep --config p/security-audit --config p/secrets <archivos> --severity ERROR
3. Mapear cada hallazgo a OWASP/CWE y severidad (ERROR=High/Critical, WARNING=Medium)
4. Descartar falsos positivos con justificación explícita (no silenciar en masa)
5. Reportar file:line, regla, evidencia redactada y fix; veredicto BLOCK/COMMENT/PASS
```

## Reglas recomendadas (banking)

`p/security-audit`, `p/secrets`, `p/owasp-top-ten`, y el pack del lenguaje (`p/python`, `p/java`, `p/javascript`). Añade reglas propias para PAN/CVV/logging de PII si el repo las tiene.

## Anti-Patterns (Never Do)

- Nunca escanees todo el repo cuando la tarea es revisar un diff.
- Nunca marques PASS si Semgrep no estaba instalado/configurado: dilo.
- Nunca añadas `# nosemgrep` para "pasar" sin justificación de seguridad registrada.
- Nunca incluyas el valor de un secreto detectado en el reporte; redáctalo (`****`).
