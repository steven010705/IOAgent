import matplotlib.pyplot as plt


def graficar_asignacion(resultado: dict):
    turnos = ["Mañana", "Tarde", "Noche"]
    valores = [
        resultado["turno_mañana"],
        resultado["turno_tarde"],
        resultado["turno_noche"],
    ]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(turnos, valores)
    ax.set_title("Asignación Óptima por Turno")
    ax.set_ylabel("Empleados")
    ax.grid(axis="y", alpha=0.25)
    return fig


def graficar_costos(resultado: dict, costos: dict):
    turnos = ["Mañana", "Tarde", "Noche"]
    valores = [
        resultado["turno_mañana"] * costos["manana"],
        resultado["turno_tarde"] * costos["tarde"],
        resultado["turno_noche"] * costos["noche"],
    ]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.pie(valores, labels=turnos, autopct="%1.1f%%", startangle=90)
    ax.set_title("Distribución del Costo por Turno")
    return fig


def graficar_utilizacion(resultado: dict, maximos: dict):
    turnos = ["Mañana", "Tarde", "Noche"]
    valores = [
        resultado["turno_mañana"] / maximos["manana"],
        resultado["turno_tarde"] / maximos["tarde"],
        resultado["turno_noche"] / maximos["noche"],
    ]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(turnos, [v * 100 for v in valores], color=["#5b9bd5", "#ed7d31", "#70ad47"])
    ax.set_title("Utilización de Capacidad por Turno")
    ax.set_ylabel("% Capacidad usada")
    ax.set_ylim(0, 100)
    ax.grid(axis="y", alpha=0.25)
    return fig


def graficar_demanda_capacidad(demanda: dict, maximos: dict):
    turnos = ["Mañana", "Tarde", "Noche"]
    valores_demanda = [demanda["manana"], demanda["tarde"], demanda["noche"]]
    valores_capacidad = [maximos["manana"], maximos["tarde"], maximos["noche"]]
    x = range(len(turnos))
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar([p - 0.15 for p in x], valores_demanda, width=0.3, label="Demanda mínima")
    ax.bar([p + 0.15 for p in x], valores_capacidad, width=0.3, label="Capacidad máxima")
    ax.set_xticks(x)
    ax.set_xticklabels(turnos)
    ax.set_title("Demanda mínima vs. Capacidad máxima")
    ax.set_ylabel("Empleados")
    ax.legend()
    ax.grid(axis="y", alpha=0.25)
    return fig
