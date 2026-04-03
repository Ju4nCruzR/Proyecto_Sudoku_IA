# sudoku.py
# Archivo principal del proyecto. Se encarga de cargar un tablero de sudoku
# y ejecutar los cuatro algoritmos de solucion sobre el mismo tablero,
# midiendo y comparando el tiempo de ejecucion de cada uno.
# Cada algoritmo tiene un limite de 60 segundos para encontrar la solucion.
# Si se supera ese limite, el algoritmo se cancela y se reporta como
# tiempo limite excedido, lo que permite comparar todos los algoritmos
# sin que el programa quede bloqueado indefinidamente.
# Este archivo es el punto de entrada del proyecto y el que se debe ejecutar
# para ver la comparacion completa de los algoritmos implementados.

import time
import sys
import signal
from tablero import leer_tablero, imprimir_tablero, copiar_tablero


# ─────────────────────────────────────────
# IMPORTACION DE ALGORITMOS
# ─────────────────────────────────────────

from fuerza_bruta      import resolver_fuerza_bruta
from backtracking      import resolver_backtracking
from forward_checking  import resolver_forward_checking
from mrv               import resolver_mrv


# ─────────────────────────────────────────
# LIMITE DE TIEMPO
# ─────────────────────────────────────────

LIMITE_SEGUNDOS = 60

# Se define una excepcion personalizada para identificar cuando un algoritmo
# supera el tiempo limite. Esto permite distinguirla de otros errores.
class TiempoExcedido(Exception):
    pass


def manejador_timeout(signum, frame):
    # Esta funcion se ejecuta automaticamente cuando se agota el tiempo
    # limite asignado a un algoritmo. Lanza la excepcion TiempoExcedido
    # para interrumpir la ejecucion del algoritmo de forma controlada.
    raise TiempoExcedido()


# ─────────────────────────────────────────
# EJECUCION DE UN ALGORITMO
# ─────────────────────────────────────────

def ejecutar_algoritmo(nombre, funcion, tablero, n):
    # Ejecuta un algoritmo de solucion sobre una copia del tablero original,
    # mide su tiempo de ejecucion e imprime el resultado en pantalla.
    # Si el algoritmo supera el limite de tiempo definido en LIMITE_SEGUNDOS,
    # se interrumpe y se reporta como tiempo limite excedido.
    # Se trabaja siempre sobre una copia para que cada algoritmo parta
    # del mismo tablero inicial sin verse afectado por los demas.
    # Retorna el tiempo transcurrido y un booleano indicando si resolvio.

    print(f"\n{'─' * 45}")
    print(f" {nombre}")
    print(f"{'─' * 45}")

    copia = copiar_tablero(tablero)
    resuelto = False
    tiempo = None
    excedio_limite = False

    # signal.SIGALRM solo funciona en sistemas Unix/Linux/Mac.
    # En Windows se usa un enfoque alternativo con threading.
    usar_signal = hasattr(signal, 'SIGALRM')

    if usar_signal:
        # En sistemas Unix se usa SIGALRM para interrumpir el algoritmo
        signal.signal(signal.SIGALRM, manejador_timeout)
        signal.alarm(LIMITE_SEGUNDOS)

    inicio = time.time()

    try:
        if usar_signal:
            resuelto = funcion(copia, n)
        else:
            # En Windows se ejecuta el algoritmo en un hilo separado
            # y se espera como maximo LIMITE_SEGUNDOS segundos
            import threading

            resultado = [False]

            def ejecutar():
                resultado[0] = funcion(copia, n)

            hilo = threading.Thread(target=ejecutar)
            hilo.daemon = True
            hilo.start()
            hilo.join(timeout=LIMITE_SEGUNDOS)

            if hilo.is_alive():
                # El hilo sigue corriendo, significa que excedio el limite
                raise TiempoExcedido()

            resuelto = resultado[0]

    except TiempoExcedido:
        excedio_limite = True

    finally:
        fin = time.time()
        tiempo = fin - inicio
        if usar_signal:
            signal.alarm(0)

    if excedio_limite:
        print(f"\n  Tiempo limite de {LIMITE_SEGUNDOS} segundos excedido.")
        print(f"  Este algoritmo no es viable para tableros de {n}x{n}.")
    elif resuelto:
        print(f"\nTablero resuelto:")
        imprimir_tablero(copia, n)
    else:
        print("\nNo se encontro solucion para este tablero.")

    print(f"\nTiempo de ejecucion: {tiempo:.4f} segundos")

    return tiempo, resuelto, excedio_limite


# ─────────────────────────────────────────
# COMPARACION DE ALGORITMOS
# ─────────────────────────────────────────

def comparar_algoritmos(tablero, n):
    # Ejecuta los cuatro algoritmos en orden de menor a mayor sofisticacion
    # y al final presenta una tabla comparativa de tiempos de ejecucion.
    # El orden de ejecucion es: fuerza bruta, backtracking, forward checking
    # y MRV. Esto permite ver de forma progresiva como cada mejora impacta
    # en el rendimiento del solucionador.

    algoritmos = [
        ("FUERZA BRUTA",      resolver_fuerza_bruta),
        ("BACKTRACKING",      resolver_backtracking),
        ("FORWARD CHECKING",  resolver_forward_checking),
        ("MRV",               resolver_mrv),
    ]

    resultados = {}

    for nombre, funcion in algoritmos:
        tiempo, resuelto, excedio = ejecutar_algoritmo(nombre, funcion, tablero, n)
        resultados[nombre] = {
            "tiempo":  tiempo,
            "resuelto": resuelto,
            "excedio":  excedio
        }

    # Se imprime la tabla comparativa al final
    print(f"\n{'═' * 45}")
    print(f" RESUMEN COMPARATIVO DE TIEMPOS ({n}x{n})")
    print(f"{'═' * 45}")
    print(f"  {'Algoritmo':<22} {'Tiempo (s)':>10}  {'Estado':>10}")
    print(f"  {'─' * 44}")

    for nombre, datos in resultados.items():
        if datos["excedio"]:
            estado = "EXCEDIDO"
        elif datos["resuelto"]:
            estado = "RESUELTO"
        else:
            estado = "SIN SOL."

        print(f"  {nombre:<22} {datos['tiempo']:>10.4f}  {estado:>10}")

    print(f"{'═' * 45}")

    # Se identifica el algoritmo mas rapido entre los que si resolvieron
    resueltos = {k: v for k, v in resultados.items() if v["resuelto"]}

    if resueltos:
        mejor = min(resueltos, key=lambda k: resueltos[k]["tiempo"])
        print(f"\n  El algoritmo mas rapido fue: {mejor}")

    print(f"{'═' * 45}\n")


# ─────────────────────────────────────────
# PUNTO DE ENTRADA
# ─────────────────────────────────────────

if __name__ == "__main__":
    # Si se pasa una ruta como argumento desde la consola, se usa esa ruta.
    # De lo contrario se usa el tablero de 9x9 por defecto.
    # Ejemplo de uso con argumento:
    #   python sudoku.py ejemplos/sudoku_16x16.txt

    if len(sys.argv) > 1:
        ruta = sys.argv[1]
    else:
        ruta = "ejemplos/sudoku_9x9.txt"

    print(f"\n{'═' * 45}")
    print(f" PROYECTO SUDOKU - COMPARACION DE ALGORITMOS")
    print(f"{'═' * 45}")
    print(f"\nCargando tablero desde: {ruta}")

    tablero, n = leer_tablero(ruta)

    print(f"\nTablero inicial ({n}x{n}):")
    imprimir_tablero(tablero, n)

    comparar_algoritmos(tablero, n)