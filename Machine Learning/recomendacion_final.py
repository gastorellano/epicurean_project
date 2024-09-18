# Importar las librerías necesarias
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Cargar el archivo de datos (ajusta la ruta a tu archivo)
df_business = pd.read_parquet(r'C:\Users\GASTON\Desktop\PROYECTO FINAL\DATA\locales_google.parquet')  # Tabla de negocios
df_reviews = pd.read_parquet(r'C:\Users\GASTON\Desktop\PROYECTO FINAL\DATA\ml_unificado.parquet')  # Tabla de reseñas con datos en 'text' unificada con los negocios


def weighted_rating(x, m, C):
    v = x['num_of_reviews']
    R = x['avg_rating']
    return (v / (v + m) * R) + (m / (v + m) * C)

def recomendacion_comida_ciudad(df, tipo_comida, ciudad, top_n=5):
    '''
    Esta función recibe un DataFrame sobre el que trabaja, el tipo de comida y la ciudad que se busca.
    Devuelve una recomendación de los locales con mejor puntuación ponderada que coincidan con esos criterios.
    '''
    # Filtrar por tipo de comida y ciudad
    df_filtrado = df[(df['category'].str.contains(tipo_comida, case=False, na=False)) & 
                     (df['city'].str.contains(ciudad, case=False, na=False))]
    
    if df_filtrado.empty:
        return f"No se encontraron restaurantes de {tipo_comida} en {ciudad}."
    
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
    
    # Seleccionar las columnas relevantes para mostrar
    return df_top5[['name', 'address', 'category', 'avg_rating', 'num_of_reviews', 'puntuacion']]

def recomendacion_por_zona(df, ciudad, top_n=5, min_reviews=10):
    '''
    Esta función recibe un DataFrame, y una ciudad o zona del Estado de California.
    Devuelve un top 10 de los mejores locales según la calificación ponderada.
    Pueden no haber reseñas suficientes en la ciudad o zona seleccionada.
    '''
    # Filtrar por ciudad
    df_filtrado = df[df['city'].str.contains(ciudad, case=False, na=False)]
    
    if df_filtrado.empty:
        return f"No se encontraron restaurantes en {ciudad}."
    
    # Filtrar solo restaurantes con un mínimo de reseñas
    df_filtrado = df_filtrado[df_filtrado['num_of_reviews'] >= min_reviews]
    
    if df_filtrado.empty:
        return f"No se encontraron restaurantes con al menos {min_reviews} reseñas en {ciudad}."
    
    # Ordenar por calificación promedio y número de reseñas
    df_top5 = df_filtrado.sort_values(['avg_rating', 'num_of_reviews'], ascending=[False, False]).head(top_n)
    
    # Seleccionar las columnas relevantes para mostrar
    return df_top5[['name', 'avg_rating', 'num_of_reviews', 'category', 'address']]


def recomendacion_segun_palabras(df_unificado, palabras_clave, min_reviews=10):
    '''
    Esta función recibe un DataFrame y una lista de palabras clave.
    Busca las reseñas que tengan esas palabras clave, y las ordena según la puntuación ponderada.
    Devuelve una tabla con los locales mejor ponderados que respeten los criterios de búsqueda.
    '''
    # Unir las palabras clave en una expresión regular
    palabras_regex = '|'.join([f'\\b{palabra}\\b' for palabra in palabras_clave])
    
    # Filtrar las reseñas que contienen las palabras clave
    df_filtrado = df_unificado[df_unificado['text'].str.contains(palabras_regex, case=False, na=False)]
    
    if df_filtrado.empty:
        return "No se encontraron reseñas con las palabras clave."
    
    # Agrupar por gmap_id para evitar duplicados
    df_agrupado = df_filtrado.groupby('gmap_id').agg({
        'name': 'first',  # Mantener el primer nombre del restaurante
        'address': 'first',  # Mantener la primera dirección del restaurante
        'city': 'first',  # Mantener la primera ciudad
        'category': 'first',  # Mantener la primera categoría
        'avg_rating': 'mean',  # Promedio de la calificación
        'num_of_reviews': 'sum',  # Sumar el número total de reseñas
        'rating': 'mean',  # Promedio de las calificaciones de las reseñas
        'text': 'first'  # Mantener el primer texto de reseña
    }).reset_index()
    
    # Filtrar solo restaurantes con un mínimo de reseñas
    df_agrupado = df_agrupado[df_agrupado['num_of_reviews'] >= min_reviews]
    
    if df_agrupado.empty:
        return f"No se encontraron restaurantes con al menos {min_reviews} reseñas que contengan las palabras clave."
    
    # Ordenar por calificación promedio y número de reseñas
    df_top = df_agrupado.sort_values(['avg_rating', 'num_of_reviews'], ascending=[False, False])
    
    # Seleccionar las columnas relevantes para mostrar
    return df_top[['name', 'address', 'city', 'category', 'avg_rating', 'num_of_reviews', 'text']].head(10)

def recomendacion_reviews_similares(df_unificado, nombre_restaurante, top_n=5):
    '''
    Esta función recibe un dataframe, y el nombre de un local gastronómico.
    Devolverá una recomendación de una categoría similar, y con reseñas similares.
    '''
    # Filtrar el DataFrame para encontrar el restaurante
    df_restaurante = df_unificado[df_unificado['name'].str.contains(nombre_restaurante, case=False, na=False)]
    
    if df_restaurante.empty:
        return f"No se encontraron restaurantes con el nombre {nombre_restaurante}."
    
    # Obtener el gmap_id del restaurante
    gmap_id_restaurante = df_restaurante.iloc[0]['gmap_id']
    
    # Filtrar las reseñas que tienen texto y corresponden a este restaurante
    df_reseñas_restaurante = df_unificado[(df_unificado['text'].notnull()) & (df_unificado['gmap_id'] == gmap_id_restaurante)]
    
    if df_reseñas_restaurante.empty:
        return f"No se encontraron reseñas para el restaurante {nombre_restaurante}."
    
    # Crear la matriz TF-IDF para las reseñas combinadas
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix_reseñas = tfidf.fit_transform(df_reseñas_restaurante['category_text'])
    tfidf_matrix_todas_reseñas = tfidf.transform(df_unificado['category_text'])
    
    # Calcular la similitud del coseno entre las reseñas del restaurante y todas las reseñas
    cosine_sim = cosine_similarity(tfidf_matrix_reseñas, tfidf_matrix_todas_reseñas)
    
    # Obtener el índice de reseñas más similares
    sim_scores = list(enumerate(cosine_sim.mean(axis=0)))  # Usar la media de similitud para comparar con todas las reseñas
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[:top_n]
    
    # Obtener los índices de los restaurantes recomendados
    restaurant_indices = [i[0] for i in sim_scores]
    
    # Asegurarse de que los índices están dentro del rango del DataFrame
    if restaurant_indices:
        # Obtener información de los restaurantes recomendados
        recomendaciones = df_unificado.iloc[restaurant_indices].drop_duplicates(subset='gmap_id')
        recomendaciones = recomendaciones[['name', 'address', 'city', 'category', 'avg_rating', 'num_of_reviews', 'text']].reset_index(drop=True)
    else:
        recomendaciones = pd.DataFrame()  # Devolver un DataFrame vacío si no hay recomendaciones
    
    return recomendaciones