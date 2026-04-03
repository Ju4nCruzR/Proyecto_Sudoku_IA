# generador.py
# Modulo encargado de generar tableros de Sudoku de diferentes tamanos y
# guardarlos como archivos .txt en la carpeta ejemplos.
# Los tableros generados sirven como casos de prueba para los algoritmos
# del proyecto. Se generan tableros de 4x4, 9x9 y 16x16.
# Los ceros representan celdas vacias en el tablero.

import random
import math
import os


# ─────────────────────────────────────────
# VERIFICACION DE RESTRICCIONES
# ─────────────────────────────────────────

def es_valido_generador(tablero, n, fila, col, num):
    # Verifica si colocar num en la posicion (fila, col) es valido
    # segun las tres restricciones del sudoku: fila, columna y subcuadricula.
    # Esta funcion es identica en logica a la de tablero.py pero se define
    # aqui de forma independiente para que generador.py no dependa de otros
    # modulos del proyecto.

    raiz = math.isqrt(n)

    # Restriccion de fila
    if num in tablero[fila]:
        return False

    # Restriccion de columna
    if num in [tablero[i][col] for i in range(n)]:
        return False

    # Restriccion de subcuadricula
    fila_inicio = (fila // raiz) * raiz
    col_inicio  = (col  // raiz) * raiz

    for i in range(fila_inicio, fila_inicio + raiz):
        for j in range(col_inicio, col_inicio + raiz):
            if tablero[i][j] == num:
                return False

    return True


# ─────────────────────────────────────────
# GENERACION DE TABLERO COMPLETO
# ─────────────────────────────────────────

def generar_tablero_completo(n):
    # Genera un tablero de sudoku completamente resuelto de tamano n x n.
    # Usa una estrategia de llenado por bloques: primero rellena la diagonal
    # principal de subcuadriculas (que son independientes entre si) con
    # numeros aleatorios validos, y luego resuelve el resto del tablero
    # con backtracking. Esto reduce drasticamente el espacio de busqueda
    # porque los bloques de la diagonal no se afectan entre si, permitiendo
    # llenarlos de forma independiente y rapida sin necesidad de validar
    # restricciones entre ellos en esa etapa inicial.

    import math
    raiz = math.isqrt(n)
    tablero = [[0] * n for _ in range(n)]

    # Paso 1: se rellenan los bloques de la diagonal principal de forma
    # independiente ya que no comparten fila ni columna entre si
    for bloque in range(raiz):
        inicio = bloque * raiz
        numeros = list(range(1, n + 1))
        random.shuffle(numeros)
        idx = 0
        for f in range(inicio, inicio + raiz):
            for c in range(inicio, inicio + raiz):
                tablero[f][c] = numeros[idx]
                idx += 1

    # Paso 2: se resuelve el resto del tablero con backtracking iterativo
    # usando una pila explícita en lugar de recursion para evitar errores
    # de profundidad maxima de pila en tableros grandes como el 16x16
    celdas_vacias = [
        (f, c) for f in range(n) for c in range(n) if tablero[f][c] == 0
    ]

    idx = 0
    intentos = {}

    while idx < len(celdas_vacias):
        f, c = celdas_vacias[idx]

        if (f, c) not in intentos:
            intentos[(f, c)] = list(range(1, n + 1))
            random.shuffle(intentos[(f, c)])

        encontrado = False
        while intentos[(f, c)]:
            num = intentos[(f, c)].pop(0)
            if es_valido_generador(tablero, n, f, c, num):
                tablero[f][c] = num
                encontrado = True
                break

        if encontrado:
            idx += 1
        else:
            # No hay valor valido, se retrocede a la celda anterior
            tablero[f][c] = 0
            del intentos[(f, c)]
            idx -= 1
            if idx < 0:
                # No se pudo generar el tablero, se intenta de nuevo
                tablero = [[0] * n for _ in range(n)]
                for bloque in range(raiz):
                    inicio = bloque * raiz
                    numeros = list(range(1, n + 1))
                    random.shuffle(numeros)
                    pos = 0
                    for fi in range(inicio, inicio + raiz):
                        for ci in range(inicio, inicio + raiz):
                            tablero[fi][ci] = numeros[pos]
                            pos += 1
                celdas_vacias = [
                    (fi, ci) for fi in range(n) for ci in range(n) if tablero[fi][ci] == 0
                ]
                idx = 0
                intentos = {}

    return tablero


# ─────────────────────────────────────────
# CREACION DEL TABLERO DE PRUEBA
# ─────────────────────────────────────────

def crear_tablero_prueba(n, celdas_visibles):
    # Toma un tablero completo y oculta algunas celdas convirtiendolas en ceros.
    # El parametro celdas_visibles indica cuantos numeros se dejan visibles.
    # Entre mas celdas visibles, mas facil es el tablero para el algoritmo.
    # Retorna el tablero con celdas ocultas listo para ser resuelto.

    tablero_completo = generar_tablero_completo(n)

    # Se copia el tablero completo para no modificar el original
    tablero_prueba = [fila[:] for fila in tablero_completo]

    total_celdas = n * n

    # Se calcula cuantas celdas hay que ocultar
    celdas_a_ocultar = total_celdas - celdas_visibles

    # Se elige aleatoriamente que posiciones se van a ocultar
    posiciones = random.sample(range(total_celdas), celdas_a_ocultar)

    for pos in posiciones:
        fila = pos // n
        col  = pos  % n
        tablero_prueba[fila][col] = 0

    return tablero_prueba


# ─────────────────────────────────────────
# GUARDADO DEL TABLERO EN ARCHIVO .txt
# ─────────────────────────────────────────

def guardar_tablero(tablero, n, nombre_archivo):
    # Guarda el tablero en un archivo .txt dentro de la carpeta ejemplos.
    # Cada fila del tablero se escribe en una linea del archivo con los
    # valores separados por espacios. Los ceros representan celdas vacias.

    # Se construye la ruta relativa hacia la carpeta ejemplos
    carpeta = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(carpeta, nombre_archivo)

    with open(ruta, 'w') as archivo:
        for fila in tablero:
            linea = " ".join(str(val) for val in fila)
            archivo.write(linea + "\n")

    print(f"Tablero {n}x{n} guardado en: {ruta}")


# ─────────────────────────────────────────
# GENERACION DE TODOS LOS EJEMPLOS
# ─────────────────────────────────────────

def generar_ejemplos():
    # Genera y guarda un tablero de prueba para cada tamano soportado.
    # La cantidad de celdas visibles se ajusta segun el tamano del tablero
    # para que los puzzles tengan una dificultad razonable en cada caso.

    configuraciones = [
        # (tamano, celdas_visibles, nombre_archivo)
        (4,  8,  "sudoku_4x4.txt"),
        (9,  30, "sudoku_9x9.txt"),
        (16, 180, "sudoku_16x16.txt"),
    ]

    for n, visibles, nombre in configuraciones:
        print(f"Generando tablero {n}x{n}...")
        tablero = crear_tablero_prueba(n, visibles)
        guardar_tablero(tablero, n, nombre)

    print("\nTodos los tableros de ejemplo fueron generados correctamente.")


# ─────────────────────────────────────────
# PUNTO DE ENTRADA
# ─────────────────────────────────────────

if __name__ == "__main__":
    # Este bloque solo se ejecuta cuando el archivo se corre directamente.
    # Al importarlo desde otro modulo, este bloque no se ejecuta.
    generar_ejemplos()