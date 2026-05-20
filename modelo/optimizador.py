import os
from pathlib import Path


def obtener_solver(msg: bool = False):
    """
    Obtiene un solver disponible.
    El problema es que CBC/ARM64 no funciona en este sistema.
    Usamos PuLP_PY como fallback robusto.
    """
    try:
        # Intenta usar GLPK si está disponible
        from pulp import GLPK
        return GLPK(msg=msg)
    except Exception:
        pass
    
    try:
        # Intenta usar CBC desde otro path o compilado
        from pulp import PULP_CBC_CMD
        solver = PULP_CBC_CMD(msg=msg)
        # Verifica que el ejecutable existe
        if Path(solver.path).exists():
            return solver
    except Exception:
        pass
    
    # Fallback final: usar PuLP's built-in solver (más lento pero siempre funciona)
    try:
        from pulp import PuLP_PY
        return PuLP_PY(msg=msg)
    except Exception:
        pass
    
    # Último intento: importar directamente desde apis
    try:
        from pulp.apis import PuLP_PY
        return PuLP_PY(msg=msg)
    except Exception:
        raise ImportError(
            "No hay solver disponible. "
            "Intenta: pip install python-glpk o pip install coinor-cbc"
        )
