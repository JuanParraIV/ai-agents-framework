"""Libro de auditoría para transferencias (traza inmutable, cuentas enmascaradas).

Cumple el requisito bancario de dejar traza de cada operación sin exponer
identificadores de cuenta/PAN (PCI-DSS): las cuentas se enmascaran antes de registrar.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional


def enmascarar(valor: str) -> str:
    """Enmascara un identificador dejando visibles solo los 2 últimos caracteres."""
    s = str(valor)
    if len(s) <= 2:
        return "*" * len(s)
    return "*" * (len(s) - 2) + s[-2:]


@dataclass
class RegistroAuditoria:
    resultado: str            # EXITOSA | RECHAZADA | REVERTIDA
    origen: str               # enmascarado
    destino: str              # enmascarado
    motivo: Optional[str]
    timestamp: str


class LibroAuditoria:
    """Colección append-only de registros de auditoría."""

    def __init__(self):
        self._registros: List[RegistroAuditoria] = []

    def registrar(self, resultado, origen, destino, motivo=None):
        self._registros.append(
            RegistroAuditoria(
                resultado=resultado,
                origen=origen,
                destino=destino,
                motivo=motivo,
                timestamp=datetime.now(timezone.utc).isoformat(),
            )
        )

    @property
    def registros(self) -> List[RegistroAuditoria]:
        return list(self._registros)

    def con_resultado(self, resultado) -> List[RegistroAuditoria]:
        return [r for r in self._registros if r.resultado == resultado]

    def con_motivo(self, motivo) -> List[RegistroAuditoria]:
        return [r for r in self._registros if r.motivo == motivo]
