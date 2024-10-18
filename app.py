import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import osmnx as ox
import networkx as nx

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

# Mostrar el mapa en Streamlit y permitir selección interactiva
st.header("Mapa de calor de siniestros - Selecciona el punto de partida y destino")
map_data = st_folium(m, width=700, height=500)

# Inicializar las variables de coordenadas seleccionadas
start_coords = None
end_coords = None

# Verificar si el usuario ha hecho clic en el mapa
if map_data and 'last_clicked' in map_data:
    if not start_coords:
        start_coords = (map_data['last_clicked']['lat'], map_data['last_clicked']['lng'])
        st.write(f"Coordenadas de partida seleccionadas: {start_coords}")
    elif not end_coords:
        end_coords = (map_data['last_clicked']['lat'], map_data['last_clicked']['lng'])
        st.write(f"Coordenadas de destino seleccionadas: {end_coords}")

# Generar el grafo de Corrientes usando OSMnx
if start_coords and end_coords:
    G = ox.graph_from_place('Corrientes, Argentina', network_type='drive')

    # Obtener el nodo más cercano a las coordenadas seleccionadas
    start_node = ox.distance.nearest_nodes(G, start_coords[1], start_coords[0])
    end_node = ox.distance.nearest_nodes(G, end_coords[1], end_coords[0])

    # Calcular la ruta más corta
    route = nx.shortest_path(G, start_node, end_node, weight='length')

    # Mostrar la ruta en el mapa
    route_map = ox.plot_route_folium(G, route, route_map=m)
    st_folium(route_map, width=700, height=500)

