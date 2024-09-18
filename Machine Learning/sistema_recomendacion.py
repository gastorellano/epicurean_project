from fastapi import FastAPI
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Crear una instancia de FastAPI
app = FastAPI()

# Cargar DataFrames en memoria al iniciar la API
df_business = pd.read_parquet(r'C:\Users\GASTON\Desktop\PROYECTO FINAL\DATA\locales_google.parquet')
df_reviews = pd.read_parquet(r'C:\Users\GASTON\Desktop\PROYECTO FINAL\DATA\ml_unificado.parquet')

# Función de puntuación ponderada
def weighted_rating(x, m, C):
    v = x['num_of_reviews']
    R = x['avg_rating']
    return (v / (v + m) * R) + (m / (v + m) * C)

# Endpoint 1: Recomendar restaurantes por tipo de comida y ciudad
@app.get("/recomendar/sabor/{tipo_comida}/{ciudad}")
def recomendacion_comida_ciudad(tipo_comida: str, ciudad: str, top_n: int = 5):
    df_filtrado = df_reviews[(df_reviews['category'].str.contains(tipo_comida, case=False, na=False)) & 
                             (df_reviews['city'].str.contains(ciudad, case=False, na=False))]
    
    if df_filtrado.empty:
        return {"message": f"No se encontraron restaurantes de {tipo_comida} en {ciudad}."}
    
    df_agrupado = df_filtrado.groupby('gmap_id').agg({
        'name': 'first',
        'address': 'first',
        'category': 'first',
        'avg_rating': 'mean',
        'num_of_reviews': 'sum',
        'rating': 'mean'
    }).reset_index()

    m = df_agrupado['num_of_reviews'].quantile(0.90)
    C = df_agrupado['avg_rating'].mean()
    df_agrupado['puntuacion'] = weighted_rating(df_agrupado, m, C)
    df_top5 = df_agrupado.sort_values('puntuacion', ascending=False).head(top_n)
    
    return df_top5[['name', 'address', 'category', 'avg_rating', 'num_of_reviews', 'puntuacion']].to_dict(orient='records')

# Endpoint 2: Recomendar restaurantes por ciudad (zona)
@app.get("/recomendar/zona/{ciudad}")
def recomendacion_por_zona(ciudad: str, top_n: int = 5, min_reviews: int = 10):
    df_filtrado = df_business[df_business['city'].str.contains(ciudad, case=False, na=False)]
    
    if df_filtrado.empty:
        return {"message": f"No se encontraron restaurantes en {ciudad}."}
    
    df_filtrado = df_filtrado[df_filtrado['num_of_reviews'] >= min_reviews]
    
    if df_filtrado.empty:
        return {"message": f"No se encontraron restaurantes con al menos {min_reviews} reseñas en {ciudad}."}
    
    df_top5 = df_filtrado.sort_values(['avg_rating', 'num_of_reviews'], ascending=[False, False]).head(top_n)
    return df_top5[['name', 'avg_rating', 'num_of_reviews', 'category', 'address']].to_dict(orient='records')

# Endpoint 3: Recomendar restaurantes según palabras clave en las reseñas
@app.get("/recomendar/palabras")
def recomendacion_segun_palabras(palabras_clave: str, min_reviews: int = 10):
    palabras_lista = palabras_clave.split(',')
    palabras_regex = '|'.join([f'\\b{palabra.strip()}\\b' for palabra in palabras_lista])
    
    df_filtrado = df_reviews[df_reviews['text'].str.contains(palabras_regex, case=False, na=False)]
    
    if df_filtrado.empty:
        return {"message": "No se encontraron reseñas con las palabras clave."}
    
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
    
    df_agrupado = df_agrupado[df_agrupado['num_of_reviews'] >= min_reviews]
    
    if df_agrupado.empty:
        return {"message": f"No se encontraron restaurantes con al menos {min_reviews} reseñas que contengan las palabras clave."}
    
    df_top = df_agrupado.sort_values(['avg_rating', 'num_of_reviews'], ascending=[False, False]).head(10)
    return df_top[['name', 'address', 'city', 'category', 'avg_rating', 'num_of_reviews', 'text']].to_dict(orient='records')

# Endpoint 4: Recomendar restaurantes según reseñas similares
@app.get("/recomendar/similares/{nombre_restaurante}")
def recomendacion_reviews_similares(nombre_restaurante: str, top_n: int = 5):
    df_restaurante = df_reviews[df_reviews['name'].str.contains(nombre_restaurante, case=False, na=False)]
    
    if df_restaurante.empty:
        return {"message": f"No se encontraron restaurantes con el nombre {nombre_restaurante}."}
    
    gmap_id_restaurante = df_restaurante.iloc[0]['gmap_id']
    df_reseñas_restaurante = df_reviews[(df_reviews['text'].notnull()) & (df_reviews['gmap_id'] == gmap_id_restaurante)]
    
    if df_reseñas_restaurante.empty:
        return {"message": f"No se encontraron reseñas para el restaurante {nombre_restaurante}."}
    
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix_reseñas = tfidf.fit_transform(df_reseñas_restaurante['category_text'])
    tfidf_matrix_todas_reseñas = tfidf.transform(df_reviews['category_text'])
    
    cosine_sim = cosine_similarity(tfidf_matrix_reseñas, tfidf_matrix_todas_reseñas)
    
    sim_scores = list(enumerate(cosine_sim.mean(axis=0)))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[:top_n]
    
    restaurant_indices = [i[0] for i in sim_scores]
    
    if restaurant_indices:
        recomendaciones = df_reviews.iloc[restaurant_indices].drop_duplicates(subset='gmap_id')
        return recomendaciones[['name', 'address', 'city', 'category', 'avg_rating', 'num_of_reviews', 'text']].to_dict(orient='records')
    else:
        return {"message": "No se encontraron recomendaciones similares."}
