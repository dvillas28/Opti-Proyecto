from gurobipy import GRB, Model, quicksum # instalada
import numpy as np    # instalada
from os import path

from cargar_parametros import cargar_parametros

# definimos parametros
Tmax = int()
N = int()

# letras griegas para definir variables, parametros, etc
GREEK = "ΑαΒβΓγΔδΕεΖζΗηΘθΙιΚκΛλΜμΝνΞξΟοΠπΡρΣσςΤτΥυΦφΧχΨψΩω"

def main():
    
    # --------- Carga de parametros y definicion de conjuntos ------------------------------------------- 
    # PENDIENTE: cargar los parametros
    datos = cargar_parametros(path.join("data", "example_data.csv"))
    print(datos)

    # conjunto I de rutas
    I = range(1,5) # PENDIENTE: cambiar cuando este lista la data

    # --------- Generacion del modelo -------------------------------------------------------------- 
    model = Model("Problema de Optimizacion")
    model.setParam("TimeLimit", 60) # tiempo max de ejecución (en segundos)

    # --------- Variables de decision -------------------------------------------------------------- 
    
    # Se definen las variables como un diccionario para facilitar el acceso por indice
    # por ejemplo, X[4] tira la cantidad de personas de la ruta 4

    # Xi: cantidad de personas por la ruta i
    X = {i: model.addVar(vtype = GRB.INTEGER, name=f"X_{i}") for i in I}

    # Ti: Tiempo de evacuacion de cada ruta i
    T = {i: model.addVar(vtype = GRB.CONTINUOUS, name=f"T_{i}") for i in I}

    # Si: 1 si el camino i esta saturado. 0 eoc
    S = {i: model.addVar(vtype = GRB.BINARY, name=f"S_{i}") for i in I}

    # Ri: 1 si el camino i esta en uso. 0 eoc
    R = {i: model.addVar(vtype = GRB.BINARY, name=f"R_{i}") for i in I}
    
    # Qi: 1 si el camino i no cumple con la calidad minima. 0 eoc
    Q = {i: model.addVar(vtype = GRB.BINARY, name=f"Q_{i}") for i in I}

    # Θi: 1 si el camino i sobrepasa la inclinacion máxima. 0 eoc
    Θ = {i: model.addVar(vtype = GRB.BINARY, name=f"Θ_{i}") for i in I}

    # Ai: 1 si el camino i no cumple con el ancho mínimo. 0 eoc
    A = {i: model.addVar(vtype = GRB.BINARY, name=f"A_{i}") for i in I}

    # Agregar las variables al modelo
    model.update()

    # --------- Restricciones ---------------------------------------------------------------------- 
    
    # R1. Tiempo máximo de cada camino: Ningún camino puede demorarse más de lo que tarde el
    # tsunami en llegar.

    for i in I:
        model.addConstr(T[i] <= Tmax, name=f"R1_{i}")

    # R2. Conservación del flujo: Todas las personas deben estar en un camino
    model.addConstr(quicksum(X[i] for i in I) == N, name="R2")

    # R3. Capacidad del camino: La cantidad de personas en un camino no puede sobrepasar la
    # capacidad máxima del camino.
    for i in I:
        model.addConstr(X[i] <= c[i], name=f"R3_{i}")
    
    # R4. Saturación:  Si la cantidad de personas en un camino supera el umbral que permite la ruta 
    # sin saturarse, la ruta se satura (ocasionando S[i] = 1).
    for i in I:
        model.addConstr(X[i] <= c[i] * b[i] * (1 - S[i]) + N * S[i], name=f"R4_{i}")

    # R5. Ruta en uso:  Si no hay personas en una ruta, esta no se encuentra en uso. 
    # Por lo cual su tiempo no será contabilizado en el cálculo de la función a minimizar.
    for i in I:
        model.addConstr( R[i] * N >= X[i] , name=f"R5_{i}")

    # R6. Cumple calidad


    # --------- Funcion Objetivo ------------------------------------------------------------------- 
    model.setObjective(quicksum((...) for i in I), GRB.MINIMIZE)


    # resolver el problema
    model.optimize()

    # --------- Impresion de resultados ------------------------------------------------------------ 


if __name__ == "__main__":
    main()