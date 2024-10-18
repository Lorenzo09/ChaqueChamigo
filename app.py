import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

# Cargar los datos de siniestros
df = pd.read_parquet('Datasets_limpios/siniestrosfinal.parquet')

# Título del dashboard
st.title("ChaqueChamigo - Dashboard de Siniestros Viales en Corrientes")

# Resumen de siniestros
st.header("Resumen de Siniestros")
st.write(f"Cantidad de siniestros: {len(df)}")
st.write(f"Cantidad de heridos: {df['heridos'].sum()}")
st.write(f"Cantidad de fallecidos: {df['fallecidos'].sum()}")

# Crear un mapa de Folium
m = folium.Map(location=[-27.467, -58.834], zoom_start=12)

# Crear lista de puntos de calor
heat_data = [[row['latitud'], row['longitud']] for index, row in df.iterrows()]

# Agregar el HeatMap al mapa
HeatMap(heat_data).add_to(m)

# Mostrar el mapa en Streamlit
st.header("Mapa de calor de siniestros")
st_folium(m, width=700, height=500)
