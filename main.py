from gurobipy import GRB, Model, quicksum # instalada
from os import path
import pandas as pd
from datos.parametros import cargar_parametros

def main():
    
############## Carga de parametros y definicion de conjuntos #######################################
    
    # De aqui salen c[i], beta[i], l[i], a[i], q[i], sigma[i], theta[i] y los otros parametros
    c, l, a, q, sigma, theta, params, names = cargar_parametros(path.join("datos", "datos_e3_version2.txt"))

    # Conjunto I de rutas
    I = range(params["I"])

############## Generacion del modelo ############################################################### 
    
    model = Model("Problema de Optimizacion")
    model.setParam("TimeLimit", 30) # tiempo max de ejecución (en segundos)

############## Variables de decision ############################################################### 
    
    # Se definen las variables como un diccionario para facilitar el acceso por indice
    # por ejemplo, X[4] tira la cantidad de personas de la ruta 4

    # Xi: cantidad de personas por la ruta i
    X = {i: model.addVar(vtype = GRB.INTEGER, name=f"X_{i}") for i in I}

    # Ti: Tiempo de evacuacion de cada ruta i
    T = {i: model.addVar(vtype = GRB.CONTINUOUS, name=f"T_{i}") for i in I}

    # Si: 1 si el i esta saturado. 0 eoc
    S = {i: model.addVar(vtype = GRB.BINARY, name=f"S_{i}") for i in I}

    # Ri: 1 si el camino i esta en uso. 0 eoc
    R = {i: model.addVar(vtype = GRB.BINARY, name=f"R_{i}") for i in I}
    
    # Qi: 1 si el camino i no cumple con la calidad minima. 0 eoc
    Q = {i: model.addVar(vtype = GRB.BINARY, name=f"Q_{i}") for i in I}

    # Thetai: 1 si el camino i sobrepasa la inclinacion máxima. 0 eoc
    Theta = {i: model.addVar(vtype = GRB.BINARY, name=f"Theta_{i}") for i in I}

    # Ai: 1 si el camino i no cumple con el ancho mínimo. 0 eoc
    A = {i: model.addVar(vtype = GRB.BINARY, name=f"A_{i}") for i in I}

    # Agregar las variables al modelo
    model.update()

############## Restricciones #######################################################################
    
    # R2. Conservación del flujo: Todas las personas deben estar en un camino
    model.addConstr(quicksum(X[i] for i in I) == params["N"], name="R2")
    
    # añadimos todas las demas restricciones del tipo "para todo i en I" en un solo loop (eficiente!)
    for i in I:
        
        # R1. Tiempo máximo de cada camino: Ningún camino puede demorarse más de lo que tarde el
        # tsunami en llegar.
        model.addConstr(T[i] <= params["Tmax"], name=f"R1_{i}")
        # model.addConstr(7*60 <= T[i], name=f"R11_{i}")

        # R3. Capacidad del camino: La cantidad de personas en un camino no puede sobrepasar la
        # capacidad máxima del camino.
        model.addConstr(X[i] <= c[i], name=f"R3_{i}")
    
        # R4. Saturación: Si la cantidad de personas en un camino supera el umbral que permite la ruta 
        # sin saturarse, la ruta se satura (ocasionando S[i] = 1).
        model.addConstr(X[i] <= c[i] * params["beta"] * (1 - S[i]) + params["N"] * S[i], name=f"R4_{i}")

        # R5. Ruta en uso:  Si no hay personas en una ruta, esta no se encuentra        # sin saturarse, la ruta se satura (ocasionando S[i] = 1).
        model.addConstr(R[i] * params["N"] >= X[i] , name=f"R5_{i}")

        # R6. Cumple calidad mínima: Si una calle no cumple el estándar mínimo de calidad, esta no se
        # Por lo cual su tiempo no será contabilizado en el cálculo de la función a minimizar.
        model.addConstr(R[i] * params["N"] >= X[i] , name=f"R5_{i}")

        # R6. Cumple calidad mínima: Si una calle no cumple el estándar mínimo de calidad, esta no se
        # considera como una calle apta para el uso.
        model.addConstr(q[i] >= params["q_min"] * (1 - Q[i]), name=f"R6_{i}")

        # R7. Cumple inclinación máxima: Si una calle sobrepasa la inclinación máxima permitida, 
        # esta no se considera una calle apta para el uso.
        model.addConstr(theta[i] * (1 - Theta[i]) <= params["theta_max"], name=f"R7_{i}")
    
        # R8. Cumple el ancho mínimo: Si una ruta no cumple con el ancho mínimo necesario, no se
        # considera una ruta apta para la evacuación.
        model.addConstr(a[i] >= params["a_min"] * (1 - A[i]), name=f"R8_{i}")

        # R9. Irrelevancia de características de la calle: Si una calle no está en uso, no 
        # nos afecta si cumplen sus características limites
        model.addConstr(Q[i] <= R[i], name=f"R9_{i}_irrelevancia_por_calidad")
        model.addConstr(Theta[i] <= R[i], name=f"R9_{i}_irrelevancia_por_inclinacion")
        model.addConstr(A[i] <= R[i], name=f"R9_{i}_irrelevancia_por_ancho")

        # R10. Las calles que no poseen iluminación, no pueden ser utilizadas de noche
        model.addConstr(X[i] <= params["M"] * (1 - (sigma[i] * params["epsilon"])), name=f"R10_{i}")

        # R11. En caso de que una calle no cumpla con ningún requisito la calle no se puede utilizar
        model.addConstr(X[i] <= params["M"] * (3 - Q[i] - Theta[i] - A[i]), name=f"R11_{i}")

        # R2
        # model.addConstr(T[i] <= R[i] ())

    # R12. Definimos Ti
    for i in I:
        model.addConstr(T[i] == ((l[i]) * params["alpha"] + theta[i] * params["kappa"] + params["gamma"] * q[i]) * R[i] + (X[i] * params["delta"]) + params["Tmax"] * (params["eta"] * Q[i] + params["lambda"] * Theta[i] + params["mu"] * A[i] + params["zeta"] * S[i]), name=f"Restriccion T_i")


############## Funcion Objetivo ####################################################################
    
    model.setObjective(quicksum(T[i] for i in I), GRB.MINIMIZE)


    # Resolver el problema
    model.optimize()


############### Impresion de resultados ############################################################
    
    print(f"Valor de la funcion objetivo = {model.ObjVal}")

    for key, value in params.items():
        print(f"{key}: {value}")

    # Imprimir el encabezado de la tabla con formato alineado
    print(f"{'ruta':<6} | {'X_i':<4} | {'T_i':<6} | {'R_i':<5} | {'Theta_i':<8} | {'A_i':<5} | {'S_i':<5} | {'Q_i':<5} | {'nombre'} ")

    # Iterar sobre los elementos de I y mostrar los valores con el mismo formato alineado
    for i in I:
        print(f"{i:<6} |{X[i].x:<5} | {round(T[i].x, 2):<6} | {R[i].x:<5} | {Theta[i].x:<8} | {A[i].x:<5} | {S[i].x:<5} | {Q[i].x:<5} | {names[i]}")

    
    # Escribir a un excel los resultados

    redondear = lambda var: round(var.x, 2)

    data = {
        "ruta": pd.Series(names),
        "X_i":pd.Series(map(redondear, X.values())),
        "T_i":pd.Series(map(redondear, T.values())),
        "R_i":pd.Series(map(redondear, R.values())),
        "Theta_i":pd.Series(map(redondear, Theta.values())),
        "A_i":pd.Series(map(redondear, A.values())),
        "S_i":pd.Series(map(redondear, S.values())),
        "Q_i":pd.Series(map(redondear, Q.values()))
    }

    df = pd.DataFrame(data)
    df.to_excel(path.join("resultados", "resultados.xlsx"), index=False)


if __name__ == "__main__":
    main()