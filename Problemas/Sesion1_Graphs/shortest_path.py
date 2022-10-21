import sys
from algoritmia.datastructures.digraphs import UndirectedGraph
from typing import *
from labyrinth import create_labyrinth
from algoritmia.datastructures.queues.fifo import Fifo

Vertex = Tuple[int, int]
Edge = Tuple[Vertex, Vertex]
Path = List[Vertex]

#transpa14
def bf_serach(g: UndirectedGraph, source: Vertex, target: Vertex) -> List[Edge]:
    aristas = []
    queue = Fifo()
    seen = set()
    queue.push((source, source))
    seen.add(source)
    while len(queue) > 0:
        u, v = queue.pop()
        aristas.append((u, v))
        for suc in g.succs(v):
            if suc not in seen:
                seen.add(suc)
                queue.push((v, suc))
    return aristas



#transpa16
def df_serach(g: UndirectedGraph, source: Vertex, target: Vertex) -> List[Edge]:
    def recorrido_desde(u, v):
        seen.add(v)
        aristas.append((u, v))
        for suc in g.succs(v):
            if suc not in seen:
                recorrido_desde(v, suc)

    aristas = []
    seen = set()
    recorrido_desde(source, source)
    return aristas


#transpa 37
def recover_path(edges: List[Edge], target: Vertex) -> Path:
    # Crea un dicionario de punteros hacia atrás (backpointers)
    bp = {}
    for orig, dest in edges:
        bp[dest] = orig
    # Reconstruye el camino yendo hacia atrás
    path = []
    path.append(target)
    while target != bp[target]:
        target = bp[target]
        path.append(target)
    # Invierte el camino pues lo hemos obtenido al revés
    path.reverse()
    return path


def read_data(f: IO[str]) -> Tuple[int, int]:
    rows = int(f.readline())
    cols = int(f.readline())
    ##additional = int(f.readline())
    return rows, cols    #Esto devuelve una tupla, no hace falta ponerle parentesis


def process(rows: int, cols: int) -> Tuple[UndirectedGraph, Path, Path]:
    g = create_labyrinth(rows, cols, int(rows*cols*0.2))

    la1 = df_serach(g, (0, 0), (rows-1, cols-1))
    path1 = recover_path(la1, (rows-1, cols-1))

    la2 = bf_serach(g, (0, 0), (rows - 1, cols - 1))
    path2 = recover_path(la2, (rows-1, cols-1))

    return g, path1, path2


def show_results(path1: Path, path2: Path):
    for vertex in path1:
        print(vertex)
    print()
    for vertex in path2:
        print(vertex)


if __name__ == '__main__':
    r, c = read_data(sys.stdin)
    g, path1, path2 = process(r, c)
    show_results(path1, path2)

