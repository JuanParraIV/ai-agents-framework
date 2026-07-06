# Contrato BDD - Historia SCRUM-12 (sub-task [BDD] SCRUM-25)
# Generado desde los Acceptance Criteria en Gherkin de JIRA. Contrato inmutable.
@SCRUM-12
Feature: Health check y observabilidad

  @smoke
  Scenario: Liveness OK
    When se consulta GET /health
    Then responde 200 con un cuerpo {"status":"UP"}

  @smoke
  Scenario: Readiness con dependencias sanas
    Given la base de datos y dependencias criticas estan disponibles
    When se consulta GET /health/ready
    Then responde 200 indicando que el servicio esta listo

  @security @negative
  Scenario: Readiness degradado por dependencia caida (fail-closed)
    Given la base de datos NO esta disponible
    When se consulta GET /health/ready
    Then responde 503 indicando la dependencia caida
    And el detalle no expone credenciales, cadenas de conexion ni secretos

  @security
  Scenario: Exposicion de metricas
    When se consulta GET /metrics
    Then responde 200 con metricas en formato de scraping
    And no se exponen datos de negocio, PII ni PAN

  @security
  Scenario: Los endpoints de salud no filtran informacion sensible
    When se consulta cualquier endpoint de health
    Then la respuesta no incluye versiones internas explotables, rutas de infra ni secretos
