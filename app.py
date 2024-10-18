import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Configuración inicial de la página
st.set_page_config(page_title="ChaqueChamigo", layout="wide")
st.title("ChaqueChamigo - Análisis de Siniestros y Recomendaciones de Seguridad Vial")

# Cargar los datos
@st.cache_data
def cargar_datos():
    return pd.read_parquet('Datasets_limpios/siniestrosfinal.parquet')

df_siniestros = cargar_datos()

# Filtros por año y tipo de vía
st.sidebar.header("Filtros")
anio = st.sidebar.selectbox("Seleccionar año", df_siniestros['anio'].unique())
tipo_via = st.sidebar.multiselect("Seleccionar tipo de vía", df_siniestros['tipo_via'].unique())

# Filtrar el dataset
df_filtered = df_siniestros[(df_siniestros['anio'] == anio) & (df_siniestros['tipo_via'].isin(tipo_via))]

# Distribución de siniestros por hora
col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribución de Siniestros por Hora del Día")
    plt.figure(figsize=(10, 6))
    sns.histplot(df_filtered['hora'], bins=24, color='purple', kde=True)
    plt.title('Distribución de Siniestros por Hora del Día')
    plt.xlabel('Hora del Día')
    plt.ylabel('Frecuencia')
    st.pyplot(plt)

with col2:
    st.subheader("Frecuencia de Siniestros por Tipo de Vía")
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df_filtered, x='tipo_via', palette='coolwarm')
    plt.title('Frecuencia de Siniestros por Tipo de Vía')
    plt.xlabel('Tipo de Vía')
    plt.ylabel('Cantidad de Siniestros')
    st.pyplot(plt)

# 1. Funcionalidad de Recomendación de Sitios Urgentes para Semáforos (Machine Learning)
st.subheader("Recomendación de Sitios Urgentes para Colocación de Semáforos")

# Preprocesar los datos para el modelo
variables_modelo = ['anio', 'mes', 'dia', 'hora', 'tipo_via', 'semaforo']
df_ml = df_siniestros[variables_modelo].dropna()

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

# 2. Funcionalidad de Recomendación de Ruta Segura
st.subheader("Recomendación de Ruta Segura entre Dos Puntos")

# Crear un grafo con las intersecciones y siniestros
G = nx.Graph()

# Agregar nodos (puntos de interés)
for index, row in df_filtered.iterrows():
    G.add_node((row['latitud'], row['longitud']), siniestros=row['cantidad_siniestros'])

# Agregar aristas (conexiones entre intersecciones ponderadas por peligrosidad)
for i in range(len(df_filtered)-1):
    lat1, lon1 = df_filtered.iloc[i]['latitud'], df_filtered.iloc[i]['longitud']
    lat2, lon2 = df_filtered.iloc[i+1]['latitud'], df_filtered.iloc[i+1]['longitud']
    G.add_edge((lat1, lon1), (lat2, lon2), weight=df_filtered.iloc[i]['cantidad_siniestros'])

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

# Conclusión
st.write("Gracias por usar *ChaqueChamigo*. Esta es solo una versión MVP que busca mostrar cómo se puede mejorar la seguridad vial utilizando datos de siniestros y herramientas tecnológicas.")





