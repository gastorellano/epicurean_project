import streamlit as st
import pandas as pd
from recomendacion_final import (
    recomendacion_comida_ciudad,
    recomendacion_por_zona,
    recomendacion_segun_palabras,
    recomendacion_reviews_similares
)

# Cargar los DataFrames en memoria
df_business = pd.read_parquet(r'C:\Users\GASTON\Desktop\PROYECTO FINAL\DATA\locales_google.parquet')
df_reviews = pd.read_parquet(r'C:\Users\GASTON\Desktop\PROYECTO FINAL\DATA\ml_unificado.parquet')

# Título de la aplicación
st.title("Sistema de Recomendación de Restaurantes")

# Sidebar con opciones para seleccionar el tipo de recomendación
st.sidebar.title("Opciones de recomendación")

# Opción 1: Recomendar restaurantes por tipo de comida y ciudad
st.sidebar.header("Recomendación por Tipo de Comida y Ciudad")
tipo_comida = st.sidebar.text_input("Tipo de comida", value="Pizza")
ciudad = st.sidebar.text_input("Ciudad", value="Buenos Aires")
top_n = st.sidebar.slider("Número de recomendaciones", min_value=1, max_value=10, value=5)

if st.sidebar.button("Recomendar por Comida y Ciudad"):
    resultados = recomendacion_comida_ciudad(df_reviews, tipo_comida, ciudad, top_n)
    st.write(f"Top {top_n} restaurantes de {tipo_comida} en {ciudad}:")
    st.write(resultados)

# Opción 2: Recomendar restaurantes por zona (ciudad)
st.sidebar.header("Recomendación por Zona")
ciudad_zona = st.sidebar.text_input("Ciudad para zona", value="Buenos Aires")
top_n_zona = st.sidebar.slider("Número de recomendaciones por zona", min_value=1, max_value=10, value=5)
min_reviews_zona = st.sidebar.slider("Mínimo de reseñas", min_value=1, max_value=100, value=10)

if st.sidebar.button("Recomendar por Zona"):
    resultados_zona = recomendacion_por_zona(df_business, ciudad_zona, top_n_zona, min_reviews_zona)
    st.write(f"Top {top_n_zona} restaurantes en la zona de {ciudad_zona}:")
    st.write(resultados_zona)

# Opción 3: Recomendar restaurantes según palabras clave en las reseñas
st.sidebar.header("Recomendación según Palabras Clave")
palabras_clave = st.sidebar.text_input("Palabras clave (separadas por coma)", value="delicioso,ambiente")
min_reviews_palabras = st.sidebar.slider("Mínimo de reseñas para palabras clave", min_value=1, max_value=100, value=10)

if st.sidebar.button("Recomendar por Palabras Clave"):
    resultados_palabras = recomendacion_segun_palabras(df_reviews, palabras_clave.split(','), min_reviews_palabras)
    st.write(f"Restaurantes que coinciden con las palabras clave {palabras_clave}:")
    st.write(resultados_palabras)

# Opción 4: Recomendar restaurantes según reseñas similares
st.sidebar.header("Recomendación por Reseñas Similares")
nombre_restaurante = st.sidebar.text_input("Nombre del restaurante", value="La Parolaccia")
top_n_similares = st.sidebar.slider("Número de recomendaciones similares", min_value=1, max_value=10, value=5)

if st.sidebar.button("Recomendar Reseñas Similares"):
    resultados_similares = recomendacion_reviews_similares(df_reviews, nombre_restaurante, top_n_similares)
    st.write(f"Restaurantes similares a {nombre_restaurante}:")
    st.write(resultados_similares)

# Información adicional
st.sidebar.info("Sistema de recomendación de restaurantes basado en reseñas y datos de usuarios.")
