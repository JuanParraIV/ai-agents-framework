"""Servicio de transferencias entre cuentas propias (SCRUM-1).

Reglas derivadas del contrato BDD (features/SCRUM-1-...feature):
- Validación de monto: precisión decimal máx. 2 y monto > 0.
- Origen y destino no pueden ser la misma cuenta.
- Solo se opera sobre cuentas del titular autenticado (autorización).
- No se transfiere con saldo insuficiente.
- Idempotencia por identificador de operación.
- Reversión atómica (compensación) ante fallo tras el cargo.
- Toda operación deja traza de auditoría con las cuentas ENMASCARADAS (PCI-DSS).
"""
from decimal import Decimal, InvalidOperation
from typing import Dict, Optional

from .auditoria import LibroAuditoria, enmascarar
from .errores import TransferenciaRechazada
from .modelo import Cuenta, ResultadoTransferencia

_MAX_DECIMALES = 2


class ServicioTransferencias:
    def __init__(self, auditoria: Optional[LibroAuditoria] = None):
        self._cuentas: Dict[str, Cuenta] = {}
        self.auditoria = auditoria or LibroAuditoria()
        self._idempotencia: Dict[str, ResultadoTransferencia] = {}

    # --- configuración de cuentas ---
    def registrar_cuenta(self, alias, saldo, es_titular=True) -> None:
        self._cuentas[alias] = Cuenta(
            alias=alias,
            saldo_disponible=Decimal(str(saldo)),
            es_titular=es_titular,
        )

    def saldo(self, alias) -> Decimal:
        return self._cuentas[alias].saldo_disponible

    def saldos(self) -> Dict[str, Decimal]:
        return {alias: c.saldo_disponible for alias, c in self._cuentas.items()}

    # --- operación principal ---
    def transferir(self, origen, destino, monto, op_id=None) -> ResultadoTransferencia:
        # Idempotencia: un reintento con el mismo op_id devuelve el resultado original.
        if op_id and op_id in self._idempotencia:
            return self._idempotencia[op_id]

        monto_dec = self._validar_monto(monto)
        self._validar_cuentas(origen, destino)

        cuenta_o = self._cuentas[origen]
        cuenta_d = self._cuentas[destino]
        if cuenta_o.saldo_disponible < monto_dec:
            self._auditar("RECHAZADA", origen, destino, motivo="saldo insuficiente")
            raise TransferenciaRechazada("saldo insuficiente")

        # Aplicación atómica del cargo y el abono.
        cuenta_o.saldo_disponible -= monto_dec
        cuenta_d.saldo_disponible += monto_dec

        resultado = ResultadoTransferencia(
            estado="EXITOSA",
            origen=origen,
            destino=destino,
            monto=monto_dec,
            op_id=op_id,
        )
        self._auditar("EXITOSA", origen, destino)
        if op_id:
            self._idempotencia[op_id] = resultado
        return resultado

    def revertir(self, resultado, motivo="fallo del sistema tras el cargo") -> ResultadoTransferencia:
        """Compensa una transferencia ya aplicada, devolviendo los saldos (rollback atómico)."""
        cuenta_o = self._cuentas[resultado.origen]
        cuenta_d = self._cuentas[resultado.destino]
        cuenta_d.saldo_disponible -= resultado.monto
        cuenta_o.saldo_disponible += resultado.monto
        resultado.estado = "REVERTIDA"
        self._auditar("REVERTIDA", resultado.origen, resultado.destino, motivo=motivo)
        return resultado

    # --- validaciones ---
    def _validar_monto(self, monto) -> Decimal:
        try:
            monto_dec = Decimal(str(monto))
        except InvalidOperation:
            raise TransferenciaRechazada("monto inválido")
        if -monto_dec.as_tuple().exponent > _MAX_DECIMALES:
            raise TransferenciaRechazada("precisión decimal inválida")
        if monto_dec <= 0:
            raise TransferenciaRechazada("monto inválido")
        return monto_dec

    def _validar_cuentas(self, origen, destino) -> None:
        if origen == destino:
            raise TransferenciaRechazada("cuenta origen y destino no pueden ser la misma")
        for alias in (origen, destino):
            cuenta = self._cuentas.get(alias)
            if cuenta is None or not cuenta.es_titular:
                self._auditar("RECHAZADA", origen, destino, motivo="cuenta no autorizada")
                raise TransferenciaRechazada("cuenta no autorizada")

    def _auditar(self, resultado, origen, destino, motivo=None) -> None:
        self.auditoria.registrar(
            resultado=resultado,
            origen=enmascarar(origen),
            destino=enmascarar(destino),
            motivo=motivo,
        )
