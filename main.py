
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import Dict
from fastapi import FastAPI
import pandas as pd
from datetime import datetime

app = FastAPI()

df = pd.read_csv('Datos/movies_data.csv', low_memory=False)


@app.get('/Home')
def home():
    return {'message': 'Bienvenido a mi API de películas'}


@app.get('/Peliculas Del Mes')
def peliculas_mes(mes:str) -> int:
    meses: Dict[str, int] = {'enero': 1,'febrero': 2,'marzo': 3,'abril': 4, 'mayo': 5, 'junio': 6,
        'julio': 7,'agosto': 8,'septiembre': 9,'octubre': 10,'noviembre': 11,'diciembre': 12}

    mes_limpio = mes.lower()
    if mes_limpio not in meses:
        print(f"Error: mes {mes} inválido")
        return 0

    mes_numero = meses[mes_limpio]
    mes_numero = meses[mes.lower()]
    peliculas = [p for p in df['release_date']
                 if isinstance(p, str) and datetime.strptime(p, '%Y-%m-%d').month == mes_numero]
    return len(peliculas)


@app.get('/Peliculas Del Dia')
def peliculas_dia(dia:str) -> int:
    dias: Dict[str, int] = {'lunes': 0,'martes': 1,'miércoles': 2,
    'jueves': 3,'viernes': 4,'sábado': 5,'domingo': 6}

    dia_limpio = dia.lower()
    if dia_limpio not in dias:
        print(f"Error: día {dia} inválido")
        return 0

    dia_numero = dias[dia_limpio]
    dia_numero = dias[dia.lower()]
    peliculas = [p for p in df['release_date']
                 if isinstance(p, str) and datetime.strptime(p, '%Y-%m-%d').weekday() == dia_numero]

    peliculas_ajustadas = []
    for p in peliculas:
        fecha = datetime.strptime(p, '%Y-%m-%d')
        if fecha.day > 6:
            try:
                fecha_ajustada = fecha.replace(day=fecha.day-7)
                peliculas_ajustadas.append(fecha_ajustada.strftime('%Y-%m-%d'))
            except ValueError:
                pass
        else:
            peliculas_ajustadas.append(p)

    return str(len(peliculas_ajustadas))


def buscar_peliculas_por_franquicia(franquicia):
    '''Devuelve una lista de películas que pertenecen a la franquicia especificada'''
    peliculas_franquicia = []
    for indice, fila in df.iterrows():
        if fila["collection_name"] == franquicia:
            peliculas_franquicia.append(fila["title"])
    return peliculas_franquicia


@app.get('/Franquicia')
def franquicia(franquicia):
    peliculas = buscar_peliculas_por_franquicia(franquicia)
    cantidad_peliculas = len(peliculas)
    ganancia_total = sum(df.loc[df['title'] == pelicula, 'revenue'].values[0]
                         for pelicula in peliculas if pelicula in df['title'].tolist())
    ganancia_promedio = ganancia_total / \
        (cantidad_peliculas if cantidad_peliculas > 0 else 0)
    return {
        'franquicia': franquicia,"peliculas": peliculas,'cantidad': cantidad_peliculas,
        'ganancia_total': ganancia_total,'ganancia_promedio': ganancia_promedio}


@app.get('/Peliculas Por Pais')
def peliculas_pais(pais):
    peliculas_de_pais = []
    for indice, fila in df.iterrows():
        if fila["production_countries"] == pais:
            peliculas_de_pais.append(fila["title"])
    return {'pais': pais, 'cantidad': len(peliculas_de_pais)}


@app.get('/Productoras')
def productoras(productora):
    peliculas = df.loc[df['production_companies'].str.contains(
        productora, na=False)]
    cantidad_peliculas = len(peliculas)
    ganancia_total = peliculas['revenue'].sum()
    return {
        "Productora": productora,
        'cantidad': cantidad_peliculas,
        'ganancia_total': int(ganancia_total)
    }


@app.get('/retorno')
def retorno(pelicula: str):
    '''Ingresas la pelicula, retornando la inversion, la ganancia, el retorno y el año en el que se lanzo'''
    for index, row in df.iterrows():
        if row['title'].lower() == pelicula.lower():
            inversion = row['budget']
            ganancia = row['revenue']
            retorno = (ganancia - inversion) / inversion
            anio = row['release_year']
            return {'pelicula': pelicula, 'inversion': inversion, 'ganancia': int(ganancia), 'retorno': round(retorno, 2), 'año': int(anio)}
    return {'error': f'No se encontró información para la película "{pelicula}"'}

  
@app.get('/Recomendacion')
def recomendacion(titulo: str):

    peliculas = pd.read_csv("Datos/movies_dataML.csv", low_memory= False)
    
    peliculas = peliculas.head(5000)
    
    vectorizer_title = TfidfVectorizer()
    titulo_vectorizado = vectorizer_title.fit_transform(
        peliculas['title'].fillna(''))


    vectorizer_genres = TfidfVectorizer()
    generos_vectorizados = vectorizer_genres.fit_transform(
        peliculas['genres'].fillna(''))

  
    caracteristicas_combinadas = cosine_similarity(
        titulo_vectorizado) + cosine_similarity(
        generos_vectorizados)


    similitud_coseno = cosine_similarity(caracteristicas_combinadas)

    try:
        idx = peliculas[peliculas['title'] ==  titulo].index[0]

        puntuaciones_similitud = list(enumerate(similitud_coseno[idx]))

        puntuaciones_similitud = sorted(puntuaciones_similitud, key=lambda x: x[1], reverse=True)

        peliculas_similares = [peliculas.iloc[i[0]]['title'] for i in puntuaciones_similitud[1:6]]

        return peliculas_similares

    except:
        return "Lo siento, no pude encontrar una coincidencia para ese título."
