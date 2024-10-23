import pandas as pd   # instalada
from os import path
from typing import Any, Union
from random import randint

def convert_to_float(value) -> Union[float, str]:
    
    if isinstance(value, str):
        try:
            return float(value.replace(",", "."))
        except ValueError:
            return value
    
    return float(value)

def convert_to_binary(value: str) -> Union[int, str]:
    
    if isinstance(value, str):
        try:
            if value.lower() == "mala":
                return 0
            elif value.lower() == "buena":
                return 1
        except ValueError:
            return value


def cargar_parametros(path: str) -> tuple[dict]:
    """
    Funcion para procesar el csv y cargar los parametros, retorna una tupla de diccionarios
    """

    otros_params = {
    "Tmax":      14*60, # tiempo [minutos] en el cual llega el tsunami
    "N":         10000, # cantidad total de personas a evacuar
    "beta":      0.8, # % de la capacidad maxima a la cual el camino satura
    "alpha":     0.255, # ponderador de tiempo asociado a las dimensiones del camino  
    "kappa":     1, # ponderador de tiempo asociado a la pendiente del camino  
    "gamma":     0.3, # ponderador de tiempo asociado a la calidad del camino  
    "delta":     0.055, # ponderador de tiempo asociado a la cantidad de gente en el camino  
    "zeta":      0.3, # % de tiempo asociado a la saturación de la via 
    "eta":       0.2, # % de penalizacion asociado al incumplimiento de la calidad mínima del camino 
    "lambda":    0.5, # % de penalizacion asociado al incumplimiento de la pendiente máxima 
    "mu":        0.2, # % de penalizacion asociado al incumplimiento del ancho minimo para una ruta 
    "a_min":     4, # ancho mínimo [m] de una ruta para ser considerada como via de evacuación
    "q_min":     2, # calidad minima de una ruta para ser considerada como via de evacuacion
    "theta_max": 30, # inclinacion máxima de una ruta para ser considerara como vía de evacuación 
    "epsilon":   0, # parametro booleano que determina si el tsunami ocurre de dia (0) o de noche (1)
    "M":      10e6, # un número muy grande
    "I":         0, # cantidad de rutas en el conjunto I
    
    }

    # leer la data desde el csv
    df = pd.read_csv(path, sep="\t")

    I = df.shape[0]
    otros_params["I"] = I # setear la cantidad de rutas en base a la cantidad de filas
    
    
    # transformar columnas numericas en floats
    columnas_numericas = ['largo [m]', 'ancho [m]', 'diferencia altura [m]', 'pendiente', 'capacidad', 'area', 'calidad']
    for col in columnas_numericas:
        df[col] = df[col].apply(convert_to_float)

    # transformar parametro de luz
    df["luz"] = df["luz"].apply(convert_to_binary)


    # pasar todo a diccionarios
    l = df["largo [m]"].to_dict()     # largo de la ruta i
    a = df["ancho [m]"].to_dict()     # ancho de la ruta i
    theta = df["pendiente"].to_dict() # inclinacion de la ruta i
    c = df["capacidad"].to_dict()     # capacidad maxima del camino i
    sigma = df["luz"].to_dict()       # parámetro booleano que representa la presencia de iluminación en la ruta i. Vale 1 en caso de que si haya iluminación y 0 en caso contrario
    
    q = df["calidad"].to_dict()       # calidad de la ruta i
    
    names = df["nombre_ruta"].to_dict()

    return c, l, a, q, sigma, theta, otros_params, names

if __name__ == "__main__":
    datos = cargar_parametros(path.join("datos_e3.txt"))