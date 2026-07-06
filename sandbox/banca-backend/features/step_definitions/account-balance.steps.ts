import { Given, When, Then } from '@cucumber/cucumber';

// SKELETON - Historia SCRUM-8 (Consulta de saldo). Contrato: account-balance.feature.
// Cada step reporta 'pending'. La logica la implementa Dev en [DEV].
// Guardrail: autorizacion a nivel de objeto (BOLA/IDOR) fail-closed; PAN nunca en claro.

Given('un cliente autenticado propietario de la cuenta {string}', function (_cuenta: string) {
  return 'pending';
});

Given('un cliente con un token JWT expirado', function () {
  return 'pending';
});

When('envia GET \\/accounts\\/ACC-100\\/balance', function () {
  return 'pending';
});

When('envia GET \\/accounts\\/ACC-200\\/balance', function () {
  return 'pending';
});

When('consulta el saldo de una cuenta que no existe', function () {
  return 'pending';
});

Then('recibe un {int} con el saldo actual, la moneda y un timestamp', function (_status: number) {
  return 'pending';
});

Then('la respuesta no revela si la cuenta existe ni su saldo', function () {
  return 'pending';
});

Then('recibe un {int} y no se devuelve ningun dato de saldo', function (_status: number) {
  return 'pending';
});

Then('recibe un {int} \\(o 403 uniforme para no revelar existencia)', function (_status: number) {
  return 'pending';
});

Then('no se filtra informacion de otras cuentas', function () {
  return 'pending';
});
