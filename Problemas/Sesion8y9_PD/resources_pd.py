from typing import *
import sys

infinity = float('infinity')

# ---------------------------------------------------------------------------
# TIPOS DEL PROGRAMA

Score    = Union[int, float]                # Entero con el beneficio obtenido
Decision = int                              # Dos posibles decisiones: 0 o 1
Solution = Tuple[Score, Optional[List[Decision]]]

# Tipos para el diccionario mem:
SParams = Tuple[int, int]                   # Parámetros de S: (u:int, n: int)
Mem     = Dict[SParams, Score]                           # Sin rec. de camino
MemPath = Dict[SParams, Tuple[Score, SParams, Decision]] # Con rec. de camino

# ------------------------------------------------------------------------------

# Salida: (Capacity, values, weights)
def read_data(f) -> Tuple[int, List[int], List[List[int]]]:
    u = int(f.readline())
    n = int(f.readline())
    m = [int(w) for w in f.readline().strip().split()]
    v = []
    for line in f.readlines():
        v.append([int(w) for w in line.strip().split()])
    return u, m, v

def process(impl: int, u: int, m: List[int], v: List[List[int]]) -> Solution:
    if impl == 0:
        return resources_direct(v, m, u)
    elif impl == 1:
        return resources_memo(v, m, u)
    elif impl == 2:
        return resources_memo_path(v, m, u)
    elif impl == 3:
        return resources_iter(v, m, u)
    elif impl == 4:
        return resources_iter_red(v, m, u)

def show_results(value: Score, decisions: Optional[List[Decision]]):
    print(value)
    if decisions is not None:
        for d in decisions:
            print(d)

# ---------------------------------------------------------------------------

# Versión recursiva directa
def resources_direct(v: List[List[int]], m: List[int], U: int) -> Solution:
    def S(u: int, n: int) -> Score:
        if n == 0:
            return 0
        if n > 0:
            mejor = -infinity
            for d in range(min(m[n-1], U)):
                mejor =  max(mejor, S(u - d, n - 1) + v[n - 1][d])
            return mejor

    # TODO: IMPLEMENTAR
    return S(U, len(m)), None

# Versión recursiva con memoización
def resources_memo(v: List[List[int]], m: List[int], U: int) -> Solution:
    def S(u: int, n: int) -> Score:
        if n == 0:
            return 0
        if(u, n) not in mem:
            if n > 0:
                mejor = -infinity
                for d in range(min(m[n-1], U)):
                    mejor = max(mejor, S(u - d, n - 1) + v[n - 1][d])
                mem[u, n] = mejor
                return mem[u, n]

    mem: Dict[SParams, Score] = {}
    return S(U, len(m)), None

# Versión recursiva con memoización y recuperación de camino
def resources_memo_path(v: List[List[int]], m: List[int], U: int) -> Solution:
    def S(u: int, n: int) -> Score:
        if n == 0:
            return 0
        if(u, n) not in mem:
            if n > 0:
                mem[u, n] = -infinity, (-1,-1), -1
                for d in range(min(m[n-1], U)):
                    mem[u, n] = max(mem[u,n], (S(u - d, n - 1) + v[n - 1][d], (u-d, n-1), d ))
                return mem[u, n][0]

    mem: Dict[SParams, Tuple[Score, SParams, Decision]] = {}
    # Recuperar el camino
    score = S(U, len(m))
    u, n = U, len(m)
    decisions = []
    while n > 0:
        _, (u, n), d = mem[u, n]  # La _ es porque los programadores de python han acordado que cuando se pone eso significa que esa variable no se usa
        decisions.append(d)
    decisions.reverse()
    # TODO: IMPLEMENTAR
    return score, decisions

# Versión iterativa con recuperación de camino
def resources_iter(v: List[List[int]], m: List[int], U: int) -> Solution:
    # TODO: IMPLEMENTAR rellenar tabla mem
    # TODO: IMPLEMENTAR recuperación de camino en sol
    pass

# Versión iterativa con reduccion del coste espacial
def resources_iter_red(v: Dict[Tuple[int, int], int], m: List[int], U: int) -> Solution:
    # TODO: IMPLEMENTAR usar dos columnas hasta rellenar la última de la tabla
    pass

# PROGRAMA PRINCIPAL -------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) == 1:
        implementacion = 0
    else:
        implementacion = int(sys.argv[1])

    u, m, v = read_data(sys.stdin)
    puntuacion, decisiones = process(implementacion, u, m, v)
    show_results(puntuacion, decisiones)
