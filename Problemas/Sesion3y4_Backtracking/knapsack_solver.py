import sys
from dataclasses import dataclass
from typing import Tuple, List, Iterable

from bt_scheme import DecisionSequence, bt_solve, ScoredDecisionSequence, Score, State

Decisions = Tuple[int, ...]

def read_data(f) -> Tuple[int, List[int], List[int]]:
    c = int(f.readline())
    Value = []
    Weight = []
    for line in f.readlines():
        val, wei = line.strip().split()
        Value.append(int(val))
        Weight.append(int(wei))
    return c, Value, Weight


def process(c: int, v: [int], w: [int]) -> Tuple[int, int, Decisions]:
    @dataclass
    class Extra: #Solo debe leerse
        weight: int
        value: int

    class KnapsackDS(ScoredDecisionSequence):
        def is_solution(self) -> bool:
            return len(self) == len(v)

        def successors(self) -> Iterable["ScoredDecisionSequence"]:
            n = len(self) #Por donde voy y lo que voy a comprobar justo ahora
            if n < len(v):
                yield self.add_decision(0, Extra(self.extra.weight, self.extra.value)) #o ponemos self.add_decision(0, self.extra) porqué los dos son iguales
                if self.extra.weight + w[n] <= c:
                    weight2 = self.extra.weight + w[n]
                    value2 = self.extra.value + v[n]
                    yield self.add_decision(1, Extra(weight2, value2))

        def score(self) -> Score:
            return self.extra.value

        def solution(self) -> Tuple[int, int, Decisions]:
            return self.extra.value, self.extra.weight, self.decisions()

        def state(self) -> Tuple[int, int]:
            return len(self), self.extra.weight

    initial_ds = KnapsackDS(Extra(0, 0))
    sol = list(bt_solve(initial_ds))
    return sol[-1]


def show_results(value: int, weight: int, decisions: Decisions):
    print(value)
    print(weight)
    for d in decisions:
        print(d)


if __name__ == "__main__":
    c, v, w = read_data(sys.stdin)
    r_v, r_w, r_decisions = process(c, v, w)
    show_results(r_v, r_w, r_decisions)