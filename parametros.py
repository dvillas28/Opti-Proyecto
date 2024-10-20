import pandas as pd   # instalada
from os import path

def cargar_parametros(path: str) -> tuple[dict]:
    """
    Funcion para procesar el csv y cargar los parametros, retorna una tupla de diccionarios
    """
    c = dict()      # capacidad maxima del camino i
    beta = dict()   # % de la capacidad maxima a la cual el camino i satura
    l = dict()      # largo de la ruta i
    a = dict()      # ancho de la ruta i
    q = dict()      # calidad de la ruta i
    sigma = dict()  # parámetro booleano que representa la presencia de iluminación en la ruta i. Vale 1 en caso de que si haya iluminación y 0 en caso contrario
    theta = dict()  # inclinacion de la ruta i

    otros_params = {
    "Tmax":      0, # tiempo en el cual llega el tsunami
    "N":         0, # cantidad total de persoans a evacuar
    "alpha":     0, # ponderador de tiempo asociado a las dimensiones del camino
    "kappa":     0, # ponderador de tiempo asociado a la pendiente del camino
    "gamma":     0, # ponderador de tiempo asociado a la calidad del camino
    "delta":     0, # ponderador de tiempo asociado a la cantidad de gente en el camino
    "zeta":      0, # % de tiempo asociado a la saturación de la via
    "eta":       0, # % de penalizacion asociado al incumplimiento de la calidad mínima del camino
    "lambda":    0, # % de penalizacion asociado al incumplimiento de la pendiente máxima
    "mu":        0, # % de penalizacion asociado al incumplimiento del ancho minimo para una ruta
    "a_min":     0, # ancho mínimo de una ruta para ser considerada como via de evacuación
    "q_min":     0, # calidad minima de una ruta para ser considerada como via de evacuacion
    "theta_max": 0, # inclinacion máxima de una ruta para ser considerara como vía de evacuación
    "epsilon":   0, # parametro booleano que determina si el tsunami ocurre de dia (0) o de noche (1)
    "M":      10e6, # un número muy grande
    "I":         0, # cantidad de rutas en el conjunto I
    
    }


    # leer la data desde el csv
    df = pd.read_csv(path)
    
    otros_params["I"] = df.shape[0] # setear la cantidad de rutas en base a la cantidad de filas

    # PENDIENTE: parsear la data
    # las columnas como calidad, o luz, debemos pasarlas a numero antes
    
    return

if __name__ == "__main__":
    datos = cargar_parametros(path.join("data", "example_data.csv"))