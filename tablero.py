# tablero.py
# Modulo principal de manejo de tableros para el solucionador de Sudoku.
# Se encarga de leer, cargar, imprimir, validar y copiar tableros de cualquier
# tamano n x n, siempre que n sea un cuadrado perfecto (4, 9, 16, etc.).
# Este modulo es importado por todos los demas modulos del proyecto.

import math


# ─────────────────────────────────────────
# LECTURA DESDE ARCHIVO .txt
# ─────────────────────────────────────────

def leer_tablero(ruta):
    # Lee un tablero de sudoku desde un archivo .txt y lo convierte en una
    # lista de listas de enteros. Cada fila del archivo corresponde a una fila
    # del tablero, y los valores deben estar separados por espacios.
    # Los ceros representan celdas vacias.
    # Retorna el tablero como lista de listas y el tamano n.

    tablero = []

    with open(ruta, 'r') as archivo:
        for linea in archivo:
            linea = linea.strip()
            if linea:
                fila = list(map(int, linea.split()))
                tablero.append(fila)

    n = len(tablero)

    # Se verifica que todas las filas tengan exactamente n columnas
    for i, fila in enumerate(tablero):
        if len(fila) != n:
            raise ValueError(
                f"La fila {i} tiene {len(fila)} columnas pero se esperaban {n}."
            )

    # Se verifica que n sea un cuadrado perfecto para poder formar subcuadriculas
    raiz = math.isqrt(n)
    if raiz * raiz != n:
        raise ValueError(
            f"El tamano {n}x{n} no es valido. n debe ser un cuadrado perfecto como 4, 9 o 16."
        )

    return tablero, n


# ─────────────────────────────────────────
# LECTURA DESDE VARIABLE (para pruebas rapidas)
# ─────────────────────────────────────────

def cargar_tablero(matriz):
    # Carga un tablero que ya esta definido como lista de listas dentro del codigo.
    # Util para hacer pruebas rapidas sin necesidad de leer un archivo externo.
    # Hace una copia del tablero recibido para no modificar el original.
    # Retorna el tablero copiado y el tamano n.

    n = len(matriz)

    raiz = math.isqrt(n)
    if raiz * raiz != n:
        raise ValueError(
            f"El tamano {n}x{n} no es valido. n debe ser un cuadrado perfecto como 4, 9 o 16."
        )

    # Se copia fila por fila para evitar referencias compartidas
    return [fila[:] for fila in matriz], n


# ─────────────────────────────────────────
# IMPRESION DEL TABLERO
# ─────────────────────────────────────────

def imprimir_tablero(tablero, n):
    # Imprime el tablero en consola con separadores visuales entre subcuadriculas.
    # Los numeros se alinean automaticamente segun el tamano del tablero.
    # Las celdas vacias se muestran con puntos en lugar de ceros para facilitar
    # la lectura visual del tablero.

    raiz = math.isqrt(n)

    # La cantidad de digitos necesarios depende del valor maximo posible, que es n
    digitos = len(str(n))
    ancho_celda = digitos + 1
    ancho_bloque = ancho_celda * raiz + 1

    separador = "+" + (("-" * ancho_bloque) + "+") * raiz

    for i in range(n):
        # Se imprime el separador horizontal al inicio de cada bloque de filas
        if i % raiz == 0:
            print(separador)

        fila_str = "|"
        for j in range(n):
            # Se imprime el separador vertical entre bloques de columnas
            if j % raiz == 0 and j != 0:
                fila_str += "|"

            valor = tablero[i][j]

            if valor == 0:
                # Las celdas vacias se representan con puntos
                fila_str += " " + "." * digitos
            else:
                fila_str += f" {valor:{digitos}d}"

        fila_str += " |"
        print(fila_str)

    print(separador)


# ─────────────────────────────────────────
# VALIDACION DE TABLERO
# ─────────────────────────────────────────

def es_valido(tablero, n, fila, col, num):
    # Verifica si es posible colocar el numero num en la posicion (fila, col)
    # sin violar ninguna de las tres restricciones del sudoku:
    # 1. El numero no puede repetirse en la misma fila.
    # 2. El numero no puede repetirse en la misma columna.
    # 3. El numero no puede repetirse dentro de la misma subcuadricula.
    # Retorna True si la asignacion es valida, False si no lo es.

    raiz = math.isqrt(n)

    # Restriccion de fila: el numero no debe aparecer en ninguna columna de esa fila
    if num in tablero[fila]:
        return False

    # Restriccion de columna: el numero no debe aparecer en ninguna fila de esa columna
    if num in [tablero[i][col] for i in range(n)]:
        return False

    # Restriccion de subcuadricula: se calcula la esquina superior izquierda del bloque
    # al que pertenece la celda (fila, col) y se revisa todo ese bloque
    fila_inicio = (fila // raiz) * raiz
    col_inicio  = (col  // raiz) * raiz

    for i in range(fila_inicio, fila_inicio + raiz):
        for j in range(col_inicio, col_inicio + raiz):
            if tablero[i][j] == num:
                return False

    return True


# ─────────────────────────────────────────
# COPIA DEL TABLERO
# ─────────────────────────────────────────

def copiar_tablero(tablero):
    # Retorna una copia completamente independiente del tablero recibido.
    # Esto es necesario para que los algoritmos puedan explorar caminos distintos
    # sin que los cambios en uno afecten al otro.

    return [fila[:] for fila in tablero]