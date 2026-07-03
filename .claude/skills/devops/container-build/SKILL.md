---
name: container-build
description: >-
  Genera Dockerfiles seguros y builds reproducibles: multi-stage, base mínima/distroless fijada por digest, usuario no-root, sin secretos en capas, SBOM en el build y escaneo previo al push. Úsala para "containeriza", "dockerfile", "build de imagen", "empaqueta en contenedor".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
metadata:
  type: skill
  tier: t2
  domain: devops
  owner: qintess-devops
  version: 1.0.0
---

# Skill: Container build (imagen segura y reproducible)

Construye la imagen del servicio con endurecimiento por defecto y trazabilidad.

## Principio rector

> La imagen es superficie de ataque en runtime. Mínima, no-root, sin secretos, escaneada antes de publicar. Lo que no necesita estar en la imagen, no entra.

## Checklist del Dockerfile

- **Multi-stage**: build separado del runtime; no arrastrar toolchain ni deps de build.
- **Base mínima** fijada por **digest** (`distroless`, `alpine`, `-slim`) — nunca `latest`.
- **Non-root**: `USER` dedicado; filesystem read-only donde se pueda.
- **Sin secretos** en `ARG`/`ENV`/capas; usar BuildKit secrets (`--mount=type=secret`) si hace falta en build.
- **Determinismo**: deps fijadas por lockfile; evitar `curl | bash`; capas ordenadas por estabilidad.
- **Metadatos**: labels OCI (`org.opencontainers.image.*`) con revisión, fuente y JIRA key.

## Workflow

```
1. Detectar runtime/lenguaje y deps; escribir Dockerfile multi-stage endurecido
2. Build reproducible:  docker build --sbom=true -t <img>:<version> .
3. Escanear ANTES de publicar:  trivy image --severity HIGH,CRITICAL <img>  (gate F3)
4. Generar SBOM (syft <img> -o cyclonedx-json) y adjuntarlo al artefacto
5. Etiquetar por versión + git sha (nunca solo latest); handoff a artifact-management
```

## Anti-Patterns (Never Do)

- Nunca corras como root si puede evitarse; nunca `chmod 777`.
- Nunca metas `.env`/claves/certs en la imagen (quedan en el historial de capas).
- Nunca publiques una imagen con CVEs High/Critical sin gate humano.
- Nunca uses tags móviles para la base ni para la imagen publicada en prod.
