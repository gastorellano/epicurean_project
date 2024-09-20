import numpy as np
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from google.cloud import storage
import pandas as pd
from datetime import datetime, timedelta
import re
import logging

# Función para la extracción de datos desde GCS
def extract_data():
    local_paths = ['gs://us-central1-epicureandag-3b408e2a-bucket/data/estado/reviews-California.parquet',
                   'gs://us-central1-epicureandag-3b408e2a-bucket/data/meta-data-sitios/metadata-sitios.parquet']
    return local_paths  # Retorna las rutas de los archivos descargados

def transform_data(**kwargs):
    ti = kwargs['ti']
    file_paths = ti.xcom_pull(task_ids='extract_data')  # Extraer las rutas de los archivos descargados

    # Cargar dataset de reviews y business
    df_reviews_g = pd.read_parquet(file_paths[0])
    df_business_google = pd.read_parquet(file_paths[1])

    # Transformaciones de reviews

    # Eliminar la columna 'pics' ya que no la necesitamos para este analisis
    df_reviews_g.drop(columns=['pics'], inplace=True)

    # Convertir la columna 'time' a formato de fecha
    df_reviews_g['time'] = pd.to_datetime(df_reviews_g['time'], unit='ms')

    # Eliminar duplicados
    df_reviews_g.drop_duplicates(inplace=True)

   # Extraer solo el día/mes/año (formato 'dd/mm/yyyy')
    df_reviews_g['time'] = df_reviews_g['time'].dt.strftime('%d/%m/%Y')

    # Asegurarse de que la columna 'time' esté en formato datetime
    df_reviews_g['time'] = pd.to_datetime(df_reviews_g['time'], errors='coerce')

    # Detectar outliers en 'time' (fechas fuera del rango)
    min_date = pd.to_datetime('2007-06-01')
    max_date = pd.to_datetime('today')

    # Filtrar las filas que tienen fechas fuera de este rango
    outliers_time = df_reviews_g[(df_reviews_g['time'] < min_date) | (df_reviews_g['time'] > max_date)]

    # Eliminamos estos outliers
    df_reviews_g = df_reviews_g[(df_reviews_g['time'] >= min_date) & (df_reviews_g['time'] <= max_date)]

    #Eliminamos la columna 'resp' ya que no la necesitamos para este analisis
    df_reviews_g = df_reviews_g.drop(columns=['resp'])

    # 'Reemplazamos valores nulos en la columna 'review_text' con 'Sin Reseña'
    df_reviews_g['text'] = df_reviews_g['text'].fillna('Sin Reseña')


    # Transformaciones de business

    # Eliminar la columna original 'MISC'
    df_business_google = df_business_google.drop(columns=['MISC'])

    # Listamos las columnas no deseadas
    col_eliminar = ['price', 'hours', 'url', 'Health & safety', 'Accessibility', 'Planning', 'description',
                    'Offerings', 'Amenities', 'Atmosphere', 'Payments', 'Popular for',
                    'Dining options', 'Crowd', 'From the business', 'Highlights',
                    'Recycling', 'Getting here', 'Activities', 'Lodging options',
                    'Health and safety']

    # Eliminamos las columnas no deseadas
    df_business_google = df_business_google.drop(columns=col_eliminar)

    columns_to_transform = ['category', 'relative_results',
                            'Service options']  # Lista de columnas que contienen listas o arrays
    for col in columns_to_transform:
        df_business_google[col] = df_business_google[col].apply(
            lambda x: ', '.join(map(str, x)) if isinstance(x, (list, np.ndarray)) else x)

    # Eliminar filas duplicadas completamente idénticas
    df_business_google = df_business_google.drop_duplicates()

    # Convertir la columna 'state' a tipo texto (string)
    df_business_google['state'] = df_business_google['state'].astype(str)

    # Eliminar filas donde 'state' es igual a 'Permanently closed'
    df_business_google = df_business_google[df_business_google['state'] != 'Permanently closed']

    # Rellenamos los valores nulos con el texto elegido
    df_business_google['category'] = df_business_google['category'].fillna('Valores Faltantes')
    df_business_google['relative_results'] = df_business_google['relative_results'].fillna('Sin resultados vinculados')
    df_business_google['Service options'] = df_business_google['Service options'].fillna('Sin dato')

    # Definimos palabras clave a buscar luego en las categorias
    palabra = r'\b(restaurant|cafe|delivery|diner|bistro|takeout|bar|pub|grill|pizzeria|coffee|bakery|food|eatery|sandwich|snack)\b'

    # Filtrar las categorías coincidentes
    df_business_google = df_business_google[
        df_business_google['category'].str.extrac(palabra, case=False, regex=True, na=False)]

    clasificacion = {
        'Dining Venue': ['Restaurant'],
        'Quick Service': ['Fast food restaurant', 'Pizza restaurant', 'Pizza Takeout'],
        'Takeout & Delivery': ['Takeout Restaurant', 'Delivery Restaurant'],
        'Mexican Dining': ['Mexican restaurant', 'Taco restaurant'],
        'American Dining': ['American restaurant', 'Burger restaurant'],
        'Sandwich Bar': ['Sandwich shop'],
        'Italian Dining': ['Italian restaurant'],
        'Chinese Dining': ['Chinese restaurant'],
        'Café & Coffee': ['Coffee shop', 'Cafe'],
        'Seafood Dining': ['Seafood restaurant'],
        'Barbecue Dining': ['Barbecue restaurant'],
        'Asian Fusion': ['Asian restaurant', 'Sushi restaurant', 'Japanese restaurant', 'Thai restaurant'],
        'Chicken House': ['Chicken restaurant', 'Chicken wings restaurant'],
        'Bakery Shop': ['Bakery', 'Bakery shop'],
        'Ice Cream Parlor': ['Ice cream shop'],
        'Indian Dining': ['Indian restaurant'],
        'Latin American Dining': ['Latin American restaurant'],
        'Juice Bar': ['Juice shop'],
        'Specialty Catering': ['Caterer'],
        'Vegetarian Dining': ['Vegetarian restaurant'],
        'Vietnamese Dining': ['Vietnamese Restaurant'],
        'Health Foods': ['Health food store', 'Health Food', 'Green Food']
    }

    def assign_group(category):
        """

        """
        if pd.isna(category):  # Si la categoría es Nula
            return 'Other'
        for key, values in clasificacion.items():
            for value in values:
                if value.lower() in category.lower():
                    return key
        return 'Other'

    df_business_google['clasificacion'] = df_business_google['category'].map(assign_group)

    df_business_google = df_business_google[df_business_google['clasificacion'] != 'Other']

    # Filtrar los registros en df_business_google que coincidan en la columna 'gmap_id'
    df_business_google = df_business_google[df_business_google['gmap_id'].isin(df_reviews_g['gmap_id'])]

    # Eliminar las filas que tienen valores nulos en la columna 'address'
    df_business_google = df_business_google.dropna(subset=['address'])

    # Función para extraer dirección y ciudad de la columna 'address'
    def extract_address_city(row):
        # Verificar si el valor en 'address' no es nulo
        if pd.isnull(row['address']):
            return pd.Series([None, None])

        # Verificar si el nombre contiene una coma
        if ',' in row['name']:
            # Si hay coma en el nombre, ajustamos el patrón para excluir el nombre del análisis
            # Permitimos caracteres especiales en la dirección y ciudad
            address_pattern = r'(?P<address>.*?),\s*(?P<city>[A-Za-z\s\'•\-]+),\s*(?P<state_zip>[A-Z]{2}\s\d{5})'
            match = re.search(address_pattern, row['address'])
        else:
            # Usamos el patrón completo con nombre
            # Permitimos caracteres especiales en el nombre, dirección y ciudad
            address_pattern = r'(?P<name>.*?),\s*(?P<address>.*?),\s*(?P<city>[A-Za-z\s\'•\-]+),\s*(?P<state_zip>[A-Z]{2}\s\d{5})'
            match = re.search(address_pattern, row['address'])

        if match:
            # Verificar si la dirección capturada contiene "port" (como en "Airport")
            if 'port' in match.group('address').lower():
                address = match.group('address').strip()
                city = match.group('city').strip()
                return pd.Series([address, city])

            # Verificar si el nombre coincide con la columna 'name' (solo si se usó el patrón con nombre)
            if 'name' in match.groupdict() and row['name'].strip() == match.group('name').strip():
                address = match.group('address').strip()
                city = match.group('city').strip()
                return pd.Series([address, city])
            elif 'name' not in match.groupdict():
                # Si no estamos utilizando el nombre, simplemente tomamos la dirección y la ciudad
                address = match.group('address').strip()
                city = match.group('city').strip()
                return pd.Series([address, city])

        # Si no coincide o no encuentra suficientes datos
        return pd.Series([None, None])

    # Aplicar la función a cada fila del DataFrame y guardar los resultados en 'address_depurada' y 'city'
    df_business_google[['address_depurada', 'city']] = df_business_google.apply(extract_address_city, axis=1)

    # Eliminamos Nulos de la columna 'city'
    df_business_google = df_business_google.dropna(subset=['city'])

    # Limpiamos espacios en la misma
    df_business_google['city'] = df_business_google['city'].str.strip()

    condados_a_ciudades = {
        'Alameda': ['Alameda', 'Albany', 'Berkeley', 'Dublin', 'Emeryville', 'Fremont', 'Hayward', 'Livermore',
                    'Newark', 'Oakland', 'Pleasanton', 'San Leandro', 'Union City', 'Castro Valley', 'San Lorenzo'],
        'Alpine': ['Markleeville', 'Markleeville'],
        'Amador': ['Amador City', 'Ione', 'Jackson', 'Plymouth', 'Sutter Creek', 'Jackson'],
        'Butte': ['Biggs', 'Chico', 'Gridley', 'Oroville', 'Durham', 'Paradise', 'Chico', 'Magalia', 'Paradise'],
        'Calaveras': ['Angels Camp', 'Copperopolis', 'Arnold', 'San Andreas'],
        'Colusa': ['Colusa', 'Williams', 'Colusa', 'Princeton'],
        'Contra Costa': ['Alameda Park', 'Antioch', 'Brentwood', 'Clayton', 'Concord', 'Crockett', 'Danville',
                         'El Cerrito', 'Hercules', 'Lafayette', 'Martinez', 'Moraga', 'Orinda', 'Pinole', 'Pittsburg',
                         'Pleasant Hill', 'Richmond', 'San Pablo', 'San Ramon', 'Walnut Creek', 'Alamo', 'Pacheco',
                         'Bay Point', 'El Sobrante', 'Oakley', 'Rodeo', 'Discovery Bay'],
        'Del Norte': ['Crescent City'],
        'El Dorado': ['Placerville', 'South Lake Tahoe', 'El Dorado Hills', 'Cool', 'Lotus', 'Cameron Park', 'Kyburz',
                      'Diamond Springs'],
        'Fresno': ['Biola', 'Clovis', 'Coalinga', 'Firebaugh', 'Fowler', 'Fresno', 'Huron', 'Kerman', 'Kingsburg',
                   'Mendota', 'Orange Cove', 'Parlier', 'Reedley', 'San Joaquin', 'Sanger', 'Selma', 'Prather',
                   'Shaver Lake', 'Riverdale', 'Five Points'],
        'Glenn': ['Orland', 'Willows'],
        'Humboldt': ['Arcata', 'Blue Lake', 'Eureka', 'Fortuna', 'Rio Dell', 'Trinidad', 'McKinleyville', 'Ferndale',
                     'Garberville', 'Loleta', 'Whitethorn', 'Willow Creek'],
        'Imperial': ['Brawley', 'Calexico', 'Calipatria', 'El Centro', 'Holtville', 'Imperial', 'Westmorland'],
        'Inyo': ['Bishop', 'Lone Pine'],
        'Kern': ['Arvin', 'Bakersfield', 'California City', 'Delano', 'Maricopa', 'McFarland', 'Ridgecrest', 'Shafter',
                 'Taft', 'Tehachapi', 'Wasco', 'Rosamond', 'Edwards AFB', 'Lamont', 'Mojave', 'Lost Hills', 'Kernville',
                 'Lake Isabella', 'Edwards'],
        'Kings': ['Avenal', 'Corcoran', 'Hanford', 'Lemoore'],
        'Lake': ['Clearlake', 'Lakeport', 'Nice', 'Spring Valley', 'Hidden Valley Lake', 'Kelseyville', 'Lower Lake'],
        'Lassen': ['Susanville', 'Bieber'],
        'Los Angeles': ['Pacific Palisades', 'Valencia', 'Reseda', 'San Pedro', 'City of Industry', 'Northridge',
                        'North Hollywood', 'Sylmar', 'Sun Valley', 'Artesia', 'Arcadia', 'Venice', 'Sherman Oaks',
                        'Van Nuys', 'Studio City', 'Granada Hills', 'Rowland Heights', 'Harbor City', 'Tujunga',
                        'Saugus', 'Highland Park', 'Pacoima', 'Universal City', 'Hollywood', 'East Los Angeles',
                        'West Hills', 'Cudahy', 'La Crescenta-Montrose', 'Canoga Park', 'Wilmington', 'Woodland Hills',
                        'Canyon Country', 'Panorama City', 'Tarzana', 'Winnetka', 'Newhall', 'Castaic',
                        'Stevenson Ranch', 'Irwindale', 'View Park-Windsor Hills', 'Lomita', 'Marina Del Rey',
                        'Valley Glen', 'Eagle Rock', 'North Hills', 'Lakewood', 'Arleta', 'Toluca Lake',
                        'Valley Village', 'Mission Hills', 'Bassett', 'Littlerock', 'Topanga', 'Playa Vista',
                        'Quartz Hill', 'East Compton', 'Porter Ranch', 'Silver Lake'],
        'Acton': ['Agoura Hills', 'Alhambra', 'Alondra Park', 'Altadena', 'Avalon', 'Azusa', 'Baldwin Park', 'Bell',
                  'Bell Gardens', 'Bellflower', 'Beverly Hills', 'Burbank', 'Calabasas', 'Carson', 'Cerritos',
                  'Chatsworth', 'Claremont', 'Commerce', 'Compton', 'Covina', 'Culver City', 'Diamond Bar', 'Downey',
                  'Duarte', 'El Monte', 'El Segundo', 'Encino', 'Gardena', 'Glendale', 'Glendora', 'Hacienda Heights',
                  'Hawaiian Gardens', 'Hawthorne', 'Hermosa Beach', 'Huntington Park', 'Industry', 'Inglewood',
                  'La Canada Flintridge', 'La Mirada', 'La Puente', 'La Verne', 'Lancaster', 'Lawndale', 'Lennox',
                  'Long Beach', 'Los Angeles', 'Lynwood', 'Malibu', 'Manhattan Beach', 'Maywood', 'Monrovia',
                  'Montebello', 'Monterey Park', 'Norwalk', 'Palmdale', 'Palos Verdes Estates', 'Paramount', 'Pasadena',
                  'Pico Rivera', 'Pomona', 'Rancho Palos Verdes', 'Redondo Beach', 'Rolling Hills Estates', 'Rosemead',
                  'San Dimas', 'San Fernando', 'San Gabriel', 'San Marino', 'Santa Clarita', 'Santa Fe Springs',
                  'Santa Monica', 'Sierra Madre', 'Signal Hill', 'South El Monte', 'South Gate', 'South Pasadena',
                  'Temple City', 'Torrance', 'Vernon', 'Walnut', 'West Covina', 'West Hollywood', 'Westlake Village',
                  'Whittier'],
        'Madera': ['Chowchilla', 'Madera', 'Bass Lake', 'North Fork', 'Coarsegold', 'Oakhurst'],
        'Marin': ['Belvedere', 'Corte Madera', 'Fairfax', 'Larkspur', 'Mill Valley', 'Novato', 'Ross', 'San Anselmo',
                  'San Rafael', 'Sausalito', 'Tiburon', 'Olema', 'Point Reyes Station', 'Greenbrae', 'Stinson Beach',
                  'Tomales'],
        'Mariposa': ['Mariposa'],
        'Mendocino': ['Fort Bragg', 'Point Arena', 'Ukiah', 'Willits', 'Mendocino', 'Little River', 'Laytonville',
                      'Philo', 'Gualala', 'Redwood Valley', 'Elk', 'Boonville'],
        'Merced': ['Atwater', 'Dos Palos', 'Gustine', 'Livingston', 'Los Banos', 'Merced', 'Delhi', 'Santa Nella'],
        'Modoc': ['Alturas'],
        'Mono': ['Mammoth Lakes', 'June Lake'],
        'Monterey': ['Carmel-by-the-Sea', 'Del Rey Oaks', 'Gonzales', 'Greenfield', 'King City', 'Marina', 'Monterey',
                     'Pacific Grove', 'Salinas', 'Sand City', 'Seaside', 'Soledad', 'Carmel Valley', 'Pebble Beach',
                     'Castroville', 'Pajaro', 'Royal Oaks', 'Prunedale', 'Aromas', 'Carmel-By-The-Sea'],
        'Napa': ['American Canyon', 'Calistoga', 'Napa', 'St. Helena', 'Yountville', 'St Helena', 'Rutherford',
                 'Santa Elena'],
        'Nevada': ['Grass Valley', 'Nevada City', 'Truckee', 'Cisco Grove', 'North San Juan', 'Penn Valley'],
        'Orange': ['Aliso Viejo', 'Anaheim', 'Brea', 'Buena Park', 'Costa Mesa', 'Cypress', 'Dana Point',
                   'Fountain Valley', 'Fullerton', 'Garden Grove', 'Huntington Beach', 'Irvine', 'La Habra', 'La Palma',
                   'Laguna Beach', 'Laguna Hills', 'Laguna Niguel', 'Laguna Woods', 'Lake Forest', 'Los Alamitos',
                   'Mission Viejo', 'Newport Beach', 'Orange', 'Placentia', 'Rancho Santa Margarita', 'San Clemente',
                   'San Juan Capistrano', 'Santa Ana', 'Seal Beach', 'Stanton', 'Tustin', 'Villa Park', 'Westminster',
                   'Yorba Linda', 'Foothill Ranch', 'Ladera Ranch', 'Silverado', 'Trabuco Canyon', 'Newport Coast'],
        'Placer': ['Auburn', 'Colfax', 'Lincoln', 'Loomis', 'Rocklin', 'Roseville', 'Kings Beach', 'Tahoe City',
                   'Granite Bay', 'Olympic Valley', 'Newcastle', 'Homewood'],
        'Plumas': ['Portola', 'Quincy', 'Chester', 'Lake Almanor', 'Blairsden-Graeagle'],
        'Riverside': ['Banning', 'Beaumont', 'Blythe', 'Calimesa', 'Canyon Lake', 'Cathedral City', 'Coachella',
                      'Corona', 'Desert Hot Springs', 'Eastvale', 'Hemet', 'Indian Wells', 'Indio', 'Jurupa Valley',
                      'La Quinta', 'Lake Elsinore', 'Menifee', 'Moreno Valley', 'Murrieta', 'Norco', 'Palm Desert',
                      'Palm Springs', 'Perris', 'Rancho Mirage', 'Riverside', 'San Jacinto', 'Temecula', 'Wildomar',
                      'Thousand Palms', 'Cabazon', 'March Air Reserve Base', 'Idyllwild-Pine Cove', 'Thermal',
                      'Bermuda Dunes', 'Mira Loma', 'Winchester', 'Anza', 'Mecca', 'Romoland', 'Sun City'],
        'Sacramento': ['Citrus Heights', 'Elk Grove', 'Folsom', 'Galt', 'Isleton', 'Rancho Cordova', 'Sacramento',
                       'Antelope', 'Arden-Arcade', 'Carmichael', 'Clay', 'Courtland', 'Elverta', 'Fair Oaks', 'Florin',
                       'Foothill Farms', 'Franklin', 'Fruitridge Pocket', 'Gold River', 'La Riviera', 'Lemon Hill',
                       'Mather', 'North Highlands', 'Orangevale', 'Parkway', 'Rancho Murieta', 'Rio Linda', 'Rosemont',
                       'Vineyard', 'Walnut Grove', 'Wilton', 'Hood', 'Rio Linda'],
        'San Benito': ['Hollister', 'San Juan Bautista', 'Tres Pinos'],
        'San Bernardino': ['Adelanto', 'Apple Valley', 'Barstow', 'Big Bear Lake', 'Chino', 'Chino Hills', 'Colton',
                           'Fontana', 'Grand Terrace', 'Hesperia', 'Highland', 'Loma Linda', 'Montclair', 'Needles',
                           'Ontario', 'Rancho Cucamonga', 'Redlands', 'Rialto', 'San Bernardino', 'Twentynine Palms',
                           'Upland', 'Victorville', 'Yucaipa', 'Yucca Valley', 'Joshua Tree', 'Crestline',
                           'Lake Arrowhead', 'Alta Loma', 'Joshua Tree', 'Oro Grande', 'Yermo', 'Bloomington', 'Phelan',
                           'Helendale', 'Fort Irwin', 'Running Springs'],
        'San Diego': ['Carlsbad', 'Chula Vista', 'Coronado', 'Del Mar', 'El Cajon', 'Encinitas', 'Escondido',
                      'Imperial Beach', 'La Mesa', 'Lemon Grove', 'National City', 'Oceanside', 'Poway', 'San Diego',
                      'San Marcos', 'Santee', 'Solana Beach', 'Vista', 'Alpine', 'Bonita', 'Borrego Springs',
                      'Fallbrook', 'Jamul', 'Julian', 'Lakeside', 'Pine Valley', 'Ramona', 'Ranchita',
                      'Rancho Santa Fe', 'Spring Valley', 'Camp Pendleton North', 'Bonsall', 'Pala',
                      'Carmel Mountain Ranch', 'Pauma Valley', 'Julian', 'La Jolla', 'Camp Pendleton'],
        'San Francisco': ['San Francisco'],
        'San Joaquin': ['Escalon', 'Lathrop', 'Lodi', 'Manteca', 'Ripon', 'Stockton', 'Tracy', 'Acampo', 'French Camp',
                        'Lockeford', 'Thornton', 'Lockeford', 'Acampo'],
        'San Luis Obispo': ['Arroyo Grande', 'Atascadero', 'Grover Beach', 'Morro Bay', 'Paso Robles', 'Pismo Beach',
                            'San Luis Obispo', 'Baywood-Los Osos', 'Santa Margarita', 'Cayucos', 'Oceano', 'Templeton',
                            'Nipomo', 'Cambria', 'San Simeon', 'Los Osos'],
        'San Mateo': ['Atherton', 'Belmont', 'Brisbane', 'Burlingame', 'Colma', 'Daly City', 'East Palo Alto',
                      'Foster City', 'Half Moon Bay', 'Hillsborough', 'Menlo Park', 'Millbrae', 'Pacifica',
                      'Portola Valley', 'Redwood City', 'San Bruno', 'San Carlos', 'San Mateo', 'South San Francisco',
                      'Woodside'],
        'Santa Barbara': ['Buellton', 'Carpinteria', 'Goleta', 'Guadalupe', 'Lompoc', 'Santa Barbara', 'Santa Maria',
                          'Solvang', 'Orcutt', 'Los Alamos', 'Los Olivos', 'Montecito', 'Isla Vista', 'Vandenberg AFB'],
        'Santa Clara': ['Campbell', 'Cupertino', 'Gilroy', 'Los Altos', 'Los Altos Hills', 'Los Gatos', 'Milpitas',
                        'Monte Sereno', 'Morgan Hill', 'Mountain View', 'Palo Alto', 'San Jose', 'Santa Clara',
                        'Saratoga', 'Sunnyvale', 'Stanford'],
        'Santa Cruz': ['Capitola', 'Santa Cruz', 'Scotts Valley', 'Watsonville', 'Boulder Creek', 'Freedom', 'Aptos',
                       'Soquel', 'Felton'],
        'Shasta': ['Anderson', 'Redding', 'Shasta Lake', 'Burney', 'McArthur', 'Platina', 'Lakehead',
                   'Fall River Mills', 'Cottonwood'],
        'Sierra': ['Loyalton', 'Sierra City'],
        'Siskiyou': ['Dorris', 'Dunsmuir', 'Etna', 'Fort Jones', 'Montague', 'Mount Shasta', 'Tulelake', 'Weed',
                     'Yreka', 'Mt Shasta', 'Mount Shasta'],
        'Solano': ['Benicia', 'Dixon', 'Fairfield', 'Rio Vista', 'Suisun City', 'Vacaville', 'Vallejo'],
        'Sonoma': ['Cloverdale', 'Cotati', 'Healdsburg', 'Petaluma', 'Rohnert Park', 'Santa Rosa', 'Sebastopol',
                   'Sonoma', 'Windsor', 'Bodega Bay', 'Guerneville', 'Geyserville', 'Forestville', 'Monte Rio'],
        'Stanislaus': ['Ceres', 'Hughson', 'Modesto', 'Newman', 'Oakdale', 'Patterson', 'Riverbank', 'Turlock',
                       'Waterford', 'Salida', 'Keyes', 'Westley'],
        'Sutter': ['Live Oak', 'Yuba City', 'Sutter'],
        'Tehama': ['Corning', 'Red Bluff', 'Tehama'],
        'Trinity': ['Weaverville', 'Wildwood', 'Lewiston'],
        'Tulare': ['Dinuba', 'Exeter', 'Farmersville', 'Lindsay', 'Porterville', 'Tulare', 'Visalia', 'Woodlake',
                   'Alpaugh', 'Orosi', 'Springville', 'Earlimart', 'Pixley', 'Terra Bella', 'Ivanhoe', 'Strathmore',
                   'Richgrove'],
        'Tuolumne': ['Sonora', 'Jamestown', 'Columbia', 'Pinecrest', 'Groveland'],
        'Ventura': ['Camarillo', 'Fillmore', 'Moorpark', 'Ojai', 'Oxnard', 'Port Hueneme', 'Santa Paula', 'Simi Valley',
                    'Thousand Oaks', 'Ventura', 'Oak Park', 'Newbury Park', 'Somis'],
        'Yolo': ['Davis', 'West Sacramento', 'Winters', 'Woodland', 'Zamora'],
        'Yuba': ['Marysville', 'Wheatland', 'Linda']
    }

    # Función para asignar el condado basado en la ciudad
    def asignar_condado(city):
        for county, cities in condados_a_ciudades.items():
            if city in cities:
                return county
        return None  # Devuelve None si la ciudad no está en ninguna lista

    # Crear la nueva columna 'county' aplicando la función a la columna 'city'
    df_business_google['county'] = df_business_google['city'].apply(asignar_condado)

    df_ubicacion = df_business_google[['gmap_id', 'address_depurada', 'city', 'county', 'latitude', 'longitude']].copy()

    # Restablecer el índice para que sea consecutivo
    df_ubicacion.reset_index(drop=True, inplace=True)

    # Creamos la nueva columna 'id_locacion' con números incrementales, que serán la PK
    df_ubicacion['id_locacion'] = range(1, len(df_ubicacion) + 1)

    # Reordenar las columnas para que 'id_locacion' esté en primer lugar
    df_ubicacion = df_ubicacion[
        ['id_locacion', 'gmap_id', 'address_depurada', 'city', 'county', 'latitude', 'longitude']]

    # Filtrar los registros en df_reviews_g que coincidan en la columna 'gmap_id'
    df_reviews_google = df_reviews_g[df_reviews_g['gmap_id'].isin(df_business_google['gmap_id'])]

    # A continuación crearemos una nueva columna 'review_id' para usar como primary key.

    # Crear una copia del DataFrame para evitar el SettingWithCopyWarning
    df_reviews_google = df_reviews_google.copy()

    # Crear la nueva columna 'review_id' con números incrementales
    df_reviews_google['review_id'] = range(1, len(df_reviews_google) + 1)

    # Reordenar las columnas para que 'review_id' esté en primer lugar
    df_reviews_google = df_reviews_google[['review_id', 'user_id', 'name', 'time', 'rating', 'text', 'gmap_id']]

    # Guardar los datasets transformados
    df_reviews_g.to_parquet('/tmp/reviews_google_transformed.parquet')
    df_business_google.to_parquet('/tmp/business_google_transformed.parquet')
    df_ubicacion.to_parquet('/tmp/ubicaciones_google_transformed.parquet')

    # Subir archivos transformados a GCS para carga posterior en BigQuery
    bucket_name = 'us-central1-epicureandag-3b408e2a-bucket'
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)

    # Subir los archivos transformados a GCS

    logger = logging.getLogger('airflow.task')
    try:
        bucket.blob('data/tmp/reviews_google_transformed.parquet').upload_from_filename(
            '/data/tmp/reviews_google_transformed.parquet')
        logger.info("Archivo reviews_google_transformed.parquet subido exitosamente.")
    except Exception as e:
        logger.error(f"Error subiendo reviews_google_transformed.parquet: {e}")

    try:
        bucket.blob('data/tmp/business_google_transformed.parquet').upload_from_filename(
            '/data/tmp/business_google_transformed.parquet')
        logger.info("Archivo business_google_transformed.parquet subido exitosamente.")
    except Exception as e:
        logger.error(f"Error subiendo business_google_transformed.parquet: {e}")

    try:
        bucket.blob('data/tmp/ubicaciones_google_transformed.parquet').upload_from_filename(
            '/data/tmp/ubicaciones_google_transformed.parquet')
        logger.info("Archivo ubicaciones_google_transformed.parquet subido exitosamente.")
    except Exception as e:
        logger.error(f"Error subiendo ubicaciones_google_transformed.parquet: {e}")



# Función para cargar datos a BigQuery
def load_data_to_bigquery(**kwargs):
    configuration_business = {
        'load': {
            'sourceUris': ['gs://us-central1-epicureandag-3b408e2a-bucket/data/tmp/business_google_transformed.parquet'],
            'destinationTable': {
                'projectId': 'epicurean-project',
                'datasetId': 'epicurean_dataset',
                'tableId': 'business',
            },
            'sourceFormat': 'PARQUET',
            'writeDisposition': 'WRITE_TRUNCATE',
        }
    }

    configuration_reviews = {
        'load': {
            'sourceUris': ['gs://us-central1-epicureandag-3b408e2a-bucket/data/tmp/reviews_google_transformed.parquet'],
            'destinationTable': {
                'projectId': 'epicurean-project',
                'datasetId': 'epicurean_dataset',
                'tableId': 'reviews',
            },
            'sourceFormat': 'PARQUET',
            'writeDisposition': 'WRITE_TRUNCATE',
        }
    }

    configuration_ubicaciones = {
        'load': {
            'sourceUris': ['gs://us-central1-epicureandag-3b408e2a-bucket/data/tmp/ubicaciones_google_transformed.parquet'],
            'destinationTable': {
                'projectId': 'epicurean-project',
                'datasetId': 'epicurean_dataset',
                'tableId': 'ubicaciones',
            },
            'sourceFormat': 'PARQUET',
            'writeDisposition': 'WRITE_TRUNCATE',
        }
    }

    return configuration_business, configuration_reviews, configuration_ubicaciones


# Definir el DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 9, 19),
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'etl_pipeline_fp',
    default_args=default_args,
    description='DAG para realizar el ETL con Airflow',
    schedule_interval='@daily',
)

# Tarea 1: Extracción de datos
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    provide_context=True,
    dag=dag,
)

# Tarea 2: Transformación de datos
transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    provide_context=True,
    dag=dag,
)

# Tarea 3: Carga de datos en BigQuery
def create_load_task(task_id, configuration, dag):
    return BigQueryInsertJobOperator(
        task_id=task_id,
        configuration=configuration,
        dag=dag
    )

config_business, config_reviews, config_ubicaciones = load_data_to_bigquery()

load_business_task = create_load_task('load_business_to_bigquery', config_business, dag)
load_reviews_task = create_load_task('load_reviews_to_bigquery', config_reviews, dag)
load_ubicaciones_task = create_load_task('load_ubicaciones_to_bigquery', config_ubicaciones, dag)

# Definir las dependencias del flujo
extract_task >> transform_task >> [load_business_task, load_reviews_task, load_ubicaciones_task]
