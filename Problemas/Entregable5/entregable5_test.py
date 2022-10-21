import time
import sys
from typing import *

from entregable5 import read_data, process


Score = int
Decision = int               # Índice de globo
Decisions = List[Decision]   # Lista con los índices de los globos explotados (en orden creciente)


def print_exception(name, msg):
    print()
    print('*' * 40)
    print(f'Exception launched executing <{name}>:')
    print(msg)
    print('*' * 40)


def check_type(p_txt: str, expected_type: str, solution: Any):
    def type_spec(obj):
        def type_spec_iterable(obj, name):
            tps = set(type_spec(e) for e in obj)
            if len(tps) == 1:
                return name + "[" + next(iter(tps)) + "]"
            else:
                return name + "[?]"


        def type_spec_dict(obj):
            tps = set((type_spec(k), type_spec(v)) for (k, v) in obj.iteritems())
            keytypes = set(k for (k, v) in tps)
            valtypes = set(v for (k, v) in tps)
            kt = next(iter(keytypes)) if len(keytypes) == 1 else '?'
            vt = next(iter(valtypes)) if len(valtypes) == 1 else '?'
            return f'Dict[{kt}, {vt}]'

        def type_spec_tuple(obj):
            kk = set(type_spec(e) for e in obj)
            if len(kk) > 1 or len(obj) <= 2:
                return f'Tuple[{", ".join(type_spec(e) for e in obj)}]'
            return f'Tuple[{next(iter(kk))}]'

        basic_types = {
            int: "int",
            str: "str",
            bool: "bool",
            float: "float",
            type(None): "None",
        }
        collection_types = {
            list:  lambda o: type_spec_iterable(o, 'List'),
            set:   lambda o: type_spec_iterable(o, 'Set'),
            dict:  type_spec_dict,
            tuple: type_spec_tuple,
        }

        t = type(obj)
        if t in basic_types:
            return basic_types[t]
        if t in collection_types:
            return collection_types[t](obj)
        return t.__name__

    try:
        tt = type_spec(solution)
    except:
        raise Exception(f"check_type. Excepción analizando el tipo de '{solution}'")

    if tt != expected_type and tt != "None":
        raise Exception(f"  Error en el tipo devuelto por '{p_txt}':\n"
                        f'    - Tipo esperado: {expected_type}\n'
                        f'    - Tipo devuelto: {tt}')


def check_solution(problem: Tuple[int, List[int], List[int]], solution: Tuple[Score, Decisions]) -> bool:
    final_score, heights, scores = problem
    score, decisions = solution
    if final_score != score:
        raise Exception(f'La puntuación devuelta por tu process no es correcta.')
    last_height = heights[decisions[0]]
    last_index = -1
    c_score = 0
    for ig in decisions:
        if ig <= last_index:
            raise Exception(f'Los índices de los globos deben ser crecientes.')
        if last_height < heights[ig]:
            raise Exception(f'Las alturas de los globos deben ser "no crecientes".')
        c_score += scores[ig]
        last_index = ig
        last_height = heights[ig]
    if c_score != final_score:
        raise Exception(f'Tus decisiones dan una puntuación diferente de la que indicas en el process')
    return True


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Use:')
        print(f'    python3 {sys.argv[0]} <instance_file_name>')
        sys.exit(1)

    # Reading the instance --------------------------------------
    heights, scores = [], []
    print('- Reading the instance (read_data)...', end='')
    sys.stdout.flush()
    try:
        with open(sys.argv[1]) as f:
             res = read_data(f)
        check_type('read_data', "Tuple[List[int], List[int]]", res)
        heights, scores = res
        print('Ok!')
    except Exception as e:
        print("ERROR!")
        #print(f"read_data({sys.argv[1]}):")
        print_exception(f"read_data('{sys.argv[1]}')", e)
        sys.exit(1)

    try:
        score = int(sys.argv[1].split('_')[-1].split('.')[0])
    except:
        raise Exception(f"La instancia '{sys.argv[1]}' no tiene un nombre válido.")

    problem = (score, heights[:], scores[:])

    # Getting the solution --------------------------------------
    score, decisions = -1, []
    print('- Getting the solution (process)...', end='')
    sys.stdout.flush()
    try:
        t1 = time.process_time()
        solution = process(heights, scores)
        check_type('process', "Tuple[int, List[int]]", solution)
        (score, decisions) = solution
        t2 = time.process_time()
        t = t2 - t1  # tiempo de proceso utilizado en process
        print('Ok!')
    except Exception as e:
        print("ERROR!")
        print_exception('process', e)
        t = -1
        sys.exit(1)

    # Checking the solution --------------------------------------
    print('- Checking the solution...', end='')
    sys.stdout.flush()
    is_valid = False
    try:
        is_valid = check_solution(problem, solution)
        print('Ok!')
    except Exception as e:
        print("ERROR!")
        print_exception('check_solution', e)
        sys.exit(1)

    # Ouput results ----------------------------------------------
    sol_msg = 'OK' if is_valid else 'ERROR'
    time_msg = 'OK' if t <= 1 else 'ERROR'
    print (f"SOLUTION {sol_msg} - TIME {time_msg} ({t:.2f} secs)")
