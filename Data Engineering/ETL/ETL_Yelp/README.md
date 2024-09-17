## Análisis Dataset YELP 

El dataset de referencia tiene interesantes datos, muy detallados, que podrían ser de relevancia para nuestro informe.
Sin embargo, cuando hacemos un análisis más profundo, observamos que el dataset business.pkl (un dataset con más de 150.000 registros) tiene una gran orientación a reseñas en la Costa Este.
En nuestro caso, hemos inclinado el análisis al Estado de California, al Sudoeste del país. No obstante, se observa la existencia de unos 5000 registros presuntamente de este Estado.
Al analizar esos datos, se concluye un error en la columna 'state', y la confirmación de que sólo podemos contar con 41 registros de comercios en el Estado de California (0.0273%).

Aún considerando esta escasa cantidad de registros, se cruzan los datos con el dataset review.json, dado que existe la posibilidad de que (más allá de haber sólo una poca cantidad de establecimientos evaluados) el número de reseña sea alto.
Pero se confirma que esto no es así: sólo 214 reseñas sobre esos 41 registros, los cuales no todos son del rubro gastronómico y afines.

Considerando esta situación, y siendo que no aporta una diferencia cuantitativa ni cualitativa a nuestro análisis, **se decide dejar de lado las reseñas de YELP para el presente proyecto**.

