import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests

# Cargar el archivo de datos (ajusta la ruta a tu archivo)
#df_business = pd.read_parquet(r'C:\Users\GASTON\Desktop\PROYECTO FINAL\DATA\locales_google.parquet')
#df_reviews = pd.read_parquet(r'C:\Users\GASTON\Desktop\PROYECTO FINAL\DATA\ml_unificado.parquet')
df_business = pd.read_csv('https://raw.githubusercontent.com/gastorellano/epicurean_project/refs/heads/main/MachineLearning/streamlit/locales_google.csv')
df_reviews = pd.read_csv('https://raw.githubusercontent.com/gastorellano/epicurean_project/refs/heads/main/MachineLearning/streamlit/ml_unificado.csv')

def weighted_rating(x, m, C):
    v = x['num_of_reviews']
    R = x['avg_rating']
    return (v / (v + m) * R) + (m / (v + m) * C)

def recomendacion_comida_ciudad(df, tipo_comida, ciudad, top_n=5):
    # Filtrar por tipo de comida y ciudad
    df_filtrado = df[(df['category'].str.contains(tipo_comida, case=False, na=False)) & 
                     (df['city'].str.contains(ciudad, case=False, na=False))]
    
    if df_filtrado.empty:
        return pd.DataFrame()  # Devuelve un DataFrame vacío si no hay resultados
    
    # Agrupar por gmap_id para evitar duplicados
    df_agrupado = df_filtrado.groupby('gmap_id').agg({
        'name': 'first',  # Mantener el primer nombre del restaurante
        'address': 'first',  # Mantener la primera dirección del restaurante
        'category': 'first',  # Mantener la primera categoría
        'avg_rating': 'mean',  # Calcular el promedio de las calificaciones
        'num_of_reviews': 'sum',  # Sumar todas las reseñas
        'rating': 'mean'  # Calcular el promedio de las calificaciones de las reseñas
    }).reset_index()

    # Calcular la puntuación ponderada
    m = df_agrupado['num_of_reviews'].quantile(0.90)
    C = df_agrupado['avg_rating'].mean()
    df_agrupado['puntuacion'] = weighted_rating(df_agrupado, m, C)
    
    # Ordenar por puntuación
    df_top5 = df_agrupado.sort_values('puntuacion', ascending=False).head(top_n)
    
    return df_top5[['name', 'address', 'category', 'avg_rating', 'num_of_reviews', 'puntuacion']]

def recomendacion_por_zona(df, ciudad, top_n=5, min_reviews=10):
    # Filtrar por ciudad
    df_filtrado = df[df['city'].str.contains(ciudad, case=False, na=False)]

    if df_filtrado.empty:
        return pd.DataFrame()  # Devuelve un DataFrame vacío si no hay resultados

    # Filtrar restaurantes con un mínimo de reseñas
    df_filtrado = df_filtrado[df_filtrado['num_of_reviews'] >= min_reviews]

    if df_filtrado.empty:
        return pd.DataFrame()  # Devuelve un DataFrame vacío si no hay resultados

    # Ordenar por calificación promedio y número de reseñas
    df_top5 = df_filtrado.sort_values(['avg_rating', 'num_of_reviews'], ascending=[False, False]).head(top_n)
    
    return df_top5[['name', 'avg_rating', 'num_of_reviews', 'category', 'address']]

def recomendacion_segun_palabras(df_unificado, palabras_clave, min_reviews=10):
    # Unir las palabras clave en una expresión regular
    palabras_regex = '|'.join([f'\\b{palabra.strip()}\\b' for palabra in palabras_clave])

    # Filtrar las reseñas que contienen las palabras clave
    df_filtrado = df_unificado[df_unificado['text'].str.contains(palabras_regex, case=False, na=False)]

    if df_filtrado.empty:
        return pd.DataFrame()  # Devuelve un DataFrame vacío si no hay resultados

    # Agrupar por gmap_id
    df_agrupado = df_filtrado.groupby('gmap_id').agg({
        'name': 'first',
        'address': 'first',
        'city': 'first',
        'category': 'first',
        'avg_rating': 'mean',
        'num_of_reviews': 'sum',
        'rating': 'mean',
        'text': 'first'
    }).reset_index()

    # Filtrar restaurantes con un mínimo de reseñas
    df_agrupado = df_agrupado[df_agrupado['num_of_reviews'] >= min_reviews]

    if df_agrupado.empty:
        return pd.DataFrame()  # Devuelve un DataFrame vacío si no hay resultados

    # Ordenar por calificación promedio y número de reseñas
    df_top = df_agrupado.sort_values(['avg_rating', 'num_of_reviews'], ascending=[False, False]).head(10)

    return df_top[['name', 'address', 'city', 'category', 'avg_rating', 'num_of_reviews', 'text']]

def recomendacion_reviews_similares(df_unificado, nombre_restaurante, top_n=5):
    # Filtrar el DataFrame para encontrar el restaurante
    df_restaurante = df_unificado[df_unificado['name'].str.contains(nombre_restaurante, case=False, na=False)]

    if df_restaurante.empty:
        return pd.DataFrame()  # Devuelve un DataFrame vacío si no se encuentra el restaurante

    # Obtener el gmap_id del restaurante
    gmap_id_restaurante = df_restaurante.iloc[0]['gmap_id']

    # Filtrar las reseñas que tienen texto y corresponden a este restaurante
    df_reseñas_restaurante = df_unificado[(df_unificado['text'].notnull()) & (df_unificado['gmap_id'] == gmap_id_restaurante)]

    if df_reseñas_restaurante.empty:
        return pd.DataFrame()  # Devuelve un DataFrame vacío si no se encuentran reseñas

    # Crear la matriz TF-IDF para las reseñas combinadas
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix_reseñas = tfidf.fit_transform(df_reseñas_restaurante['text'])  
    tfidf_matrix_todas_reseñas = tfidf.transform(df_unificado['text'])

    # Calcular la similitud del coseno entre las reseñas del restaurante y todas las reseñas
    cosine_sim = cosine_similarity(tfidf_matrix_reseñas, tfidf_matrix_todas_reseñas)

    # Obtener el índice de reseñas más similares
    sim_scores = list(enumerate(cosine_sim.mean(axis=0)))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[:top_n]

    # Obtener los índices de los restaurantes recomendados
    restaurant_indices = [i[0] for i in sim_scores]

    if restaurant_indices:
        recomendaciones = df_unificado.iloc[restaurant_indices].drop_duplicates(subset='gmap_id')
        recomendaciones = recomendaciones[['name', 'address', 'city', 'category', 'avg_rating', 'num_of_reviews', 'text']].reset_index(drop=True)
    else:
        recomendaciones = pd.DataFrame()  # DataFrame vacío si no hay recomendaciones

    return recomendaciones
