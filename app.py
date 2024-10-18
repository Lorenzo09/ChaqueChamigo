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

# Distribución según presencia de semáforos
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

# Recomendación de sitios urgentes para semáforos (Machine Learning)
st.subheader("Recomendación de Sitios Urgentes para Colocación de Semáforos")

# Preprocesar los datos para el modelo
variables_modelo = ['anio', 'mes', 'dia', 'hora_num', 'tipo_via', 'semaforo']
df_ml = df_siniestros_final[variables_modelo].dropna()

# Convertir las columnas categóricas a numéricas
df_ml['semaforo'] = df_ml['semaforo'].apply(lambda x: 1 if x == 'Si' else 0)
df_ml = pd.get_dummies(df_ml, columns=['tipo_via'], drop_first=True)

# Separar las características y el objetivo
X = df_ml.drop('semaforo', axis=1)
y = df_ml['semaforo']

# Dividir en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar el modelo
modelo_rf = RandomForestClassifier(random_state=42)
modelo_rf.fit(X_train, y_train)

# Función para predecir necesidad de semáforo
def recomendar_semaforos(nuevos_datos):
    predicciones = modelo_rf.predict(nuevos_datos)
    return predicciones

# Mostrar sitios recomendados para semáforos
nuevos_sitios = X_test  # En tu aplicación podrías usar datos futuros
recomendaciones = recomendar_semaforos(nuevos_sitios)
df_recomendaciones = pd.DataFrame(recomendaciones, columns=["Recomendación de Semáforo"])
st.write("Predicción de semáforos necesarios en los siguientes sitios:", df_recomendaciones)

# Recomendación de Ruta Segura
st.subheader("Recomendación de Ruta Segura entre Dos Puntos")

# Crear un grafo con las intersecciones y siniestros
G = nx.Graph()

# Agregar nodos (puntos de interés)
for index, row in df_filtered.iterrows():
    G.add_node((row['latitud'], row['longitud']), siniestros=row['cantidad_de_involucrados'])

# Agregar aristas (conexiones entre intersecciones ponderadas por peligrosidad)
for i in range(len(df_filtered)-1):
    lat1, lon1 = df_filtered.iloc[i]['latitud'], df_filtered.iloc[i]['longitud']
    lat2, lon2 = df_filtered.iloc[i+1]['latitud'], df_filtered.iloc[i+1]['longitud']
    G.add_edge((lat1, lon1), (lat2, lon2), weight=df_filtered.iloc[i]['cantidad_de_involucrados'])

# Función para encontrar la ruta más segura
def ruta_mas_segura(origen, destino):
    ruta_segura = nx.shortest_path(G, source=origen, target=destino, weight='weight')
    return ruta_segura

# Selección de puntos en el mapa por el usuario (en un futuro, agregar mapas interactivos)
st.write("Seleccione dos puntos para obtener la ruta más segura")
origen = (-27.48, -58.83)  # Punto de ejemplo seleccionado por el usuario
destino = (-27.5, -58.85)  # Otro punto seleccionado por el usuario
ruta = ruta_mas_segura(origen, destino)
st.write(f"La ruta más segura entre {origen} y {destino} es: {ruta}")

# Comentarios adicionales
st.write("Este dashboard muestra las principales métricas y visualizaciones relacionadas con los siniestros viales. Los datos pueden ser filtrados por diferentes variables como el año, el tipo de vía, la presencia de semáforo, y más.")






