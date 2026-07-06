# Contrato BDD - Historia SCRUM-11 (sub-task [BDD] SCRUM-23)
# Generado desde los Acceptance Criteria en Gherkin de JIRA. Contrato inmutable.
@SCRUM-11
Feature: Gestion de perfil de usuario

  @smoke
  Scenario: Consulta del perfil propio
    Given un cliente autenticado
    When envia GET /me
    Then recibe un 200 con sus datos de perfil
    And la respuesta no incluye password, hash ni datos de otros usuarios

  Scenario: Actualizacion de datos de contacto validos
    Given un cliente autenticado
    When envia PATCH /me con un telefono con formato valido
    Then recibe un 200 con el perfil actualizado

  @negative
  Scenario: Intento de modificar un campo inmutable (email)
    Given un cliente autenticado
    When envia PATCH /me intentando cambiar su email
    Then recibe un 400 (el email no es editable por este endpoint)
    And el email permanece sin cambios

  @security @negative
  Scenario: Intento de escalada de privilegios (campos privilegiados)
    Given un cliente autenticado con rol "user"
    When envia PATCH /me intentando fijar "role":"admin" o "balance"
    Then esos campos se ignoran o se rechazan
    And el rol y el saldo permanecen sin cambios

  @negative
  Scenario: Dato con formato invalido
    Given un cliente autenticado
    When envia PATCH /me con un telefono con formato invalido
    Then recibe un 400 de validacion y el perfil no se altera

  @security @negative
  Scenario: Peticion sin autenticacion
    Given una peticion sin token JWT valido
    When envia GET /me o PATCH /me
    Then recibe un 401 Unauthorized
