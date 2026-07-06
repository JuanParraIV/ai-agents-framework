# Contrato BDD - Historia SCRUM-7 (sub-task [BDD] SCRUM-15)
# Generado desde los Acceptance Criteria en Gherkin de JIRA. Contrato inmutable.
@SCRUM-7
Feature: Registro de nuevos usuarios

  @smoke
  Scenario: Registro valido con datos correctos
    Given no existe un usuario con email "nuevo@test.com"
    When envia POST /auth/register con email, password fuerte y datos validos
    Then recibe un 201
    And el usuario queda persistido con la password almacenada solo como hash
    And la respuesta no incluye la password ni el hash

  @negative
  Scenario: Email duplicado
    Given ya existe un usuario con email "nuevo@test.com"
    When intenta registrarse de nuevo con ese email
    Then recibe un 409 Conflict
    And el mensaje no revela datos del usuario existente

  @security @negative
  Scenario: Password que no cumple la politica de seguridad
    Given un registro con una password debil (corta o sin complejidad)
    When envia POST /auth/register
    Then recibe un 400 con el detalle de la politica incumplida
    And no se crea ningun usuario

  @negative
  Scenario: Email con formato invalido
    Given un registro con email "no-es-un-email"
    When envia POST /auth/register
    Then recibe un 400 de validacion

  @negative
  Scenario: Campos obligatorios faltantes
    Given un registro sin el campo email
    When envia POST /auth/register
    Then recibe un 400 indicando el campo faltante

  @security @negative
  Scenario: Payload con campos no permitidos (mass assignment)
    Given un registro que intenta fijar el campo "role" a "admin" o el "balance" inicial
    When envia POST /auth/register
    Then esos campos privilegiados se ignoran o se rechazan
    And el usuario se crea con el rol por defecto y sin saldo manipulado
