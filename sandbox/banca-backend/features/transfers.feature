# Contrato BDD - Historia SCRUM-10 (sub-task [BDD] SCRUM-21)
# Generado desde los Acceptance Criteria en Gherkin de JIRA. Contrato inmutable.
@SCRUM-10
Feature: Transferencia entre cuentas

  @smoke
  Scenario: Transferencia con fondos suficientes
    Given una cuenta origen propia con saldo 100.00
    And una cuenta destino valida
    When transfiere 40.00 de la origen a la destino
    Then recibe un 201 con el id de la transaccion
    And la cuenta origen queda con saldo 60.00 y la destino incrementada en 40.00 de forma atomica

  @negative
  Scenario: Fondos insuficientes
    Given una cuenta origen propia con saldo 10.00
    When intenta transferir 40.00
    Then recibe un 422 Unprocessable Entity
    And ningun saldo se altera

  @negative
  Scenario: Importe invalido (cero o negativo)
    Given una cuenta origen propia con saldo 100.00
    When intenta transferir -5.00 o 0.00
    Then recibe un 400 de validacion
    And ningun saldo se altera

  @security @negative
  Scenario: Transferir desde una cuenta que no es propia (BOLA/IDOR)
    Given un cliente autenticado que NO es propietario de la cuenta origen
    When intenta transferir desde esa cuenta
    Then recibe un 403 Forbidden
    And ningun saldo se altera

  @negative
  Scenario: Cuenta destino inexistente
    Given una cuenta origen propia con saldo 100.00
    When intenta transferir a una cuenta destino que no existe
    Then recibe un 404 (o 422) y ningun saldo se altera

  @security
  Scenario: Reintento con la misma clave de idempotencia
    Given una transferencia de 40.00 ya ejecutada con Idempotency-Key "K-1"
    When se reenvia la misma peticion con Idempotency-Key "K-1"
    Then no se ejecuta un segundo debito
    And se devuelve el resultado de la transferencia original

  @security @negative
  Scenario: Peticion sin autenticacion
    Given una peticion sin token JWT valido
    When envia POST /transfers
    Then recibe un 401 Unauthorized
