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
