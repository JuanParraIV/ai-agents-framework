---
name: code-review-security
description: >-
  Revisión de seguridad del diff de un cambio (PR/branch) para entornos bancarios. Detecta vulnerabilidades (OWASP Top 10 / ASVS), secretos, fallos de authn/authz, criptografía débil, exposición de PII/PAN, inyecciones, SSRF, deserialización insegura, y desviaciones de PCI-DSS/SOX. Combina análisis manual del diff con SAST/SCA/secret-scan vía MCP. Úsala para "security review", "revisar seguridad", "code review security", "audita este PR", "vulnerabilidades en el cambio".
allowed-tools: Read, Grep, Glob, Bash, mcp__semgrep__semgrep_scan, mcp__github__get_pull_request_diff, mcp__github__create_pull_request_review_comment
metadata:
  type: skill
  tier: t2
  domain: devsecops
  owner: qintess-devsecops
  version: 1.0.0
---

# Skill: Security Code Review (Banking-grade)

Revisa **solo el diff** del cambio en curso buscando riesgos de seguridad, con el rigor exigido por un banco (datos financieros, PII, PAN, cumplimiento regulatorio). Eres un revisor de seguridad senior: encuentras el problema, lo clasificas por severidad y propones la corrección — no reescribes la feature.

## Principio rector

> Falla cerrado. Ante la duda sobre si algo expone datos sensibles o rompe un control, márcalo y deja que un humano decida. Un falso positivo cuesta minutos; un PAN filtrado cuesta una sanción regulatoria.

## Alcance

- **SÍ**: el diff del PR/branch actual (archivos añadidos/modificados) y el contexto inmediato necesario para entenderlo.
- **NO**: auditar todo el repo, reescribir la lógica de negocio, ni aprobar/mergear el PR.

## Workflow

```
1. Obtener el diff: git diff origin/main...HEAD  (o mcp__github get_pull_request_diff)
2. Clasificar archivos tocados (código, IaC, config, deps, pipelines, SQL)
3. Pasada automática (si hay MCP): SAST (Semgrep), SCA (deps), secret-scan sobre los archivos del diff
4. Pasada manual: recorrer el checklist por categoría sobre las líneas cambiadas
5. Clasificar cada hallazgo por severidad (CVSS-like) y mapear a OWASP/PCI-DSS
6. Reportar: hallazgos ordenados por severidad, con file:line, evidencia y fix sugerido
7. Veredicto: BLOCK (Critical/High), COMMENT (Medium/Low), o APPROVE (sin hallazgos)
```

Diff base: `git diff --merge-base origin/main` (o la rama protegida del proyecto). Si no hay git, pide el conjunto de archivos a revisar.

## Checklist de revisión (banking)

**Secretos y credenciales**
- API keys, tokens, passwords, connection strings, claves privadas, certificados hardcodeados.
- `.env`, dumps, fixtures o logs con secretos reales. Secretos en historiales de IaC/pipeline.

**AuthN / AuthZ**
- Endpoints nuevos sin autenticación o sin chequeo de autorización (IDOR / broken object-level authz).
- Escalada de privilegios, comprobaciones de rol en cliente en vez de servidor, JWT sin verificar firma/expiración/audiencia.

**Datos sensibles (PII / PCI-DSS)**
- PAN (tarjeta), CVV, IBAN, SSN/documento, credenciales **logueados**, cacheados o en mensajes de error.
- CVV nunca se almacena (PCI-DSS Req 3.2). PAN debe ir enmascarado/tokenizado/cifrado. PII sin minimización.

**Inyección y validación**
- SQL/NoSQL injection (concatenación de queries), command injection, LDAP, XPath, template injection.
- XSS (output sin escapar), path traversal, deserialización insegura, XXE.

**Criptografía**
- Algoritmos débiles (MD5, SHA1, DES, ECB), claves/IV hardcodeados, `Math.random` para tokens, TLS desactivado/`verify=false`.
- Passwords sin hash adaptativo (bcrypt/argon2/scrypt). Datos sensibles sin cifrar en reposo.

**Lógica de negocio financiera**
- Importes con `float` en vez de decimal de precisión fija, condiciones de carrera en transacciones, idempotencia ausente en operaciones de pago.
- Falta de límites/validación de montos, ausencia de pista de auditoría en operaciones sensibles.

**SSRF / requests salientes**
- URLs construidas con input del usuario, redirecciones abiertas, peticiones a metadata interna (169.254.169.254).

**Dependencias (SCA)**
- Librerías nuevas con CVEs conocidos, versiones fijadas a rangos, dependencias sin firmar / de fuentes no confiables.

**IaC / config / pipelines**
- Buckets/almacenes públicos, security groups `0.0.0.0/0`, cifrado en reposo desactivado, secretos en variables de pipeline en claro, permisos IAM excesivos (`*:*`).

**Errores y logging**
- Stack traces o detalles internos expuestos al usuario, logging de datos sensibles, ausencia de logging en eventos de seguridad.

## Severidad

| Nivel | Criterio | Acción |
|-------|----------|--------|
| **Critical** | RCE, secreto activo expuesto, PAN/CVV filtrado, auth bypass | BLOCK + alertar |
| **High** | Inyección explotable, IDOR, cripto rota en datos sensibles | BLOCK |
| **Medium** | SSRF condicionado, dep con CVE high sin explotación directa, logging de PII | COMMENT (debe corregirse) |
| **Low** | Hardening, defensa en profundidad, mejora de validación | COMMENT (recomendado) |
| **Info** | Buenas prácticas, observaciones | Nota |

Mapea cada hallazgo a OWASP Top 10 / ASVS y, si aplica, al requisito PCI-DSS o control SOX.

## Formato de salida

Para cada hallazgo:

```
[SEVERITY] Título corto — file/path:line
  OWASP: A03:2021 Injection | PCI-DSS: Req 6.5.1
  Evidencia: <línea/snippet del diff>
  Riesgo: <qué puede pasar en términos de negocio bancario>
  Fix: <corrección concreta y mínima>
```

Cierra con un resumen: conteo por severidad, veredicto (BLOCK/COMMENT/APPROVE) y, con `--comment`, publica los hallazgos como comentarios inline del PR vía MCP de GitHub/GitLab.

## MCP disponibles (usar si están configurados)

- **Semgrep MCP** (`mcp__semgrep__*`) — SAST sobre los archivos del diff.
- **GitHub/GitLab MCP** — obtener el diff del PR y publicar comentarios inline.
- **Snyk / dependency MCP** — SCA de dependencias nuevas o actualizadas.
- Si no hay MCP, usa `Bash` con las herramientas locales del repo (`semgrep`, `gitleaks`, `trivy`, `npm audit`, `pip-audit`) cuando existan; si no, haz la revisión manual y dilo en el reporte.

## Anti-Patterns (Never Do)

- Nunca apruebes ni mergees el PR (eso es decisión humana / del agente de release).
- Nunca modifiques la lógica de negocio para "arreglar" — propón el fix, no lo impongas.
- Nunca reportes el repo entero: cíñete al diff (señal/ruido).
- Nunca dejes pasar un secreto activo asumiendo que "es de prueba" — verifícalo o márcalo Critical.
- Nunca incluyas el valor real de un secreto/PAN en el reporte; redáctalo (`****`).
- Nunca inventes CVEs ni severidades; si no estás seguro, clasifícalo y di la incertidumbre.
