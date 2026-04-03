# backtracking.py
# Modulo que implementa la segunda estrategia de solucion para el Sudoku:
# backtracking basico. A diferencia de la fuerza bruta, este algoritmo
# aplica las restricciones del sudoku en cada asignacion para descartar
# valores invalidos antes de seguir explorando. Esto reduce significativamente
# el espacio de busqueda, aunque sin anticiparse a problemas futuros.
# El camino hacia la solucion no importa, solo el estado final del tablero.

import math
from tablero import es_valido, copiar_tablero


# ─────────────────────────────────────────
# BUSQUEDA DE CELDA VACIA
# ─────────────────────────────────────────

def encontrar_celda_vacia(tablero, n):
    # Recorre el tablero de izquierda a derecha y de arriba a abajo
    # buscando la primera celda que contenga un cero, lo que indica
    # que esa celda aun no tiene un valor asignado.
    # Retorna una tupla (fila, col) con la posicion encontrada,
    # o None si no hay celdas vacias, lo que significa que el tablero
    # esta completamente resuelto.

    for fila in range(n):
        for col in range(n):
            if tablero[fila][col] == 0:
                return (fila, col)
    return None


# ─────────────────────────────────────────
# SOLUCIONADOR POR BACKTRACKING BASICO
# ─────────────────────────────────────────

def resolver_backtracking(tablero, n):
    # Intenta resolver el tablero usando backtracking basico.
    # El algoritmo selecciona la primera celda vacia disponible y prueba
    # cada valor del 1 al n. Antes de asignar un valor verifica que no
    # viole ninguna restriccion del sudoku en ese momento. Si encuentra
    # un valor valido lo asigna y avanza recursivamente a la siguiente
    # celda. Si ningun valor es valido en una celda, retrocede a la
    # celda anterior y prueba el siguiente valor disponible.
    # La diferencia clave con fuerza bruta es que aqui se descartan
    # valores invalidos de inmediato, sin necesidad de explorar todos
    # los caminos posibles que parten de una asignacion incorrecta.
    # Retorna True si encontro una solucion, False si no existe solucion.
    # La solucion queda almacenada directamente en el tablero recibido.

    celda = encontrar_celda_vacia(tablero, n)

    if celda is None:
        # No hay mas celdas vacias, el tablero esta completamente resuelto
        return True

    fila, col = celda

    for num in range(1, n + 1):

        # Solo se asigna el valor si no viola ninguna restriccion actual
        if es_valido(tablero, n, fila, col, num):
            tablero[fila][col] = num

            if resolver_backtracking(tablero, n):
                return True

            # Si la asignacion no llevo a una solucion, se deshace
            tablero[fila][col] = 0

    # Ningun valor fue valido para esta celda, se retrocede
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
    print(" SOLUCIONADOR POR BACKTRACKING BASICO")
    print("─" * 45)

    ruta = "ejemplos/sudoku_9x9.txt"
    tablero, n = leer_tablero(ruta)

    print("─" * 45)
    print(f"Tablero inicial ({n}x{n}):")
    imprimir_tablero(tablero, n)

    inicio = time.time()
    resuelto = resolver_backtracking(tablero, n)
    fin = time.time()

    if resuelto:
        print("─" * 45)
        print("Tablero resuelto:")
        imprimir_tablero(tablero, n)
    else:
        print("─" * 45)
        print("No se encontro solucion.")

    print(f"─" * 45)
    print(f"Tiempo de ejecucion: {fin - inicio:.4f} segundos")
    print("─" * 45)