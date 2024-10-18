import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import osmnx as ox
import networkx as nx

# Cargar los datos de siniestros
df = pd.read_csv('Datasets_limpios/siniestrosfinal.csv')

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

# Función para obtener coordenadas a partir de direcciones
def get_location(address):
    geolocator = Nominatim(user_agent="chaquechamigo")
    location = geolocator.geocode(address)
    if location:
        return (location.latitude, location.longitude)
    else:
        return None

# Sección de ruta segura
st.subheader("Encuentra la ruta más segura")
start = st.text_input("Ingresa tu dirección de partida:")
end = st.text_input("Ingresa tu destino:")

if st.button("Generar Ruta"):
    # Obtener coordenadas de las direcciones
    start_coords = get_location(start)
    end_coords = get_location(end)
    
    if start_coords and end_coords:
        st.write(f"Coordenadas de partida: {start_coords}")
        st.write(f"Coordenadas de destino: {end_coords}")
        
        # Crear un grafo de las calles en Corrientes
        G = ox.graph_from_place('Corrientes, Argentina', network_type='drive')

        # Usar ox.get_nearest_node para obtener el nodo más cercano
        try:
            start_node = ox.get_nearest_node(G, (start_coords[0], start_coords[1]))
            end_node = ox.get_nearest_node(G, (end_coords[0], end_coords[1]))

            # Definir una función de peso para la ruta, que penaliza áreas con más siniestros
            def custom_weight(u, v, data):
                lat_u, lon_u = G.nodes[u]['y'], G.nodes[u]['x']
                siniestros_cercanos = df[((df['latitud'] - lat_u)**2 + (df['longitud'] - lon_u)**2) < 0.0001]  # Ajusta el rango de cercanía
                penalizacion = len(siniestros_cercanos)
                return data.get('length', 1) * (1 + penalizacion)

            # Obtener la ruta más segura en base al heatmap
            route = ox.shortest_path(G, start_node, end_node, weight=custom_weight)

            # Mostrar la ruta en el mapa
            route_map = ox.plot_route_folium(G, route, route_map=m)
            st_data = st_folium(route_map, width=700, height=500)

        except nx.NodeNotFound:
            st.error("No se pudo encontrar un nodo cercano a las coordenadas proporcionadas. Intenta con una dirección diferente.")
    else:
        st.error("No se pudo obtener la geolocalización de una o ambas direcciones. Intenta con otras.")



