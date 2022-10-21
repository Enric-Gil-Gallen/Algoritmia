import sys
from typing import *

Score = int                 # El tipo de las puntuaciones
Decision = int              # Un índice de globo
Decisions = List[Decision]  # Lista con los índices de los globos explotados
Sparams = Tuple[int, int]   # Parametros de S: a:int, n:int

# ------------------------------------------------------------

# Salida: Una tupla con dos listas de enteros: (alturas de los globos, puntuaciones de los globos)
def read_data(f) -> Tuple[List[int], List[int]]:
    # Leemos las lineas
    lineas = f.readlines()
    # Llenameos la matriz
    alturas = []
    puntaciones = []
    for linea in lineas:
        l: str = linea.split()
        alturas.append(int(l[0]))
        puntaciones.append(int(l[1]))

    sol = alturas, puntaciones
    return sol


# Salida: Una tupla (puntuación, lista con los índices de los globos explotados)
def process(heights: List[int], scores: List[int]) -> Tuple[Score, Decisions]:
    maxheight = max(heights)
    heights.reverse()
    scores.reverse()

    def S(a: int, n: int) -> Score:
        if n == 0:
            return 0
        if (a, n) not in mem:
            if n > 0 and heights[n-1] <= a:
                mem[a, n] = max((S(a, n-1), (a, n-1), 0), (S(heights[n-1], n-1) + scores[n-1], (heights[n-1], n-1), 1))

            if n > 0 and heights[n-1] > a:
                mem[a, n] = S(a, n-1), (a, n-1), 0
        return mem[a, n][0]

    mem: Dict[Sparams, Tuple[Score, Sparams, Decision]] = {}
    score = S(maxheight, len(scores))
    a, n = maxheight, len(scores)
    decisions = []
    while n > 0:
        _, (a, n), d = mem[a, n]
        decisions.append(d)
    pos_decisions = []
    for i in range(len(decisions)):
        if decisions[i] == 1:
            pos_decisions.append(i)

    return score, pos_decisions


def show_results(score: int, decisions: List[int]):
    print(score)
    print(decisions)

# ------------------------------------------------------------

if __name__ == '__main__':
    g_heights, g_scores = read_data(sys.stdin)
    g_score, g_decisions = process(g_heights, g_scores)
    show_results(g_score, g_decisions)
