import sys
from dataclasses import dataclass
from typing import Tuple, List, Iterable

from bab_scheme import BoundedDecisionSequence, bab_max_solve, Score

Decision = int
Solution = Tuple[int, int, Tuple[Decision, ...]]


def read_data(f) -> Tuple[int, List[int], List[int]]:
    c = int(f.readline())
    Value = []
    Weight = []
    for line in f.readlines():
        val, wei = line.strip().split()
        Value.append(int(val))
        Weight.append(int(wei))
    return c, Value, Weight


def process(c: int, v: [int], w: [int]) -> Solution:
    @dataclass
    class Extra: #Solo debe leerse
        weight: int
        value: int

    class KnapsackBDS(BoundedDecisionSequence):
        def calculate_pes_bound(self) -> Score:
            weight2 = self.extra.weight
            value2 = self.extra.value
            for i in range(len(self), len(v)):
                if weight2 + w[i] <= c:
                    weight2 += w[i]
                    value2 += v[i]
            return value2  # El v[n:] hace un subvector del vector desde n hasta el final.

        def calculate_opt_bound(self) -> Score:
            weight2 = self.extra.weight
            value2 = self.extra.value
            for i in range(len(self), len(v)):
                if weight2 + w[i] <= c:
                    weight2 += w[i]
                    value2 += v[i]
                else:
                    capacidad_disponible = c - weight2
                    value2 += (v[i]/w[i]) * capacidad_disponible
                    break
            return value2   # El v[n:] hace un subvector del vector desde n hasta el final.

        def is_solution(self) -> bool:
            return len(self) == len(v)

        def successors(self) -> Iterable["KnapsackBDS"]:
            n = len(self)   # Por donde voy y lo que voy a comprobar justo ahora
            if n < len(v):
                yield self.add_decision(0, Extra(self.extra.weight, self.extra.value))  # o ponemos self.add_decision(0, self.extra) porqué los dos son iguales
                if self.extra.weight + w[n] <= c:
                    weight2 = self.extra.weight + w[n]
                    value2 = self.extra.value + v[n]
                    yield self.add_decision(1, Extra(weight2, value2))

        def solution(self) -> Solution:
            return self.extra.value, self.extra.weight, self.decisions()

    initial_ds = KnapsackBDS(Extra(0, 0))
    sol = list(bab_max_solve(initial_ds))
    return sol[-1]


def show_results(solution: Solution):
    for d in solution:
        print(d)


if __name__ == "__main__":
    c, v, w = read_data(sys.stdin)
    solution = process(c, v, w)
    show_results(solution)
