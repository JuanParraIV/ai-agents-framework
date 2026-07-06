import { Given, Then } from '@cucumber/cucumber';

// SKELETON compartido - Backend de prueba API Banca Digital.
// Steps genericos reutilizados por varias historias (auth y codigos de estado HTTP).
// Cada step reporta 'pending'; la implementacion la aporta el agente Dev en [DEV].
// NO anadir logica de negocio ni aserciones aqui.

const PENDING = 'PENDING: implementar en [DEV]';

// --- Contexto de autenticacion ---

Given('una peticion sin token JWT valido', function () {
  return 'pending'; // ${PENDING}
});

Given('un cliente autenticado', function () {
  return 'pending';
});

Given('un cliente autenticado que NO es propietario de la cuenta {string}', function (_cuenta: string) {
  return 'pending';
});

// --- Codigos de estado HTTP genericos (anclados: no colisionan entre si) ---

Then('recibe un {int}', function (_status: number) {
  return 'pending';
});

Then('recibe un {int} de validacion', function (_status: number) {
  return 'pending';
});

Then('recibe un {int} Unauthorized', function (_status: number) {
  return 'pending';
});

Then('recibe un {int} Forbidden', function (_status: number) {
  return 'pending';
});

Then('recibe un {int} Too Many Requests', function (_status: number) {
  return 'pending';
});

Then('recibe un {int} Conflict', function (_status: number) {
  return 'pending';
});

Then('recibe un {int} Unprocessable Entity', function (_status: number) {
  return 'pending';
});

// Referencia al marcador para trazabilidad (no ejecuta logica).
void PENDING;
