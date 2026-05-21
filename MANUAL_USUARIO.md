# Manual de Usuario

## 1. Introducción

Este proyecto resuelve un problema de asignación de empleados a turnos en un centro de atención telefónica mediante programación entera. El objetivo es distribuir los empleados disponibles entre los turnos de mañana, tarde y noche para minimizar el costo total, respetando la demanda mínima y las capacidades máximas de cada turno.

## 2. Objetivo del sistema

- Encontrar la asignación óptima de empleados por turno.
- Minimizar el costo total de operación.
- Garantizar que cada turno cumpla con su demanda mínima.
- Utilizar exactamente el total de empleados disponibles.

## 3. Requisitos previos

### 3.1 Software necesario

- Python 3.8 o superior
- `pip`
- Navegador web moderno

### 3.2 Dependencias de Python

El proyecto utiliza las siguientes librerías:

- `streamlit`
- `pandas`
- `pulp`
- `matplotlib`

Opcionalmente, para un mejor rendimiento del solver, instale:

- `coinor-cbc` (recomendado)
- `python-glpk` (alternativa)

### 3.3 Instalación de dependencias

Desde la carpeta raíz del proyecto, ejecute:

```bash
pip install streamlit pandas pulp matplotlib
pip install coinor-cbc
```

Si no puede instalar `coinor-cbc`, puede usar el solver interno de PuLP o `python-glpk`.

## 4. Estructura del proyecto

- `app.py`: Interfaz principal de Streamlit y flujo de ejecución.
- `README.md`: Documentación del proyecto.
- `MANUAL_USUARIO.md`: Este manual.
- `datos/demanda.csv`: Datos de demanda mínima, costo y capacidad máxima por turno.
- `modelo/modelo_entero.py`: Definición del modelo de optimización.
- `modelo/optimizador.py`: Selección del solver disponible.
- `modelo/restricciones.py`: Restricciones del modelo de asignación.
- `visualizacion/graficas.py`: Funciones para generar gráficos de resultados.
- `agente/agenteIA.py`: Genera un análisis del resultado y escenarios adicionales.
- `resultados/solucion.json`: Archivo de salida que puede contener resultados guardados.

## 5. Datos de entrada

Los datos se toman de `datos/demanda.csv` y contienen las columnas:

- `turno`: Nombre del turno (`mañana`, `tarde`, `noche`).
- `demanda_minima`: Empleados mínimos requeridos por turno.
- `costo`: Costo por empleado en cada turno.
- `maximo`: Capacidad máxima de empleados por turno.

Ejemplo del archivo:

```csv
turno,demanda_minima,costo,maximo
mañana,8,80,10
tarde,12,100,12
noche,6,120,8
```

## 6. Cómo ejecutar la aplicación

1. Abra una terminal.
2. Cambie al directorio raíz del proyecto:

```bash
cd c:\Users\bxto0\Downloads\IOAgent-main\IOAgent-main
```

3. Ejecute la aplicación Streamlit:

```bash
streamlit run app.py
```

4. Abra el enlace local que muestra Streamlit en su navegador.

## 7. Uso de la aplicación

### 7.1 Pantalla inicial

La aplicación presenta:

- Título y descripción del problema.
- Turnos disponibles.
- Costo unitario por turno.
- Explicación de la técnica de programación entera usada.

### 7.2 Parámetros de entrada

- `Empleados disponibles`: número total de empleados que debe distribuirse entre los tres turnos.
- `Porcentaje adicional para capacidad máxima (%)`: ajusta temporalmente la capacidad máxima total permitida para el análisis.

### 7.3 Botón "Resolver modelo"

Después de ingresar los parámetros, haga clic en `Resolver modelo` para que el sistema calcule la asignación óptima.

## 8. Interpretación de resultados

La aplicación muestra:

- Costo óptimo total.
- Empleados asignados por turno.
- Detalle de costos por turno.
- Gráficos de:
  - Asignación óptima por turno.
  - Distribución del costo por turno.
  - Utilización de capacidad por turno.
  - Demanda mínima vs. capacidad máxima.

## 9. Modelo matemático

El modelo de programación entera usa estas variables de decisión:

- `x1`: empleados asignados al turno mañana.
- `x2`: empleados asignados al turno tarde.
- `x3`: empleados asignados al turno noche.

Función objetivo:

```text
Min Z = c_m x1 + c_t x2 + c_n x3
```

Restricciones:

- `x1 >= demanda_manhana`
- `x2 >= demanda_tarde`
- `x3 >= demanda_noche`
- `x1 <= max_manhana`
- `x2 <= max_tarde`
- `x3 <= max_noche`
- `x1 + x2 + x3 == disponibles`

Todas las variables son enteras no negativas.

## 10. Agente de análisis IA

El módulo `agente/agenteIA.py` realiza un análisis automático del resultado, incluyendo:

- Identificación del turno con mayor carga.
- Verificación de restricciones activas.
- Escenario de demanda aumentada en 20%.
- Recomendaciones de mejora.

## 11. Personalización de datos

Para cambiar el escenario, edite `datos/demanda.csv` con nuevos valores de demanda mínima, costo y capacidad máxima. Asegúrese de conservar los nombres de columnas y el formato CSV.

## 12. Mensajes de error comunes

- Si `datos/demanda.csv` no existe, la aplicación mostrará un error y se detendrá.
- Si el total de empleados disponibles es menor a la demanda mínima total o mayor a la capacidad máxima permitida, el sistema mostrará una advertencia de factibilidad.
- Si no hay solver instalado, instale `coinor-cbc` o use el solver interno de PuLP.

## 13. Recomendaciones de uso

- Use el valor mínimo de empleados disponibles como punto de partida.
- Ajuste el porcentaje de capacidad máxima solo para analizar escenarios lo suficientemente flexibles.
- Compare diferentes configuraciones de costos y demanda para validar decisiones operativas.

## 14. Contacto del equipo

Proyecto realizado por:

- Riveros Guio Marlon Yecid
- Niño Rivera Steven Alberto
- Castañeda Monsalve Miguel Angel
- Castro Quiroga Sara Sofia

---

Este documento describe cómo utilizar el proyecto y cómo entender sus resultados. Puede copiarlo o modificarlo según sus necesidades.
