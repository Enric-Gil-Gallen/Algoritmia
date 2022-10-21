import sys
from dataclasses import dataclass
from math import ceil
from typing import *

from bab_scheme import BoundedDecisionSequence, bab_min_solve, Score

Decision = int  # Numero de contenedor 0, 1, 2...
Solution = Tuple[Decision, ...]


#   Salida: (C, weights)
def read_data(f) -> Tuple[int, List[int]]:
    C = int(f.readline())
    w = [int(e) for e in f.readlines()]
    # w = []
    # for linea in f.readlines():
    #   w.append(int(linea))
    return C, w


#   Salida: Tuple[Decision, ...]
def process(C: int, w: List[int]) -> Solution:
    @dataclass
    class Extra:
        container_weights: Tuple[int, ...]

    class BinPackingBDS(BoundedDecisionSequence):
        def calculate_opt_bound(self) -> Score:
            liquido = sum(w[len(self):])
            for peso_contenedor in self.extra.container_weights:
                liquido -= C - peso_contenedor
                if liquido < 0:
                    return len(self.extra.container_weights)
            return len(self.extra.container_weights) + ceil(liquido/C)

        def calculate_pes_bound(self) -> Score:
            cw2 = list(self.extra.container_weights)
            ha_cabido = False
            for i in range(len(self), len(w)):
                for nc in range(len(cw2)):
                    if cw2[nc] + w[i] <= C:     #   Si cabe
                        cw2[nc] += w[i]
                        ha_cabido = True
                        break
                    if not ha_cabido:
                        cw2.append(w[i])

            return len(cw2)


        def is_solution(self) -> bool:
            return len(self) == len(w)

        def successors(self) -> Iterable["BoundedDecisionSequence"]:
            n = len(self)
            if n < len(w):
                #   Crea un hijo por cada conentedor existente, en el que quepa el objeto
                for num_container, container_weight in enumerate(self.extra.container_weights):
                    if container_weight + w[n] <= C:                #   Si el objeto cabe
                        cw2 = list(self.extra.container_weights)    #   copia tupla a lista
                        cw2[num_container] += w[n]                  #   modifica la lista
                        yield self.add_decision(num_container, Extra(tuple(cw2)))

                #  Crea un hijo con un contenedor nuevo para el objeto nuevo
                num_container = len(self.extra.container_weights)
                cw2 = self.extra.container_weights + (w[n],)
                yield self.add_decision(num_container, Extra(cw2))

    cw = (0,)
    initial_ps = BinPackingBDS(Extra(cw))
    return bab_min_solve(initial_ps)


def show_results(solution: Solution):
    for nc in solution:
        print(nc)


if __name__ == "__main__":
    capacidad, pesos = read_data(sys.stdin)
    decisiones = process(capacidad, pesos)
    show_results(decisiones)
