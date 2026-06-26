# Jira: SCRUM-1 (historia) / SCRUM-4 (sub-task BDD)
#
# Step definitions SKELETON para el contrato BDD de "Transferencia de dinero entre
# cuentas propias". Generado por qa-bdd-engineer.
#
# IMPORTANTE (gobierno SoD / BDD-first):
#   - Estos steps son ESQUELETOS pendientes de implementar por el developer (SCRUM-5).
#   - Cada cuerpo lanza NotImplementedError("pending: SCRUM-5") a propósito.
#   - NO contienen lógica de negocio ni aserciones reales.
#   - El dry-run de behave valida que todos los steps estén enlazados (0 undefined).
#
# Convenciones de datos:
#   - Cuentas y montos son datos de prueba; los identificadores de cuenta/PAN reales
#     NUNCA se incluyen aquí. En la implementación, enmascarar (****) en trazas/logs.

from behave import given, when, then

_PENDING = "pending: implementar en SCRUM-5 (DEV)"


# ---------------------------------------------------------------------------
# Background / contexto del titular y sus cuentas
# ---------------------------------------------------------------------------

@given('un cliente autenticado en la app')
def step_cliente_autenticado(context):
    raise NotImplementedError(_PENDING)


@given('el cliente es titular de la cuenta origen "{cuenta}" con saldo disponible de {saldo} EUR')
def step_titular_cuenta_origen(context, cuenta, saldo):
    raise NotImplementedError(_PENDING)


@given('el cliente es titular de la cuenta destino "{cuenta}" con saldo disponible de {saldo} EUR')
def step_titular_cuenta_destino(context, cuenta, saldo):
    raise NotImplementedError(_PENDING)


@given('existe una cuenta "{cuenta}" que no pertenece al cliente autenticado')
def step_cuenta_ajena(context, cuenta):
    raise NotImplementedError(_PENDING)


@given('el cliente envió una transferencia de {monto} EUR desde "{origen}" hacia "{destino}" con el identificador de operación "{op_id}"')
def step_transferencia_previa(context, monto, origen, destino, op_id):
    raise NotImplementedError(_PENDING)


@given('esa transferencia ya fue confirmada')
def step_transferencia_confirmada(context):
    raise NotImplementedError(_PENDING)


# ---------------------------------------------------------------------------
# Acciones (When / And derivado de When)
# ---------------------------------------------------------------------------

@when('el cliente transfiere {monto} EUR desde "{origen}" hacia "{destino}"')
def step_transfiere(context, monto, origen, destino):
    raise NotImplementedError(_PENDING)


@when('el cliente intenta transferir {monto} EUR desde "{origen}" hacia "{destino}"')
def step_intenta_transferir(context, monto, origen, destino):
    raise NotImplementedError(_PENDING)


@when('el cliente reenvía la misma transferencia con el identificador de operación "{op_id}"')
def step_reenvia_transferencia(context, op_id):
    raise NotImplementedError(_PENDING)


@when('ocurre un fallo en el sistema tras aplicar el cargo y antes de confirmar el abono')
def step_fallo_tras_cargo(context):
    raise NotImplementedError(_PENDING)


# ---------------------------------------------------------------------------
# Resultados / aserciones (Then / And derivado de Then)
# ---------------------------------------------------------------------------

@then('la transferencia se confirma de forma inmediata')
def step_confirma_inmediata(context):
    raise NotImplementedError(_PENDING)


@then('el saldo disponible de "{cuenta}" pasa a {saldo} EUR')
def step_saldo_pasa_a(context, cuenta, saldo):
    raise NotImplementedError(_PENDING)


@then('el saldo disponible de "{cuenta}" permanece en {saldo} EUR')
def step_saldo_permanece(context, cuenta, saldo):
    raise NotImplementedError(_PENDING)


@then('se registra una traza de auditoría con el resultado "{resultado}" y las cuentas enmascaradas')
def step_auditoria_resultado_enmascarado(context, resultado):
    raise NotImplementedError(_PENDING)


@then('se registra una traza de auditoría con el resultado "{resultado}"')
def step_auditoria_resultado(context, resultado):
    raise NotImplementedError(_PENDING)


@then('se registra una traza de auditoría del intento no autorizado')
def step_auditoria_no_autorizado(context):
    raise NotImplementedError(_PENDING)


@then('la transferencia es rechazada con el motivo "{motivo}"')
def step_rechazada_con_motivo(context, motivo):
    raise NotImplementedError(_PENDING)


@then('ningún saldo es modificado')
def step_ningun_saldo_modificado(context):
    raise NotImplementedError(_PENDING)


@then('no se genera un nuevo cargo')
def step_no_nuevo_cargo(context):
    raise NotImplementedError(_PENDING)


@then('la app devuelve el resultado de la transferencia original')
def step_devuelve_resultado_original(context):
    raise NotImplementedError(_PENDING)


@then('la operación se revierte por completo (rollback)')
def step_operacion_revertida(context):
    raise NotImplementedError(_PENDING)
