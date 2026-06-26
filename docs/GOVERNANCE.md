# GOVERNANCE.md — RBAC, Approval Gates y Audit Trail (Fase 0)

Modelo de gobierno operativo del framework. Lo aplican los guardrails de [`CLAUDE.md`](../CLAUDE.md) y la capa L6 de [`ARCHITECTURE.md`](./ARCHITECTURE.md).

---

## 1. Matriz RBAC (operador → agentes/skills → MCP)

| Operador | Agentes que invoca | Skills | MCP | Puede tocar prod |
|----------|--------------------|--------|-----|------------------|
| **Product** | product-analyst | story-refinement, epic-decomposition | atlassian | No |
| **Dev** | developer, test-generator, security-reviewer*(read)* | implement-from-bdd, code-review-security*(read)*, test-generation | atlassian, github | No — solo PR |
| **QA** | qa-bdd-engineer, test-generator | bdd-test-generation, test-generation, coverage-gap-analysis, mutation-testing | atlassian, github | No |
| **DevSecOps** | security-reviewer, compliance-auditor | code-review-security, sast/sca/secret/container/iac-security/dast-scan, threat-modeling, compliance-check, sbom-generation | semgrep, snyk, trivy, gitleaks, zap, sonarqube, github | Block/gate (no escribe) |
| **DevOps** | devops-pipeline, release-manager | pipeline-generation, container-build, artifact-management, release-orchestration, rollback | github, artifactory, servicenow | Con aprobación |
| **Platform** | platform-engineer | iac-generation, k8s-manifest, helm-chart, gitops-setup, environment-provisioning, secrets-management | terraform, kubernetes, argocd, vault, cloud | `plan` sí · `apply` con aprobación |
| **SRE** | sre-agent | slo-management, observability-setup, incident-response, runbook-generation, postmortem, capacity-planning, chaos-testing | datadog, prometheus, grafana, pagerduty, kubernetes | Mitigación con aprobación |
| **Compliance** | compliance-auditor | audit-trail, regulatory-mapping, evidence-collection | servicenow, confluence, atlassian | Solo lectura |

Principio: **least privilege**. Un operador no listado para un agente/MCP **no** puede invocarlo.

---

## 2. Approval Gates (Human-in-the-loop)

Acciones que **siempre** requieren aprobación humana explícita y registro de **quién** aprobó:

| Acción | Gate | Regulación |
|--------|------|------------|
| Merge a `main`/`develop`/`release/*` | Revisor humano (≠ autor) | SOX (SoD) |
| Deploy a producción | Aprobador + ventana de cambio | ITIL / SOX |
| `terraform apply` / `pulumi up` en prod | Aprobador tras revisar `plan` | DORA |
| `kubectl apply/delete` en prod | Aprobador | DORA |
| Cambios IAM / roles / políticas | Aprobador de seguridad | ISO 27001 |
| Rotación / acceso a secretos | Aprobador + Vault audit | PCI-DSS |
| Mitigación en prod durante incidente | Incident commander | DORA |
| Cambio que afecta datos de tarjeta/PII | Aprobador de cumplimiento | PCI-DSS / GDPR |

Regla de oro: **ningún agente aprueba lo que produjo otro agente del mismo flujo sin un humano en el medio** cuando la acción está en esta tabla.

---

## 3. Audit Trail (esquema mínimo)

Cada acción significativa de un agente emite un registro **inmutable**:

```json
{
  "timestamp": "2026-06-26T14:03:11Z",
  "operator": "dev:jmparra",
  "agent": "developer",
  "skill": "implement-from-bdd",
  "action": "open_pull_request",
  "target": "repo:core-payments#PR-482",
  "jira": "PROJ-456",
  "inputs_redacted": true,
  "result": "success",
  "approver": null,
  "gate": "n/a"
}
```

- `inputs_redacted`: confirma que no se almacenan secretos/PAN/PII.
- `approver` + `gate`: obligatorios cuando la acción está en §2.
- Retención según política del banco (típ. ≥ 1 año para SOX/PCI).

---

## 4. Modos de autonomía (promoción gradual)

Cada agente se promueve por etapas tras demostrar métricas:

```
suggest  →  act-with-approval  →  act-autonomous (solo acciones no críticas)
(propone)   (ejecuta tras gate)    (ejecuta sin gate donde RBAC lo permite)
```

Producción y las acciones de §2 **nunca** llegan a `act-autonomous`.

---

## 5. Mapeo de cumplimiento

| Regulación | Controles del framework |
|------------|--------------------------|
| **PCI-DSS** | secret-scan, enmascarado de PAN, CVV nunca almacenado, cifrado, SBOM, RBAC |
| **SOX** | SoD (no self-approve), audit trail, change management vía ServiceNow |
| **GDPR / ley local** | clasificación y minimización de datos, residencia, redacción |
| **DORA / BASEL** | SLOs, error budgets, DR, runbooks, postmortems |
| **ISO 27001** | RBAC, least privilege, gestión de secretos, trazabilidad |

---

Relacionado: [`CLAUDE.md`](../CLAUDE.md) · [`ARCHITECTURE.md`](./ARCHITECTURE.md) · [`ARCHITECTURE-DETAILED.md`](./ARCHITECTURE-DETAILED.md)
