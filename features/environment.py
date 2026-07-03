# Jira: SCRUM-1 / SCRUM-4 / SCRUM-5
#
# Hooks de behave. Añade src/ al path de import (a nivel de módulo, antes de que
# behave cargue los step definitions) y garantiza aislamiento por escenario.
# Las trazas de auditoría enmascaran las cuentas (****); aquí no hay datos reales.

import os
import sys

_SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)


def before_scenario(context, scenario):
    """Cada escenario arranca con un servicio limpio (lo crea el Background)."""
    context.servicio = None


def after_scenario(context, scenario):
    """Limpieza por escenario para garantizar independencia/idempotencia."""
    context.servicio = None
