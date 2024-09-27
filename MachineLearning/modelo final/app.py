import streamlit as st
import pandas as pd
import os
from google.cloud import bigquery
from google.oauth2 import service_account
from recomendacion_final import (
    recomendacion_comida_ciudad,
    recomendacion_por_zona,
    recomendacion_segun_palabras,
    recomendacion_reviews_similares
)

# Configurar el cliente de BigQuery
credentials = service_account.Credentials.from_service_account_file(
    os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
 
client = bigquery.Client(credentials=credentials)

# Consulta a BigQuery para cargar los datos
def cargar_datos_bigquery(query):
    try:
        df = client.query(query).to_dataframe()
        return df
    except Exception as e:
        st.error(f"Error al cargar los datos desde BigQuery: {e}")
        return pd.DataFrame()

# Query para los datos de locales
query_business = """
    SELECT * FROM `epicurean_project.recommendation_data.locales_google`
"""

# Query para los datos de reseñas
query_reviews = """
    SELECT * FROM `epicurean_project.recommendation_data.ml_unificado`
"""

# Cargar los DataFrames en memoria desde BigQuery
df_business = cargar_datos_bigquery(query_business)
df_reviews = cargar_datos_bigquery(query_reviews)

if df_business.empty or df_reviews.empty:
    st.error("Error al cargar los datos. Verifica las consultas o la conexión a BigQuery.")


# Estilos para encuadrar las tarjetas con efecto hover
st.markdown(
    """
    <style>
    .tarjeta {
        background-color: #4C5259;
        padding: 15px;
        margin: 15px;
        border: 1px solid #ddd;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        width: 145px;
        transition: transform 0.3s ease;
    }
    .tarjeta:hover {
        transform: scale(1.05);
        box-shadow: 2px 2px 15px rgba(0, 0, 0, 0.3);
    }
    </style>
    """, unsafe_allow_html=True
)

# Agregar el logo
st.image("https://raw.githubusercontent.com/gastorellano/epicurean_project/main/IMG/logo_epicurean.jpeg", width=150)
# Título de la aplicación
st.title("Recomendación de Establecimientos Gastronómicos")

# Sidebar con opciones para seleccionar el tipo de recomendación
st.sidebar.title("Indique sus preferencias")

# Opción 1: Recomendar restaurantes por tipo de comida y ciudad
st.sidebar.header("Recomendación por Tipo de Comida y Ciudad")
tipo_comida = st.sidebar.text_input("Tipo de comida", value="Pizza")
ciudad = st.sidebar.text_input("Ciudad", value="San Diego")
top_n = st.sidebar.slider("Número de recomendaciones", min_value=1, max_value=10, value=5)

if st.sidebar.button("Recomendar por Comida y Ciudad"):
    if not tipo_comida or not ciudad:
        st.warning("Por favor, ingrese un tipo de comida y una ciudad.")
    else:
        resultados = recomendacion_comida_ciudad(df_reviews.copy(), tipo_comida, ciudad, top_n)
        if resultados.empty:
            st.warning(f"No se encontraron restaurantes de {tipo_comida} en {ciudad}.")
        else:
            st.write(f"Top {top_n} restaurantes de **{tipo_comida}** en **{ciudad}**:")
            cols = st.columns(min(len(resultados), top_n))
            for i, col in enumerate(cols):
                if i < len(resultados):
                    with col:
                        address = resultados.iloc[i]['address']
                        google_maps_url = f"https://www.google.com/maps/search/{address.replace(' ', '+')}"
                        st.markdown(f"""
                        <div class="tarjeta">
                        <h4>{resultados.iloc[i]['name']}</h4>
                        <p><b>Rating:</b> {resultados.iloc[i]['avg_rating']}</p>
                        <p><b>Total reviews:</b> {resultados.iloc[i]['num_of_reviews']}</p>
                        <p><b>Category:</b> {resultados.iloc[i]['category']}</p>
                        <p><b>Address:</b> <a href="{google_maps_url}" target="_blank">{address}</a></p>
                        </div>
                        """, unsafe_allow_html=True)

# Opción 2: Recomendar restaurantes por zona (ciudad)
st.sidebar.header("Recomendación por Zona")
ciudad_zona = st.sidebar.text_input("Ciudad para zona", value="San Diego")
top_n_zona = st.sidebar.slider("Número de recomendaciones por zona", min_value=1, max_value=10, value=5)
min_reviews_zona = st.sidebar.slider("Mínimo de reseñas", min_value=1, max_value=100, value=10)

if st.sidebar.button("Recomendar por Zona"):
    if not ciudad_zona:
        st.warning("Por favor, ingrese una ciudad para la zona.")
    else:
        resultados_zona = recomendacion_por_zona(df_business.copy(), ciudad_zona, top_n_zona, min_reviews_zona)
        if resultados_zona.empty:
            st.warning(f"No se encontraron restaurantes en la zona de {ciudad_zona} con al menos {min_reviews_zona} reseñas.")
        else:
            st.write(f"Top {top_n_zona} restaurantes en la zona de **{ciudad_zona}**:")
            cols = st.columns(min(len(resultados_zona), top_n_zona))
            for i, col in enumerate(cols):
                if i < len(resultados_zona):
                    with col:
                        address = resultados_zona.iloc[i]['address']
                        google_maps_url = f"https://www.google.com/maps/search/{address.replace(' ', '+')}"
                        st.markdown(f"""
                        <div class="tarjeta">
                        <h4>{resultados_zona.iloc[i]['name']}</h4>
                        <p><b>Rating:</b> {resultados_zona.iloc[i]['avg_rating']}</p>
                        <p><b>Total reviews:</b> {resultados_zona.iloc[i]['num_of_reviews']}</p>
                        <p><b>Category:</b> {resultados_zona.iloc[i]['category']}</p>
                        <p><b>Address:</b> <a href="{google_maps_url}" target="_blank">{address}</a></p>
                        </div>
                        """, unsafe_allow_html=True)

# Opción 3: Recomendar restaurantes según palabras clave en las reseñas
st.sidebar.header("Recomendación por Palabras Clave")
palabras_clave_input = st.sidebar.text_input("Palabras clave (separadas por comas)", value="pizza, pasta")
min_reviews_palabras = st.sidebar.slider("Mínimo de reseñas", min_value=1, max_value=100, value=10, key="slider_min_reviews_palabras")

if st.sidebar.button("Recomendar por Palabras Clave"):
    if not palabras_clave_input:
        st.warning("Por favor, ingrese al menos una palabra clave.")
    else:
        palabras_clave = [palabra.strip() for palabra in palabras_clave_input.split(',')]
        resultados_palabras = recomendacion_segun_palabras(df_reviews.copy(), palabras_clave, min_reviews_palabras)
        if resultados_palabras.empty:
            st.warning(f"No se encontraron restaurantes que coincidan con las palabras clave: {', '.join(palabras_clave)}.")
        else:
            st.write(f"Restaurantes que coinciden con las palabras clave: **{', '.join(palabras_clave)}**:")
            cols = st.columns(min(len(resultados_palabras), 5))
            for i, col in enumerate(cols):
                if i < len(resultados_palabras):
                    with col:
                        address = resultados_palabras.iloc[i]['address']
                        google_maps_url = f"https://www.google.com/maps/search/{address.replace(' ', '+')}"
                        st.markdown(f"""
                        <div class="tarjeta">
                        <h4>{resultados_palabras.iloc[i]['name']}</h4>
                        <p><b>Address:</b> <a href="{google_maps_url}" target="_blank">{address}</a></p>
                        <p><b>City:</b> {resultados_palabras.iloc[i]['city']}</p>
                        <p><b>Category:</b> {resultados_palabras.iloc[i]['category']}</p>
                        <p><b>Rating:</b> {resultados_palabras.iloc[i]['avg_rating']}</p>
                        <p><b>Total reviews:</b> {resultados_palabras.iloc[i]['num_of_reviews']}</p>
                        <p><b>Text reviews:</b> {resultados_palabras.iloc[i]['text']}</p>
                        </div>
                        """, unsafe_allow_html=True)

# Opción 4: Recomendar restaurantes según reseñas similares
st.sidebar.header("Recomendación por Reseñas Similares")
nombre_restaurante = st.sidebar.text_input("Nombre del restaurante", value="Pizza Hut")
top_n_similares = st.sidebar.slider("Número de recomendaciones similares", min_value=1, max_value=10, value=5)

if st.sidebar.button("Recomendar Reseñas Similares"):
    if not nombre_restaurante:
        st.warning("Por favor, ingrese un nombre de restaurante.")
    else:
        resultados_similares = recomendacion_reviews_similares(df_reviews, nombre_restaurante, top_n_similares)
        if resultados_similares.empty:
            st.warning(f"No se encontraron restaurantes similares a **{nombre_restaurante}**.")
        else:
            st.write(f"Restaurantes similares a **{nombre_restaurante}**:")
            cols = st.columns(min(len(resultados_similares), top_n_similares))
            for i, col in enumerate(cols):
                if i < len(resultados_similares):
                    with col:
                        address = resultados_similares.iloc[i]['address']
                        google_maps_url = f"https://www.google.com/maps/search/{address.replace(' ', '+')}"
                        st.markdown(f"""
                        <div class="tarjeta">
                        <h4>{resultados_similares.iloc[i]['name']}</h4>
                        <p><b>Address:</b> <a href="{google_maps_url}" target="_blank">{address}</a></p>
                        <p><b>City:</b> {resultados_similares.iloc[i]['city']}</p>
                        <p><b>Category:</b> {resultados_similares.iloc[i]['category']}</p>
                        <p><b>Rating:</b> {resultados_similares.iloc[i]['avg_rating']}</p>
                        <p><b>Total reviews:</b> {resultados_similares.iloc[i]['num_of_reviews']}</p>
                        <p><b>Text reviews:</b> {resultados_similares.iloc[i]['text']}</p>
                        </div>
                        """, unsafe_allow_html=True)
