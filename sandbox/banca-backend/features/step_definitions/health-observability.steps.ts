import { Given, When, Then } from '@cucumber/cucumber';

// SKELETON - Historia SCRUM-12 (Health check y observabilidad). Contrato: health-observability.feature.
// Cada step reporta 'pending'. La logica la implementa Dev en [DEV].
// Guardrail: readiness fail-closed (503 si dependencia caida); nunca exponer secretos, PII ni PAN.

Given('la base de datos y dependencias criticas estan disponibles', function () {
  return 'pending';
});

Given('la base de datos NO esta disponible', function () {
  return 'pending';
});

When('se consulta GET \\/health\\/ready', function () {
  return 'pending';
});

When('se consulta GET \\/health', function () {
  return 'pending';
});

When('se consulta GET \\/metrics', function () {
  return 'pending';
});

When('se consulta cualquier endpoint de health', function () {
  return 'pending';
});

// Regex por el cuerpo JSON literal con llaves { } (no compatible con cucumber expressions).
Then(/^responde 200 con un cuerpo \{"status":"UP"\}$/, function () {
  return 'pending';
});

Then('responde {int} indicando que el servicio esta listo', function (_status: number) {
  return 'pending';
});

Then('responde {int} indicando la dependencia caida', function (_status: number) {
  return 'pending';
});

Then('el detalle no expone credenciales, cadenas de conexion ni secretos', function () {
  return 'pending';
});

Then('responde {int} con metricas en formato de scraping', function (_status: number) {
  return 'pending';
});

Then('no se exponen datos de negocio, PII ni PAN', function () {
  return 'pending';
});

Then('la respuesta no incluye versiones internas explotables, rutas de infra ni secretos', function () {
  return 'pending';
});
