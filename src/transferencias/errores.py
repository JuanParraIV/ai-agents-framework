"""Errores de dominio para el servicio de transferencias."""


class TransferenciaRechazada(Exception):
    """La transferencia no cumple una regla de negocio y es rechazada.

    El ``motivo`` es el texto exacto del contrato BDD (p.ej. "saldo insuficiente").
    """

    def __init__(self, motivo: str):
        super().__init__(motivo)
        self.motivo = motivo
