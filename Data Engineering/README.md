# Tratamiento de datos y Pipeline





# Diagrama Entidad-Relación
La Base de Datos se encuentra implementada con tres tablas:
- Business:
Tiene los siguientes atributos: gmap_id (PRIMARY KEY), name, address, latitude, longitude, category, avg_rating, num_of_reviews, state, relative_results, service_options, clasificacion, address_depurada,    city, county.
- Reviews:
Tiene las siguientes columnas: review_id (PRIMARY KEY), gmap_id (Foreign Key), user_id, name, time, rating, text.
- Ubicaciones:
Tiene las siguientes columnas: id_locacion (PRIMARY KEY), gmap_id (Foreign Key), address_depurada, city, county, latitude, longitude.

<p align="center">
  <img src="/IMG/DER/DER.jpeg" alt="DER" />
</p>

La Tabla Business tiene una relación 1 a N con la tabla Reviews, a través de la clave 'gmap_id'. A su vez, la tabla Business tiene una relación 1 a 1 con la tabla Ubicaciones, también sobre la clave 'gmap_id'.

Esa es la Base de Datos implementada en el servicio Google Cloud.
A la hora de realizar preliminarmente el Dashboard, se incorpora la tabla 'análisis_económico', con las siguientes columnas: County (PRIMARY KEY), Per capita income, Rent y Property Cost.
Esta tabla se encuentra conectada en una relación 1 a 1 con la tabla Ubicaciones, a través de su columna 'county'. De esa forma, se puede implementar el Dashboard relacionando correctamente los datos.

<p align="center">
  <img src="/IMG/DER/DER (Dashboard).jpeg" alt="DER Dashboards" />
</p>
