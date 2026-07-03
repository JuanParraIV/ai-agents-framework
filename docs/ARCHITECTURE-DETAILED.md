# AI Agents Framework — Arquitectura Detallada (Banking SDLC)

Especificación componente-a-componente. Acompaña al plano por fases de [`ARCHITECTURE.md`](./ARCHITECTURE.md).

Convenciones:
- **Estado**: ✅ existe · 🟡 parcial · ⏳ por construir.
- Skills viven en `.claude/skills/<dominio>/<skill>/SKILL.md`. Agentes en `.claude/agents/<agente>.md`.
- `mcp__<server>__<tool>` es el namespacing de MCP en Claude Code.

---

## A. Capa de Orquestación (L5)

**Router de intención**: Claude Code enruta por `description` + trigger phrases del agente. Para flujos multi-agente, un agente orquestador (o el operador humano) encadena sub-tasks de JIRA como estado compartido.

**Workflows SDLC** (máquinas de estado sobre sub-tasks de JIRA):

| Workflow | Secuencia | Gate(s) |
|----------|-----------|---------|
| Feature delivery | product → qa-bdd → developer → security-reviewer → devops → sre | BDD Done · no Critical/High · tests green · human approve prod |
| Hotfix | developer → security-reviewer → release-manager | security fast-track · human approve |
| Infra change | platform-engineer → security-reviewer → devops | iac-security pass · CAB approve |
| Incident | sre-agent → (developer\|platform) → compliance-auditor | postmortem obligatorio |

**Estados de historia**: `AI-draft → Ready → BDD-Done → In-Dev → In-Review → Security-Passed → Ready-to-Release → Deployed → Verified`.

---

## B. Capa de Agentes (L4)

### B.1 product-analyst ✅ (Product)
- **Rol**: issues crudos → User Stories con Gherkin AC + sub-tasks.
- **Skills**: `story-refinement`.
- **MCP**: `mcp__atlassian__*` (jira_get_issue, jira_search, jira_create_issue, jira_update_issue, jira_add_comment, jira_create_issue_link, jira_get_transitions, jira_transition_issue); `mcp__markitdown__convert_to_markdown` (ingesta de PDFs/Office de requisitos a Markdown).
- **Tools nativos**: Read, Grep, Glob.
- **Gate**: crea en `AI-draft`; nunca asigna a personas.

### B.2 qa-bdd-engineer ✅ (QA)
- **Rol**: Gherkin AC → `.feature` + step skeletons (pending). Contrato inmutable.
- **Skills**: `bdd-test-generation`, `coverage-gap-analysis`.
- **MCP**: Atlassian (get_issue, add_comment, transition_issue).
- **Tools**: Read, Write, Edit, Bash, Grep, Glob.
- **Gate**: solo escribe `features/`+`steps/`; transiciona solo `[BDD]`.

### B.3 developer ✅ (Dev)
- **Rol**: implementa código + step definitions hasta pasar el BDD.
- **Skills**: `implement-from-bdd`, `code-review-security` (self-check).
- **MCP**: Atlassian (get_issue, update_issue, add_comment, transition_issue).
- **Tools**: Read, Write, Edit, Bash, Grep, Glob.
- **Gate**: BDD-First Gate; ≤15 archivos / ≤500 líneas por PR; nunca toca `.feature`.

### B.4 test-generator ✅ (QA)
- **Rol**: tests reales ejecutables (unit/integration/E2E) + cobertura + mutación.
- **Skills**: `test-generation`, `coverage-gap-analysis`, `mutation-testing`.
- **MCP**: ninguno (code-centric).
- **Tools**: Read, Write, Edit, Bash, Grep, Glob.

### B.5 security-reviewer ✅ (DevSecOps)
- **Rol**: revisión de seguridad del diff + orquestación de SAST/SCA/secret/IaC/DAST + cumplimiento.
- **Skills**: `code-review-security` ✅, `sast-scan`, `sca-scan`, `secret-scan`, `container-scan`, `iac-security-scan`, `dast-scan`, `threat-modeling`, `compliance-check`, `sbom-generation`.
- **MCP**: `mcp__semgrep__*`, Snyk/Dependency-Track, Trivy/Grype, gitleaks, OWASP ZAP, SonarQube, GitHub/GitLab.
- **Tools**: Read, Grep, Glob, Bash.
- **Gate**: BLOCK en Critical/High; fail-closed; nunca aprueba el PR.

### B.6 devops-pipeline ✅ (DevOps)
- **Rol**: genera/actualiza pipelines CI/CD con quality+security gates; build y empaquetado.
- **Skills**: `pipeline-generation`, `container-build`, `artifact-management`.
- **MCP**: GitHub/GitLab CI, Artifactory/Nexus.
- **Tools**: Read, Write, Edit, Bash, Grep, Glob.
- **Gate**: pipeline incluye gates de F2 y F3; sin secretos en claro.

### B.7 release-manager ✅ (DevOps/Release)
- **Rol**: orquesta releases, versionado, changelog, rollback, change request.
- **Skills**: `release-orchestration`, `rollback`.
- **MCP**: GitHub (releases/tags), ServiceNow (change management), Atlassian.
- **Tools**: Read, Write, Edit, Bash.
- **Gate**: aprobación humana/CAB para prod; release firmada y trazable a JIRA.

### B.8 platform-engineer ✅ (Platform)
- **Rol**: IaC, Kubernetes, Helm, GitOps, provisioning de entornos, secretos.
- **Skills**: `iac-generation`, `k8s-manifest`, `helm-chart`, `gitops-setup`, `environment-provisioning`, `secrets-management`.
- **MCP**: Terraform/Pulumi, Kubernetes, ArgoCD, Vault, Cloud (AWS/Azure/GCP).
- **Tools**: Read, Write, Edit, Bash, Grep, Glob.
- **Gate**: `terraform plan` (nunca `apply` directo a prod sin aprobación); security baseline; GitOps como fuente de verdad.

### B.9 sre-agent ✅ (SRE)
- **Rol**: SLO/SLI, observabilidad, respuesta a incidentes, runbooks, postmortems, capacity, chaos.
- **Skills**: `slo-management`, `observability-setup`, `incident-response`, `runbook-generation`, `postmortem`, `capacity-planning`, `chaos-testing`.
- **MCP**: Datadog/Prometheus/Grafana, PagerDuty/Opsgenie, Kubernetes.
- **Tools**: Read, Write, Edit, Bash, Grep, Glob.
- **Gate**: acciones de mitigación en prod requieren aprobación; postmortem sin culpa obligatorio.

### B.10 compliance-auditor ✅ (Compliance/Risk)
- **Rol**: trazabilidad requisito↔código↔test↔deploy, recolección de evidencia, mapeo regulatorio.
- **Skills**: `audit-trail`, `regulatory-mapping`, `evidence-collection`.
- **MCP**: ServiceNow, Confluence, Atlassian, `markitdown` (evidencia/regulación en PDF → Markdown), almacén de evidencia.
- **Tools**: Read, Grep, Glob.
- **Gate**: solo lectura sobre artefactos; nunca modifica código/infra.

---

## C. Capa de Skills (L3) — catálogo completo

### product/
| Skill | Estado | Qué hace |
|-------|--------|----------|
| `story-refinement` | ✅ | issues → stories + Gherkin AC + sub-tasks |
| `epic-decomposition` | ⏳ | épica → historias sprint-sized con dependencias |
| `requirements-traceability` | ⏳ | matriz requisito↔historia↔test |

### dev/
| Skill | Estado | Qué hace |
|-------|--------|----------|
| `code-review-security` | ✅ | revisión de seguridad del diff (banking) |
| `implement-from-bdd` | ✅ | código + steps para pasar el BDD |
| `code-review-quality` | ⏳ | revisión de calidad/reuse/simplicidad del diff |
| `refactor` | ⏳ | refactor seguro guiado por tests |
| `api-design` | ⏳ | diseño de API (OpenAPI) + contratos |
| `db-migration` | ⏳ | migraciones reversibles + revisión |

### qa/
| Skill | Estado | Qué hace |
|-------|--------|----------|
| `bdd-test-generation` | ✅ | Gherkin → `.feature` + skeletons |
| `test-generation` | ✅ | unit/integration reales + ejecución |
| `coverage-gap-analysis` | ✅ | gaps de cobertura → tests dirigidos |
| `mutation-testing` | ✅ | efectividad de tests vía mutantes |
| `e2e-testing` | ⏳ | flujos E2E (Playwright/Cypress) |
| `performance-testing` | ⏳ | carga/estrés (k6/JMeter) + umbrales |
| `contract-testing` | ⏳ | contratos consumidor/proveedor (Pact) |

### devsecops/
| Skill | Estado | Qué hace |
|-------|--------|----------|
| `sast-scan` | ✅ | SAST (Semgrep/SonarQube) sobre el diff |
| `sca-scan` | ✅ | dependencias vulnerables (Snyk) |
| `secret-scan` | ✅ | secretos (gitleaks/trufflehog) |
| `container-scan` | ✅ | imágenes (Trivy/Grype) |
| `iac-security-scan` | ✅ | misconfig IaC (tfsec/checkov) |
| `dast-scan` | ✅ | dinámico (OWASP ZAP) |
| `threat-modeling` | ✅ | STRIDE sobre el diseño |
| `compliance-check` | ✅ | mapeo PCI-DSS/SOX/GDPR |
| `sbom-generation` | ✅ | SBOM (CycloneDX/SPDX) por release |

### devops/
| Skill | Estado | Qué hace |
|-------|--------|----------|
| `pipeline-generation` | ✅ | CI/CD con quality+security gates |
| `container-build` | ✅ | Dockerfile seguro + build reproducible |
| `artifact-management` | ✅ | versionado/firmado de artefactos |
| `release-orchestration` | ✅ | versionado, changelog, despliegue |
| `rollback` | ✅ | rollback probado y trazable |

### platform/
| Skill | Estado | Qué hace |
|-------|--------|----------|
| `iac-generation` | ✅ | Terraform/Pulumi con baseline seguro |
| `k8s-manifest` | ✅ | manifests con límites/probes/policies |
| `helm-chart` | ✅ | charts parametrizados |
| `gitops-setup` | ✅ | ArgoCD/Flux como fuente de verdad |
| `environment-provisioning` | ✅ | entornos efímeros/reproducibles |
| `secrets-management` | ✅ | Vault/ESO, rotación, sin secretos en claro |

### sre/
| Skill | Estado | Qué hace |
|-------|--------|----------|
| `slo-management` | ✅ | SLI/SLO + error budgets |
| `observability-setup` | ✅ | métricas/logs/traces + dashboards |
| `incident-response` | ✅ | triage, mitigación, comms |
| `runbook-generation` | ✅ | runbooks por servicio |
| `postmortem` | ✅ | postmortem sin culpa + acciones |
| `capacity-planning` | ✅ | tendencias y dimensionamiento |
| `chaos-testing` | ✅ | experimentos de resiliencia |

### compliance/
| Skill | Estado | Qué hace |
|-------|--------|----------|
| `audit-trail` | ✅ | traza inmutable de acciones |
| `regulatory-mapping` | ✅ | control↔regulación (PCI/SOX/DORA) |
| `evidence-collection` | ✅ | evidencia para auditoría/regulador |

---

## D. Capa MCP / Integraciones (L2)

| MCP server | Tools (ej.) | Usado por | Fase |
|------------|-------------|-----------|------|
| `atlassian` (JIRA/Confluence) | jira_get_issue, jira_search, jira_create_issue, jira_transition_issue | product, qa-bdd, developer, release, compliance | F1 ✅ |
| `markitdown` | convert_to_markdown (uri: http/https/file/data) | product, compliance | F1 ✅ |
| `github` / `gitlab` | get_pull_request_diff, create_review_comment, create_pr | developer, security-reviewer, devops | F1–F4 |
| `semgrep` | semgrep_scan | security-reviewer | F3 |
| `snyk` / `dependency-track` | test, monitor | security-reviewer | F3 |
| `trivy` / `grype` | image_scan, fs_scan | security-reviewer, devops | F3–F4 |
| `gitleaks` / `trufflehog` | scan | security-reviewer | F3 |
| `owasp-zap` | active_scan | security-reviewer | F3 |
| `sonarqube` | quality_gate | security-reviewer, devops | F3–F4 |
| `artifactory` / `nexus` | upload, retrieve | devops, release | F4 |
| `servicenow` | create_change, get_cab | release, compliance | F4, F7 |
| `terraform` / `pulumi` | plan, state | platform | F5 |
| `kubernetes` | get, apply (dry-run) | platform, sre | F5–F6 |
| `argocd` | sync, app_status | platform | F5 |
| `vault` | read_secret, rotate | platform, todos (secrets) | F0, F5 |
| `aws`/`azure`/`gcp` | recursos cloud | platform | F5 |
| `datadog`/`prometheus`/`grafana` | query_metrics, dashboards | sre | F6 |
| `pagerduty`/`opsgenie` | get_incidents, ack | sre | F6 |

> **Secretos**: ningún MCP recibe credenciales hardcodeadas; se inyectan por entorno (`${VAR}`) o desde Vault. Ver `.mcp.json`.

---

## E. Capa de Gobierno (L6)

### E.1 Matriz RBAC (operador → puede invocar)
| Operador | Agentes permitidos | Acciones prod |
|----------|--------------------|---------------|
| Product | product-analyst | no |
| Dev | developer, test-generator, security-reviewer (read) | no (PR only) |
| QA | qa-bdd-engineer, test-generator | no |
| DevSecOps | security-reviewer, compliance-auditor | block/gate |
| DevOps | devops-pipeline, release-manager | con aprobación |
| Platform | platform-engineer | plan sí / apply con aprobación |
| SRE | sre-agent | mitigación con aprobación |
| Compliance | compliance-auditor | solo lectura |

### E.2 Approval Gates (human-in-the-loop)
- Merge a `main`/`develop`, deploy a prod, `terraform apply`, rotación de secretos, cambios IAM, acciones de mitigación en prod → **requieren aprobación humana** y registro de quién aprobó.

### E.3 Audit trail (campos mínimos)
`timestamp · operador · agente · skill · acción · target (repo/issue/recurso) · inputs (redactados) · resultado · aprobador (si aplica)`.

### E.4 Cumplimiento mapeado
- **PCI-DSS**: secret-scan, enmascarado de PAN, cifrado, SBOM, segregación.
- **SOX**: SoD (no self-approve), audit trail, change management.
- **GDPR / ley local**: clasificación y minimización de datos, residencia.
- **DORA / BASEL**: SLOs, DR, runbooks, postmortems, resiliencia operativa.
- **ISO 27001**: RBAC, least privilege, gestión de secretos.

---

## F. Estructura de carpetas objetivo

```
ai-agents-framework/
├─ .mcp.json
├─ README.md
├─ CLAUDE.md                      # guardrails globales ✅
├─ docs/
│  ├─ ARCHITECTURE.md             # plano por fases
│  └─ ARCHITECTURE-DETAILED.md    # este documento
└─ .claude/
   ├─ agents/
   │  ├─ product-analyst.md ✅  developer.md ✅  qa-bdd-engineer.md ✅  test-generator.md ✅
   │  ├─ security-reviewer.md ✅ devops-pipeline.md ✅ release-manager.md ✅
   │  └─ platform-engineer.md ✅ sre-agent.md ✅ compliance-auditor.md ✅
   └─ skills/
      ├─ product/  dev/  qa/      # ✅ pobladas (F1–F3 core)
      └─ devsecops/ devops/ platform/ sre/ compliance/   # ✅ pobladas (F3–F7)
```

---

## G. Roadmap de construcción de componentes (orden sugerido)

1. **F0**: `CLAUDE.md` con guardrails + matriz RBAC + esquema de audit trail.
2. **F3**: agente `security-reviewer` + skills `sast/sca/secret/container/iac-security/compliance` (mayor valor para un banco; ya está `code-review-security`).
3. **F4**: `devops-pipeline` + `pipeline-generation` (conecta los gates de F2/F3 en CI/CD).
4. **F5**: `platform-engineer` + skills IaC/K8s/GitOps.
5. **F6**: `sre-agent` + skills SLO/observabilidad/incidentes.
6. **F7**: `compliance-auditor` + skills de evidencia/regulación (transversal).

Cada componente nuevo: definir agente → skills → MCP → gate → validar referencias → actualizar este documento.
