import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap
import networkx as nx
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from geopy.distance import geodesic
import osmnx as ox

# Cargar los datos
df_siniestros_final = pd.read_parquet('Datasets_limpios/siniestrosfinal.parquet')

# Crear la columna 'hora_num' si aún no existe
df_siniestros_final['hora_num'] = pd.to_datetime(df_siniestros_final['hora'], format='%H:%M:%S', errors='coerce').dt.hour

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

# Tabs para organizar el contenido
tab1, tab2, tab3 = st.tabs(["📊 Dashboard Principal", "📈 Gráficos Secundarios", "🔍 Análisis Predictivo"])

# -------------------- Tab 1: Dashboard Principal --------------------
with tab1:
    st.header("Datos Principales")

    # Crear layout de 3 columnas para los KPIs
    st.subheader("KPI's de Semáforos")
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

    # Mapa de calor de siniestros viales
    st.subheader("Mapa de Calor de Siniestros Viales")
    map_data = [[row['latitud'], row['longitud']] for index, row in df_filtered.iterrows() if pd.notnull(row['latitud']) and pd.notnull(row['longitud'])]
    m = folium.Map(location=[-27.480, -58.830], zoom_start=13)
    HeatMap(map_data).add_to(m)
    folium_static(m)

    # Gráfico interactivo de cantidad de accidentes por año
    st.subheader("Cantidad de Accidentes por Año")
    accidentes_por_anio = df_filtered.groupby('anio').size().reset_index(name='cantidad')
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=accidentes_por_anio, x='anio', y='cantidad', marker='o', ax=ax)
    ax.set_title('Accidentes por Año')
    ax.set_xlabel('Año')
    ax.set_ylabel('Cantidad de Accidentes')
    st.pyplot(fig)

# -------------------- Tab 2: Gráficos Secundarios --------------------
with tab2:
    st.header("Gráficos Secundarios")

    # Crear layout de 2 columnas para los gráficos secundarios
    col1, col2 = st.columns(2)

    # Gráfico 1: Distribución de siniestros por hora
    with col1:
        st.subheader("Distribución de Siniestros por Hora")
        plt.figure(figsize=(8, 4))
        sns.countplot(data=df_filtered, x='hora_num', palette='Blues')
        plt.title("Distribución de Siniestros por Hora")
        plt.xlabel('Hora del Día')
        plt.ylabel('Frecuencia')
        st.pyplot(plt)

    # Gráfico 2: Distribución de siniestros por tipo de vía
    with col2:
        st.subheader("Distribución de Siniestros por Tipo de Vía")
        plt.figure(figsize=(8, 4))
        sns.countplot(data=df_filtered, x='tipo_via', palette='coolwarm')
        plt.title('Distribución de Siniestros por Tipo de Vía')
        plt.xlabel('Tipo de Vía')
        plt.ylabel('Frecuencia')
        plt.xticks(rotation=45)
        st.pyplot(plt)

    # Gráfico 3: Distribución por día de la semana
    st.subheader("Distribución de Siniestros por Día de la Semana")
    plt.figure(figsize=(8, 4))
    sns.countplot(data=df_filtered, x='dia', palette='Set2')
    plt.title("Distribución de Siniestros por Día")
    plt.xlabel('Día de la Semana')
    plt.ylabel('Frecuencia')
    st.pyplot(plt)

    # Gráfico 4: Distribución por mes
    st.subheader("Distribución de Siniestros por Mes")
    plt.figure(figsize=(8, 4))
    sns.countplot(data=df_filtered, x='mes', palette='Set3')
    plt.title("Distribución de Siniestros por Mes")
    plt.xlabel('Mes')
    plt.ylabel('Frecuencia')
    st.pyplot(plt)

# -------------------- Tab 3: Análisis Predictivo --------------------
with tab3:
    st.header("Análisis Predictivo")

    # Modelo de recomendación de semáforos
    st.subheader("Recomendación de Sitios Urgentes para Colocación de Semáforos")

    # Filtrar los siniestros sin semáforo
    siniestros_sin_semaforo = df_siniestros_final[df_siniestros_final['semaforo'] == 'No Funciona']

    # Contar los siniestros por ubicación (latitud y longitud)
    siniestros_por_ubicacion = siniestros_sin_semaforo.groupby(['latitud', 'longitud']).size().reset_index(name='cantidad_siniestros')

    # Encontrar las 5 ubicaciones con más accidentes
    top_5_ubicaciones = siniestros_por_ubicacion.nlargest(5, 'cantidad_siniestros')

    m = folium.Map(location=[-27.48, -58.83], zoom_start=13)

    for index, row in top_5_ubicaciones.iterrows():
        folium.Marker(
            location=[row['latitud'], row['longitud']],
            popup=f"Cantidad de Siniestros: {row['cantidad_siniestros']}",
            icon=folium.Icon(color='red')
        ).add_to(m)

    folium_static(m)

    # Recomendación de Ruta Segura
    st.subheader("Recomendación de Ruta Segura entre Dos Ubicaciones")

    # Seleccionar dos ubicaciones de inicio y fin
    lat_inicio = st.number_input("Latitud de Inicio", value=-27.4668)
    lon_inicio = st.number_input("Longitud de Inicio", value=-58.8467)
    lat_fin = st.number_input("Latitud de Destino", value=-27.4650)
    lon_fin = st.number_input("Longitud de Destino", value=-58.8403)

    # Descargar la red vial de OpenStreetMap para la zona que te interesa (especificando una latitud/longitud central y un radio)
    G = ox.graph_from_point((lat_inicio, lon_inicio), dist=2000, network_type='drive')

    # Encontrar el nodo más cercano al punto de inicio y al punto de destino en el grafo de calles
    nodo_inicio = ox.nearest_nodes(G, lon_inicio, lat_inicio)
    nodo_fin = ox.nearest_nodes(G, lon_fin, lat_fin)

    # Calcular la ruta más corta en términos de distancia usando el grafo vial
    ruta_segura = nx.shortest_path(G, source=nodo_inicio, target=nodo_fin, weight='length')

    # Crear el mapa en Folium
    m = folium.Map(location=[(lat_inicio + lat_fin) / 2, (lon_inicio + lon_fin) / 2], zoom_start=13)

    # Añadir marcadores para el punto de inicio y fin
    folium.Marker(location=[lat_inicio, lon_inicio], popup="Inicio", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(location=[lat_fin, lon_fin], popup="Destino", icon=folium.Icon(color='red')).add_to(m)

    # Extraer las coordenadas de la ruta más segura
    ruta_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in ruta_segura]

    # Dibujar la ruta en el mapa
    folium.PolyLine(locations=ruta_coords, color='blue').add_to(m)

    # Mostrar el mapa en Streamlit
    folium_static(m)




