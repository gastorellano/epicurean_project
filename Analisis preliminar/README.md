## Análisis Explotatorio de Datos (Google Maps y Yelp)

En primer término, corresponde analizar (preliminarmente) la calidad de los datos analizados. Por ese motivo, se ha procedido a identificar la confiabilidad, cantidad y calidad de los datasets que inicialmente utilizaremos para llevar adelante nuestro informe.

Se parte de dos conjuntos de datasets, que contienen reseñas de los servicios de Google Maps y Yelp. El primero es considerablemente superior al segundo en cuanto a cantidad de registros aportados.


<p align="center">
  <img src="/Analisis preliminar/img/proporcion_datos_reseñas.png" alt="data1" />
</p>

En términos generales, los datos iniciales resultan ser un histórico de valoraciones (y metadatos que aportan información sobre el usuario emisor de la reseña, y diferentes servicios o establecimientos). Tienen como tope el año 2021, lo que motivó a tomar la decisión de valerse de la conexión con una API para obtener datos más actualizados que permitan valorar adecuadamente la situación actual.

Adentrándonos en el análisis de los datos, comenzaremos por los datos de la plataforma Yelp, que es de menor cuantía e importancia en materia de isights. Esto nos indica que es un fuente interesante para la confirmación de información que surja de otras fuentes.

Se observa que en este conjunto existen  columnas duplicadas que tienen una inmensa cantidad de datos faltantes, que representan el 0.01% de los datos del mismo, por lo que resultan irrelevantes.
Los datos existentes en esas columnas resultan ser de la misma organización, responden a un error de redacción que probablemente sea el que motive la creación de esas columnas adicionales. Por estas implicancias, se recomienda su eliminación, lo que reducirá significativamente la cantidad de valores faltantes.

Se observa poca confiabilidad del dato en algunas columnas en particular: state, postal_code, entre otros.
Sin embargo, son confiables los datos relevantes como el nombre del comercio, su categoría y su ubicación geográfica.


Al analizar el conjunto de datos provenientes de Google, se decide analizar todo el conjunto de metadatos,y sólo una muestra de ciertos Estados de mayor relevancia económica para las reseñas. Ello, porque en una vista previa se observa que todos los datasets disponibles sbre reseñas respetan el mismo formato.

<p align="center">
  <img src="/Analisis preliminar/img/estados.jpg" alt="Estados" />
</p>

Se puede observar que las principales economías regionales, factor clave para el desarrollo de inversiones gastronómicas y el cumplimiento de los objetivos de nuestra empresa, son Washington, Utah, Massachusetts, Texas y California ([Fuente](#https://www.lanacion.com.ar/estados-unidos/texas/texas-california-y-mas-estos-son-los-cinco-estados-con-las-economias-mas-solidas-de-eeuu-nid18062024/)).

Avanzando con el análisis de esa muestra, primero corresponde analizar los metadatos de Google. Podemos observar una gran cantidad de valores faltantes y nulos en las columnas “description” y “price”. Los datos faltantes superan el 90% en ambos casos, por lo que su infomación es, prima facie, irrelevante para identificar posibles insights.
Podemos ver una alta cantidad de filas duplicadas, lo que reduce en un porcentaje considerable la cantidad de datos disponibles. Es recomendable realizar una limpieza de las mismas, para evitar información redundante que pudiera perjudicar el análisis del dataset.
Se observa que la columna “Rating” sigue el sistema de calificación de Google maps: califica de 1 a 5 estrellas. Se observa que no hay valores que escapen de esa frecuencia de valores.


<p align="center">
  <img src="/Analisis preliminar/img/datos_filas_duplicadas.png" alt="Duplicados" />
</p>

<p align="center">
  <img src="/Analisis preliminar/img/nulos_analisis calidad.png" alt="Nulos" />
</p>

Se observa poca confiabilidad del dato en algunas columnas en particular. Sin embargo, son confiables los datos relevantes como el nombre del comercio, su categoría y su ubicación geográfica.

Toma relevancia la información sobre los comercios en particular. Podemos observar una gran cantidad de valores faltantes y nulos en ciertas columnas. Esos datos faltantes superan el 90%, por lo que su infomación es, prima facie, irrelevante para identificar posibles insights.
Podemos ver una alta cantidad de filas duplicadas, lo que reduce en un porcentaje considerable la cantidad de datos disponibles. Es recomendable realizar una limpieza de las mismas, para evitar información redundante que pudiera perjudicar el análisis del dataset.
Se observa que la columna “Rating” sigue el sistema de calificación de Google maps: califica de 1 a 5 estrellas. Se observa que no hay valores que escapen de esa frecuencia de valores.

Determinada la calidad del dato, finalizamos integrando la información observada, conjuntamente con otras fuentes adicionales (Como el Bureau de Comercio de los Estados Unidos), donde podemos observar una viabilidad comercial en el Estado de Florida.
Observamos las [perspectivas económicas mundiales](#https://www.bancomundial.org/es/publication/global-economic-prospects?cid=ECR_GA_worldbank_ES_EXTP_search&s_kwcid=AL!18468!3!705358720696!b!!g!!economia%20mundial&gad_source=1) del Banco Mundial y, las tendencias que dan cuenta del [crecimiento del Estado de California](#https://www.infobae.com/economia/2022/10/30/california-deja-atras-a-alemania-y-se-ubica-como-la-cuarta-economia-del-mundo/), uno de los Estados seleccionados para la muestra.
Además, podemos observar que el Estado de California tiene ciertas particularidades, además de ser una de las economías más grandes y dinámicas del mundo, con un crecimiento económico constante y una población con uno de los ingresos per cápita más altos de los Estados Unidos: La diversidad cultural, el auge de la tecnología (que ha optado por instalarse y establecerse en fuertes zonas de éste Estado), y la robusta oferta turística han impulsado el desarrollo del sector gastronómico en la región. 
Este entorno hace que California sea una ubicación estratégica para empresas que buscan invertir en el rubro gastronómico y sectores afines, tanto en áreas urbanas como turísticas, lo que se adapta perfectamente a los objetivos de nuestro proyecto.

Por ese motivo, focalizando en el análisis de este Estado, observamos que se justifica la elección. Contamos con gran cantidad de reseñas, y denota fuertemente la supremacía de los restaurantes y otros sectores afines de ese rubro gastronómico.

<p align="center">
  <img src="/Analisis preliminar/img/categorias.png" alt="Categorías" />
</p>

<p align="center">
  <img src="/Analisis preliminar/img/promedio_calificaciones.png" alt="Categorías" />
</p>

Notamos un sesgo en la información, justificada en el crecimiento de la cantidad de reseñas en general, que hace prácticamente innecesario el estudio de los datos demasiado atrás en el tiempo.

Lo observado hasta aquí nos permite determinar que tenemos viabilidad suficiente para proporcionar a las empresas del sector gastronómico y afines la información necesaria para tomar decisiones estratégicas sobre dónde invertir o expandir sus operaciones dentro del Estado de California. 
Dependiendo del tipo de producto o servicio que ofrezcan, es posible que algunas empresas tengan mejores oportunidades en zonas urbanas cercanas a polos tecnológicos, mientras que otras se beneficiarán más en zonas turísticas con alto flujo de visitantes. 
A través del análisis de datos de mercado, nuestro informe identificará las áreas más rentables, ofreciendo recomendaciones personalizadas para maximizar el retorno de inversión en función de las características de cada empresa.

---
<a href="https://www.linkedin.com/in/gaston-orellano/"><img src="/IMG/lkd.png" alt="LinkedIn" width="40"/></a>