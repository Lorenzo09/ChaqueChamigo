import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap

# Cargar los datos de siniestros
df = pd.read_parquet('Datasets_limpios/siniestrosfinal.parquet')

# Título del dashboard
st.title("ChaqueChamigo - Dashboard de Siniestros Viales en Corrientes")

# Mostrar resumen de siniestros
st.header("Resumen de Siniestros")
st.write("Cantidad de siniestros:", df.shape[0])
st.write("Cantidad de heridos:", df['heridos'].sum())
st.write("Cantidad de fallecidos:", df['fallecidos'].sum())

# Visualizar el mapa de calor
st.subheader("Mapa de calor de siniestros")
m = folium.Map(location=[-27.480, -58.830], zoom_start=13)
heat_data = [[row['latitud'], row['longitud']] for index, row in df.iterrows()]
HeatMap(heat_data).add_to(m)
st_data = st._folium_static(m)

# Aquí puedes agregar gráficos usando streamlit.pyplot para los análisis que desees
