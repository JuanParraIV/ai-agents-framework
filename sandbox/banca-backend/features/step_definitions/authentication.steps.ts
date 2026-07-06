import { Given, When, Then } from '@cucumber/cucumber';

// SKELETON - Historia SCRUM-6 (Autenticacion con JWT). Contrato: authentication.feature.
// Cada step reporta 'pending'. La logica la implementa Dev en [DEV].
// Guardrail: ninguna credencial/PAN real; la password nunca en claro en logs.

Given('un usuario registrado y activo con email {string}', function (_email: string) {
  return 'pending';
});

Given('un usuario registrado con email {string}', function (_email: string) {
  return 'pending';
});

Given('no existe ningun usuario con email {string}', function (_email: string) {
  return 'pending';
});

Given('una peticion de login sin el campo password', function () {
  return 'pending';
});

Given('un usuario que ha superado el numero maximo de intentos fallidos permitidos', function () {
  return 'pending';
});

Given('un usuario existente cuyo estado es {string}', function (_estado: string) {
  return 'pending';
});

When('envia POST \\/auth\\/login con email y password validos', function () {
  return 'pending';
});

When('envia POST \\/auth\\/login con la password incorrecta', function () {
  return 'pending';
});

When('envia POST \\/auth\\/login con ese email', function () {
  return 'pending';
});

When('envia POST \\/auth\\/login con credenciales correctas', function () {
  return 'pending';
});

When('envia POST \\/auth\\/login', function () {
  return 'pending';
});

When('intenta un nuevo login aunque las credenciales sean correctas', function () {
  return 'pending';
});

Then('el cuerpo contiene un access token JWT firmado y con expiracion', function () {
  return 'pending';
});

Then('el token incluye el subject del usuario y no expone datos sensibles \\(PAN, password)', function () {
  return 'pending';
});

Then('el mensaje de error es generico y no indica si el email existe', function () {
  return 'pending';
});

Then('recibe un {int} con el mismo mensaje generico que una password incorrecta', function (_status: number) {
  return 'pending';
});

Then('ninguna credencial se registra en logs en claro', function () {
  return 'pending';
});

Then('el intento queda registrado en el audit trail sin exponer la password', function () {
  return 'pending';
});

Then('no se emite ningun token', function () {
  return 'pending';
});
