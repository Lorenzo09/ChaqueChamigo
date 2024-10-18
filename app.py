import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap

# Configuración de estilo para los gráficos
sns.set(style="whitegrid")

# Cargar los datos
df_siniestros_final = pd.read_parquet('Dataset_limpios/df_siniestros_totales.parquet')

# Título del Dashboard
st.title('Dashboard Interactivo de Siniestros Viales')

# Gráfico 1: Distribución de siniestros por Año
st.subheader('Distribución de Siniestros por Año')
fig, ax = plt.subplots(figsize=(10, 6))
sns.countplot(data=df_siniestros_final, x='anio', palette='Blues', ax=ax)
ax.set_title('Distribución de siniestros por Año')
ax.set_xlabel('Año')
ax.set_ylabel('Frecuencia')
st.pyplot(fig)

# Gráfico 2: Distribución de siniestros por Mes
st.subheader('Distribución de Siniestros por Mes')
fig, ax = plt.subplots(figsize=(10, 6))
sns.countplot(data=df_siniestros_final, x='mes', palette='Blues', ax=ax)
ax.set_title('Distribución de siniestros por Mes')
ax.set_xlabel('Mes')
ax.set_ylabel('Frecuencia')
st.pyplot(fig)

# Gráfico 3: Distribución de siniestros por Día
st.subheader('Distribución de Siniestros por Día')
fig, ax = plt.subplots(figsize=(10, 6))
sns.countplot(data=df_siniestros_final, x='dia', palette='Blues', ax=ax)
ax.set_title('Distribución de siniestros por Día')
ax.set_xlabel('Día')
ax.set_ylabel('Frecuencia')
st.pyplot(fig)

# Gráfico 4: Distribución de siniestros por Tipo de Vía
st.subheader('Distribución de Siniestros por Tipo de Vía')
fig, ax = plt.subplots(figsize=(10, 6))
sns.countplot(data=df_siniestros_final, x='tipo_via', palette='coolwarm', ax=ax)
ax.set_title('Distribución de Siniestros por Tipo de Vía')
ax.set_xlabel('Tipo de Vía')
ax.set_ylabel('Frecuencia')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
st.pyplot(fig)

# Mapa de Calor
st.subheader('Mapa de Calor de Siniestros')
m = folium.Map(location=[-27.480, -58.830], zoom_start=13)
heat_data = [[row['latitud'], row['longitud']] for index, row in df_siniestros_final.iterrows()]
HeatMap(heat_data).add_to(m)
st_folium(m)

# Gráfico 5: Distribución de Siniestros por Hora del Día
df_siniestros_final['hora'] = pd.to_datetime(df_siniestros_final['hora'], format='%H:%M:%S').dt.hour
st.subheader('Distribución de Siniestros por Hora del Día')
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(df_siniestros_final['hora'], bins=24, color='purple', kde=True, ax=ax)
ax.set_title('Distribución de Siniestros por Hora del Día')
ax.set_xlabel('Hora del Día')
ax.set_ylabel('Frecuencia')
st.pyplot(fig)

# Gráfico 6: Frecuencia de Siniestros según Presencia de Semáforo
st.subheader('Frecuencia de Siniestros según Presencia de Semáforo')
fig, ax = plt.subplots(figsize=(10, 6))
sns.countplot(data=df_siniestros_final, x='semaforo', palette='spring', ax=ax)
ax.set_title('Frecuencia de Siniestros según Presencia de Semáforo')
ax.set_xlabel('Semáforo')
ax.set_ylabel('Frecuencia')
st.pyplot(fig)




