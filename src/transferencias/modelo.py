"""Modelo de dominio para transferencias entre cuentas propias (SCRUM-1)."""
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class Cuenta:
    """Cuenta bancaria con saldo disponible. ``es_titular`` indica si pertenece
    al cliente autenticado (control de autorización / least privilege)."""

    alias: str
    saldo_disponible: Decimal
    es_titular: bool = True


@dataclass
class ResultadoTransferencia:
    """Resultado de una operación de transferencia.

    ``estado`` es EXITOSA o REVERTIDA. Los identificadores de cuenta se guardan
    en claro solo en memoria de proceso; en las trazas de auditoría se enmascaran.
    """

    estado: str
    origen: str
    destino: str
    monto: Decimal
    op_id: Optional[str] = None
