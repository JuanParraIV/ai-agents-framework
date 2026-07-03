---
name: observability-setup
description: >-
  Instrumenta métricas, logs estructurados y traces distribuidos (OpenTelemetry) con dashboards y alertas accionables basadas en SLO (burn-rate), sin exponer PII/PAN en la telemetría. Úsala para "observabilidad", "métricas", "dashboards", "alertas", "tracing", "opentelemetry".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
metadata:
  type: skill
  tier: t2
  domain: sre
  owner: qintess-sre
  version: 1.0.0
---

# Skill: Observability setup

Hace el servicio observable: los tres pilares (métricas, logs, traces) correlacionados y alertas que llevan a una acción.

## Principio rector

> Si no puedes responder "¿por qué está lento/roto?" con la telemetría, no es observable. Y la telemetría nunca contiene PAN/PII (redacción en el pipeline).

## Los tres pilares

- **Métricas**: RED (Rate, Errors, Duration) por servicio y los SLIs; Prometheus/OTel.
- **Logs**: estructurados (JSON), con trace_id para correlacionar; **sin PII/PAN** (redactar en origen).
- **Traces**: distribuidos (OpenTelemetry) a través de los límites de servicio.

## Alertas

- **Basadas en SLO / burn-rate**, no en umbrales arbitrarios de CPU.
- Cada alerta es **accionable**: enlaza al runbook y al dashboard. Sin alertas sin dueño.
- Multi-ventana (fast/slow burn) para atrapar tanto picos como degradación lenta.

## Workflow

```
1. Instrumentar RED + los SLIs; exportar vía OpenTelemetry
2. Logs estructurados con trace_id; verificar que NO llevan PII/PAN
3. Dashboards por servicio (SLO, RED, dependencias)
4. Alertas de burn-rate ligadas a runbooks; probar que disparan
5. Versionar dashboards/alertas como código; PR contra main
```

## Anti-Patterns (Never Do)

- Nunca loguees PAN/CVV/PII: redáctalos en el pipeline de telemetría.
- Nunca crees alertas no accionables ni sin runbook (fatiga de alertas).
- Nunca alertes solo por métricas de infra ignorando la experiencia del usuario.
- Nunca dejes dashboards/alertas fuera de control de versiones.
