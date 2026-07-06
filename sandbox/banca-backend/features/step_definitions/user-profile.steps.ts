import { Given, When, Then } from '@cucumber/cucumber';

// SKELETON - Historia SCRUM-11 (Gestion de perfil). Contrato: user-profile.feature.
// Cada step reporta 'pending'. La logica la implementa Dev en [DEV].
// Guardrail: opera sobre el usuario del token (anti IDOR); whitelist de campos editables;
// email/id/rol/saldo inmutables; nunca devolver password ni hash.
// Nota: el Given generico "un cliente autenticado" vive en common.steps.ts.

Given('un cliente autenticado con rol {string}', function (_rol: string) {
  return 'pending';
});

When('envia GET \\/me', function () {
  return 'pending';
});

When('envia PATCH \\/me con un telefono con formato valido', function () {
  return 'pending';
});

When('envia PATCH \\/me intentando cambiar su email', function () {
  return 'pending';
});

When('envia PATCH \\/me intentando fijar {string}:{string} o {string}', function (_role: string, _admin: string, _balance: string) {
  return 'pending';
});

When('envia PATCH \\/me con un telefono con formato invalido', function () {
  return 'pending';
});

When('envia GET \\/me o PATCH \\/me', function () {
  return 'pending';
});

Then('recibe un {int} con sus datos de perfil', function (_status: number) {
  return 'pending';
});

Then('la respuesta no incluye password, hash ni datos de otros usuarios', function () {
  return 'pending';
});

Then('recibe un {int} con el perfil actualizado', function (_status: number) {
  return 'pending';
});

Then('recibe un {int} \\(el email no es editable por este endpoint)', function (_status: number) {
  return 'pending';
});

Then('el email permanece sin cambios', function () {
  return 'pending';
});

Then('esos campos se ignoran o se rechazan', function () {
  return 'pending';
});

Then('el rol y el saldo permanecen sin cambios', function () {
  return 'pending';
});

Then('recibe un {int} de validacion y el perfil no se altera', function (_status: number) {
  return 'pending';
});
