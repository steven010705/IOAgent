import os
from pathlib import Path


def obtener_solver(msg: bool = False):
    """
    Obtiene un solver disponible.
    Prioriza CBC en Windows y usa fallback al solver interno de PuLP.
    """
    try:
        # Usar CBC si está disponible y el ejecutable se encuentra
        from pulp import PULP_CBC_CMD
        solver = PULP_CBC_CMD(msg=msg)
        if solver.path and Path(solver.path).exists():
            return solver
    except Exception:
        pass

    try:
        # Intentar GLPK si CBC no está disponible
        from pulp import GLPK
        return GLPK(msg=msg)
    except Exception:
        pass

    try:
        # Fallback final: usar el solver interno de PuLP
        from pulp.apis import PuLP_PY
        return PuLP_PY(msg=msg)
    except Exception:
        raise ImportError(
            "No hay solver disponible. "
            "Instala coinor-cbc con pip install coinor-cbc o glpk con pip install python-glpk"
        )
