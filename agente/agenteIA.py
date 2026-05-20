from __future__ import annotations

import math

from agente.prompts import PROMPT_BASE


def _restricciones_activas(resultado: dict, demanda: dict, maximos: dict, disponibles: int) -> list[str]:
    activas = []

    manana = resultado["turno_mañana"]
    tarde = resultado["turno_tarde"]
    noche = resultado["turno_noche"]
    total = manana + tarde + noche

    if manana == demanda["manana"]:
        activas.append("Cobertura mínima de mañana")
    if tarde == demanda["tarde"]:
        activas.append("Cobertura mínima de tarde")
    if noche == demanda["noche"]:
        activas.append("Cobertura mínima de noche")

    if manana == maximos["manana"]:
        activas.append("Capacidad máxima de mañana")
    if tarde == maximos["tarde"]:
        activas.append("Capacidad máxima de tarde")
    if noche == maximos["noche"]:
        activas.append("Capacidad máxima de noche")

    if total == disponibles:
        activas.append("Disponibilidad total de empleados")

    return activas


def _escenario_20(demanda: dict, maximos: dict, disponibles: int) -> str:
    d_manana = math.ceil(demanda["manana"] * 1.2)
    d_tarde = math.ceil(demanda["tarde"] * 1.2)
    d_noche = math.ceil(demanda["noche"] * 1.2)
    total_requerido = d_manana + d_tarde + d_noche

    factible_capacidad = (
        d_manana <= maximos["manana"]
        and d_tarde <= maximos["tarde"]
        and d_noche <= maximos["noche"]
    )
    faltante = max(0, total_requerido - disponibles)

    if not factible_capacidad:
        return (
            f"Con +20% de demanda se requerirían (mañana={d_manana}, tarde={d_tarde}, noche={d_noche}), "
            "pero al menos un turno excede su capacidad máxima actual. "
            "Se necesitaría ampliar capacidad o rediseñar turnos."
        )

    if faltante > 0:
        return (
            f"Con +20% de demanda se requerirían {total_requerido} empleados en total, "
            f"es decir, {faltante} empleados adicionales frente a los {disponibles} disponibles."
        )

    return (
        f"Con +20% de demanda se requerirían {total_requerido} empleados en total y aún sería factible "
        "con la disponibilidad y capacidades actuales."
    )


def analizar_resultados(resultado: dict, demanda: dict, maximos: dict, disponibles: int) -> str:
    if resultado.get("estado") != "Optimal":
        return "No se puede interpretar una solución no óptima."

    _ = PROMPT_BASE.format(resultado=resultado)
    # El prompt queda disponible como plantilla de referencia para integrar un LLM externo
    # sin alterar el flujo: primero modelo matemático, luego interpretación.

    activas = _restricciones_activas(resultado, demanda, maximos, disponibles)
    escenario = _escenario_20(demanda, maximos, disponibles)

    manana = resultado["turno_mañana"]
    tarde = resultado["turno_tarde"]
    noche = resultado["turno_noche"]
    costo = resultado["costo"]

    mayor_turno = max(
        [("mañana", manana), ("tarde", tarde), ("noche", noche)],
        key=lambda x: x[1],
    )[0]

    lineas = [
        "### ANÁLISIS",
        f"La solución óptima asigna {manana} en mañana, {tarde} en tarde y {noche} en noche, con costo total {costo}.",
        f"La mayor carga operativa está en el turno {mayor_turno}.",
        "",
        "### RESTRICCIONES ACTIVAS",
        ", ".join(activas) if activas else "No se detectaron restricciones activas en igualdad.",
        "",
        "### MEJORAS",
        "- Evaluar personal temporal o flexible para picos en el turno de mayor carga.",
        "- Analizar esquemas de incentivos para turnos de mayor costo y rotación.",
        "- Simular sensibilidad de costos ante cambios de disponibilidad total.",
        "",
        "### ESCENARIO (+20% DEMANDA)",
        escenario,
        "",
        "### RECOMENDACIÓN GERENCIAL",
        "Mantener seguimiento semanal de demanda por turno y preparar un plan de contingencia para incrementos súbitos.",
    ]

    return "\n".join(lineas)
