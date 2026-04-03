# fuerza_bruta.py
# Modulo que implementa la primera estrategia de solucion para el Sudoku:
# fuerza bruta pura. Este enfoque prueba todas las combinaciones posibles
# de numeros en las celdas vacias sin aplicar ninguna logica de poda.
# Es el metodo mas simple conceptualmente pero el mas ineficiente en la
# practica, especialmente para tableros grandes como el de 16x16.
# Se incluye principalmente como punto de referencia para comparar su
# rendimiento contra los metodos mas inteligentes del proyecto.

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
    # esta completamente lleno.

    for fila in range(n):
        for col in range(n):
            if tablero[fila][col] == 0:
                return (fila, col)
    return None


# ─────────────────────────────────────────
# SOLUCIONADOR POR FUERZA BRUTA
# ─────────────────────────────────────────

def resolver_fuerza_bruta(tablero, n):
    # Intenta resolver el tablero de sudoku probando todos los valores
    # posibles en cada celda vacia, de forma recursiva.
    # Para cada celda vacia, prueba los numeros del 1 al n en orden.
    # Si un numero no viola ninguna restriccion en ese momento, lo coloca
    # y avanza a la siguiente celda vacia. Si en algun punto no hay valor
    # valido para una celda, retrocede y prueba el siguiente numero en la
    # celda anterior. A diferencia del backtracking clasico, este metodo
    # no aplica ninguna estrategia adicional para reducir el espacio de
    # busqueda, lo que lo hace mucho mas lento.
    # Retorna True si encontro una solucion, False si no existe solucion.
    # La solucion queda almacenada directamente en el tablero recibido.

    celda = encontrar_celda_vacia(tablero, n)

    if celda is None:
        # No hay mas celdas vacias, el tablero esta completamente resuelto
        return True

    fila, col = celda

    # Se prueban todos los numeros posibles del 1 al n en orden estricto
    # sin ninguna priorizacion ni descarte inteligente
    for num in range(1, n + 1):

        if es_valido(tablero, n, fila, col, num):
            # Se asigna el numero si no viola restricciones en este momento
            tablero[fila][col] = num

            if resolver_fuerza_bruta(tablero, n):
                return True

            # Si la asignacion no llevo a una solucion, se deshace
            tablero[fila][col] = 0

    # Ningun numero funciono en esta celda, se retrocede
    return False


# ─────────────────────────────────────────
# PUNTO DE ENTRADA PARA PRUEBAS
# ─────────────────────────────────────────

if __name__ == "__main__":
    # Este bloque permite probar el modulo directamente desde la consola
    # usando el tablero de ejemplo del enunciado del proyecto.
    # Al importar este modulo desde sudoku.py, este bloque no se ejecuta.
 
    import time
    from tablero import leer_tablero, imprimir_tablero

    print("─" * 45)
    print("SOLUCIONADOR POR FUERZA BRUTA")
    print("─" * 45)

    ruta = "ejemplos/sudoku_9x9.txt"
    tablero, n = leer_tablero(ruta)

    print("─" * 45)
    print(f"Tablero inicial ({n}x{n}):")
    imprimir_tablero(tablero, n)

    inicio = time.time()
    resuelto = resolver_fuerza_bruta(tablero, n)
    fin = time.time()

    if resuelto:
        print("─" * 45)
        print("Tablero resuelto:")
        imprimir_tablero(tablero, n)
    else:
        print("No se encontro solucion.")

    print("─" * 45)
    print(f"Tiempo de ejecucion: {fin - inicio:.4f} segundos")
    print("─" * 45)