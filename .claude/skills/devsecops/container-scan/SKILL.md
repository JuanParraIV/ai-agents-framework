---
name: container-scan
description: >-
  Escaneo de imágenes de contenedor con Trivy/Grype: CVEs de la base y paquetes del sistema, secretos embebidos, malas prácticas de Dockerfile (root, latest, capas con secretos). Falla cerrado ante High/Critical. Úsala para "container scan", "escanea la imagen", "trivy", "vulnerabilidades del contenedor".
allowed-tools: Read, Grep, Glob, Bash
metadata:
  type: skill
  tier: t2
  domain: devsecops
  owner: qintess-devsecops
  version: 1.0.0
---

# Skill: Container scan (Trivy/Grype)

Escanea la imagen construida (o el `Dockerfile`/`FROM`) del cambio.

## Principio rector

> Fail-closed: CVE High/Critical en la imagen que llega a runtime → BLOCK. Prefiere bases mínimas (distroless/alpine) y digests fijados (no `latest`).

## Workflow

```
1. Localizar Dockerfile(s) y la imagen base (FROM) tocados por el diff
2. Escanear:
     - Imagen:      trivy image --severity HIGH,CRITICAL <imagen>
     - Filesystem:  trivy fs --severity HIGH,CRITICAL .
     - Config:      trivy config <Dockerfile>   (misconfig + best practices)
3. Revisar Dockerfile: USER no-root, sin secretos en ARG/ENV, sin curl|bash, digests fijados
4. Clasificar por severidad y si el paquete vulnerable está en el path de ejecución
5. Fix: bump de base/paquete, multi-stage para no arrastrar build deps. Veredicto BLOCK/COMMENT/PASS
```

## Anti-Patterns (Never Do)

- Nunca corras el contenedor como root si puede evitarse.
- Nunca dejes secretos en capas (ARG/ENV/COPY de .env) — quedan en el historial de capas.
- Nunca uses tags móviles (`latest`) en producción: fija por digest.
- Nunca marques PASS si Trivy/Grype no estaba disponible: dilo.
