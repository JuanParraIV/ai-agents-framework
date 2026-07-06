# Contrato BDD - Historia SCRUM-8 (sub-task [BDD] SCRUM-17)
# Generado desde los Acceptance Criteria en Gherkin de JIRA. Contrato inmutable.
@SCRUM-8
Feature: Consulta de saldo de cuenta

  @smoke
  Scenario: Consulta del saldo de una cuenta propia
    Given un cliente autenticado propietario de la cuenta "ACC-100"
    When envia GET /accounts/ACC-100/balance
    Then recibe un 200 con el saldo actual, la moneda y un timestamp

  @security @negative
  Scenario: Acceso a una cuenta ajena (BOLA/IDOR)
    Given un cliente autenticado que NO es propietario de la cuenta "ACC-200"
    When envia GET /accounts/ACC-200/balance
    Then recibe un 403 Forbidden
    And la respuesta no revela si la cuenta existe ni su saldo

  @security @negative
  Scenario: Peticion sin autenticacion
    Given una peticion sin token JWT valido
    When envia GET /accounts/ACC-100/balance
    Then recibe un 401 Unauthorized

  @security @negative
  Scenario: Token expirado o invalido (fail-closed)
    Given un cliente con un token JWT expirado
    When envia GET /accounts/ACC-100/balance
    Then recibe un 401 y no se devuelve ningun dato de saldo

  @negative
  Scenario: Cuenta inexistente
    Given un cliente autenticado
    When consulta el saldo de una cuenta que no existe
    Then recibe un 404 (o 403 uniforme para no revelar existencia)
    And no se filtra informacion de otras cuentas
