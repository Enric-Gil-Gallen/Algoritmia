import sys
from typing import *


def read_data(f) -> List[int]:
    v = []
    for line in f.readlines():
        v.append(int(line))
    return v

def process_rec(vector: List[int]) -> Optional[int]:
    def tail_dec_solve(start: int, end: int) -> Optional[int]:
        ne = end - start
        if ne == 0:     # is_simple
            return None # trivial_solution
        elif ne == 1:   # is_simple
            return start if vector[start] == start else None    # trivial_solution
        else:
            # decrease
            h = (start + end) // 2
            if h == vector[h]:
                return h
            elif h < vector[h]:     # Quitar derecha
                end = h
            else:                   # Quitar izquierda
                start = h + 1
            return tail_dec_solve(start, end)

    return tail_dec_solve(0, len(vector))


def process(vector: List[int]) -> Optional[int]:
    start = 0
    end = len(vector)
    while end - start > 1:
        # decrease
        h = (start + end) // 2
        if h == vector[h]:
            return h
        elif h < vector[h]:  # Quitar derecha
            end = h
        else:  # Quitar izquierda
            start = h + 1

        ne = end - start
        if ne == 0:  # is_simple
            return None  # trivial_solution
        elif ne == 1:  # is_simple
            return start if vector[start] == start else None  # trivial_solution


def show_results(results: Optional[int]) -> Optional[int]:
    if results == None:
        print("No hay punto fijo")
    else:
        print(results)

if __name__ == "__main__":
    datos = read_data(sys.stdin)
    results = process(datos)
    show_results(results)