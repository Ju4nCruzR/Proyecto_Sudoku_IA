# Proyecto Sudoku - Satisfacción de Restricciones (CSP)

Proyecto Aplicativo 2 de la asignatura Introducción a la Inteligencia Artificial.
Pontificia Universidad Javeriana - 2026.

El objetivo del proyecto es resolver tableros de Sudoku de tamaño n×n implementando
y comparando cuatro estrategias distintas, desde la más básica hasta la más eficiente,
todas enmarcadas dentro de la teoría de problemas de satisfacción de restricciones (CSP).

---

## Estructura del proyecto

Proyecto_Sudoku_IA/
│
├── sudoku.py              <- Archivo principal. Ejecuta y compara los cuatro algoritmos.
├── tablero.py             <- Lectura, impresión, validación y copia de tableros.
├── fuerza_bruta.py        <- Solución 1: fuerza bruta.
├── backtracking.py        <- Solución 2: backtracking básico.
├── forward_checking.py    <- Solución 3: backtracking con forward checking.
├── mrv.py                 <- Solución 4: backtracking con forward checking y MRV.
├── .gitignore
│
└── ejemplos/
├── generador.py       <- Genera tableros de prueba y los guarda como archivos .txt.
├── sudoku_4x4.txt
├── sudoku_9x9.txt
└── sudoku_16x16.txt

---

## Algoritmos implementados

### Solución 1 - Fuerza Bruta
Prueba todas las combinaciones posibles de números en las celdas vacías sin aplicar
ninguna estrategia de descarte. Es el método más simple pero completamente inviable
para tableros grandes debido a la explosión combinatoria del espacio de búsqueda.

### Solución 2 - Backtracking Básico
Aplica las restricciones del sudoku en cada asignación para descartar valores inválidos
de inmediato. Reduce significativamente el espacio de búsqueda respecto a la fuerza bruta,
pero no se anticipa a problemas futuros, por lo que puede explorar muchos caminos
que inevitablemente fallarán.

### Solución 3 - Backtracking con Forward Checking
Mantiene un registro de los valores posibles (dominio) para cada celda vacía. Cada vez
que se asigna un valor, elimina ese valor de los dominios de las celdas vecinas. Si el
dominio de alguna celda queda vacío, retrocede de inmediato sin seguir explorando esa
rama. Esto lo hace considerablemente más eficiente que el backtracking básico.

### Solución 4 - Backtracking con Forward Checking y MRV
Extiende el forward checking con la heurística MRV (Minimum Remaining Values): en lugar
de elegir siempre la primera celda vacía disponible, selecciona la celda cuyo dominio
tenga la menor cantidad de valores posibles. Atacar primero las celdas más restringidas
reduce el factor de ramificación del árbol de búsqueda y detecta conflictos mucho antes,
logrando una mejora drástica en rendimiento respecto a todos los métodos anteriores.

---

## Resultados comparativos

Los siguientes tiempos se obtuvieron resolviendo el mismo tablero de 16×16
con 136 celdas vacías en la misma máquina:

| Algoritmo        | Tiempo (s) | Estado   |
|------------------|------------|----------|
| Fuerza Bruta     | 18.5062    | Resuelto |
| Backtracking     | 18.5964    | Resuelto |
| Forward Checking |  2.8021    | Resuelto |
| MRV              |  0.0190    | Resuelto |

MRV resuelve el tablero casi 1000 veces más rápido que fuerza bruta.
En tableros con más celdas vacías, fuerza bruta y backtracking superan
el límite de tiempo de 60 segundos, mientras que MRV mantiene tiempos
de respuesta muy bajos.

---

## Cómo ejecutar el proyecto

### Generar tableros de ejemplo
```bash
python ejemplos/generador.py
```

### Resolver con comparación de los cuatro algoritmos
```bash
# Tablero 9x9 (por defecto)
python sudoku.py

# Tablero específico
python sudoku.py ejemplos/sudoku_16x16.txt
python sudoku.py ejemplos/sudoku_4x4.txt
```

### Probar un algoritmo individualmente
```bash
python fuerza_bruta.py
python backtracking.py
python forward_checking.py
python mrv.py
```

---

## Requisitos

- Python 3.8 o superior
- No requiere librerías externas

---

## Autores

Proyecto desarrollado por estudiantes de Ingeniería de Sistemas
Juan Diego Soler
Juan Sebastián Cruz 
Santiago Andrés Rayo
Pontificia Universidad Javeriana - Bogotá
Asignatura: Introducción a la Inteligencia Artificial
Profesor: Ing. Julio Omar Palacio Niño, M.Sc.