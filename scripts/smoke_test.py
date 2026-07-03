#!/usr/bin/env python3
"""Smoke test de integridad del framework (TB-4).

Valida que las referencias entre capas no estén rotas (evita la "deriva entre skills
y agentes" que lista ARCHITECTURE.md §8):

  ERROR (exit 1):
    - Un agente referencia una skill que no existe.
    - El `name:` de una skill no coincide con su directorio.
    - Un hook declarado en .claude/settings.json apunta a un script inexistente.
    - .mcp.json o .claude/settings.json no son JSON válidos.

  WARN (no falla):
    - Un agente/skill referencia un server MCP no presente en .mcp.json
      (típicamente un server de una fase futura, p.ej. semgrep en F3).
    - Advertencias operativas (p.ej. endpoint del MCP de GitHub).

Uso:  python3 scripts/smoke_test.py
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

errores = []
warnings = []


def rel(p):
    return os.path.relpath(p, ROOT)


def frontmatter(path):
    txt = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n", txt, re.DOTALL)
    fm = m.group(1) if m else ""
    return fm, txt


def campo(fm, clave):
    m = re.search(rf"^{clave}:\s*(.+)$", fm, re.MULTILINE)
    return m.group(1).strip() if m else ""


def mcp_servers_ref(texto):
    return set(re.findall(r"mcp__([a-z0-9-]+)__", texto))


# --- 1. Cargar configuración ---
try:
    mcp_cfg = json.load(open(os.path.join(ROOT, ".mcp.json"), encoding="utf-8"))
    servers = set((mcp_cfg.get("mcpServers") or {}).keys())
except Exception as e:
    errores.append(f".mcp.json no es JSON válido: {e}")
    servers = set()

try:
    settings = json.load(open(os.path.join(ROOT, ".claude/settings.json"), encoding="utf-8"))
except Exception as e:
    errores.append(f".claude/settings.json no es JSON válido: {e}")
    settings = {}

# --- 2. Inventario de skills ---
skills = {}  # name -> path
for sk in glob.glob(os.path.join(ROOT, ".claude/skills/*/*/SKILL.md")):
    fm, txt = frontmatter(sk)
    name = campo(fm, "name")
    dirname = os.path.basename(os.path.dirname(sk))
    if not name:
        errores.append(f"skill sin `name:` → {rel(sk)}")
        continue
    if name != dirname:
        errores.append(f"skill `name: {name}` no coincide con su carpeta '{dirname}' → {rel(sk)}")
    skills[name] = sk
    for srv in mcp_servers_ref(campo(fm, "allowed-tools")):
        if srv not in servers:
            warnings.append(f"skill '{name}' referencia MCP no configurado: mcp__{srv}__* ({rel(sk)})")

# --- 3. Agentes: skills referenciadas + MCP ---
for ag in glob.glob(os.path.join(ROOT, ".claude/agents/*.md")):
    fm, txt = frontmatter(ag)
    cuerpo = txt[len(fm):] if fm else txt
    # skills referenciadas como `/skill-name` en backticks
    for ref in set(re.findall(r"`/([a-z][a-z0-9-]+)`", cuerpo)):
        if ref not in skills:
            errores.append(f"agente '{rel(ag)}' referencia skill inexistente: /{ref}")
    # MCP en frontmatter tools
    for srv in mcp_servers_ref(campo(fm, "tools")):
        if srv not in servers:
            warnings.append(f"agente '{rel(ag)}' referencia MCP no configurado: mcp__{srv}__*")

# --- 4. Hooks declarados en settings.json apuntan a scripts existentes ---
hooks = settings.get("hooks", {})
for evento, grupos in hooks.items():
    for grupo in grupos:
        for h in grupo.get("hooks", []):
            cmd = h.get("command", "")
            for m in re.finditer(r'\$CLAUDE_PROJECT_DIR/(\S+?\.py)', cmd):
                script = os.path.join(ROOT, m.group(1))
                if not os.path.exists(script):
                    errores.append(f"hook {evento} apunta a script inexistente: {m.group(1)}")

# --- 5. Advertencia operativa: endpoint del MCP de GitHub ---
gh = (mcp_cfg.get("mcpServers", {}) if servers else {}).get("github", {})
if "githubcopilot.com" in json.dumps(gh):
    warnings.append("MCP 'github' usa api.githubcopilot.com/mcp/ — verificar conectividad/"
                    "scopes del token (ver RUNBOOK-F1); evaluar fallback (gh CLI / server oficial).")

# --- Reporte ---
print(f"Skills detectadas: {len(skills)}  | Servers MCP configurados: {sorted(servers)}")
for w in warnings:
    print(f"  WARN  {w}")
for e in errores:
    print(f"  ERROR {e}")

if errores:
    print(f"\nSMOKE TEST FAILED — {len(errores)} error(es), {len(warnings)} warning(s).")
    sys.exit(1)
print(f"\nSMOKE TEST OK — 0 errores, {len(warnings)} warning(s). Referencias íntegras.")
sys.exit(0)
