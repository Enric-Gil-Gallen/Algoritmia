from typing import *


Position = Tuple[int, int]
Sudoku = List[List[int]]


def vacias(s: Sudoku) -> Iterable[Position]:
    for fila in range(9):
        for col in range(9):
            if s[fila][col] == 0:
                yield fila, col


def primera_vacia(s: Sudoku) -> Optional[Position]:
    try:
        return next(vacias(s))
    except StopIteration:
        return None


def posibles_en(s: Sudoku, pos: Position) -> Set[int]:
    fila, col = pos
    used = set(s[fila][c] for c in range(9))
    used = used.union(s[f][col] for f in range(9))
    fc, cc = fila // 3 * 3, col // 3 * 3
    used = used.union(s[fc + f][cc + c]
                      for f in range(3)
                      for c in range(3))
    return set(range(1, 10)) - used


def pretty_print(s: Sudoku):
    for i, fila in enumerate(s):
        for j, columna in enumerate(fila):
            print(columna if columna != 0 else ' ', end="")
            if j in [2, 5]:
                print("|", end="")
        print()
        if i in [2, 5]:
            print("---+---+---")


def desde_cadenas(cadenas: List[str]) -> Sudoku:
    return [
              [ int(c) if c != '.' else 0 for c in cad.strip() ]
              for cad in cadenas
           ]

