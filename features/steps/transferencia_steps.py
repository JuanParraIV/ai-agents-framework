# Jira: SCRUM-1 (historia) / SCRUM-4 (sub-task BDD) / SCRUM-5 (DEV)
#
# Step definitions para el contrato BDD de "Transferencia de dinero entre cuentas
# propias". Implementados por el rol Developer (SCRUM-5) contra el servicio de
# dominio en src/transferencias/. El .feature es INMUTABLE: aquí no se altera el
# contrato, solo se enlaza con la implementación.
#
# Convenciones de datos:
#   - Cuentas y montos son datos de prueba; los identificadores reales / PAN nunca
#     aparecen aquí. Las trazas de auditoría enmascaran las cuentas (****).

from decimal import Decimal

from behave import given, when, then

from transferencias.errores import TransferenciaRechazada
from transferencias.servicio import ServicioTransferencias


# ---------------------------------------------------------------------------
# Background / contexto del titular y sus cuentas
# ---------------------------------------------------------------------------

@given('un cliente autenticado en la app')
def step_cliente_autenticado(context):
    context.servicio = ServicioTransferencias()
    context.cliente_autenticado = True
    context.error = None
    context.resultado = None
    context.resultado_original = None
    context.ultima_transferencia = None
    context.snapshot = {}


@given('el cliente es titular de la cuenta origen "{cuenta}" con saldo disponible de {saldo} EUR')
def step_titular_cuenta_origen(context, cuenta, saldo):
    context.servicio.registrar_cuenta(cuenta, saldo, es_titular=True)


@given('el cliente es titular de la cuenta destino "{cuenta}" con saldo disponible de {saldo} EUR')
def step_titular_cuenta_destino(context, cuenta, saldo):
    context.servicio.registrar_cuenta(cuenta, saldo, es_titular=True)


@given('existe una cuenta "{cuenta}" que no pertenece al cliente autenticado')
def step_cuenta_ajena(context, cuenta):
    context.servicio.registrar_cuenta(cuenta, "0.00", es_titular=False)


@given('el cliente envió una transferencia de {monto} EUR desde "{origen}" hacia "{destino}" con el identificador de operación "{op_id}"')
def step_transferencia_previa(context, monto, origen, destino, op_id):
    context.resultado_original = context.servicio.transferir(origen, destino, monto, op_id=op_id)
    context.ultima_transferencia = {"origen": origen, "destino": destino, "monto": monto, "op_id": op_id}


@given('esa transferencia ya fue confirmada')
def step_transferencia_confirmada(context):
    assert context.resultado_original is not None
    assert context.resultado_original.estado == "EXITOSA"


# ---------------------------------------------------------------------------
# Acciones (When / And derivado de When)
# ---------------------------------------------------------------------------

@when('el cliente transfiere {monto} EUR desde "{origen}" hacia "{destino}"')
def step_transfiere(context, monto, origen, destino):
    context.snapshot = context.servicio.saldos()
    context.error = None
    context.resultado = context.servicio.transferir(origen, destino, monto)


@when('el cliente intenta transferir {monto} EUR desde "{origen}" hacia "{destino}"')
def step_intenta_transferir(context, monto, origen, destino):
    context.snapshot = context.servicio.saldos()
    context.resultado = None
    context.error = None
    try:
        context.resultado = context.servicio.transferir(origen, destino, monto)
    except TransferenciaRechazada as exc:
        context.error = exc


@when('el cliente reenvía la misma transferencia con el identificador de operación "{op_id}"')
def step_reenvia_transferencia(context, op_id):
    t = context.ultima_transferencia
    context.snapshot = context.servicio.saldos()
    context.resultado = context.servicio.transferir(t["origen"], t["destino"], t["monto"], op_id=op_id)


@when('ocurre un fallo en el sistema tras aplicar el cargo y antes de confirmar el abono')
def step_fallo_tras_cargo(context):
    context.resultado = context.servicio.revertir(context.resultado)


# ---------------------------------------------------------------------------
# Resultados / aserciones (Then / And derivado de Then)
# ---------------------------------------------------------------------------

@then('la transferencia se confirma de forma inmediata')
def step_confirma_inmediata(context):
    assert context.error is None, f"transferencia rechazada inesperadamente: {context.error}"
    assert context.resultado is not None
    assert context.resultado.estado == "EXITOSA"


@then('el saldo disponible de "{cuenta}" pasa a {saldo} EUR')
def step_saldo_pasa_a(context, cuenta, saldo):
    assert context.servicio.saldo(cuenta) == Decimal(saldo), \
        f"saldo de {cuenta}: esperado {saldo}, real {context.servicio.saldo(cuenta)}"


@then('el saldo disponible de "{cuenta}" permanece en {saldo} EUR')
def step_saldo_permanece(context, cuenta, saldo):
    assert context.servicio.saldo(cuenta) == Decimal(saldo), \
        f"saldo de {cuenta}: esperado {saldo}, real {context.servicio.saldo(cuenta)}"


@then('se registra una traza de auditoría con el resultado "{resultado}" y las cuentas enmascaradas')
def step_auditoria_resultado_enmascarado(context, resultado):
    entradas = context.servicio.auditoria.con_resultado(resultado)
    assert entradas, f"no hay traza de auditoría con resultado {resultado}"
    e = entradas[-1]
    assert "*" in e.origen and "*" in e.destino, "las cuentas no están enmascaradas en la traza"


@then('se registra una traza de auditoría con el resultado "{resultado}"')
def step_auditoria_resultado(context, resultado):
    assert context.servicio.auditoria.con_resultado(resultado), \
        f"no hay traza de auditoría con resultado {resultado}"


@then('se registra una traza de auditoría del intento no autorizado')
def step_auditoria_no_autorizado(context):
    assert context.servicio.auditoria.con_motivo("cuenta no autorizada"), \
        "no hay traza de auditoría del intento no autorizado"


@then('la transferencia es rechazada con el motivo "{motivo}"')
def step_rechazada_con_motivo(context, motivo):
    assert context.error is not None, "se esperaba un rechazo y no ocurrió"
    assert context.error.motivo == motivo, \
        f"motivo esperado '{motivo}', real '{context.error.motivo}'"


@then('ningún saldo es modificado')
def step_ningun_saldo_modificado(context):
    assert context.servicio.saldos() == context.snapshot, "algún saldo fue modificado"


@then('no se genera un nuevo cargo')
def step_no_nuevo_cargo(context):
    assert context.servicio.saldos() == context.snapshot, "se generó un cargo adicional"


@then('la app devuelve el resultado de la transferencia original')
def step_devuelve_resultado_original(context):
    assert context.resultado is context.resultado_original, \
        "no se devolvió el resultado de la transferencia original"


@then('la operación se revierte por completo (rollback)')
def step_operacion_revertida(context):
    assert context.resultado is not None
    assert context.resultado.estado == "REVERTIDA"
