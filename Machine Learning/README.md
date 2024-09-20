## Implementación de Sistema de Recomendación
<p align="center">
  <img src="/IMG/recomendacion.jpeg" alt="sistema de recomendación" />
</p>

El sistema de recomendación implementado pretende dar una serie de opciones al usuario, para que obtenga sugerencias de diversos locales gastronómicos, sobre la base de una serie de criterios.

- Recomendación según ciudad y preferencia (la cual puede ser un alimento, categoría, etc.).
- Recomendación de los mejores comercios gastronómicos según una zona o ciudad.
- Recomendación a partir de análisis de sentimientos, buscando las palabras claves a partir de reseñas en la columna 'text'.
- Recomendación a partir de las reseñas similares, de un comercio indicado por el usuario.

<p align="center">
  <img src="/IMG/recomendacion_review.jpg" alt="reviews" />
</p>


Tras la carga de datos, se realiza un proceso de ETL, eliminación de registros nulos, duplicados, y se obtienen dos archivos .parquet con los datos de los comercios y las reseñas disponibles.
Se crea un archivo unificado, que se usará para uno de los modelos, que cuenta con aquellos reviews con reseñas escritas, y se eliminan las columnas que no se van a utilizar en el modelo.
A continuación, se detallarán los pasos para el desarrollo de los modelos.

<p align="center">
  <img src="/IMG/desarrollo-MVP.jpeg" alt="MVP" />
</p>

## Forma de desarrollo e implementación
- Importación de Galerías necesarias:
Previo a cualquier desarrollo, deben instalarse y descargarse las galerías necesarias.

- Carga de Datos
En primer término, como se ha aclarado, se realiza un proceso de ETL y se generan dos archivos que darán lugar a la primera muestra para la implementación del modelo.

- Se declaran las funciones necesarias:

En primer lugar, se declara una función que calcula una puntuación ponderada, a partir del promedio de reseñas, y también de la cantidad de reseñas de cada comercio.
Esta función será necesaria para el ranking que retornará cada función de recomendación.

A continuación, se crean diferentes sistemas de recomendación, que darán lugar a los diferentes endpoints.

1) Recomendación por preferencia y zona:

El primer modelo, recibe una preferencia (como comida o categoría), y una zona (que puede ser un 'lugar' o ciudad, según están distribuidos los Condados del Estado de California).
Este sistema de recomendación está diseñado para recomendar los mejores locales de comida en una ciudad específica, basándose en el tipo de comida y utilizando una puntuación ponderada que toma en cuenta la calificación y el número de reseñas.

El modelo busca todos los locales cuya categoría de comida coincida con el tipo de comida ingresado y que se encuentren en la ciudad especificada. Utiliza expresiones regulares para buscar coincidencias de texto, sin distinguir entre mayúsculas y minúsculas. 
Para evitar que se repitan los comercios, agrupa por la columna 'gmap_id', y selecciona las columnas deseadas.
Luego, aplica la función de la puntuación ponderada, y ordena en forma descendente de acuerdo a la misma.

2) Recomendación general por zona:

Este modelo de recomendación está diseñado para proporcionar una lista de los mejores locales en una ciudad o zona específica, basándose en la calificación promedio y el número de reseñas. 
No toma la preferencia (comida o categoría), sino los locales mejor puntuados en determinada ciudad.
El modelo busca los locales de la ciudad o zona especificada. Utiliza expresiones regulares para buscar coincidencias, sin distinguir entre mayúsculas y minúsculas. Luego, se filtran aquellos que tengan al menos el número mínimo de reseñas, que es 10 por defecto. Allí, los registros se ordenan en base a la puntuación ponderada (calificación promedio y número de reseñas), en orden descendente.


3) Recomendación según palabras clave:

Este modelo recibe una lista de palabras clave, que serán matcheadas con la columna 'text' (reseñas escritas). Luego, ordena los resultados a partir de las calificaciones ponderadas.

Se construye una expresión regular (regex) que permite buscar las palabras clave dentro del texto de las reseñas de manera eficiente. Las palabras clave se unen utilizando el operador |, que significa "o" en regex, y se usan bordes de palabra (\\b) para asegurarse de que las palabras clave sean buscadas como palabras completas (no como partes de otras palabras). Este enfoque hace que la búsqueda sea más precisa.

Se buscan las reseñas que contienen al menos una de las palabras clave. Luego, agrupa los resultados por gmap_id para evitar que se repita el mismo negocio. Se toman los valores, y ordenarán de acuerdo a la calificación ponderada.
Finalmente, se seleccionan las columnas más relevantes para mostrar en el resultado: nombre, dirección, ciudad, categoría, calificación promedio, número de reseñas y el texto de una reseña representativa. Se muestran los 10 mejores resultados ordenados.


4) Recomendación en base a reseñas similares:

Este es el modelo más complejo, y busca recomendar locales gastronómicos con categorías y reseñas similares al restaurante que se proporciona como entrada. 
El modelo busca un restaurante cuyo nombre coincida con el que el usuario ingresa. Para evitar problemas con mayúsculas o minúsculas, utiliza una búsqueda insensible a estas diferencias. Si no se encuentra el restaurante, la función retorna un mensaje informando que no se encontraron resultados.
Si se encuentra, se extrae su identificador único (gmap_id), para filtrar las reseñas correspondientes a ese local, la cual servirá para obtener las reseñas relacionadas a ese restaurante que contienen texto. 
Es necesario mencionar que se incorpora una columna, que combina el texto de las reseñas y la categoría.

Para realizar la recomendación, se toman en cuenta los siguientes pasos:

**Vectorización TF-IDF de las reseñas**: 
El modelo convierte el texto de las reseñas en una representación numérica utilizando la técnica TF-IDF (Term Frequency-Inverse Document Frequency). Esto permite cuantificar la relevancia de las palabras en las reseñas, excluyendo palabras comunes en inglés que no aportan mucho al análisis (palabras vacías o "stop words"). Se realiza esta transformación tanto en las reseñas del restaurante como en todas las reseñas del DataFrame unificado, lo que facilita la comparación.

**Cálculo de la similitud entre reseñas**: 
Una vez vectorizadas las reseñas, se utiliza la similitud del coseno (medida que cuantifica la semejanza entre dos vectores, calculando el coseno del ángulo entre ellos) para comparar las reseñas del restaurante seleccionado con todas las reseñas del DataFrame . La similitud del coseno mide cuán similares son dos textos basados en la orientación de sus vectores en el espacio TF-IDF. Se toma la media de la similitud de todas las reseñas del restaurante para compararlas con el resto de los locales.

**Selección de las reseñas más similares**: 
La función ordena las reseñas en base a la similitud obtenida, priorizando aquellas con mayor similitud a las reseñas del restaurante de entrada. Luego, selecciona los top_n restaurantes (5 por defecto) con reseñas similares.

**Obtención de información de los restaurantes recomendados**: A partir de los índices de las reseñas más similares, la función extrae la información de los locales recomendados, como el nombre, dirección, ciudad, categoría, calificación promedio, número de reseñas, y el texto de la reseña. Si no hay recomendaciones válidas, se devuelve un DataFrame vacío.


- Crear instancia de FastAPI:
Para desplegar el modelo en una API, se utiliza FastAPI. En el archivo sistema_recomendacion.py, se instancia la misma.

- Declarar endpoints HTTP:
En el archivo principal de la API, se declara cada uno de los endpoints que corresponden a los sistemas de recomendación desarrollados. Estos endpoints permiten la interacción con la API para realizar recomendaciones basadas en diferentes criterios.

## Prueba del Sistema de Recomendación:
Puedo ver la prueba de mi sistema de recomendación [aquí](https://drive.google.com/file/d/1L5St4tRXbFGrvCxId5KMWVALMLEPTQJ0/view?usp=sharing).