import { setWorldConstructor, World, IWorldOptions } from '@cucumber/cucumber';

// World compartido entre steps. De momento solo transporta estado de peticion/respuesta
// para que el agente Dev lo rellene al implementar los steps. NO contiene logica de negocio.
export class BancaWorld extends World {
  // Peticion en construccion (headers, body, endpoint) - lo rellena Dev.
  public request: Record<string, unknown> = {};
  // Respuesta HTTP capturada tras ejecutar la peticion - lo rellena Dev.
  public response: { status?: number; body?: unknown } = {};

  constructor(options: IWorldOptions) {
    super(options);
  }
}

setWorldConstructor(BancaWorld);
