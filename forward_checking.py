# forward_checking.py
# Modulo que implementa la tercera estrategia de solucion para el Sudoku:
# backtracking con comprobacion hacia adelante (forward checking).
# A diferencia del backtracking basico, este algoritmo mantiene un registro
# de los valores disponibles (dominio) para cada celda vacia del tablero.
# Cada vez que se asigna un valor a una celda, se eliminan ese valor de los
# dominios de todas las celdas vecinas que comparten fila, columna o
# subcuadricula. Si el dominio de alguna celda vecina queda vacio, el
# algoritmo retrocede de inmediato sin seguir explorando ese camino,
# ya que se sabe con certeza que no llevara a una solucion valida.
# Esto lo hace significativamente mas eficiente que el backtracking basico.

import math
from tablero import es_valido, copiar_tablero


# ─────────────────────────────────────────
# INICIALIZACION DE DOMINIOS
# ─────────────────────────────────────────

def inicializar_dominios(tablero, n):
    # Construye un diccionario que mapea cada celda vacia del tablero
    # a su conjunto de valores posibles (dominio).
    # Para cada celda vacia se revisan todas las restricciones actuales
    # del tablero y se incluyen solo los valores que no violan ninguna.
    # Las celdas ya ocupadas no se incluyen en el diccionario porque
    # su valor ya esta definido y no cambiara.
    # Retorna el diccionario de dominios.

    dominios = {}

    for fila in range(n):
        for col in range(n):
            if tablero[fila][col] == 0:
                # Se incluyen en el dominio solo los valores validos
                # segun el estado actual del tablero
                dominios[(fila, col)] = [
                    num for num in range(1, n + 1)
                    if es_valido(tablero, n, fila, col, num)
                ]

    return dominios


# ─────────────────────────────────────────
# BUSQUEDA DE CELDA VACIA
# ─────────────────────────────────────────

def encontrar_celda_vacia(tablero, n):
    # Recorre el tablero de izquierda a derecha y de arriba a abajo
    # buscando la primera celda que contenga un cero.
    # Retorna una tupla (fila, col) con la posicion encontrada,
    # o None si no hay celdas vacias, lo que indica que el tablero
    # esta completamente resuelto.

    for fila in range(n):
        for col in range(n):
            if tablero[fila][col] == 0:
                return (fila, col)
    return None


# ─────────────────────────────────────────
# OBTENCION DE CELDAS VECINAS
# ─────────────────────────────────────────

def obtener_vecinas(fila, col, n):
    # Retorna un conjunto con las posiciones de todas las celdas que
    # comparten fila, columna o subcuadricula con la celda (fila, col).
    # Estas son las celdas cuyos dominios se deben actualizar cuando
    # se asigna un valor a la celda actual.

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
    # Si al eliminar un valor el dominio de alguna celda vecina queda
    # vacio, se retorna None de inmediato indicando que esta rama
    # no puede llevar a una solucion valida.
    # Si todos los dominios siguen siendo validos, retorna una copia
    # actualizada de los dominios para continuar la busqueda.

    # Se trabaja sobre una copia para poder deshacer cambios al retroceder
    nuevos_dominios = {celda: list(vals) for celda, vals in dominios.items()}

    vecinas = obtener_vecinas(fila, col, n)

    for vecina in vecinas:
        if vecina in nuevos_dominios:
            # Se elimina el valor asignado del dominio de la celda vecina
            if num in nuevos_dominios[vecina]:
                nuevos_dominios[vecina].remove(num)

            # Si el dominio quedo vacio, esta rama no tiene solucion
            if len(nuevos_dominios[vecina]) == 0:
                return None

    return nuevos_dominios


# ─────────────────────────────────────────
# SOLUCIONADOR CON FORWARD CHECKING
# ─────────────────────────────────────────

def resolver_forward_checking(tablero, n, dominios=None):
    # Intenta resolver el tablero usando backtracking con comprobacion
    # hacia adelante. En cada paso selecciona la primera celda vacia,
    # prueba cada valor de su dominio actual, y antes de continuar
    # verifica que ninguna celda vecina haya quedado sin valores posibles.
    # Si detecta que una rama no puede llevar a solucion, retrocede
    # de inmediato sin explorar ese camino, lo que reduce drasticamente
    # el numero de estados que hay que evaluar comparado con backtracking.
    # Retorna True si encontro una solucion, False si no existe solucion.
    # La solucion queda almacenada directamente en el tablero recibido.

    # En la primera llamada se inicializan los dominios desde cero
    if dominios is None:
        dominios = inicializar_dominios(tablero, n)

    celda = encontrar_celda_vacia(tablero, n)

    if celda is None:
        # No hay mas celdas vacias, el tablero esta completamente resuelto
        return True

    fila, col = celda

    for num in dominios.get((fila, col), []):

        if es_valido(tablero, n, fila, col, num):
            tablero[fila][col] = num

            # Se actualizan los dominios de las celdas vecinas
            nuevos_dominios = comprobacion_hacia_adelante(dominios, fila, col, num, n)

            if nuevos_dominios is not None:
                # Se elimina la celda actual de los dominios porque ya fue asignada
                nuevos_dominios.pop((fila, col), None)

                if resolver_forward_checking(tablero, n, nuevos_dominios):
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
    print(" SOLUCIONADOR CON FORWARD CHECKING")
    print("─" * 45)

    ruta = "ejemplos/sudoku_9x9.txt"
    tablero, n = leer_tablero(ruta)

    print(f"─" * 45)
    print(f"Tablero inicial ({n}x{n}):")
    imprimir_tablero(tablero, n)

    inicio = time.time()
    resuelto = resolver_forward_checking(tablero, n)
    fin = time.time()

    if resuelto:
        print("─" * 45)
        print("Tablero resuelto:")
        imprimir_tablero(tablero, n)
    else:
        print("─" * 45)
        print("No se encontro solucion.")

    print("─" * 45)
    print(f"Tiempo de ejecucion: {fin - inicio:.4f} segundos")
    print("─" * 45)