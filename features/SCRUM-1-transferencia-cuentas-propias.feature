# Jira: SCRUM-1 (historia) / SCRUM-4 (sub-task BDD)
# Contrato BDD inmutable. Generado por qa-bdd-engineer a partir de los Acceptance
# Criteria aprobados en SCRUM-1 (9 escenarios efectivos). NO modificar una vez Dev
# (SCRUM-5) arranque. Datos enmascarados; sin PAN/CVV reales.

@SCRUM-1 @transferencias
Feature: Transferencia de dinero entre cuentas propias

  Background:
    Given un cliente autenticado en la app
    And el cliente es titular de la cuenta origen "ORIGEN" con saldo disponible de 1000.00 EUR
    And el cliente es titular de la cuenta destino "DESTINO" con saldo disponible de 200.00 EUR

  @smoke @happy-path
  Scenario: Transferencia exitosa entre cuentas propias (happy path)
    When el cliente transfiere 300.00 EUR desde "ORIGEN" hacia "DESTINO"
    Then la transferencia se confirma de forma inmediata
    And el saldo disponible de "ORIGEN" pasa a 700.00 EUR
    And el saldo disponible de "DESTINO" pasa a 500.00 EUR
    And se registra una traza de auditoría con el resultado "EXITOSA" y las cuentas enmascaradas

  @negative
  Scenario: Rechazo por saldo insuficiente
    When el cliente intenta transferir 1500.00 EUR desde "ORIGEN" hacia "DESTINO"
    Then la transferencia es rechazada con el motivo "saldo insuficiente"
    And el saldo disponible de "ORIGEN" permanece en 1000.00 EUR
    And el saldo disponible de "DESTINO" permanece en 200.00 EUR
    And se registra una traza de auditoría con el resultado "RECHAZADA"

  @negative
  Scenario Outline: Rechazo por monto inválido
    When el cliente intenta transferir <monto> EUR desde "ORIGEN" hacia "DESTINO"
    Then la transferencia es rechazada con el motivo "monto inválido"
    And ningún saldo es modificado

    Examples:
      | monto   |
      | 0.00    |
      | -50.00  |

  @negative
  Scenario: Rechazo cuando origen y destino son la misma cuenta
    When el cliente intenta transferir 100.00 EUR desde "ORIGEN" hacia "ORIGEN"
    Then la transferencia es rechazada con el motivo "cuenta origen y destino no pueden ser la misma"
    And ningún saldo es modificado

  @negative @security
  Scenario: Rechazo al operar sobre una cuenta que no es del titular
    Given existe una cuenta "AJENA" que no pertenece al cliente autenticado
    When el cliente intenta transferir 100.00 EUR desde "ORIGEN" hacia "AJENA"
    Then la transferencia es rechazada con el motivo "cuenta no autorizada"
    And ningún saldo es modificado
    And se registra una traza de auditoría del intento no autorizado

  @idempotency
  Scenario: Idempotencia ante reintento con el mismo identificador de operación
    Given el cliente envió una transferencia de 300.00 EUR desde "ORIGEN" hacia "DESTINO" con el identificador de operación "OP-123"
    And esa transferencia ya fue confirmada
    When el cliente reenvía la misma transferencia con el identificador de operación "OP-123"
    Then no se genera un nuevo cargo
    And el saldo disponible de "ORIGEN" permanece en 700.00 EUR
    And la app devuelve el resultado de la transferencia original

  @atomicity
  Scenario: Rollback atómico cuando falla el abono tras el cargo
    When el cliente transfiere 300.00 EUR desde "ORIGEN" hacia "DESTINO"
    And ocurre un fallo en el sistema tras aplicar el cargo y antes de confirmar el abono
    Then la operación se revierte por completo (rollback)
    And el saldo disponible de "ORIGEN" permanece en 1000.00 EUR
    And el saldo disponible de "DESTINO" permanece en 200.00 EUR
    And se registra una traza de auditoría con el resultado "REVERTIDA"

  @negative
  Scenario: Rechazo por monto con precisión decimal inválida
    When el cliente intenta transferir 100.005 EUR desde "ORIGEN" hacia "DESTINO"
    Then la transferencia es rechazada con el motivo "precisión decimal inválida"
    And ningún saldo es modificado
