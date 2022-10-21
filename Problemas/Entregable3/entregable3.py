import copy
import sys
from typing import *
from dataclasses import dataclass

from bt_scheme import DecisionSequence, bt_vc_solve

# Tipos ----------------------------------------------------------------------

Board = List[List[str]]  # Matriz como lista de listas, con un carácter por celda ['#', 'o', '.']
Pos = Tuple[int, int]  # Posición en el tablero: (fila,col)
Step = Tuple[Pos, Pos]  # Un movimiento del puzle
Solution = Tuple[Step, ...]  # Tupla con los movimientos que resuelven el puzle

State = Tuple[int, bool]  # Numero de movimientos que llevas + si puedes hacer algun movimiento mas


# Funciones principales ------------------------------------------------------

# Salida. Matriz como lista de listas, con un carácter por celda ['#', 'o', '.']
def read_data(f) -> Board:
    # Leemos las lineas
    lineas = f.readlines()

    # Llenameos la matriz
    posFila = 0
    sol = []
    for linea in lineas:
        sol.append([])  # Se tiene que crear la  fila sino despues no de deja introducir el elemento
        for caracter in linea:
            if caracter != "\n":
                sol[posFila].append(caracter)
        posFila += 1

    return sol


# Salida. La solución como una tupla de Step (o None, si no hay solución).
def process(board: Board) -> Optional[Solution]:

    numeroTotalMovimientos: int = numBolas(board)
    print("Total bolas: "+str(numeroTotalMovimientos))
    numFilaTablero = len(board) - 1
    numColumnasTablero = len(board[0]) - 1
    limiteArriba = -1
    limiteAbajo = numFilaTablero + 1
    limiteDerecha = numColumnasTablero + 1
    limiteIzquierda = -1
    sol: Optional = None

    def solitario_vc_solve(board: Board, totalBolas:int) ->Optional[Solution]:
        @dataclass
        class Extra:
            nuevoBoard: Board
            numMovimientos: int
            step: Step

        class SolitarioDS(DecisionSequence):
            def is_solution(self) -> bool:
                # La solucion sera correcta caundo tenga tantas decisiones como "bolas" habia en el tablero menos 1
                return totalBolas-1 == len(self) or numBolas(self.extra.nuevoBoard) == 1

            def successors(self) -> Iterable["SolitarioDS"]:
                n = len(self)
                if n < totalBolas:
                    nuevoBoardAux = copy.deepcopy(self.extra.nuevoBoard)
                    for row in range(len(nuevoBoardAux)):
                        for col in range(len(nuevoBoardAux[row])):
                                conteidoPos = nuevoBoardAux[row][col]
                                # print(conteidoPos)
                                # print(row," " ,col)
                                if conteidoPos != "#" and conteidoPos != ".":
                                    # Miramos Derecha
                                    if col + 1 != limiteDerecha and col + 2 != limiteDerecha and \
                                            nuevoBoardAux[row][col + 1] == "o" and nuevoBoardAux[row][
                                        col + 2] == "."and nuevoBoardAux[row][col+1] != "#":
                                        posicionActualAux = row, col
                                        posicionSiguinteAux = row + 2, col
                                        nuevoBoardAux[row][col] = "."
                                        nuevoBoardAux[row][col + 1] = "."
                                        nuevoBoardAux[row][col + 2] = "o"
                                        nextPos: Step = posicionActualAux, posicionSiguinteAux
                                        numMov = copy.copy(self.extra.numMovimientos)
                                        numMov += 1
                                        yield self.add_decision(nextPos, Extra(nuevoBoardAux,
                                                                               numMov, nextPos))
                                    # Miramos Izquierda
                                    elif col - 1 != limiteIzquierda and col - 2 != limiteIzquierda and \
                                            nuevoBoardAux[row][col - 1] == "o" and nuevoBoardAux[row][
                                        col - 2] == "."and nuevoBoardAux[row][col-1] != "#":
                                        # print("Izquirda")
                                        # print(row, " ", col)
                                        # print(self.extra.nuevoBoard[row][col - 1])
                                        # print(self.extra.nuevoBoard[row][col - 2])
                                        posicionActualAux = row, col
                                        posicionSiguinteAux = row + 2, col
                                        nuevoBoardAux[row][col] = "."
                                        nuevoBoardAux[row][col - 1] = "."
                                        nuevoBoardAux[row][col - 2] = "o"
                                        nextPos: Step = posicionActualAux, posicionSiguinteAux
                                        numMov = copy.copy(self.extra.numMovimientos)
                                        numMov += 1
                                        yield self.add_decision(nextPos, Extra(nuevoBoardAux,
                                                                               numMov, nextPos))
                                    # Miramos Arriba
                                    elif row - 1 != limiteArriba and row - 2 != limiteArriba and \
                                             nuevoBoardAux[row - 2][col] == "." and nuevoBoardAux[row-1][col] != "#":
                                        # print("Arriba")
                                        # print(row, " ", col)
                                        # print(self.extra.nuevoBoard[row - 1][col])
                                        # print(self.extra.nuevoBoard[row - 2][col])
                                        posicionActualAux = row, col
                                        posicionSiguinteAux = row - 2, col
                                        nuevoBoardAux[row][col] = "."
                                        nuevoBoardAux[row - 1][col] = "."
                                        nuevoBoardAux[row - 2][col] = "o"
                                        nextPos: Step = posicionActualAux, posicionSiguinteAux
                                        numMov = copy.copy(self.extra.numMovimientos)
                                        numMov += 1
                                        yield self.add_decision(nextPos, Extra(nuevoBoardAux,
                                                                               numMov, nextPos))
                                    # Miramos Abajo
                                    elif row + 1 != limiteAbajo and row + 2 != limiteAbajo and \
                                            nuevoBoardAux[row + 1][col] == "o" and \
                                            nuevoBoardAux[row + 2][col] == "."and nuevoBoardAux[row+1][col] != "#":
                                        # print("Abajo")
                                        # print(row, " ", col)
                                        # print(self.extra.nuevoBoard[row + 1][col])
                                        # print(self.extra.nuevoBoard[row + 2][col])
                                        posicionActualAux = row, col
                                        posicionSiguinteAux = row + 2, col
                                        nuevoBoardAux[row][col] = "."
                                        nuevoBoardAux[row + 1][col] = "."
                                        nuevoBoardAux[row + 2][col] = "o"
                                        nextPos: Step = posicionActualAux, posicionSiguinteAux
                                        numMov = copy.copy(self.extra.numMovimientos)
                                        numMov += 1
                                        yield self.add_decision(nextPos, Extra(nuevoBoardAux,
                                                                               numMov, nextPos))

            # Estado actual
            def state(self):
                # print(totalBolas-1, len(self), numBolas(self.extra.nuevoBoard))
                return self.extra.numMovimientos, numBolas(self.extra.nuevoBoard)

        initial_ds = SolitarioDS(Extra(board, 0, None))
        return bt_vc_solve(initial_ds)


    return solitario_vc_solve(board, numeroTotalMovimientos)


def numBolas(board: Board) -> int:
    sol: int = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == "o":
                sol += 1
    return sol


def show_results(solution: Optional[Solution]):
    # Cada linea tiene 4 enteros separados por espacios:
    # Fila Columna (Ficha que movemos) -- Fila Columna (Donde se mueve)
    # En el caso que no tenga solucion la cadena sera None
    if solution != None:
        for n in solution:
            break
            #print(n)

    # print(n)


# Programa principal ------------------------------------------------------

if __name__ == '__main__':
    board = read_data(sys.stdin)
    solution = process(board)
    show_results(solution)
