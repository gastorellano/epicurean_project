from fastapi import FastAPI
import pandas as pd
from recomendacion_final import (
    recomendacion_comida_ciudad,
    recomendacion_por_zona,
    recomendacion_segun_palabras,
    recomendacion_reviews_similares
)

# Crear una instancia de FastAPI
app = FastAPI()

# Cargar DataFrames en memoria al iniciar la API
df_business = pd.read_parquet(r'C:\Users\GASTON\Desktop\PROYECTO FINAL\DATA\locales_google.parquet')
df_reviews = pd.read_parquet(r'C:\Users\GASTON\Desktop\PROYECTO FINAL\DATA\ml_unificado.parquet')

# Endpoint 1: Recomendar restaurantes por tipo de comida y ciudad
@app.get("/recomendar/sabor/{tipo_comida}/{ciudad}")
def recomendar_comida_ciudad(tipo_comida: str, ciudad: str, top_n: int = 5):
    try:
        return recomendacion_comida_ciudad(df_reviews, tipo_comida, ciudad, top_n)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en recomendar_comida_ciudad: {e}")

from fastapi import HTTPException

# Endpoint 2: Recomendar restaurantes por ciudad (zona)
@app.get("/recomendar/zona/{ciudad}")
def recomendar_por_zona(ciudad: str, top_n: int = 5, min_reviews: int = 10):
    try:
        return recomendacion_por_zona(df_business, ciudad, top_n, min_reviews)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en recomendar_por_zona: {e}")


# Endpoint 3: Recomendar restaurantes según palabras clave en las reseñas
@app.get("/recomendar/palabras")
def recomendar_segun_palabras(palabras_clave: str, min_reviews: int = 10):
    try:
        return recomendacion_segun_palabras(df_reviews, palabras_clave.split(','), min_reviews)  # Separar las palabras clave
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en recomendar_segun_palabras: {e}")

    
# Endpoint 4: Recomendar restaurantes según reseñas similares
@app.get("/recomendar/similares/{nombre_restaurante}")
def recomendar_reviews_similares(nombre_restaurante: str, top_n: int = 5):
    try:
        return recomendacion_reviews_similares(df_reviews, nombre_restaurante, top_n)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en recomendar_reviews_similares: {e}")
