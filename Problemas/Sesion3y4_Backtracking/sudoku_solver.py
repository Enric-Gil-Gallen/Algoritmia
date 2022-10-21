import sys
from typing import *
from sudoku import desde_cadenas, primera_vacia, posibles_en
from sudoku import Sudoku
from sudoku import pretty_print
from copy import deepcopy
from dataclasses import dataclass
from bt_scheme import bt_solve, Solution
from bt_scheme import DecisionSequence


def read_data(f) -> Sudoku:
    return desde_cadenas(f.readlines())


def process(sudoku: Sudoku) -> Iterable[Sudoku]:
    @dataclass
    class Extra:
        sudoku: Sudoku

    class SudokuDS(DecisionSequence):
        def is_solution(self) -> bool:
            return primera_vacia(self.extra.sudoku) is None

        def solution(self) -> Solution:
            return self.extra.sudoku

        def successors(self) -> Iterable["SudokuDS"]:
            pos = primera_vacia(self.extra.sudoku)
            if pos is not None:
                for num in posibles_en(self.extra.sudoku, pos):
                    sudoku2 = deepcopy(self.extra.sudoku)
                    r, c = pos
                    self.extra.sudoku2[r][c] = num
                    yield self.add_decision(num, Extra(sudoku2))

    initial_ds = SudokuDS(sudoku)
    return bt_solve(initial_ds)


def show_results(solutions: Iterable[Sudoku]):
    for sol in solutions:
        print(pretty_print(sol))
    print("<END>")


if __name__ == "__main__":
    datos = read_data(sys.stdin)
    results = process(datos)
    show_results(results)
