#!/usr/bin/env python3
"""Secret-scan del diff en staging. Enforcement de CLAUDE.md §2/§5 (nunca commitear
secretos, credenciales, PAN/CVV).

Dos modos:
  - Sin args: hook PreToolUse de Claude Code (lee JSON por stdin). Solo actúa si el
    comando Bash es un `git commit`; escanea el diff staged y bloquea (exit 2) si hay hallazgos.
  - `--staged`: modo git pre-commit; escanea el diff staged y bloquea (exit 1) si hay hallazgos.

Nunca imprime el valor del secreto: solo la categoría y el archivo (redacted).
"""
import json
import re
import subprocess
import sys

# (patrón, etiqueta). Se aplican solo a líneas AÑADIDAS del diff staged.
_PATRONES = [
    (re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----"), "private key"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "aws access key id"),
    (re.compile(r"(?i)aws_secret_access_key\s*[:=]\s*\S+"), "aws secret access key"),
    (re.compile(r"ghp_[A-Za-z0-9]{36}"), "github token"),
    (re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}"), "github token"),
    (re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"), "slack token"),
    (re.compile(r"(?i)(api[_-]?key|secret|token|passwd|password)\s*[:=]\s*[\"']?[A-Za-z0-9/+_\-]{16,}"), "credential"),
    (re.compile(r"(?i)\bcvv\b\s*[:=]\s*\d{3,4}"), "CVV"),
]

_PAN = re.compile(r"(?<!\d)(?:\d[ -]?){13,19}(?!\d)")


def _luhn_ok(num: str) -> bool:
    digits = [int(c) for c in num]
    total = 0
    par = False
    for d in reversed(digits):
        if par:
            d *= 2
            if d > 9:
                d -= 9
        total += d
        par = not par
    return total % 10 == 0


def scan(text: str):
    hits = set()
    for regex, etiqueta in _PATRONES:
        if regex.search(text):
            hits.add(etiqueta)
    for m in _PAN.finditer(text):
        digits = re.sub(r"[ -]", "", m.group())
        if 13 <= len(digits) <= 19 and _luhn_ok(digits):
            hits.add("possible PAN (Luhn)")
    return sorted(hits)


def staged_added_text() -> str:
    try:
        diff = subprocess.run(
            ["git", "diff", "--cached", "-U0"], capture_output=True, text=True
        ).stdout
    except Exception:
        return ""
    return "\n".join(
        line[1:] for line in diff.splitlines()
        if line.startswith("+") and not line.startswith("+++")
    )


def _report_and_block(hits, block_code: int) -> int:
    sys.stderr.write(
        "BLOQUEADO por secret-scan (CLAUDE.md §2/§5). Posibles secretos en el diff staged: "
        + ", ".join(hits)
        + ".\nRedacta el valor (****) o usa Vault/variable de entorno; NO lo commitees.\n"
    )
    return block_code


def main() -> int:
    if "--staged" in sys.argv:
        hits = scan(staged_added_text())
        return _report_and_block(hits, 1) if hits else 0

    # modo hook Claude Code
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if data.get("tool_name") != "Bash":
        return 0
    cmd = (data.get("tool_input") or {}).get("command", "")
    if "git commit" not in cmd:
        return 0
    hits = scan(staged_added_text())
    return _report_and_block(hits, 2) if hits else 0


if __name__ == "__main__":
    sys.exit(main())
