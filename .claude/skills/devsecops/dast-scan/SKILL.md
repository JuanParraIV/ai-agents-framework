---
name: dast-scan
description: >-
  Escaneo dinámico (DAST) con OWASP ZAP contra un entorno desplegado (nunca producción sin autorización): inyección, XSS, headers de seguridad, authn/session, exposición de datos. Falla cerrado ante High/Critical. Requiere una URL target de un entorno no productivo. Úsala para "dast", "zap scan", "escaneo dinámico", "pentest ligero".
allowed-tools: Read, Grep, Glob, Bash
metadata:
  type: skill
  tier: t2
  domain: devsecops
  owner: qintess-devsecops
  version: 1.0.0
---

# Skill: DAST scan (OWASP ZAP)

Escaneo dinámico contra una instancia **desplegada en un entorno no productivo** del servicio afectado por el cambio.

## Principio rector

> Fail-closed y autorización explícita: **nunca** escanees producción ni un sistema de terceros sin autorización registrada. Sin target autorizado → detente y solicita uno.

## Workflow

```
1. Confirmar target autorizado (staging/QA), NO producción. Sin autorización -> STOP.
2. Baseline (pasivo, rápido):  zap-baseline.py -t <URL> -r zap-report.html
3. Escaneo activo (si autorizado y con auth configurada): zap-full-scan.py -t <URL>
4. Revisar: headers (CSP/HSTS/X-Frame), cookies (Secure/HttpOnly/SameSite), authn/session,
   inyección/XSS reflejado, exposición de errores/datos, CORS permisivo
5. Clasificar por severidad; correlacionar con hallazgos SAST. Veredicto BLOCK/COMMENT/PASS
```

## Anti-Patterns (Never Do)

- Nunca escanees producción ni sistemas de terceros sin autorización explícita registrada.
- Nunca uses credenciales reales de cliente/PII para el escaneo: usa cuentas de prueba.
- Nunca marques PASS si no hubo target desplegado: repórtalo como "no ejecutado".
- Nunca dejes el escaneo activo corriendo contra un entorno compartido sin avisar.
