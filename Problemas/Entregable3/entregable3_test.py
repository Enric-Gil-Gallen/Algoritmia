import time
import sys
from typing import *

from entregable3 import read_data, process

Board    = List[List[str]]  # Matriz como lista de listas, con un carácter por celda ['#', 'o', '.']
Pos      = Tuple[int, int]  # Posición en el tablero: (fila,col)
Step     = Tuple[Pos, Pos]  # Un movimiento del puzle
Solution = Tuple[Step,...]  # Tupla con los movimientos que resuelven el puzle


def check_solution(board: Board, solution: Solution) -> bool:
    nrows = len(board)
    ncols = len(board[0])
    np = 0
    for r in range(nrows):
        for c in range(ncols):
            if board[r][c] == 'o':
                np += 1
    for i, ((sr, sc), (tr, tc)) in enumerate(solution):
        if np < 1:
            raise Exception('Wrong number of pieces: {np}')
        if np == 1:
            raise Exception('Wrong step: there is just one piece.')
        if sr < 0 or sc < 0 or tr < 0 or tc <0 or sr >= nrows or sc >=ncols or tr >= nrows or tc >= ncols:
            raise Exception('Step {i}: (row, col) out of the board bounds')
        if board[sr][sc] != 'o':
            raise Exception(f'Step {i}: source ({sr}, {sc}) must have a piece')
        if board[tr][tc] == 'o':
            raise Exception(f'Step {i}: target ({tr}, {tc}) must be empty')
        if abs(sr-tr) not in [0, 2] or abs(sc-tc) not in [0, 2] or abs(sr - tr) + abs(sc - tc) != 2:
            raise Exception(f'Step {i}: invalid (({sr}, {sc}), ({tr}, {tc}))')
        mr, mc = (sr+tr)//2, (sc+tc)//2
        if board[mr][mc] != 'o':
            raise Exception(f'Step {i}: ({mr}, {mc}) must have a piece')
        board[sr][sc] = '.'
        board[mr][mc] = '.'
        board[tr][tc] = 'o'
        np -= 1
    if np != 1:
        raise Exception('There must be just a piece after all the steps. There are {np} pieces')
    return True


if __name__ == '__main__':
    is_large_board = False
    has_solution = True
    if len(sys.argv) != 2:
        print('Use:')
        print(f'    python3 {sys.argv[0]} <instance_file_name>')
        sys.exit(1)

    if '_large' in sys.argv[1]:
        is_large_board = True
    if '_no_sol' in sys.argv[1]:
        has_solution = False

    # Reading the instance --------------------------------------
    board: Board = []
    print('- Reading the instance (read_data)...', end='')
    sys.stdout.flush()
    try:
        with open(sys.argv[1]) as f:
            board = read_data(f)
        print('Ok!')
    except Exception as e:
        print("ERROR!")
        print("read_data: exception launched reading <instance_file_name> ({sys.argv[1]}):", e)
        sys.exit(1)

    board_copy = [line[:] for line in board]
    # Getting the solution --------------------------------------
    num_ds: int = -1
    solution: Optional[Solution] = None
    print('- Getting the solution (process)...', end='')
    sys.stdout.flush()
    try:
        t1 = time.process_time()
        solution = process(board)
        t2 = time.process_time()
        t = t2 - t1  # tiempo de proceso utilizado en process
        print('Ok!')
    except Exception as e:
        print("ERROR!")
        print("process: exception launched:", e)
        t = -1
        sys.exit(1)

    # Checking the solution --------------------------------------
    print('- Checking the solution...', end='')
    sys.stdout.flush()
    is_valid = False
    if solution is None:
        is_valid = not has_solution
        print('Ok!')
    else:
        try:
            is_valid = check_solution(board_copy, solution)
            print('Ok!')
        except Exception as e:
            print("ERROR!")
            print("\ncheck_solution: Exception launched:", e)
            sys.exit(1)


    # Ouput results ----------------------------------------------
    sol_msg = 'OK' if is_valid else 'ERROR'
    time_msg = 'OK' if t <= 1 else 'ERROR'
    print (f"SOLUTION {sol_msg} - TIME {time_msg} ({t:.2f} secs)")
