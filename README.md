# <h1 align=center> **PROYECTO INDIVIDUAL Nº1** </h1>

# <h1 align=center>**`Machine Learning Operations (MLOps)`**</h1>

## Proyecto de análisis de datos y desarrollo de API de películas

Este proyecto tiene como objetivo realizar un análisis exploratorio de datos de películas, desarrollar una API para consultar información 
sobre películas y entrenar un modelo de recomendación de películas basado en similitud de puntuaciones.

## Datos utilizados

Los datos se trabajaron en Visual Studio. Se utilizó para obtener los datos y limpiarlos, realizando las transformaciones necesarias para su análisis.
Los datos fueron proporcionados en formato CSV y consistían en información sobre películas, incluyendo su título, año de estreno, presupuesto, 
 ingresos y otros detalles relevantes.

Durante el proceso de análisis, se llevaron a cabo las siguientes transformaciones en los datos:

-Las columnas belongs_to_collection, production_companies, genres, production_countries y spoken_lenguages estaban anidados y debieron ser desanidados.

-Los valores nulos de los campos revenue y budget fueron rellenados con el número 0.

-Los valores nulos del campo release date fueron eliminados.

-Las fechas en el campo release date fueron transformadas al formato AAAA-mm-dd y se creó la columna release_year para extraer el año de la fecha de estreno.

-Se creó la columna return para calcular el retorno de inversión. 

-Se eliminaron las columnas que no serían utilizadas en el análisis, como video, imdb_id, adult, original_title, 
 vote_count, poster_path, homepage y colmunas extras que se hiceron para el desanidado.
 
Una vez limpios los datos se guardaron en eñ archivo "movies_data.csv" para posterior mente empezar a trabajar los endpoints. 
Ademas, el proceso de transformacion se guardo en el archivo "Transformaciones.ipynb"


## Desarrollo de la API

Se utilizó el framework FastAPI para desarrollar una API con 6 endpoints que permiten consultar información sobre películas. 
Los endpoints son los siguientes:

/peliculas_mes(mes): retorna la cantidad de películas estrenadas en un mes determinado.
/peliculas_dia(dia): retorna la cantidad de películas estrenadas en un día de la semana determinado.
/franquicia(franquicia): retorna la cantidad de películas, ganancia total y ganancia promedio de una franquicia determinada.
/peliculas_pais(pais): retorna la cantidad de películas producidas en un país determinado.
/productoras(productora): retorna la ganancia total y la cantidad de películas producidas por una productora determinada.
/retorno(pelicula): retorna la inversión, ganancia, retorno y año de estreno de una película determinada.

También se desarrolló una función adicional /recomendacion(titulo) que utiliza el modelo de recomendación entrenado para sugerir 
películas similares a una película determinada.

## Análisis exploratorio de datos

Se realizó un análisis exploratorio de datos utilizando diversas librerías de Python como pandas, seaborn y matplotlib. 
Se investigaron las relaciones entre las variables de los datasets, se identificaron outliers y se hiceron ajustes cuando se eligieron las variables que iban a 
ser usadas para ML. 
Los resultados de este análisis se presentan en el archivo "EDA.ipynb", donde se pueden encontrar los gráficos y tablas generados a partir de los datos.
Los cambio fueron guardados en el archivo "movies_dataML.csv".

## Modelo de recomendación

Se entrenó un modelo de recomendación basado en similitud de puntuaciones utilizando la librería scikit-learn. El modelo utiliza los datos de 
puntuaciones de las películas para calcular la similitud entre ellas y sugerir películas similares a una determinada. 
El modelo se integró en la API como una función adicional.

## Deployment

La API se encuentra deployada en Render y se utilizó la librería gunicorn para manejar múltiples conexiones a la API 
LINK: https://peliculasapi.onrender.com/docs#/

## Conclusiones

Este proyecto permitió explorar diversos aspectos del análisis de datos, el desarrollo de API y el entrenamiento de modelos de machine learning.
Se pudo obtener información valiosa sobre la base de datos de películas y desarrollar una API sencilla y eficiente para su consulta. 
