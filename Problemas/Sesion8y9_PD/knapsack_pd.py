from typing import *
import sys

# ---------------------------------------------------------------------------
# TIPOS DEL PROGRAMA

Score    = int                                  # Entero con el valor de la mochila
Decision = int                                  # Dos posibles decisiones: 0 o 1
Solution = Tuple[Score, Optional[List[Decision]]]

# Tipos para el diccionario mem:
SParams = Tuple[int, int]                   # Parámetros de S: (c:int, n: int)
Mem     = Dict[SParams, Score]                           # Sin rec. de camino
MemPath = Dict[SParams, Tuple[Score, SParams, Decision]] # Con rec. de camino

# ---------------------------------------------------------------------------

# Salida: (Capacity, values, weights)
def read_data(f) -> Tuple[int, List[int], List[int]]:
    capacity = int(f.readline())
    v = []
    w = []
    for line in f.readlines():
        vv, ww = line.strip().split()
        v.append(int(vv))
        w.append(int(ww))
    return capacity, v, w

# Salida: (score, decisiones)
def process(impl: int, C: int, v: List[int], w: List[int]) -> Solution:
    if impl == 0:
        return knapsack_direct(w, v, C)
    elif impl == 1:
        return knapsack_memo(w, v, C)
    elif impl == 2:
        return knapsack_memo_path(w, v, C)
    elif impl == 3:
        return knapsack_iter(w, v, C)
    elif impl == 4:
        return knapsack_iter_red(w, v, C)

def show_results(score: Score, decisions: Optional[List[int]]):
    print(score)
    if decisions is not None:
        for d in decisions:
            print(d)

# --------------------------------------------------------------------------

# Versión recursiva directa
def knapsack_direct(w: List[int], v: List[int], C: int) -> Solution:
    def S(c: int, n: int) -> Score:
        if n == 0:
            return 0
        if n > 0 and w[n-1] <= c:
            return max( S(c, n-1), S(c-w[n-1], n-1) + v[n-1] )
        if n > 0 and w[n-1] > c:
            return S(c, n-1)
    # TODO: IMPLEMENTAR
    return S(C, len(v)), None

# Versión recursiva con memoización
def knapsack_memo(w: List[int], v: List[int], C: int) -> Solution:
    def S(c: int, n: int) -> Score:
        if n == 0:
            return 0
        if (c, n) not in mem:
            if n > 0 and w[n - 1] <= c:
                mem[c, n] = max(S(c, n - 1), S(c - w[n - 1], n - 1) + v[n - 1])
            if n > 0 and w[n - 1] > c:
                mem[c, n] = S(c, n - 1)
        return mem[c, n]

    mem: Dict[SParams, Score] = {}
    # TODO: IMPLEMENTAR
    return S(C, len(v)), None

# Versión recursiva con memoización y recuperación de camino
def knapsack_memo_path(w: List[int], v: List[int], C: int) -> Solution:
    def S(c: int, n: int) -> Score:
        if n == 0:
            return 0
        if (c, n) not in mem:
            if w[n - 1] <= c:
                mem[c, n] = max((S(c, n-1), (c, n-1), 0), (S(c-w[n-1], n-1) + v[n-1], (c-w[n-1], n-1), 1))
            else:
                mem[c, n] = (S(c, n - 1), (c, n-1), 0)
        return mem[c, n][0]

    mem: Dict[SParams, Tuple[Score, SParams, Decision]] = {}
    # Recuperar el camino
    score = S(C, len(v))
    c, n = C, len(v)
    decisions = []
    while n > 0:
        _, (c, n), d = mem[c, n] # La _ es porque los programadores de python han acordado que cuando se pone eso significa que esa variable no se usa
        decisions.append(d)
    decisions.reverse()
    # TODO: IMPLEMENTAR
    return score, decisions

# Versión iterativa con recuperación de camino
def knapsack_iter(w: List[int], v: List[int], C: int) -> Solution:
    mem: Dict[SParams, Tuple, SParams, Decision] = {}
    N = len(v)
    # Rellenamos la fila n = 0
    for c in range(0, C + 1):
        mem[c, 0] = (0, (-1, -1), -1)
    # Rellenamos filas de n = 1 a n = N
    for n in range(1, N + 1):
        for c in range(0, C + 1):
            if (c, n) not in mem:
                if w[n - 1] <= c:
                    mem[c, n] = max((mem[c, n - 1][0], (c, n - 1), 0),
                                    (mem[c - w[n - 1], n - 1][0] + v[n - 1], (c - w[n - 1], n - 1), 1))
                else:
                    mem[c, n] = (mem[c, n - 1][0], (c, n - 1), 0)

    # Recuperar el camino
    score = mem[C, len(v)][0]
    c, n = C, len(v)
    decisions = []
    while n > 0:
        _, (c, n), d = mem[
            c, n]  # La _ es porque los programadores de python han acordado que cuando se pone eso significa que esa variable no se usa
        decisions.append(d)
    decisions.reverse()
    # TODO: IMPLEMENTAR
    return score, decisions

# Versión iterativa con reduccion del coste espacial
def knapsack_iter_red(w: List[int], v: List[int], C: int) -> Solution:
    N = len(v)
    current: List[Score] = [0] * (C + 1)
    previous: List[Score] = [0] * (C + 1)

    for n in range(1, N + 1):
        current, previous = previous, current
        for c in range(0, C + 1):
            if w[n - 1] <= c:
                current[c] = max(previous[c], previous[c - w[n - 1]] + v[n - 1])
            else:
                current[c] = previous[c]
    return None

# PROGRAMA PRINCIPAL -------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) == 1:
        implementacion = 0
    else:
        implementacion = int(sys.argv[1])

    capacidad, valores, pesos = read_data(sys.stdin)
    puntuacion, decisiones = process(implementacion, capacidad, valores, pesos)
    show_results(puntuacion, decisiones)
