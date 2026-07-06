import { Given, When, Then } from '@cucumber/cucumber';

// SKELETON - Historia SCRUM-9 (Listado de transacciones). Contrato: account-transactions.feature.
// Cada step reporta 'pending'. La logica la implementa Dev en [DEV].
// Guardrail: BOLA/IDOR fail-closed; PAN truncado (ultimos 4); limite maximo de size.

Given('una cuenta propia con multiples transacciones', function () {
  return 'pending';
});

Given('una cuenta propia recien creada sin movimientos', function () {
  return 'pending';
});

Given('una peticion con size negativo o excesivamente grande', function () {
  return 'pending';
});

Given('transacciones que referencian una tarjeta', function () {
  return 'pending';
});

When('envia GET \\/accounts\\/ACC-100\\/transactions?page=1&size=20', function () {
  return 'pending';
});

When('consulta sus transacciones', function () {
  return 'pending';
});

When('envia GET \\/accounts\\/ACC-200\\/transactions', function () {
  return 'pending';
});

When('envia GET \\/accounts\\/ACC-100\\/transactions', function () {
  return 'pending';
});

When('envia GET \\/accounts\\/ACC-100\\/transactions?page=0&size=100000', function () {
  return 'pending';
});

When('se listan las transacciones', function () {
  return 'pending';
});

Then('recibe un {int} con la lista paginada ordenada por fecha descendente', function (_status: number) {
  return 'pending';
});

Then('la respuesta incluye metadatos de paginacion \\(total, page, size)', function () {
  return 'pending';
});

Then('recibe un {int} con una lista vacia y total 0', function (_status: number) {
  return 'pending';
});

Then('recibe un {int} Forbidden sin revelar movimientos', function (_status: number) {
  return 'pending';
});

Then('recibe un {int}, o el size se acota al maximo permitido', function (_status: number) {
  return 'pending';
});

Then('cualquier PAN se muestra truncado \\(solo ultimos 4 digitos) y nunca completo', function () {
  return 'pending';
});
