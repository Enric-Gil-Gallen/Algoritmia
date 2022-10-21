"""
Version: 3.0 (3-oct-2021)

@author: David Llorens (dllorens@uji.es)
         (c) Universitat Jaume I 2021
@license: GPL3
"""
from abc import abstractmethod
from functools import total_ordering
from typing import *

from algoritmia.datastructures.priorityqueues import MaxHeap, MinHeap
from algoritmia.datastructures.doubleendedpriorityqueues import MaxMinIntervalHeap, MinMaxIntervalHeap

from bt_scheme import DecisionSequence  # Importamos DecisionSequence del backtracking

Solution = TypeVar('Solution')

Decision = TypeVar('Decision')
Score = Union[int, float]

@total_ordering  # Implementando  < y ==, genera el resto
class BoundedDecisionSequence(DecisionSequence):
    __slots__ = ("_pes", "_opt")

    def __init__(self, extra_fields=None, decisions: Tuple[Decision, ...] = ()):
        super().__init__(extra_fields, decisions)
        self._pes: Score = self.calculate_pes_bound()
        self._opt: Score = self.calculate_opt_bound()

    # Nota: Para no repetir cálculos, y dado que son inmutables, las cotas se
    # deberían calcular sólo una vez. Los métodos calculate_opt_bound u calculate_pes_bound
    # se calculan solo una vez y se guarda en self._opt y self._pes.
    # - Los métodos opt() y pes() sólo devuelven el valor de estos atributos.
    @abstractmethod
    def calculate_opt_bound(self) -> Score:
        pass

    @abstractmethod
    def calculate_pes_bound(self) -> Score:
        pass

    # Optimistic bound. Must be iqual to score() for full solutions
    def opt(self) -> Score:
        return self._opt

    # Pessimistic bound. Must be iqual to score() for full solutions
    def pes(self) -> Score:
        return self._pes

    # Comparar dos BabDecisionSequence es comparar sus cotas optimistas
    def __lt__(self, other: "BoundedDecisionSequence") -> bool:
        return self._opt < other._opt

    def __eq__(self, other: "BoundedDecisionSequence") -> bool:
        return self._opt == other._opt


def bab_max_solve(initial_ds: BoundedDecisionSequence) -> Optional[Solution]:
    heap = MaxHeap()
    heap.add(initial_ds)
    bps = initial_ds.pes()
    while len(heap) > 0:
        best_ds = heap.extract_opt()
        if best_ds.is_solution():
            return best_ds.solution()
        for new_ds in best_ds.successors():
            bps = max(bps, new_ds.pes())
            if new_ds.opt() >= bps:
                heap.add(new_ds)


def bab_min_solve(initial_ds: BoundedDecisionSequence) -> Optional[Solution]:
    heap = MinHeap()
    heap.add(initial_ds)
    bps = initial_ds.pes()
    while len(heap) > 0:
        best_ds = heap.extract_opt()
        if best_ds.is_solution():
            return best_ds.solution()
        for new_ds in best_ds.successors():
            bps = min(bps, new_ds.pes())
            if new_ds.opt() <= bps:
                heap.add(new_ds)

