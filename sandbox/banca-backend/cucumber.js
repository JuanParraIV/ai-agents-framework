// Cucumber.js configuration - Backend de prueba API Banca Digital
// Los .feature son el contrato (AC de JIRA). Los steps son SKELETONS: reportan
// 'pending' hasta que el agente Dev implemente la logica de negocio.
module.exports = {
  default: {
    requireModule: ['ts-node/register'],
    require: [
      'features/step_definitions/**/*.ts',
      'features/support/**/*.ts'
    ],
    paths: ['features/**/*.feature'],
    format: ['progress']
  }
};
