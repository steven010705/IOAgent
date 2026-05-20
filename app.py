import json
from pathlib import Path

import pandas as pd
import streamlit as st

from agente.agenteIA import analizar_resultados
from modelo.modelo_entero import resolver_modelo_entero
from visualizacion.graficas import graficar_asignacion, graficar_costos


st.set_page_config(page_title="Atiende+ S.A.S. - Programación Entera", layout="wide")
st.title("Agente Inteligente basado en Investigación de Operaciones")
st.caption("Programación Entera Pura + Agente IA de interpretación")

csv_path = Path("datos/demanda.csv")
if not csv_path.exists():
    st.error("No se encontró el archivo de datos en datos/demanda.csv")
    st.stop()

demanda_df = pd.read_csv(csv_path)
st.subheader("Datos de Demanda")
st.dataframe(demanda_df, use_container_width=True)

st.subheader("Parámetros del Modelo")
col1, col2 = st.columns(2)
with col1:
    disponibles = st.number_input("Empleados disponibles", min_value=1, value=25, step=1)
with col2:
    resolver = st.button("Resolver modelo", type="primary")

if resolver:
    demanda = {
        "manana": int(demanda_df.loc[demanda_df["turno"] == "mañana", "demanda_minima"].iloc[0]),
        "tarde": int(demanda_df.loc[demanda_df["turno"] == "tarde", "demanda_minima"].iloc[0]),
        "noche": int(demanda_df.loc[demanda_df["turno"] == "noche", "demanda_minima"].iloc[0]),
    }
    costos = {
        "manana": int(demanda_df.loc[demanda_df["turno"] == "mañana", "costo"].iloc[0]),
        "tarde": int(demanda_df.loc[demanda_df["turno"] == "tarde", "costo"].iloc[0]),
        "noche": int(demanda_df.loc[demanda_df["turno"] == "noche", "costo"].iloc[0]),
    }
    maximos = {
        "manana": int(demanda_df.loc[demanda_df["turno"] == "mañana", "maximo"].iloc[0]),
        "tarde": int(demanda_df.loc[demanda_df["turno"] == "tarde", "maximo"].iloc[0]),
        "noche": int(demanda_df.loc[demanda_df["turno"] == "noche", "maximo"].iloc[0]),
    }

    resultado = resolver_modelo_entero(
        demanda=demanda,
        costos=costos,
        maximos=maximos,
        disponibles=int(disponibles),
    )

    Path("resultados").mkdir(exist_ok=True)
    with open("resultados/solucion.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)

    st.subheader("Resultado del Modelo")
    st.json(resultado)

    if resultado.get("estado") == "Optimal":
        st.subheader("Interpretación del Agente IA")
        analisis = analizar_resultados(
            resultado=resultado,
            demanda=demanda,
            maximos=maximos,
            disponibles=int(disponibles),
        )
        st.markdown(analisis)

        st.subheader("Visualización")
        vcol1, vcol2 = st.columns(2)
        with vcol1:
            st.pyplot(graficar_asignacion(resultado))
        with vcol2:
            st.pyplot(graficar_costos(resultado, costos))
