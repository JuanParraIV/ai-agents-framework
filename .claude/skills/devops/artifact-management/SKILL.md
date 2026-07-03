---
name: artifact-management
description: >-
  Versiona, firma y publica artefactos (imágenes, paquetes) en un repositorio inmutable con procedencia y trazabilidad a JIRA/commit. Versionado semántico + git sha, firma cosign/sigstore, atestación SLSA, política de retención. Úsala para "publica el artefacto", "versiona el release", "firma la imagen", "sube a artifactory/nexus".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
metadata:
  type: skill
  tier: t2
  domain: devops
  owner: qintess-devops
  version: 1.0.0
---

# Skill: Artifact management (versionado, firma, trazabilidad)

Gestiona el ciclo del artefacto desde el build hasta el repositorio inmutable, con evidencia.

## Principio rector

> Un artefacto en prod debe poder responder: ¿de qué commit y JIRA salió, quién lo construyó, está firmado y sin manipular? Sin eso, no es liberable.

## Reglas

- **Versionado**: SemVer + metadatos de build (`1.4.2+<git-sha-corto>`); tag inmutable.
- **Inmutabilidad**: nunca re-publicar la misma versión; el repo (Artifactory/Nexus/OCI) es append-only.
- **Firma**: `cosign sign` (sigstore) de la imagen/artefacto; verificar en el deploy.
- **Procedencia**: atestación SLSA / provenance (build, fuente, materiales) + SBOM adjunto.
- **Trazabilidad**: artefacto ↔ commit ↔ JIRA key ↔ SBOM ↔ resultados de gates.
- **Retención**: política por entorno; conservar releases de prod como evidencia (SOX/PCI).

## Workflow

```
1. Calcular versión (SemVer + git sha); verificar que no exista ya (inmutabilidad)
2. Publicar en el repo inmutable:  jf rt upload / oras push / docker push <img>:<version>
3. Firmar:  cosign sign <ref>   y adjuntar SBOM + provenance
4. Registrar la trazabilidad (JIRA key, commit, gates pasados) como metadatos del artefacto
5. Handoff al release-manager: el deploy a prod requiere gate humano/CAB
```

## Anti-Patterns (Never Do)

- Nunca sobrescribas una versión ya publicada (rompe la inmutabilidad y la auditoría).
- Nunca publiques sin firma ni SBOM un artefacto destinado a prod.
- Nunca uses `latest` como versión de release.
- Nunca guardes las credenciales del repo de artefactos en el pipeline en claro.
