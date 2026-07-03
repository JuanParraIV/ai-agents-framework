#!/usr/bin/env python3
"""PreToolUse hook (Claude Code): impide MODIFICAR un .feature existente.

Enforcement mecánico del guardrail CLAUDE.md §1.5 / GOVERNANCE (contrato BDD
inmutable). QA puede CREAR un .feature nuevo (Write a ruta inexistente); nadie
puede sobrescribirlo o editarlo una vez existe.

Protocolo: lee el evento PreToolUse como JSON por stdin. Si la acción modifica
un .feature existente, sale con código 2 (bloquea) y explica el motivo por stderr.
"""
import json
import os
import sys


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0  # sin payload válido, no bloquea (fail-open solo para el parser)

    tool = data.get("tool_name", "")
    tool_input = data.get("tool_input") or {}
    path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""

    if not path.endswith(".feature"):
        return 0

    modifica = tool in ("Edit", "MultiEdit", "NotebookEdit") or (
        tool == "Write" and os.path.exists(path)
    )
    if modifica:
        sys.stderr.write(
            f"BLOQUEADO: '{path}' es un contrato BDD inmutable (CLAUDE.md §1.5). "
            "El .feature no se modifica una vez existe. Si el contrato es incorrecto, "
            "detente y escala a QA (qa-bdd-engineer) para regenerarlo.\n"
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
