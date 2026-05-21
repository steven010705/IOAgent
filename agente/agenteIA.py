import math
from typing import Dict

from modelo.modelo_entero import resolver_modelo_entero


def _formato_turno(turno: str) -> str:
    if turno == "manana":
        return "mañana"
    return turno


def analizar_resultados(
    resultado: dict,
    demanda: dict,
    maximos: dict,
    disponibles: int,
    costos: dict,
) -> str:
    asignados = {
        "manana": resultado.get("turno_mañana", 0),
        "tarde": resultado.get("turno_tarde", 0),
        "noche": resultado.get("turno_noche", 0),
    }
    turno_mayor_carga = max(asignados, key=asignados.get)
    total_demanda = sum(demanda.values())
    total_capacidad = sum(maximos.values())
    total_asignados = sum(asignados.values())
    demanda_20 = {turno: math.ceil(demanda[turno] * 1.2) for turno in demanda}
    demanda_20_total = sum(demanda_20.values())

    restricciones_activas = []
    for turno in ["manana", "tarde", "noche"]:
        if asignados[turno] == demanda[turno]:
            restricciones_activas.append(f"Turno {_formato_turno(turno)} alcanzó demanda mínima.")
        if asignados[turno] == maximos[turno]:
            restricciones_activas.append(f"Turno {_formato_turno(turno)} alcanzó capacidad máxima.")
    if total_asignados == disponibles:
        restricciones_activas.append("Disponibilidad total igualada.")

    escenario_text = []
    if demanda_20_total > total_capacidad:
        escenario_text.append(
            "Si demanda aumenta 20%, el nuevo mínimo total excede la capacidad máxima y el escenario no es factible sin más recursos."
        )
    else:
        if demanda_20_total > disponibles:
            adicional = demanda_20_total - disponibles
            escenario_text.append(
                f"Si demanda aumenta 20%, podrían requerirse {adicional} empleados adicionales para mantener la nueva demanda mínima."
            )
        else:
            escenario_text.append(
                "Si demanda aumenta 20%, el modelo puede ajustar la asignación con la dotación actual dentro de la capacidad máxima."
            )
        nuevo_resultado = resolver_modelo_entero(
            demanda=demanda_20,
            costos=costos,
            maximos=maximos,
            disponibles=disponibles,
        )
        if nuevo_resultado.get("estado") != "Optimal":
            escenario_text.append(
                "Con la misma dotación actual, el modelo no alcanza solución óptima en el escenario 20% mayor, lo que sugiere que hace falta más personal o mayor capacidad."
            )

    salida = [
        "ANÁLISIS:",
        f"La mayor carga se concentra en el turno {_formato_turno(turno_mayor_carga)}.",
        "El resultado es óptimo porque cumple la demanda mínima de cada turno, utiliza exactamente todos los empleados disponibles y minimiza el costo total.",
        "",
        "RESTRICCIONES ACTIVAS:",
    ]
    if restricciones_activas:
        salida.extend(restricciones_activas)
    else:
        salida.append("No hay restricciones de demanda o capacidad exactamente activas, salvo la igualdad de disponibilidad.")

    salida.extend([
        "",
        "MEJORAS:",
        "Evaluar personal temporal en los turnos con mayor carga.",
        "Revisar los costos unitarios por turno para confirmar si la asignación refleja correctamente el costo marginal.",
        "Considerar escenarios múltiples si la demanda varía con frecuencia."
    ])

    salida.extend([
        "",
        "ESCENARIO:",
    ])
    salida.extend(escenario_text)

    salida.extend([
        "",
        "RECOMENDACIÓN:",
        "Redistribuir recursos en horas pico y priorizar los turnos de menor costo para empleados adicionales.",
        "Usar este agente como apoyo para comparar cambios en disponibilidad versus demanda."
    ])

    return "\n".join(salida)
