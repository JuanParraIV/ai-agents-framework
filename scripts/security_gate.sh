#!/usr/bin/env bash
# Security gate (F3 / TB-5) — fail-closed sobre el diff del cambio.
#
# Ejecuta los escáneres DISPONIBLES sobre el diff contra la rama base y sale != 0
# si alguno reporta hallazgos (secretos / SAST). Degrada con elegancia: si una
# herramienta no está instalada, lo AVISA y sigue — nunca asume "verde" por ausencia.
#
# Uso:   scripts/security_gate.sh [rama-base]     (default: origin/main)
# Enforcement del gate del agente security-reviewer (BLOCK ante Critical/High).
set -uo pipefail

BASE="${1:-origin/main}"
fallos=0
ejecutados=()
ausentes=()

# Rango del diff (merge-base con la base; si no existe, todo el árbol trabajado).
if git rev-parse --verify -q "$BASE" >/dev/null; then
  RANGE="$(git merge-base "$BASE" HEAD 2>/dev/null)"
else
  RANGE=""
  echo "aviso: rama base '$BASE' no encontrada; se escanea el árbol completo." >&2
fi

echo "== Security gate (base: $BASE) =="

# 1) Secret scan (gitleaks) — bloqueante.
if command -v gitleaks >/dev/null 2>&1; then
  ejecutados+=("gitleaks")
  if ! gitleaks detect --no-banner --redact --exit-code 1 >/tmp/gitleaks.out 2>&1; then
    echo "  [BLOCK] gitleaks: posibles secretos (ver detalle, redactado)."; fallos=1
  else
    echo "  [ok] gitleaks: sin secretos."
  fi
else
  ausentes+=("gitleaks")
fi

# 2) SAST (semgrep) — bloqueante ante severidad ERROR (High/Critical).
if command -v semgrep >/dev/null 2>&1; then
  ejecutados+=("semgrep")
  if ! semgrep --error --severity ERROR --config p/security-audit --quiet >/tmp/semgrep.out 2>&1; then
    echo "  [BLOCK] semgrep: hallazgos de severidad ERROR (High/Critical)."; fallos=1
  else
    echo "  [ok] semgrep: sin hallazgos High/Critical."
  fi
else
  ausentes+=("semgrep")
fi

# 3) IaC (checkov/tfsec) — informativo si hay archivos IaC en el diff.
if [ -n "$RANGE" ] && git diff --name-only "$RANGE"..HEAD | grep -qE '\.(tf|yaml|yml)$'; then
  if command -v checkov >/dev/null 2>&1; then
    ejecutados+=("checkov"); echo "  [info] checkov disponible para IaC del diff."
  else
    ausentes+=("checkov (IaC en el diff)")
  fi
fi

echo "-- escáneres ejecutados: ${ejecutados[*]:-ninguno}"
[ ${#ausentes[@]} -gt 0 ] && echo "-- NO instalados (no se asume verde): ${ausentes[*]}"

if [ "$fallos" -ne 0 ]; then
  echo "SECURITY GATE: BLOCK — hay hallazgos Critical/High. Escala a un humano."
  exit 1
fi
echo "SECURITY GATE: PASS (con los escáneres disponibles). No sustituye la revisión humana."
exit 0
