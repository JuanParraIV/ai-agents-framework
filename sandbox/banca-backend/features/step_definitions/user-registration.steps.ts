import { Given, When, Then } from '@cucumber/cucumber';

// SKELETON - Historia SCRUM-7 (Registro de usuarios). Contrato: user-registration.feature.
// Cada step reporta 'pending'. La logica la implementa Dev en [DEV].
// Guardrail: password solo como hash; anti mass-assignment (role/balance).

Given('no existe un usuario con email {string}', function (_email: string) {
  return 'pending';
});

Given('ya existe un usuario con email {string}', function (_email: string) {
  return 'pending';
});

Given('un registro con una password debil \\(corta o sin complejidad)', function () {
  return 'pending';
});

Given('un registro con email {string}', function (_email: string) {
  return 'pending';
});

Given('un registro sin el campo email', function () {
  return 'pending';
});

Given('un registro que intenta fijar el campo {string} a {string} o el {string} inicial', function (_campo: string, _valor: string, _saldo: string) {
  return 'pending';
});

When('envia POST \\/auth\\/register con email, password fuerte y datos validos', function () {
  return 'pending';
});

When('intenta registrarse de nuevo con ese email', function () {
  return 'pending';
});

When('envia POST \\/auth\\/register', function () {
  return 'pending';
});

Then('el usuario queda persistido con la password almacenada solo como hash', function () {
  return 'pending';
});

Then('la respuesta no incluye la password ni el hash', function () {
  return 'pending';
});

Then('el mensaje no revela datos del usuario existente', function () {
  return 'pending';
});

Then('recibe un {int} con el detalle de la politica incumplida', function (_status: number) {
  return 'pending';
});

Then('no se crea ningun usuario', function () {
  return 'pending';
});

Then('recibe un {int} indicando el campo faltante', function (_status: number) {
  return 'pending';
});

Then('esos campos privilegiados se ignoran o se rechazan', function () {
  return 'pending';
});

Then('el usuario se crea con el rol por defecto y sin saldo manipulado', function () {
  return 'pending';
});
