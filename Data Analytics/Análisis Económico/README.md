## Análisis Económico del Estado de California

<p align="center">
  <img src="/IMG/economia_california.jpg" alt="Economia California" />
</p>
El objetivo del proyecto presentado por EPICUREAN Data Solutions es proporcionar a diferentes empresas del sector gastronómico y afines información completa y detallada para tomar decisiones estratégicas.
En el afán de cumplir ese objetivo, no puede ser ajeno al alcance del mismo un análisis de los factores socio-económicos que rodean al Estado de California.
No basta con sostener ciegamente que el Estado de California es la **cuarta economía más grande del Mundo**, sino que podemos respaldar con datos esa apreciación.

Hemos adelantado que los diferentes productos o servicios ofrecidos tienen mayor o menor recepción y popularidad en determinadas zonas de este Estado. Sin embargo, es preciso comenzar analizando la naturaleza económica de los diferentes Condados del Estado de California, para empezar a obtener insights confiables que pongan en el radar del cliente potenciales inversiones, sobre la base de reportes e informes personalizados.
A través del análisis de datos de mercado, se pueden identificar las áreas más rentables para maximizar el retorno de inversión en función de las características de cada empresa.

## Datos utilizados
Esta informacion proviene de diferentes encuestas realizadas por el United States Census Bureau. Detallada demográfica, social, económica y de vivienda de una muestra representativa de hogares en los Estados Unidos. Puede accederse a los datos a través de https://data.census.gov/

En esta primera instancia, se descargaron datos localmente, y se realizó un [proceso de ETL](/Data%20Engineering/ETL/ETL_Censo/ETL_censo.ipynb). Puedes consultar los [archivos iniciales utilizados aquí](https://drive.google.com/drive/folders/1ifNVXNGDjE-oSPRV68v_sc9XprTTDRVv?usp=sharing). El proceso realiza una depuración y normalización de las tablas, elimina duplicados y valores faltantes, para crear un dataset [que se puede descargar aquí](/DATA/datosEconomicos.parquet). Éste tiene diferentes métricas de consideración de condiciones socioeconómicas, divididas por Condado del Estado de California.

## Análisis Económico
Es preciso mencionar que se puede visualizar [aquí](/Data%20Analytics/Análisis%20Económico/Análisis_económico.ipynb) el análisis económico detallado con sus respectivos avances y fundado en gráficos estadísticos.

El análisis económico pretende dar información adicional a nuestros clientes, pero no abarcar la totalidad de las cuestiones vinculadas a gastos, impuestos o costos de implementación de un nuevo comercio.
Es menester recordar que el objeto de este proyecto es realizar un análisis basado en reseñas y sentimientos, para identificar preferencias de consumo en diversas zonas. A partir de allí, el informe económico excede el marco de ésta investigación. Se trata, en definitiva, de una propuesta adicional que efectivamente aportará valor al usuario.


## Conclusiones preliminares del análisis económico

Las decisiones de inversión en el sector gastronómico deben considerar no solo el ingreso y la población, sino también factores como el costo del alquiler, la competencia en el área y las tendencias del consumidor.
Es recomendable realizar un análisis más profundo que incluya variables adicionales, como el gasto promedio en restaurantes, las tendencias de crecimiento de la población y la accesibilidad de la ubicación, para obtener una perspectiva más completa.

Sin embargo, se observa una tendencia favorable a la buena recepción, al menos desde el punto de vista económico, de los condados de Los Ángeles, San Francisco, San Diego, San José y algunos otros.

Este informe puede servir de punto de partida para analizar preferencias de consumo y ubicaciones de los locales gastronómicos existentes.



---
<a href="https://www.linkedin.com/in/gaston-orellano/"><img src="/IMG/lkd.png" alt="LinkedIn" width="40"/></a>