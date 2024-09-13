## Análisis rubro gastronómico en principales polos de Estados Unidos

<p align="center">
  <img src="/IMG/logo_epicurean.jpeg" alt="Logo" />
</p>

## Indice

<details>
  <summary>Tabla de contenido</summary>

  1. [Índice](#indice)
  2. [Presentación](#presentación)
  3. [Propuesta de Proyecto](#propuesta-de-proyecto)
  4. [Stack Tecnológico](#stack-tecnológico)
  5. [Ciclo de Vida del Dato](#ciclo-de-vida-del-dato)
  6. [Análisis Exploratorio](#análisis-exploratorio)
  7. [KPI](#kpi)
  8. [Metodología de Trabajo](#metodología-de-trabajo)
  9. [Cronología](#cronología-de-trabajo)
  10. [Equipo de Trabajo](#equipo-de-trabajo)

</details>

## Presentación
EPICUREAN Data Solutions es una empresa consultora especializada en Data Analysis, Data Science y Machine Learning, especialmente orientada en el rubro gastronómico y otras actividades afines; que ofrece soluciones personalizadas, adaptadas a las necesidades específicas de cada cliente, utilizando herramientas avanzadas de análisis de datos y modelado predictivo. 
El enfoque descansa en la optimización de  procesos, identificación oportunidades de crecimiento y mejora de la eficiencia operativa en el sector gastronómico, para conseguir resultados basados en datos precisos y estratégicos. 
Epicurean tiene el compromiso de acompañar a las empresas en su transformación digital, brindándoles insights valiosos que impulsen su éxito en un mercado competitivo.

## Propuesta de Proyecto

# Cliente Objetivo:
El proyecto adquiere importancia para empresas o emprendedores del sector gastronómico y afines, que buscan expandir o establecer nuevos negocios en el sector, en el Estado de California. 

# Contexto:
De acuerdo a nuestro análisis preliminar, podemos notar que el Estado de California es una de las economías más grandes y dinámicas del mundo, con un crecimiento económico constante y una población con uno de los ingresos per cápita más altos de los Estados Unidos. La diversidad cultural, el auge de la tecnología, y la robusta oferta turística han impulsado el desarrollo del sector gastronómico en la región. Este entorno hace que California sea una ubicación estratégica para empresas que buscan invertir en el rubro gastronómico y sectores afines, tanto en áreas urbanas como turísticas.
<p align="center">
  <img src="/IMG/estado_california.jpeg" alt="California" />
</p>

# Problemática:
A pesar del potencial económico de California, las inversiones en el sector gastronómico no siempre generan el retorno esperado. Muchas empresas enfrentan dificultades debido a una mala orientación de sus inversiones, principalmente porque no han realizado un análisis adecuado del mercado y de los intereses específicos de cada área. 
Zonas urbanas con alto desarrollo tecnológico y áreas turísticas presentan características de mercado diferentes, y sin un análisis exhaustivo, es común que las empresas subestimen las particularidades de cada zona, lo que afecta directamente el éxito de sus proyectos.
El desafío consiste en comparar estas zonas para entender si los consumidores del rubro gastronómico tienen preferencias o comportamientos diferentes que puedan influir en el éxito de cada negocio y, en consecuencia, en las posibles inversiones.

**Epicurean Data Solutions permite analizar qué proyectos gastronómicos son adecuados para determinadas zonas del país, considerando los gustos de los consumidores, el standard de calidad exigido por el público objetivo, y las preferencias de consumo en general. De esta forma, se puede orientar específicamente a nuestros clientes con la toma de decisiones en relación a sus objetivos empresariales y a las características especiales de su compañía.**

# Alcance del proyecto:
Este proyecto de análisis de datos tiene como objetivo proporcionar a las empresas del sector gastronómico y afines la información necesaria para tomar decisiones estratégicas sobre dónde invertir o expandir sus operaciones dentro del Estado de California. Dependiendo del tipo de producto o servicio que ofrezcan, algunas empresas tendrán mejores oportunidades en zonas urbanas cercanas a polos tecnológicos, mientras que otras se beneficiarán más en zonas turísticas con alto flujo de visitantes. A través del análisis de datos de mercado, nuestro informe identificará las áreas más rentables, ofreciendo recomendaciones personalizadas para maximizar el retorno de inversión en función de las características de cada empresa.

# Objetivos del proyecto:
El proyecto tiene los siguientes objetivos como norte:

- Analizar las valoraciones y reseñas de los restaurantes en áreas tecnológicas y turísticas para identificar diferencias en preferencias y comportamientos de los clientes.

- Determinar el potencial de inversión en “zonas tech” y “zonas turísticas” en función de la calidad de los restaurantes, popularidad y proximidad geográfica.

- Identificar oportunidades de crecimiento en el sector gastronómico y afines en California, seleccionando entre zonas tecnológicas con alta demanda de servicios y zonas turísticas con gran flujo de visitantes.

- Desarrollar un sistema de recomendación que, de acuerdo a las preferencias del consumidor, le brinde las mejores opciones en la zona.

## Stack Tecnológico.
Para realizar un proyecto de esta naturaleza se debe contar con un conjunto de herramientas definido. Entre ellas, podemos visualizar ciertas herramientas, galerías y sistemas que ofrecen la posibilidad de crear, integrar y coordinar los diferentes hitos.
Los mismos son detallados [aquí](/IMG/STACK%20TEC/README.md), y a continuación podré visualizarlos de acuerdo al ciclo de vida del dato.

## Ciclo de vida del dato. 

<p align="center">
  <img src="/IMG/STACK TEC/Pipeline.jpeg" alt="Tecnología utilizada" />
</p>

## Análisis Exploratorio
Se realiza un análisis preliminar de datos, a partir de los cuales se puede observar la calidad del dato, permitiendo adelantar conclusiones y medidas de acción.
Inicialmente, se analizan dos datasets: uno que contiene un conjunto histórico de reseñas en Google Maps, y otro de la plataforma Yelp.
Adicionalmente, se contempla la alimentación de nuestro conjunto con la API de Google, para mantener la información actualizada.
Luego, aparecieron fuentes adicionales de alta confianza, como los datos censuales de la Oficina de Comercio de los Estados Unidos, que otorgan información que terminaría resultando esencial para medir el nivel de vida y posibilidades de consumo de la población.

Respecto a los datasets iniciales, contamos con gran cantidad de columnas duplicadas (que tienen una inmensa cantidad de datos faltantes), pero que representan el 0.01% de los datos, por lo que resultan irrelevantes.
Los datos existentes en esas columnas resultan ser de la misma organización, responden a un error de redacción que probablemente sea el que motive la creación de esas columnas adicionales. Por estas implicancias, se recomienda su eliminación, lo que reducirá significativamente la cantidad de valores faltantes.

Se observa poca confiabilidad del dato en algunas columnas en particular. Sin embargo, son confiables los datos relevantes como el nombre del comercio, su categoría y su ubicación geográfica.

Toma relevancia la información sobre los comercios en particular. Podemos observar una gran cantidad de valores faltantes y nulos en ciertas columnas. Esos datos faltantes superan el 90%, por lo que su infomación es, prima facie, irrelevante para identificar posibles insights.
Podemos ver una alta cantidad de filas duplicadas, lo que reduce en un porcentaje considerable la cantidad de datos disponibles. Es recomendable realizar una limpieza de las mismas, para evitar información redundante que pudiera perjudicar el análisis del dataset.
Se observa que la columna “Rating” sigue el sistema de calificación de Google maps: califica de 1 a 5 estrellas. Se observa que no hay valores que escapen de esa frecuencia de valores.

Determinada la calidad del dato, podemos observar ciertos insights que dan cuenta de la viabilidad del proyecto propuesto, sobre la industria gastronómica en el Estado de Florida.

Puede analizarse en profundidad en la [carpeta](/Data%20Analytics/) correspondiente.


## KPI
Se han definido los siguientes KPI:

**KPI 1:** Incrementar en un 5% trimestral la cantidad de reseñas del establecimiento gastronómico.  
**Definición:** Este KPI mide la popularidad y visibilidad de los establecimientos en función del crecimiento en el número de reseñas obtenidas en un período determinado. Se enfoca en monitorear cómo las estrategias de marketing y servicio al cliente están incentivando a los consumidores a dejar reseñas.  
Para establecer una línea de referencia inicial, los datos del trimestre anterior se calcularán utilizando los promedios de las reseñas obtenidas por los locales de la competencia directa en el mismo período. Esto permitirá evaluar el rendimiento del establecimiento en relación con sus competidores más cercanos.

**Fórmula:**

KPI = ((Cant. Reseñas (tri actual) − Cant. Reseñas (tri ant)) / Cant. Reseñas (tri ant)) x 100%

---

**KPI 2:** Incrementar en un 5% trimestral la oferta de servicios externos.  
**Definición:** Este KPI tiene el objetivo de aumentar el consumo en los servicios que no requieren consumo en el local (por ejemplo, pick up o delivery), que son más habituales en zonas tech.

**Fórmula:**

KPI = ((Servicios externos (tri actual) − Servicios externos (tri ant)) / Servicios externos (tri ant)) x 100%

---

**KPI 3:** Incrementar en un 5% cada bimestre la cantidad de valoraciones de 4 y 5 estrellas.  
**Definición:** Este KPI mide la evolución de la percepción positiva de los clientes sobre la calidad del establecimiento, buscando un crecimiento continuo en las valoraciones positivas (4 o más estrellas) cada dos meses.

**Fórmula:**

KPI = ((Cant. ≥4 (bimestre actual) − Cant. ≥4 (bimestre ant)) / Cant. ≥4 (bimestre ant)) x 100%

## Metodología de Trabajo
En EPICUREAN implementamos la metodología SCRUM, que se caracteriza por su flexibilidad, permitiendo adaptarse rápidamente a los cambios y necesidades del proyecto, y fomentando la transparencia a través de una comunicación abierta y constante. Además, promueve la responsabilidad compartida dentro del equipo, asegurando que todos estén alineados con los objetivos comunes. SCRUM se organiza en iteraciones llamadas sprints, que permiten recibir feedback continuo y mejorar de manera incremental.

En lo que específicamente aquí se refiere, durante cada sprint se llevan a cabo una serie de eventos clave, como la planificación, en donde se definen las tareas a completar; el Scrum Diario (Daily), una breve reunión para alinear el trabajo diario; la revisión del sprint (Demo), donde se presentan los avances; y la retrospectiva del sprint, un espacio para reflexionar y mejorar el proceso.

A continuación puede analizarse el cronograma de trabajo implementado, a través de un diagrama de Gantt.

## Cronología de Trabajo 
<p align="center">
  <img src="/IMG/GANTT/Diagrama Gantt.png" alt="Gantt" />
</p>


## Equipo de Trabajo

<table align="center">
  <tr>
    <td align="center"><b>Yesica Méndez</b></td>
    <td align="center"><b>Analía Romano</b></td>
    <td align="center"><b>Sebastián López</b></td>
    <td align="center"><b>Gastón Orellano</b></td>
    <td align="center"><b>Melanie Butus</b></td>
  </tr>
  <tr>
    <td align="center"><img src="/IMG/yesica.jpeg" alt="yesica" width="100"/></td>    
    <td align="center"><img src="/IMG/analia.jpg" alt="analia" width="100"/></td>
    <td align="center"><img src="/IMG/sebastian.jpg" alt="sebastian" style="border-radius: 50%; width: 100px; height: 100px;" width="100"/></td>
    <td align="center"><img src="/IMG/gaston.jpeg" alt="gaston" width="100"/></td>
    <td align="center"><img src="/IMG/melanie.jpg" alt="melanie" width="100"/></td>
  </tr>
  <tr>
    <td align="center">Data Engineer</td>
    <td align="center">Data Engineer</td>
    <td align="center">Data Analyst</td>
    <td align="center">Data Analyst</td>
    <td align="center">Data Scientist</td>
  </tr>

  <tr>
    <td align="center"><a href="https://www.linkedin.com/in/yesica-mendez-aroca/"><img src="/IMG/lkd.png" alt="LinkedIn" width="40"/></a></td>
    <td align="center"><a href="https://www.linkedin.com/in/ana-marce-romano-119b54254/"><img src="/IMG/lkd.png" alt="LinkedIn" width="40"/></a></td>
    <td align="center"><a href="https://www.linkedin.com/in/sebastian-lopez-bianchessi/"><img src="/IMG/lkd.png" alt="LinkedIn" width="40"/></a></td>
    <td align="center"><a href="https://www.linkedin.com/in/gaston-orellano/"><img src="/IMG/lkd.png" alt="LinkedIn" width="40"/></a></td>
    <td align="center"><a href="https://www.linkedin.com/in/melanie-butus-7013551a9/"><img src="/IMG/lkd.png" alt="LinkedIn" width="40"/></a></td>
  </tr>
</table>
