from typing import Dict
from fastapi import FastAPI
import pandas as pd
from datetime import datetime
from sklearn.neighbors import NearestNeighbors
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler

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


@app.get('/Retorno')
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

#Preparamos el Modelo 
    
datoML = pd.read_csv("Datos/movies_dataML.csv", low_memory=False)

caracteristicas = datoML[["genres","spoken_languages","popularity","vote_average"]]

genres_dum = caracteristicas["genres"].str.get_dummies(sep=", ")

language_dum = caracteristicas["spoken_languages"].str.get_dummies(sep=",")

datom_c = pd.concat([language_dum,genres_dum, caracteristicas[["popularity", "vote_average"]]], axis=1)

imputer = SimpleImputer(strategy='most_frequent')

X_imputed = imputer.fit_transform(datom_c)

scaler = MinMaxScaler()

X_scaled = scaler.fit_transform(X_imputed)

model = NearestNeighbors()

model.fit(X_scaled)


@app.get('/Recomendacion')
def recomendacion(titulo: str):
    '''Ingresas un nombre de película y te recomienda 5 similares'''

    movie_index = datoML[datoML['title'] == titulo].index[0]

    X_movie = X_scaled[movie_index].reshape(1, -1)

    distances, indices = model.kneighbors(X_movie)
    Recomendacion = datoML.iloc[indices[0]]['title'].tolist()

    respuesta = {}
    for i, movie in enumerate(Recomendacion[:5]):
        respuesta[str(i+1)] = str(movie)

    return {'Las Películas Recomendadas son': respuesta}
