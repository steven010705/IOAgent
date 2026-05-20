from pulp import LpProblem


def agregar_restricciones(modelo: LpProblem, x, demanda: dict, maximos: dict, disponibles: int) -> None:
    modelo += x["manana"] >= demanda["manana"], "Cobertura_Manana_Minima"
    modelo += x["tarde"] >= demanda["tarde"], "Cobertura_Tarde_Minima"
    modelo += x["noche"] >= demanda["noche"], "Cobertura_Noche_Minima"

    modelo += x["manana"] <= maximos["manana"], "Capacidad_Manana_Maxima"
    modelo += x["tarde"] <= maximos["tarde"], "Capacidad_Tarde_Maxima"
    modelo += x["noche"] <= maximos["noche"], "Capacidad_Noche_Maxima"

    modelo += x["manana"] + x["tarde"] + x["noche"] <= disponibles, "Disponibilidad_Total"
