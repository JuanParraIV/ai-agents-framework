#!/usr/bin/env python3
"""PostToolUse hook (Claude Code): emite el audit trail (GOVERNANCE.md §3).

Por cada acción SIGNIFICATIVA de un agente (escritura de archivo, comando git/gh/infra
mutante, o llamada MCP de escritura) escribe una línea JSON en audit/<YYYY-MM-DD>.jsonl.

Principios:
  - Nunca bloquea (siempre exit 0). El logging jamás debe frenar el flujo (fail-open).
  - inputs_redacted: no se almacena el input crudo; el `target` va redactado (****).
  - Enriquecimiento honesto: operator/agent/skill se toman de env (AUDIT_OPERATOR/
    AUDIT_AGENT/AUDIT_SKILL) o de git; si no se conocen, quedan null (no se inventan).

Esquema por registro:
  timestamp · operator · agent · skill · action · target · jira ·
  inputs_redacted · result · approver · gate · tool
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

# --- redacción de posibles secretos en el target ---
_REDACT = [
    re.compile(r"-----BEGIN[^-]*PRIVATE KEY-----"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"(?i)(password|secret|token|api[_-]?key)\s*[:=]\s*\S+"),
]

# Verbos MCP de solo-lectura → no significativos.
_MCP_READONLY = ("get_", "get", "search", "list", "read", "download", "profile",
                 "transitions", "watchers", "_me", "field", "board", "sprint_issues")

# Patrones Bash mutantes → (substring, etiqueta de acción).
_BASH_ACCIONES = [
    ("git commit", "commit"),
    ("git push", "push"),
    ("git checkout -b", "create_branch"),
    ("git tag", "tag"),
    ("gh pr create", "open_pull_request"),
    ("gh pr merge", "merge_pull_request"),
    ("docker build", "container_build"),
    ("terraform apply", "terraform_apply"),
    ("terraform plan", "terraform_plan"),
    ("kubectl apply", "kubectl_apply"),
    ("helm install", "helm_install"),
    ("helm upgrade", "helm_upgrade"),
]


def redact(s: str) -> str:
    s = str(s)
    for r in _REDACT:
        s = r.sub("****", s)
    return s[:300]


def clasificar(tool: str, cmd: str, tool_input: dict):
    """Devuelve (action, target) si es significativa; None si no lo es."""
    if tool in ("Edit", "MultiEdit", "NotebookEdit"):
        return "modify_file", tool_input.get("file_path") or tool_input.get("notebook_path") or "?"
    if tool == "Write":
        return "create_or_overwrite_file", tool_input.get("file_path") or "?"
    if tool.startswith("mcp__"):
        if any(k in tool for k in _MCP_READONLY):
            return None
        action = tool.split("__")[-1] if "__" in tool else tool
        target = (tool_input.get("issue_key") or tool_input.get("issueIdOrKey")
                  or tool_input.get("repo") or tool_input.get("pullNumber")
                  or tool_input.get("key") or "?")
        return action, str(target)
    if tool == "Bash":
        for sub, label in _BASH_ACCIONES:
            if sub in cmd:
                return label, redact(cmd)
        return None
    return None


def infer_jira(tool_input: dict, cmd: str) -> str:
    for k in ("issue_key", "issueIdOrKey", "issue_id", "key"):
        v = tool_input.get(k)
        if v:
            return str(v)
    try:
        branch = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, timeout=3,
        ).stdout.strip()
    except Exception:
        branch = ""
    m = re.search(r"[A-Z][A-Z0-9]+-\d+", f"{branch} {cmd}")
    return m.group(0) if m else None


def infer_result(resp) -> str:
    if isinstance(resp, dict):
        if resp.get("is_error") or resp.get("error"):
            return "error"
        return "success"
    if resp is None:
        return "unknown"
    return "success"


def git_email() -> str:
    try:
        return subprocess.run(
            ["git", "config", "user.email"], capture_output=True, text=True, timeout=3
        ).stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    tool = data.get("tool_name", "")
    tool_input = data.get("tool_input") or {}
    cmd = tool_input.get("command", "") if tool == "Bash" else ""

    clasif = clasificar(tool, cmd, tool_input)
    if clasif is None:
        return 0
    action, target = clasif

    registro = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "operator": os.environ.get("AUDIT_OPERATOR") or git_email(),
        "agent": os.environ.get("AUDIT_AGENT"),
        "skill": os.environ.get("AUDIT_SKILL"),
        "action": action,
        "target": redact(target),
        "jira": infer_jira(tool_input, cmd),
        "inputs_redacted": True,
        "result": infer_result(data.get("tool_response")),
        "approver": None,
        "gate": None,
        "tool": tool,
    }

    try:
        base = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
        audit_dir = os.path.join(base, "audit")
        os.makedirs(audit_dir, exist_ok=True)
        fname = datetime.now(timezone.utc).strftime("%Y-%m-%d") + ".jsonl"
        with open(os.path.join(audit_dir, fname), "a", encoding="utf-8") as fh:
            fh.write(json.dumps(registro, ensure_ascii=False) + "\n")
    except Exception:
        # fail-open: la auditoría no debe frenar el flujo, pero avisa por stderr.
        sys.stderr.write("aviso: no se pudo escribir el audit trail\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
