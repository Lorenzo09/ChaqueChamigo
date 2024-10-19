🚦 Chaque Chamigo 🚦
¡Bienvenido al proyecto Chaque Chamigo! Este es un proyecto de análisis y visualización de rutas seguras basado en datos de siniestros viales en tiempo real y su visualización interactiva. 🎯 El dashboard permite a los usuarios encontrar las rutas más seguras entre dos puntos dentro de una ciudad, utilizando modelos de predicción y análisis geoespacial. 🌍

🛠️ Características Principales
📊 KPIs y Visualizaciones Interactivas: Muestra métricas clave sobre siniestros viales y semáforos, con gráficos interactivos.
📍 Recomendación de Rutas Seguras: Utiliza un algoritmo basado en grafos para encontrar la ruta más segura entre dos puntos, minimizando la cantidad de siniestros viales a lo largo del trayecto.
🛣️ Visualización de Mapas: Muestra las rutas recomendadas en mapas interactivos con Folium.
🔍 Análisis Predictivo: Usa modelos de regresión para predecir posibles siniestros viales basados en el tiempo y la ubicación.
🚀 Tecnologías Utilizadas
Este proyecto fue desarrollado utilizando las siguientes herramientas:

Python 🐍
Streamlit para la creación de dashboards interactivos 📊
Folium para visualizaciones de mapas 🌍
OSMnx para el análisis de rutas y grafos 🛣️
NetworkX para el manejo de redes y grafos 📈
Scikit-learn para modelos predictivos de Machine Learning 🤖
Pandas y Geopandas para manipulación de datos 🧮
📂 Estructura del Proyecto
bash
Copiar código
📁 SafeRoutesDashboard/
├── 📄 app.py               # Código principal del dashboard
├── 📄 requirements.txt     # Dependencias del proyecto
├── 📄 README.md            # Archivo de documentación (este mismo 😄)
├── 📁 data/                # Carpeta con los datasets utilizados
└── 📁 JupyterNotebooks/    # Códigos ipynb de ETL y EDA

🚦 Descripción del Proyecto
Este proyecto busca mejorar la seguridad vial utilizando datos reales de siniestros y semáforos. Los usuarios pueden ingresar un punto de inicio y un destino, y la aplicación les mostrará la ruta más segura, evitando las zonas con mayor número de accidentes.

¿Cómo funciona?
Datos de Entrada: El usuario ingresa coordenadas geográficas (latitud y longitud) de inicio y fin.
Generación de Grafos: El sistema crea un grafo donde los nodos son intersecciones y las aristas (conexiones) son las calles ponderadas por la cantidad de siniestros viales.
Ruta Segura: Utilizando el algoritmo de caminos más cortos, el sistema calcula la ruta con menor cantidad de siniestros viales.
Visualización: Finalmente, se despliega un mapa interactivo con la ruta recomendada. 📍

🏃‍♂️ Cómo Ejecutar el Proyecto
Para correr este proyecto en tu máquina local, sigue los siguientes pasos:

Clona el repositorio:

bash
Copiar código
git clone https://github.com/tu-usuario/safe-routes-dashboard.git
cd safe-routes-dashboard
Instala las dependencias: Asegúrate de tener Python 3.x instalado. Luego, instala las dependencias necesarias:

bash
Copiar código
pip install -r requirements.txt
Ejecuta la aplicación:

bash
Copiar código
streamlit run app.py
¡Explora la aplicación en tu navegador! Deberías ver el dashboard en http://localhost:8501.

O simplemente haz click en el siguiente [link](https://chaquechamigo.streamlit.app/)

📊 Capturas del Dashboard
Aquí algunas capturas del proyecto funcionando:

Panel de Control Principal 📊
<img src="../ChaqueChamigo/capturas/Dashboard1.jpeg" alt="Dashboard Principal" width="600"/>
<img src="../ChaqueChamigo/capturas/Dashboard2.jpeg" alt="Dashboard Principal" width="600"/>

Rutas Seguras Mapeadas 🗺️
<img src="../ChaqueChamigo/capturas/Dashboard4.jpeg" alt="Rutas Seguras" width="600"/>

📈 Modelos Predictivos
Este proyecto también incluye un componente de machine learning, donde se utilizan modelos de regresión lineal para predecir la cantidad de siniestros viales en diferentes horarios del día y en distintas intersecciones.

🤝 Contribuciones
¡Las contribuciones son bienvenidas! Si tienes alguna idea para mejorar este proyecto, siéntete libre de hacer un fork y enviar un pull request. También puedes abrir issues para reportar bugs o sugerir nuevas funcionalidades.

🔗 Contacto
Cualquier consulta o duda, puedes contactarme por:

Email: lorenzo.lacava@example.com
GitHub: Lorenzo Lacava
LinkedIn: Lorenzo Lacava