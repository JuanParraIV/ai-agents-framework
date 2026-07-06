# Contrato BDD - Historia SCRUM-9 (sub-task [BDD] SCRUM-19)
# Generado desde los Acceptance Criteria en Gherkin de JIRA. Contrato inmutable.
@SCRUM-9
Feature: Listado de transacciones de una cuenta

  @smoke
  Scenario: Historial paginado ordenado por fecha
    Given una cuenta propia con multiples transacciones
    When envia GET /accounts/ACC-100/transactions?page=1&size=20
    Then recibe un 200 con la lista paginada ordenada por fecha descendente
    And la respuesta incluye metadatos de paginacion (total, page, size)

  Scenario: Cuenta sin transacciones
    Given una cuenta propia recien creada sin movimientos
    When consulta sus transacciones
    Then recibe un 200 con una lista vacia y total 0

  @security @negative
  Scenario: Acceso a transacciones de una cuenta ajena (BOLA/IDOR)
    Given un cliente autenticado que NO es propietario de la cuenta "ACC-200"
    When envia GET /accounts/ACC-200/transactions
    Then recibe un 403 Forbidden sin revelar movimientos

  @security @negative
  Scenario: Peticion sin autenticacion
    Given una peticion sin token JWT valido
    When envia GET /accounts/ACC-100/transactions
    Then recibe un 401 Unauthorized

  @negative
  Scenario: Parametros de paginacion invalidos
    Given una peticion con size negativo o excesivamente grande
    When envia GET /accounts/ACC-100/transactions?page=0&size=100000
    Then recibe un 400, o el size se acota al maximo permitido

  @security
  Scenario: Enmascaramiento de datos sensibles
    Given transacciones que referencian una tarjeta
    When se listan las transacciones
    Then cualquier PAN se muestra truncado (solo ultimos 4 digitos) y nunca completo
