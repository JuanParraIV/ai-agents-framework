---
name: secret-scan
description: >-
  Detección de secretos (credenciales, tokens, claves privadas, connection strings, PAN/CVV) en el diff y el historial con gitleaks/trufflehog. Falla cerrado ante cualquier secreto activo. Complementa el hook pre-commit; esta skill es la pasada del revisor sobre el PR. Úsala para "secret scan", "busca secretos", "gitleaks", "hay credenciales en el PR".
allowed-tools: Read, Grep, Glob, Bash
metadata:
  type: skill
  tier: t2
  domain: devsecops
  owner: qintess-devsecops
  version: 1.0.0
---

# Skill: Secret scan

Busca secretos en el diff **y en el historial** de la rama (un secreto commiteado y luego borrado sigue en el historial).

## Principio rector

> Fail-closed: cualquier secreto que pueda ser activo → Critical → BLOCK. No asumas "es de prueba"; si no puedes probar que es falso, trátalo como real.

## Workflow

```
1. Escanear el historial de la rama:  gitleaks detect --no-banner --redact --exit-code 1
2. Escanear el diff staged/uncommitted: gitleaks protect --staged --redact
3. Pasada de patrones para banca: PAN (validado por Luhn), CVV, IBAN, claves privadas, JWT
4. Para cada hallazgo: file:line, tipo (redactado), y remediación
5. Remediación: rotar el secreto expuesto + purgar del historial (git filter-repo/BFG) + mover a Vault
```

## Relación con el hook pre-commit

El hook `secret_scan.py` (`.claude/hooks/`) bloquea el commit; esta skill es la **red de revisión** sobre el PR y el historial. Si el hook falló o se saltó, aquí se detecta.

## Anti-Patterns (Never Do)

- Nunca incluyas el valor del secreto en el reporte/comentario: redáctalo (`****`).
- Nunca marques PASS si gitleaks no estaba disponible: dilo.
- Nunca te limites al diff si el secreto pudo entrar antes en la rama: escanea el historial.
- Nunca cierres el hallazgo con "borrado en un commit posterior": sigue en el historial hasta purgarlo y rotarlo.
