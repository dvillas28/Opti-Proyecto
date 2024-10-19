import pandas as pd   # instalada
from os import path

def cargar_parametros(path: str) -> tuple:
    """
    Funcion para procesar el csv
    """
    
    data = pd.read_csv(path)

    # PENDIENTE: parsear la data
    # las columnas como calidad, o luz, debemos pasarlas a numero antes
    
    return data

if __name__ == "__main__":
    datos = cargar_parametros(path.join("data", "example_data.csv"))
    print(datos)