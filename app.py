import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap

# Cargar los datos
df_siniestros_final = pd.read_parquet('Datasets_limpios/siniestrosfinal.parquet')

# Configuración de la página
st.set_page_config(page_title="Dashboard de Siniestros Viales", layout="wide")

# Título del dashboard
st.title("Dashboard Interactivo de Siniestros Viales")

# Sidebar para filtros
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

# Extraer la hora en formato numérico
df_filtered['hora_num'] = pd.to_datetime(df_filtered['hora'], format='%H:%M:%S', errors='coerce').dt.hour

# Crear layout de 2 columnas para organizar gráficos
col1, col2 = st.columns(2)

# Gráfico principal de frecuencia de siniestros por la variable seleccionada
with col1:
    st.subheader(f"Distribución de siniestros por {selected_variable.capitalize()}")
    plt.figure(figsize=(8, 4))
    sns.countplot(data=df_filtered, x=selected_variable, palette='Blues')
    plt.title(f"Distribución de siniestros por {selected_variable.capitalize()}")
    plt.xlabel(selected_variable.capitalize())
    plt.ylabel('Frecuencia')
    st.pyplot(plt)

# Gráfico por tipo de vía
with col2:
    st.subheader("Distribución de Siniestros por Tipo de Vía")
    plt.figure(figsize=(8, 4))
    sns.countplot(data=df_filtered, x='tipo_via', palette='coolwarm')
    plt.title('Distribución de Siniestros por Tipo de Vía')
    plt.xlabel('Tipo de Vía')
    plt.ylabel('Frecuencia')
    plt.xticks(rotation=45)
    st.pyplot(plt)

# Distribución de siniestros por hora del día
st.subheader("Distribución de Siniestros por Hora del Día")
plt.figure(figsize=(10, 6))
sns.histplot(df_filtered['hora_num'], bins=24, color='purple', kde=True)
plt.title('Distribución de Siniestros por Hora del Día')
plt.xlabel('Hora del Día')
plt.ylabel('Frecuencia')
st.pyplot(plt)

# Distribución según presencia de semáforo
st.subheader("Frecuencia de Siniestros según Presencia de Semáforo")
plt.figure(figsize=(10, 6))
sns.countplot(data=df_filtered, x='semaforo', palette='spring')
plt.title('Frecuencia de Siniestros según Presencia de Semáforo')
plt.xlabel('Semáforo')
plt.ylabel('Frecuencia')
st.pyplot(plt)

# Mapa de calor de siniestros viales
st.subheader("Mapa de Calor de Siniestros Viales")
map_data = [[row['latitud'], row['longitud']] for index, row in df_filtered.iterrows() if pd.notnull(row['latitud']) and pd.notnull(row['longitud'])]
m = folium.Map(location=[-27.480, -58.830], zoom_start=13)
HeatMap(map_data).add_to(m)
folium_static(m)

# Crear layout de KPIs
st.subheader("KPI's")
kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

# Total de siniestros
with kpi_col1:
    total_siniestros = df_filtered.shape[0]
    st.metric(label="Total de Siniestros", value=total_siniestros)

# Siniestros con semáforo (Funciona, Intermitente, No Funciona)
with kpi_col2:
    siniestros_con_semaforo = df_filtered[df_filtered['semaforo'].isin(['Funciona', 'Intermitente', 'No Funciona'])].shape[0]
    st.metric(label="Siniestros con Semáforo", value=siniestros_con_semaforo)

# Porcentaje de siniestros con semáforo
with kpi_col3:
    porcentaje_con_semaforo = (siniestros_con_semaforo / total_siniestros) * 100
    st.metric(label="Porcentaje con Semáforo", value=f"{porcentaje_con_semaforo:.2f}%")

# Comentarios adicionales
st.write("Este dashboard muestra las principales métricas y visualizaciones relacionadas con los siniestros viales. Los datos pueden ser filtrados por diferentes variables como el año, el tipo de vía, la presencia de semáforo, y más.")


