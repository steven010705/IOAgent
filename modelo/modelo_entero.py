from pulp import LpInteger, LpMinimize, LpProblem, LpStatus, LpVariable, value

from modelo.optimizador import obtener_solver
from modelo.restricciones import agregar_restricciones


def resolver_modelo_entero(demanda: dict, costos: dict, maximos: dict, disponibles: int) -> dict:
    modelo = LpProblem("Asignacion_Turnos_AtiendeMas", LpMinimize)

    x = {
        "manana": LpVariable("X1_manana", lowBound=0, cat=LpInteger),
        "tarde": LpVariable("X2_tarde", lowBound=0, cat=LpInteger),
        "noche": LpVariable("X3_noche", lowBound=0, cat=LpInteger),
    }

    modelo += (
        costos["manana"] * x["manana"]
        + costos["tarde"] * x["tarde"]
        + costos["noche"] * x["noche"]
    ), "Costo_Total"

    agregar_restricciones(modelo, x, demanda, maximos, disponibles)
    modelo.solve(obtener_solver(msg=False))

    estado = LpStatus[modelo.status]
    if estado != "Optimal":
        return {
            "estado": estado,
            "costo": None,
            "turno_mañana": None,
            "turno_tarde": None,
            "turno_noche": None,
        }

    resultado = {
        "estado": estado,
        "costo": int(value(modelo.objective)),
        "turno_mañana": int(value(x["manana"])),
        "turno_tarde": int(value(x["tarde"])),
        "turno_noche": int(value(x["noche"])),
    }
    return resultado
