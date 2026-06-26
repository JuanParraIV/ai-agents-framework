# AI Agents Framework — Arquitectura Completa (Banking SDLC)

> Plataforma de **AI Agents** donde múltiples operadores (Product, Dev, QA, DevSecOps, DevOps, Platform, SRE, Compliance) ejecutan tareas del **SDLC completo de un banco** a través de **agentes** que componen **skills** reutilizables y se integran con sistemas reales vía **MCP**, bajo una capa de **gobierno, RBAC y auditoría** acorde a regulación financiera.

Este documento es el **plano por fases** para una implementación 100% exitosa. El detalle componente-a-componente está en [`ARCHITECTURE-DETAILED.md`](./ARCHITECTURE-DETAILED.md).

---

## 1. Principios de diseño

1. **BDD-first / Spec-first**: el contrato (`.feature`, AC, SLO, policy) se define antes que la implementación.
2. **Separación de responsabilidades (SoD)**: cada agente tiene fronteras duras; ningún agente aprueba/mergea su propio trabajo (requisito SOX).
3. **Human-in-the-loop en producción**: toda acción que toca prod, dinero o datos sensibles requiere aprobación humana explícita.
4. **Least privilege**: cada agente/skill recibe solo los MCP/tools mínimos.
5. **Todo auditable**: cada acción de agente deja traza inmutable (quién, qué, cuándo, sobre qué, con qué resultado).
6. **Fail-closed**: ante incertidumbre sobre seguridad/cumplimiento, se bloquea y escala.
7. **Skills reutilizables, agentes componibles**: un skill lo pueden usar varios agentes/operadores.

---

## 2. Capas de la arquitectura (vista de bloques)

```
┌──────────────────────────────────────────────────────────────────────────┐
│ L6  GOBIERNO Y CUMPLIMIENTO   RBAC · SoD · Approval Gates · Audit · PCI/SOX │
├──────────────────────────────────────────────────────────────────────────┤
│ L5  ORQUESTACIÓN              Router de intención · Workflows SDLC · Gates  │
├──────────────────────────────────────────────────────────────────────────┤
│ L4  AGENTES (por operador)    product · dev · qa · devsecops · devops ·     │
│                               platform · sre · compliance · release        │
├──────────────────────────────────────────────────────────────────────────┤
│ L3  SKILLS (capacidades)      .claude/skills/<dominio>/<skill>/SKILL.md     │
├──────────────────────────────────────────────────────────────────────────┤
│ L2  MCP / INTEGRACIONES       JIRA·Git·Semgrep·Snyk·Trivy·Vault·Terraform·  │
│                               K8s·Datadog·PagerDuty·ServiceNow·SonarQube    │
├──────────────────────────────────────────────────────────────────────────┤
│ L1  PLATAFORMA / RUNTIME      Claude Code subagents · memoria · secrets     │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Operadores y su mapa al SDLC

| Operador | Fase SDLC principal | Agente(s) | Pregunta que responde |
|----------|---------------------|-----------|------------------------|
| **Product** | Plan | `product-analyst` | ¿Qué construimos y cómo se valida? |
| **Dev** | Develop | `developer` | ¿Cómo lo implemento sin romper el contrato? |
| **QA** | Test | `qa-bdd-engineer`, `test-generator` | ¿Funciona y está cubierto? |
| **DevSecOps** | Secure | `security-reviewer` | ¿Es seguro y cumple regulación? |
| **DevOps** | Build/Release | `devops-pipeline`, `release-manager` | ¿Se construye, empaqueta y libera bien? |
| **Platform** | Provision | `platform-engineer` | ¿La infra es correcta, segura y reproducible? |
| **SRE** | Operate | `sre-agent` | ¿Está sano, observable y recuperable? |
| **Compliance** | Audit | `compliance-auditor` | ¿Hay evidencia y traza para el regulador? |

---

## 4. Flujo end-to-end (un cambio atraviesa el SDLC)

```
Product        Dev/QA              DevSecOps         DevOps/Platform        SRE/Compliance
─────────      ──────────────      ───────────       ────────────────       ──────────────
issue ─▶ story  ─▶ BDD contract ─▶ implement ─▶ security ─▶ pipeline ─▶ deploy ─▶ observe ─▶ audit
         (AC)      (.feature)       (code)       review     (CI/CD)     (IaC)     (SLO)     (evidence)
                                       │            │           │          │         │
                                   gate: BDD     gate: no    gate: tests  gate:    gate:
                                   Done          Critical    green +SCA   human    SLO ok
                                                 vulns                    approve
```

Cada flecha tiene un **gate** (criterio de salida) y, donde toca prod/datos/dinero, un **gate humano**.

---

## 5. Implementación por FASES (roadmap 100% exitoso)

Cada fase es entregable e independientemente valiosa. No se avanza sin cumplir los *Exit criteria*.

### Fase 0 — Fundaciones y Gobierno  `[✅ hecho]`
- **Objetivo**: cimientos seguros antes de automatizar nada crítico.
- **Entregables**: estructura de repo ✅, `.mcp.json` ✅, `CLAUDE.md` con guardrails globales ✅, matriz RBAC + approval gates + esquema de audit trail en `docs/GOVERNANCE.md` ✅, `.claude/settings.json` con permisos least-privilege (deny a prod/secretos) ✅, `.env.example` + `.gitignore` para manejo de secretos ✅.
- **MCP**: Vault (prod), Git.
- **Exit criteria**: RBAC documentada y aplicada ✅; ningún secreto en repo/contexto (settings deny + gitignore) ✅; esquema de audit trail definido ✅; gates humanos para prod definidos ✅.

### Fase 1 — Plan & Build (núcleo BDD-first)  `[hecho parcialmente]`
- **Agentes**: `product-analyst`, `qa-bdd-engineer`, `developer`.
- **Skills**: `story-refinement`, `bdd-test-generation`, `implement-from-bdd`.
- **MCP**: Atlassian (JIRA), Git/GitHub.
- **Exit criteria**: un issue real recorre issue→story→`.feature`→PR con gate BDD funcionando.

### Fase 2 — Quality Engineering  `[hecho parcialmente]`
- **Agentes**: `test-generator` (+ `qa-bdd-engineer`).
- **Skills**: `test-generation`, `coverage-gap-analysis`, `mutation-testing`, `e2e-testing`, `performance-testing`, `contract-testing`.
- **MCP**: Git, runners de test, Playwright/k6.
- **Exit criteria**: cobertura ≥80% line+branch en módulos críticos; suite verde reproducible en CI.

### Fase 3 — Security & Compliance (crítico bancario)  `[siguiente]`
- **Agente**: `security-reviewer` (DevSecOps).
- **Skills**: `code-review-security` ✅, `sast-scan`, `sca-scan`, `secret-scan`, `container-scan`, `iac-security-scan`, `dast-scan`, `threat-modeling`, `compliance-check`, `sbom-generation`.
- **MCP**: Semgrep, Snyk/Dependency-Track, Trivy/Grype, gitleaks, OWASP ZAP, SonarQube.
- **Exit criteria**: ningún PR mergea con hallazgos Critical/High; SBOM por release; mapeo a PCI-DSS/SOX/GDPR evidenciado.

### Fase 4 — Delivery (CI/CD)  `[planificado]`
- **Agentes**: `devops-pipeline`, `release-manager`.
- **Skills**: `pipeline-generation`, `container-build`, `artifact-management`, `release-orchestration`, `rollback`.
- **MCP**: Git CI, Artifactory/Nexus, ServiceNow (change management).
- **Exit criteria**: pipeline reproducible con quality+security gates; releases versionadas, firmadas y trazables a JIRA; rollback probado.

### Fase 5 — Platform & Infrastructure  `[planificado]`
- **Agente**: `platform-engineer`.
- **Skills**: `iac-generation`, `k8s-manifest`, `helm-chart`, `gitops-setup`, `environment-provisioning`, `secrets-management`.
- **MCP**: Terraform/Pulumi, Kubernetes, ArgoCD, Vault, Cloud (AWS/Azure/GCP).
- **Exit criteria**: entornos provisionados por IaC con security baseline; GitOps como única fuente de verdad; drift detectado.

### Fase 6 — Operate & Reliability (SRE)  `[planificado]`
- **Agente**: `sre-agent`.
- **Skills**: `slo-management`, `observability-setup`, `incident-response`, `runbook-generation`, `postmortem`, `capacity-planning`, `chaos-testing`.
- **MCP**: Datadog/Prometheus/Grafana, PagerDuty/Opsgenie, Kubernetes.
- **Exit criteria**: SLO/SLI definidos con error budgets; alertas accionables; runbooks por servicio; ciclo de incidente con postmortem sin culpa.

### Fase 7 — Governance Hardening & Audit  `[continuo]`
- **Agente**: `compliance-auditor`.
- **Skills**: `audit-trail`, `regulatory-mapping`, `evidence-collection`.
- **MCP**: ServiceNow, Confluence, almacén de evidencia.
- **Exit criteria**: evidencia automática para auditoría (SOX/PCI/regulador local); trazabilidad requisito→código→test→deploy; reportes para CAB/auditoría.

---

## 6. Dependencias entre fases

```
F0 ──▶ F1 ──▶ F2 ──▶ F3 ──┬──▶ F4 ──▶ F5 ──▶ F6
       (BDD)   (QA)  (Sec) │                    │
                           └────────────────────┴──▶ F7 (Audit, atraviesa todas)
```
- F0 es prerrequisito de todo. F3 (Security) debe estar antes de F4 (Delivery) para que el gate de seguridad sea real. F7 es transversal y se alimenta de todas.

---

## 7. Modelo de gobierno (banking)

| Control | Mecanismo | Regulación |
|---------|-----------|------------|
| Segregación de funciones | Ningún agente mergea/aprueba lo propio; gates humanos | SOX |
| Datos de tarjeta | Nunca PAN/CVV en logs/contexto; enmascarado/tokenizado | PCI-DSS |
| Datos personales | Minimización, clasificación, residencia | GDPR / ley local |
| Cambios en prod | Aprobación CAB vía ServiceNow + ventana de cambio | ITIL / SOX |
| Trazabilidad | Requisito↔código↔test↔deploy↔evidencia | Auditoría / regulador |
| Resiliencia operativa | SLOs, DR, runbooks, postmortems | DORA / BASEL |
| Acceso | RBAC por operador; least privilege en MCP | ISO 27001 |

---

## 8. Riesgos y mitigaciones

| Riesgo | Mitigación |
|--------|-----------|
| Agente actúa sobre prod sin control | Gates humanos obligatorios + RBAC + dry-run por defecto |
| Fuga de secretos/PII al contexto del LLM | Vault + redacción + secret-scan en pre-commit |
| Falsos negativos de seguridad | Defensa en capas (SAST+SCA+DAST+manual) + fail-closed |
| Deriva entre skills y agentes | Skills versionadas; referencias validadas en CI del framework |
| Sobre-automatización | Empezar en modo "suggest", promover a "act" por fase tras métricas |

---

## 9. Estado actual del framework

| Componente | Estado |
|-----------|--------|
| Agentes `product-analyst`, `developer`, `qa-bdd-engineer`, `test-generator` | ✅ definidos |
| Skills F1 (`story-refinement`, `bdd-test-generation`, `implement-from-bdd`) | ✅ |
| Skills F2 (`test-generation`, `coverage-gap-analysis`, `mutation-testing`) | ✅ |
| Skill F3 `code-review-security` | ✅ |
| `.mcp.json` (Atlassian) | ✅ |
| **F0 gobierno**: `CLAUDE.md`, `docs/GOVERNANCE.md`, `.claude/settings.json`, `.env.example`, `.gitignore` | ✅ |
| Resto de F3–F7 (agentes/skills/MCP) | ⏳ por construir (ver detalle) |

Ver el desglose exhaustivo de cada agente, skill y MCP en [`ARCHITECTURE-DETAILED.md`](./ARCHITECTURE-DETAILED.md).
