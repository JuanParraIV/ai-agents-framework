# Contrato BDD - Historia SCRUM-6 (sub-task [BDD] SCRUM-13)
# Generado desde los Acceptance Criteria en Gherkin de JIRA. Contrato inmutable.
@SCRUM-6
Feature: Autenticacion de usuarios con JWT

  @smoke
  Scenario: Login exitoso con credenciales validas
    Given un usuario registrado y activo con email "user@test.com"
    When envia POST /auth/login con email y password validos
    Then recibe un 200
    And el cuerpo contiene un access token JWT firmado y con expiracion
    And el token incluye el subject del usuario y no expone datos sensibles (PAN, password)

  @security @negative
  Scenario: Credenciales invalidas no revelan si el email existe
    Given un usuario registrado con email "user@test.com"
    When envia POST /auth/login con la password incorrecta
    Then recibe un 401
    And el mensaje de error es generico y no indica si el email existe

  @security @negative
  Scenario: Email no registrado
    Given no existe ningun usuario con email "fantasma@test.com"
    When envia POST /auth/login con ese email
    Then recibe un 401 con el mismo mensaje generico que una password incorrecta

  @negative
  Scenario: Payload malformado o campos faltantes
    Given una peticion de login sin el campo password
    When envia POST /auth/login
    Then recibe un 400 de validacion
    And ninguna credencial se registra en logs en claro

  @security @negative
  Scenario: Bloqueo por fuerza bruta (fail-closed)
    Given un usuario que ha superado el numero maximo de intentos fallidos permitidos
    When intenta un nuevo login aunque las credenciales sean correctas
    Then recibe un 429 Too Many Requests
    And el intento queda registrado en el audit trail sin exponer la password

  @security @negative
  Scenario: Usuario inactivo o deshabilitado
    Given un usuario existente cuyo estado es "inactivo"
    When envia POST /auth/login con credenciales correctas
    Then recibe un 403
    And no se emite ningun token
