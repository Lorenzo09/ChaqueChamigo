import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap

# Cargar los datos
df_siniestros_final = pd.read_parquet('Datasets_limpios/siniestrosfinal.parquet')

# Dashboard interactivo en Streamlit
st.title("Dashboard de Siniestros Viales")
st.sidebar.header("Filtros")

# Filtrar por rango de años
min_year = int(df_siniestros_final['anio'].min())
max_year = int(df_siniestros_final['anio'].max())
selected_year_range = st.sidebar.slider("Seleccione el rango de años", min_year, max_year, (min_year, max_year))

# Filtrar el dataset por el rango seleccionado
df_filtered = df_siniestros_final[df_siniestros_final['anio'].between(selected_year_range[0], selected_year_range[1])]

# Seleccionar columnas para interactuar
variables = ['anio', 'mes', 'dia', 'hora', 'tipo_via', 'semaforo']
selected_variable = st.sidebar.selectbox("Seleccione una variable para el gráfico principal", variables)

# Frecuencia de siniestros por variable seleccionada
st.subheader(f"Distribución de siniestros por {selected_variable.capitalize()}")
plt.figure(figsize=(10, 6))
sns.countplot(data=df_filtered, x=selected_variable, palette='Blues')
plt.title(f"Distribución de siniestros por {selected_variable.capitalize()}")
plt.xlabel(selected_variable.capitalize())
plt.ylabel('Frecuencia')
st.pyplot(plt)

# Gráfico por tipo de vía
st.subheader("Distribución de Siniestros por Tipo de Vía")
plt.figure(figsize=(10, 6))
sns.countplot(data=df_filtered, x='tipo_via', palette='coolwarm')
plt.title('Distribución de Siniestros por Tipo de Vía')
plt.xlabel('Tipo de Vía')
plt.ylabel('Frecuencia')
plt.xticks(rotation=45)
st.pyplot(plt)

# Gráfico por hora del día
st.subheader("Distribución de Siniestros por Hora del Día")

# Asegurarnos de que la columna 'hora' ya esté en formato datetime y extraer solo la hora
df_filtered['hora'] = pd.to_datetime(df_filtered['hora'], errors='coerce').dt.hour

# Crear el gráfico
plt.figure(figsize=(10, 6))
sns.histplot(df_filtered['hora'], bins=24, color='purple', kde=True)
plt.title('Distribución de Siniestros por Hora del Día')
plt.xlabel('Hora del Día')
plt.ylabel('Frecuencia')

# Mostrar el gráfico en Streamlit
st.pyplot(plt)


# Gráfico por presencia de semáforo
st.subheader("Frecuencia de Siniestros según Presencia de Semáforo")
plt.figure(figsize=(10, 6))
sns.countplot(data=df_filtered, x='semaforo', palette='spring')
plt.title('Frecuencia de Siniestros según Presencia de Semáforo')
plt.xlabel('Semáforo')
plt.ylabel('Frecuencia')
st.pyplot(plt)

# Mapa de calor interactivo con Folium
st.subheader("Mapa de Calor de Siniestros Viales")
map_data = [[row['latitud'], row['longitud']] for index, row in df_filtered.iterrows() if pd.notnull(row['latitud']) and pd.notnull(row['longitud'])]
m = folium.Map(location=[-27.480, -58.830], zoom_start=13)
HeatMap(map_data).add_to(m)
folium_static(m)

# Crear KPIs basados en los gráficos
st.subheader("KPI's")
total_siniestros = df_filtered.shape[0]
siniestros_con_semaforo = df_filtered[df_filtered['semaforo'] == 'Si'].shape[0]
st.metric(label="Total de Siniestros", value=total_siniestros)
st.metric(label="Siniestros con Semáforo", value=siniestros_con_semaforo)
st.metric(label="Porcentaje con Semáforo", value=f"{(siniestros_con_semaforo / total_siniestros) * 100:.2f}%")

# Comentarios adicionales
st.write("Este dashboard muestra las principales métricas y visualizaciones relacionadas con los siniestros viales. Los datos pueden ser filtrados por diferentes variables como el año, el tipo de vía, la presencia de semáforo, y más.")

