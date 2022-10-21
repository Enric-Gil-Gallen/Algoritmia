import sys
from typing import *


def read_data(f) -> Tuple[int, int, List[int]]:
    mode = int(f.readline())
    C = int(f.readline())
    w = [int(e) for e in f.readlines()]
    # w = []
    # for linea in f.readlines():
    #   w.append(int(linea))
    return mode, C, w


def process(mode: int, C: int, w: List[int]) -> List[int]:
    if mode == 0:
        return minetras_quepa(w, C)
    if mode == 1:
        return primero_que_quepa(w, C)
    if mode == 2:
        return primero_que_quepa_ordenado(w, C)

    raise Exception(f'process: unknown mode {mode}')


def show_results(solution: List[int]):
    for nc in solution:
        print(nc)


def minetras_quepa(w: List[int], C: int) -> List[int]:
    solution = []
    nc = 0
    espacio = C
    for w_i in w:
        if w_i > espacio:
            nc += 1
            espacio = C
        solution.append(nc)
        espacio -= w_i
    return solution


def primero_que_quepa(w: List[int], C: int) -> List[int]:
    solution = []
    c_space = [C] * len(w) #n contenedores con C de espacio libre cada uno
    for w_i in w:
        for nc in range(len(w)):
            if w_i <= c_space[nc]:
                solution.append(nc)
                c_space[nc] -= w_i
                break
    return solution


def primero_que_quepa_ordenado(w: List[int], C: int) -> List[int]:
    sorted_w = sorted(range(len(w)), key=lambda i: -w[i]) #Ordena los indices por peso de mayor a menor
    solution = [-1] * len(w)
    c_space = [C] * len(w)  # n contenedores con C de espacio libre cada uno
    for i in sorted_w:
        for nc in range(len(w)):
            if w[i] <= c_space[nc]:
                solution[i] = nc
                c_space[nc] -= w[i]
                break
    return solution


if __name__ == "__main__":

    modo, capacidad, pesos = read_data(sys.stdin)
    solucion = process(modo, capacidad, pesos)
    show_results(solucion)

