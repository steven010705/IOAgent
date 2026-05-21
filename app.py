import json
from pathlib import Path

import pandas as pd
import streamlit as st

from agente.agenteIA import analizar_resultados
from modelo.modelo_entero import resolver_modelo_entero
from visualizacion.graficas import (
    graficar_asignacion,
    graficar_costos,
    graficar_utilizacion,
    graficar_demanda_capacidad,
)


DATA_PATH = Path("datos/demanda.csv")

st.set_page_config(page_title="Atiende+ S.A.S. - Asignación de Turnos", layout="wide")


def cargar_datos():
    if not DATA_PATH.exists():
        st.error("No se encontró el archivo de datos en datos/demanda.csv")
        st.stop()

    datos = pd.read_csv(DATA_PATH)
    demanda = {
        "manana": int(datos.loc[datos["turno"] == "mañana", "demanda_minima"].iloc[0]),
        "tarde": int(datos.loc[datos["turno"] == "tarde", "demanda_minima"].iloc[0]),
        "noche": int(datos.loc[datos["turno"] == "noche", "demanda_minima"].iloc[0]),
    }
    costos = {
        "manana": int(datos.loc[datos["turno"] == "mañana", "costo"].iloc[0]),
        "tarde": int(datos.loc[datos["turno"] == "tarde", "costo"].iloc[0]),
        "noche": int(datos.loc[datos["turno"] == "noche", "costo"].iloc[0]),
    }
    maximos = {
        "manana": int(datos.loc[datos["turno"] == "mañana", "maximo"].iloc[0]),
        "tarde": int(datos.loc[datos["turno"] == "tarde", "maximo"].iloc[0]),
        "noche": int(datos.loc[datos["turno"] == "noche", "maximo"].iloc[0]),
    }
    min_disponibles = sum(demanda.values())
    base_max_disponibles = sum(maximos.values())

    return demanda, costos, maximos, min_disponibles, base_max_disponibles


def mostrar_encabezado():
    with st.container():
        st.title("Caso Real: Optimización de Asignación de Turnos en un Centro de Atención Telefónica")
        st.markdown(
            "La empresa Atiende+ S.A.S. distribuye empleados disponibles entre tres turnos para minimizar costos operativos y mantener cobertura adecuada."
        )
        st.markdown(
            "Restricción sobre 'Empleados disponibles': debe estar entre la cantidad mínima $D_{min}$ (suma de demandas mínimas por turno) y la capacidad máxima total $C_{max}$ (suma de las capacidades máximas por turno). La mínima cantidad garantiza la cobertura básica en cada turno; la máxima refleja el límite físico de puestos disponibles en los turnos." 
        )
        st.divider()
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("**Turnos operativos**")
            st.markdown("- Turno mañana: 6:00 am – 2:00 pm")
            st.markdown("- Turno tarde: 2:00 pm – 10:00 pm")
            st.markdown("- Turno noche: 10:00 pm – 6:00 am")
        with col2:
            st.metric("Técnica", "Programación Entera Pura")
            st.metric("Área", "Investigación de Operaciones")
        st.info(
            "El modelo asigna todos los empleados disponibles entre los turnos y minimiza el costo total manteniendo las demandas mínimas."
        )
        st.divider()


def mostrar_descripcion():
    with st.container():
        st.subheader("Problema que resuelve")
        st.markdown(
            "Determinar cómo distribuir los empleados disponibles entre los turnos para minimizar costos operativos y mantener la cobertura mínima de atención."
        )
        st.divider()


def mostrar_modelo(costos):
    with st.container():
        st.subheader("Cómo lo resuelve el modelo matemático")
        st.markdown(
            "El modelo usa variables enteras de asignación y una restricción principal que obliga a distribuir todos los empleados disponibles entre los tres turnos."
        )
        c1, c2, c3 = st.columns(3)
        c1.metric("Costo mañana", f"${costos['manana']}")
        c2.metric("Costo tarde", f"${costos['tarde']}")
        c3.metric("Costo noche", f"${costos['noche']}")

        st.caption("Variables de decisión y función objetivo")
        st.latex(r"""
\begin{aligned}
x_1 &= \text{empleados turno mañana}\\
x_2 &= \text{empleados turno tarde}\\
x_3 &= \text{empleados turno noche}\\
D &= \text{total de empleados disponibles}
\end{aligned}
""")
        st.latex(r"""
\begin{aligned}
\mathrm{Min}\; Z &= c_m x_1 + c_t x_2 + c_n x_3
\end{aligned}
""")
        st.latex(r"""
\begin{aligned}
x_1 + x_2 + x_3 &= D\\
x_1 &\ge d_1\\
x_2 &\ge d_2\\
x_3 &\ge d_3\\
x_1, x_2, x_3 &\in \mathbb{Z}_{\ge0}
\end{aligned}
""")
        st.caption("La restricción principal exige usar todos los empleados disponibles y las demandas mínimas se mantienen como restricciones secundarias.")
        st.divider()


def mostrar_tecnica():
    with st.container():
        st.subheader("Técnica de Investigación de Operaciones utilizada")
        st.markdown(
            "Se emplea Programación Entera Pura porque las variables representan personas y solo pueden tomar valores enteros."
        )
        st.info("Variables enteras + restricciones lineales + optimización de costos = Modelo académico válido.")
        st.divider()


def mostrar_parametros(min_disponibles, base_max_disponibles):
    with st.container():
        st.subheader("Parámetros del modelo")
        col1, col2 = st.columns([3, 1])
        with col1:
            margen = st.number_input(
                "Porcentaje adicional para capacidad máxima (%)",
                min_value=0,
                max_value=100,
                value=0,
                step=5,
                help="Aumenta temporalmente el límite máximo permitido para 'Empleados disponibles' en este análisis.",
            )
            max_disponibles = int(base_max_disponibles * (1 + margen / 100))
            st.caption(f"Capacidad máxima base: {base_max_disponibles}. Capacidad máxima permitida actual: {max_disponibles}.")
            
            disponibles = st.number_input(
                "Empleados disponibles",
                min_value=min_disponibles,
                max_value=max_disponibles,
                value=min_disponibles,
                step=1,
                help=f"Debe haber entre {min_disponibles} y {max_disponibles} empleados disponibles.",
            )
        with col2:
            resolver = st.button("Resolver modelo", type="primary")
        st.caption("El total de empleados disponibles se distribuye íntegramente entre los tres turnos.")
        st.divider()
    return disponibles, resolver, max_disponibles


def validar_parametros(disponibles, min_disponibles, max_disponibles):
    if disponibles < min_disponibles:
        st.error("Empleados disponibles < demanda mínima total. El problema es infactible.")
        return False
    if disponibles > max_disponibles:
        st.error(
            "Empleados disponibles exceden la capacidad máxima total de los turnos. Ajuste el total disponible o los máximos por turno."
        )
        return False
    return True


def mostrar_resultados(resultado, costos, disponibles, demanda, maximos):
    st.subheader("Resultados del modelo")
    rcol1, rcol2, rcol3, rcol4 = st.columns(4)
    rcol1.metric("Costo óptimo", f"${resultado.get('costo')}")
    rcol2.metric("Empleados mañana", resultado.get("turno_mañana"))
    rcol3.metric("Empleados tarde", resultado.get("turno_tarde"))
    rcol4.metric("Empleados noche", resultado.get("turno_noche"))

    st.markdown(
        "El modelo distribuye todos los empleados disponibles respetando las demandas mínimas y minimizando el costo total."
    )
    st.divider()

    asignados = {
        "mañana": resultado.get("turno_mañana"),
        "tarde": resultado.get("turno_tarde"),
        "noche": resultado.get("turno_noche"),
    }
    detalle = pd.DataFrame(
        {
            "Turno": ["mañana", "tarde", "noche"],
            "Asignados": [asignados["mañana"], asignados["tarde"], asignados["noche"]],
            "Costo unitario": [costos["manana"], costos["tarde"], costos["noche"]],
            "Costo total": [
                asignados["mañana"] * costos["manana"],
                asignados["tarde"] * costos["tarde"],
                asignados["noche"] * costos["noche"],
            ],
        }
    )
    st.dataframe(detalle.set_index("Turno"), width="stretch")

    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(graficar_asignacion(resultado))
    with col2:
        st.pyplot(graficar_costos(resultado, costos))

    col3, col4 = st.columns(2)
    with col3:
        st.pyplot(graficar_demanda_capacidad(demanda, maximos))
    with col4:
        st.pyplot(graficar_utilizacion(resultado, maximos))

    st.divider()
    st.subheader("Escenarios")
    escenarios = []
    for ajuste in (-2, 2):
        nuevo = disponibles + ajuste
        if nuevo >= sum(demanda.values()) and nuevo <= sum(maximos.values()):
            escenario = resolver_modelo_entero(
                demanda=demanda,
                costos=costos,
                maximos=maximos,
                disponibles=nuevo,
            )
            escenarios.append(
                {
                    "Escenario": f"{ajuste:+d} empleados",
                    "X1": escenario.get("turno_mañana"),
                    "X2": escenario.get("turno_tarde"),
                    "X3": escenario.get("turno_noche"),
                    "Costo": escenario.get("costo"),
                }
            )
    if escenarios:
        st.dataframe(pd.DataFrame(escenarios).set_index("Escenario"), width="stretch")
    else:
        st.markdown("No hay escenarios alternativos factibles con el ajuste propuesto.")

    st.divider()
    return asignados


def mostrar_recomendaciones(asignados, costos, demanda):
    with st.container():
        st.subheader("Recomendaciones gerenciales")
        st.markdown(
            "- Mantener la asignación mínima de empleados en cada turno y usar los recursos adicionales donde el costo marginal sea menor."
        )
        if asignados["noche"] > demanda["noche"]:
            st.markdown(
                "- Si la asignación nocturna supera la demanda mínima, ajustar el equipo de noche solo si el volumen adicional de atención lo justifica."
            )
        st.markdown(
            "- Revisar periódicamente los costos por turno para actualizar la asignación con el menor costo operativo."
        )
        st.divider()


def mostrar_ia(resultado, demanda, maximos, disponibles, costos):
    with st.container():
        st.subheader("Papel del agente IA")
        st.markdown(
            "El agente IA interpreta los resultados del optimizador, genera conclusiones y apoya la toma de decisiones gerenciales."
        )
        if resultado.get("estado") == "Optimal":
            analisis = analizar_resultados(
                resultado=resultado,
                demanda=demanda,
                maximos=maximos,
                disponibles=disponibles,
                costos=costos,
            )
            st.markdown(analisis)
        else:
            st.warning("No se generó interpretación IA porque el modelo no alcanzó solución óptima.")
        st.divider()


def main():
    mostrar_encabezado()
    mostrar_descripcion()
    demanda, costos, maximos, min_disponibles, base_max_disponibles = cargar_datos()
    mostrar_modelo(costos)
    mostrar_tecnica()
    disponibles, resolver, max_disponibles = mostrar_parametros(min_disponibles, base_max_disponibles)

    if resolver:
        if not validar_parametros(disponibles, min_disponibles, max_disponibles):
            return

        resultado = resolver_modelo_entero(
            demanda=demanda,
            costos=costos,
            maximos=maximos,
            disponibles=int(disponibles),
        )

        Path("resultados").mkdir(exist_ok=True)
        with open("resultados/solucion.json", "w", encoding="utf-8") as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False)

        if resultado.get("estado") != "Optimal":
            st.error(
                f"Estado del optimizador: {resultado.get('estado')}. El problema puede ser infactible o no alcanzó solución óptima."
            )
            with st.expander("Resultado crudo"):
                st.json(resultado)
            return

        asignados = mostrar_resultados(resultado, costos, disponibles, demanda, maximos)
        mostrar_ia(resultado, demanda, maximos, disponibles, costos)
        mostrar_recomendaciones(asignados, costos, demanda)

    st.caption("Ajusta el número de empleados disponibles para observar cómo cambia la asignación y el costo total.")


if __name__ == "__main__":
    main()
