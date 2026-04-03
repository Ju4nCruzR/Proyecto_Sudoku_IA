# mrv.py
# Modulo que implementa la cuarta estrategia de solucion para el Sudoku:
# backtracking con forward checking y la heuristica MRV (Minimum Remaining
# Values). Esta estrategia extiende el forward checking del modulo anterior
# agregando una heuristica de seleccion de variables: en lugar de elegir
# siempre la primera celda vacia disponible, el algoritmo selecciona la
# celda cuyo dominio tenga la menor cantidad de valores posibles.
# La idea es atacar primero las celdas mas restringidas, lo que reduce
# la probabilidad de tomar decisiones incorrectas y obliga a detectar
# conflictos mucho mas temprano en el arbol de busqueda.
# Esta heuristica es ampliamente usada en la teoria de CSP y representa
# una mejora natural sobre el forward checking puro.

import math
from tablero import es_valido


# ─────────────────────────────────────────
# INICIALIZACION DE DOMINIOS
# ─────────────────────────────────────────

def inicializar_dominios(tablero, n):
    # Construye un diccionario que mapea cada celda vacia del tablero
    # a su conjunto de valores posibles segun el estado actual.
    # Solo se incluyen las celdas vacias porque las celdas ya ocupadas
    # tienen su valor definido y no forman parte del espacio de busqueda.
    # Retorna el diccionario de dominios.

    dominios = {}

    for fila in range(n):
        for col in range(n):
            if tablero[fila][col] == 0:
                dominios[(fila, col)] = [
                    num for num in range(1, n + 1)
                    if es_valido(tablero, n, fila, col, num)
                ]

    return dominios


# ─────────────────────────────────────────
# SELECCION DE VARIABLE POR MRV
# ─────────────────────────────────────────

def seleccionar_celda_mrv(dominios):
    # Implementa la heuristica MRV seleccionando la celda vacia cuyo
    # dominio tenga la menor cantidad de valores posibles restantes.
    # Esta es la diferencia fundamental respecto al forward checking
    # basico, que simplemente elige la primera celda vacia disponible.
    # Elegir la celda mas restringida primero reduce el factor de
    # ramificacion del arbol de busqueda y detecta conflictos antes,
    # evitando explorar ramas que inevitablemente fallaran.
    # Retorna la celda con el dominio mas pequeno.

    return min(dominios, key=lambda celda: len(dominios[celda]))


# ─────────────────────────────────────────
# OBTENCION DE CELDAS VECINAS
# ─────────────────────────────────────────

def obtener_vecinas(fila, col, n):
    # Retorna un conjunto con las posiciones de todas las celdas que
    # comparten fila, columna o subcuadricula con la celda (fila, col).
    # Estas son las celdas cuyos dominios se actualizan al asignar
    # un valor a la celda actual.

    raiz = math.isqrt(n)
    vecinas = set()

    # Celdas en la misma fila
    for c in range(n):
        if c != col:
            vecinas.add((fila, c))

    # Celdas en la misma columna
    for f in range(n):
        if f != fila:
            vecinas.add((f, col))

    # Celdas en la misma subcuadricula
    fila_inicio = (fila // raiz) * raiz
    col_inicio  = (col  // raiz) * raiz

    for f in range(fila_inicio, fila_inicio + raiz):
        for c in range(col_inicio, col_inicio + raiz):
            if (f, c) != (fila, col):
                vecinas.add((f, c))

    return vecinas


# ─────────────────────────────────────────
# COMPROBACION HACIA ADELANTE
# ─────────────────────────────────────────

def comprobacion_hacia_adelante(dominios, fila, col, num, n):
    # Aplica la comprobacion hacia adelante despues de asignar num
    # a la celda (fila, col). Elimina num del dominio de todas las
    # celdas vecinas que aun no tienen valor asignado.
    # Si el dominio de alguna celda vecina queda vacio, retorna None
    # indicando que esta rama no puede llevar a una solucion valida.
    # Si todos los dominios siguen siendo validos, retorna una copia
    # actualizada de los dominios para continuar la busqueda.

    nuevos_dominios = {celda: list(vals) for celda, vals in dominios.items()}

    vecinas = obtener_vecinas(fila, col, n)

    for vecina in vecinas:
        if vecina in nuevos_dominios:
            if num in nuevos_dominios[vecina]:
                nuevos_dominios[vecina].remove(num)

            # Si el dominio quedo vacio, esta rama no tiene solucion
            if len(nuevos_dominios[vecina]) == 0:
                return None

    return nuevos_dominios


# ─────────────────────────────────────────
# SOLUCIONADOR CON MRV
# ─────────────────────────────────────────

def resolver_mrv(tablero, n, dominios=None):
    # Intenta resolver el tablero usando backtracking con forward checking
    # y la heuristica MRV. La diferencia clave respecto a forward_checking.py
    # esta en la funcion seleccionar_celda_mrv, que elige siempre la celda
    # mas restringida en lugar de la primera disponible. Esto permite que
    # el algoritmo tome decisiones mas informadas en cada paso, reduciendo
    # el numero total de estados que necesita explorar para llegar a la
    # solucion o determinar que no existe una.
    # Retorna True si encontro una solucion, False si no existe solucion.
    # La solucion queda almacenada directamente en el tablero recibido.

    if dominios is None:
        dominios = inicializar_dominios(tablero, n)

    # Si no quedan celdas en los dominios, el tablero esta resuelto
    if not dominios:
        return True

    # Se selecciona la celda con menos valores posibles usando MRV
    fila, col = seleccionar_celda_mrv(dominios)

    for num in dominios[(fila, col)]:

        if es_valido(tablero, n, fila, col, num):
            tablero[fila][col] = num

            # Se actualizan los dominios de las celdas vecinas
            nuevos_dominios = comprobacion_hacia_adelante(dominios, fila, col, num, n)

            if nuevos_dominios is not None:
                # Se elimina la celda actual porque ya fue asignada
                nuevos_dominios.pop((fila, col), None)

                if resolver_mrv(tablero, n, nuevos_dominios):
                    return True

            # Si no llevo a solucion, se deshace la asignacion
            tablero[fila][col] = 0

    # Ningun valor del dominio funciono para esta celda, se retrocede
    return False


# ─────────────────────────────────────────
# PUNTO DE ENTRADA PARA PRUEBAS
# ─────────────────────────────────────────

if __name__ == "__main__":
    # Este bloque permite probar el modulo directamente desde la consola.
    # Al importar este modulo desde sudoku.py, este bloque no se ejecuta.

    import time
    from tablero import leer_tablero, imprimir_tablero

    print("─" * 45)
    print(" SOLUCIONADOR CON MRV")
    print("─" * 45)

    ruta = "ejemplos/sudoku_9x9.txt"
    tablero, n = leer_tablero(ruta)

    print("─" * 45)
    print(f"Tablero inicial ({n}x{n}):")
    imprimir_tablero(tablero, n)

    inicio = time.time()
    resuelto = resolver_mrv(tablero, n)
    fin = time.time()

    if resuelto:
        print("─" * 45)
        print("Tablero resuelto:")
        imprimir_tablero(tablero, n)
    else:
        print("\nNo se encontro solucion.")

    print("─" * 45)
    print(f"Tiempo de ejecucion: {fin - inicio:.4f} segundos")
    print("─" * 45)