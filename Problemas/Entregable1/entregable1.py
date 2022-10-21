import sys
from typing import *

from algoritmia.datastructures.digraphs import UndirectedGraph
from algoritmia.datastructures.queues import Fifo

Vertex = Tuple[int, int]
Edge = Tuple[Vertex, Vertex]
Path = List[Vertex]
Pair = Tuple[int, int]

# -----------------------------------------------------


def recuperador_camino(lista_aristas: List[Edge], v: Vertex) -> List[Vertex]:
    # Crea un dicionario de punteros hacia atrás (backpointers)
    bp = {}
    for orig, dest in lista_aristas:
        bp[dest] = orig
    # Reconstruye el camino yendo hacia atrás
    camino = []
    camino.append(v)
    while v != bp[v]:
        v = bp[v]
        camino.append(v)
    # Invierte el camino pues lo hemos obtenido al revés
    camino.reverse()
    return camino


def recorredor_aristas_anchura(grafo: UndirectedGraph, v_inicial: Vertex, matriz) -> Tuple[List[Edge], Any]:
    aristas = []
    distancia = 0
    queue = Fifo()
    seen = set()
    queue.push((v_inicial, v_inicial, distancia)) ##Le pasamos la distancia en la que se encuentra el vértice
    seen.add(v_inicial)
    recorro_inicio = False ##Variable que nos indica si el recorredor empieza desde inicio o desde fin

    # Comprobamos si empieza desde inincio o desde final y asignamos en matriz
    if v_inicial == (0, 0):
        matriz[0][0] = (distancia, 0)
        recorro_inicio = True
    else:
        matriz[v_inicial[0]][v_inicial[1]] = (0, distancia)


    while len(queue) > 0:
        u, v, d = queue.pop()
        aristas.append((u, v))
        for suc in grafo.succs(v):
            p1, p2 = suc
            if suc not in seen:
                # Dependendiendo de si recorremos desde inicio o desde fin incrementamos distancia y la asignamos a su pos de matriz
                ida, vuelta = matriz[p1][p2]
                if recorro_inicio:
                    ida = d+1
                else:
                    vuelta = d+1
                matriz[p1][p2] = (ida, vuelta)
                seen.add(suc)
                queue.push((v, suc, d+1))
    return aristas, matriz


# -----------------------------------------------------


# - Recibe un descriptor de fichero que contiene lineas de texto que
#   representan un laberinto.
# - Devuelve una tupla de dos elementos:
#   - El primero: una tupla con el tamaño del laberinto: (num_rows, num_cols)
#   - El segundo: el grafo del laberinto.
def read_data(f) -> Tuple[Pair, UndirectedGraph]:
    dd = {'n': (-1, 0), 's': (1, 0), 'e': (0, 1), 'w': (0, -1)}
    m = []
    for line in f.readlines():
        m.append(line.strip().split(','))
    rows = len(m)
    cols = len(m[0])
    e = [((r, c), (r + dd[d][0], c + dd[d][1])) for r in range(rows)
         for c in range(cols) for d in 'nsew' if d not in m[r][c]]
    return (rows, cols), UndirectedGraph(E=e)


# - Tiene dos parámetros,
#   - El primero: una tupla con el tamaño del laberinto (num_rows, num_cols)
#   - El segundo: el grafo del laberinto.
# - Devuelve una tupla con tres elementos. Por orden:
#    - Una tupla (row, col) con la posición donde colocar el tesoro.
#    - Una lista de vértices con el camino desde la entrada hasta el tesoro.
#    - Una lista de vértices con el camino desde el tesoro hasta la salida.

def process(size: Pair, lab: UndirectedGraph) -> Tuple[Pair, Path, Path]:
    r, c = size
    v_inicio = (0, 0)
    v_fin = (r-1, c-1)
    camino_max = 0
    sol_pos_matriz = (0, 0)

    ##Creamos la matriz y inicializamos con una Tupla[int, int]
    matriz_caminos = []
    for i in range(r):
        matriz_caminos.append([])
        for j in range(c):
            matriz_caminos[i].append((0, 0))

    # Obtenemos tanto la matriz como el camino de ida y de vuelta
    recorre_inicio = recorredor_aristas_anchura(lab, v_inicio, matriz_caminos)
    lista_inicio, matriz_inicio = recorre_inicio
    recorre_final = recorredor_aristas_anchura(lab, v_fin, matriz_inicio)
    lista_fin, matriz_fin = recorre_final

    # Comprobamos la distancia máxima
    for row in range(len(matriz_fin)):
        for col in range(len(matriz_fin[row])):
            ida, vuelta = matriz_fin[row][col]
            suma_actual = ida + vuelta

            if suma_actual > camino_max:
                camino_max = suma_actual
                sol_pos_matriz = (row, col)
            elif suma_actual == camino_max:
                if row < sol_pos_matriz[0]:
                    sol_pos_matriz = (row, col)
                elif row == sol_pos_matriz[0] and col < sol_pos_matriz[1]:
                    sol_pos_matriz = (row, col)

    # Recuperamos el vector de caminos más corto desde inicio y desde fin
    camino_inicio = recuperador_camino(lista_inicio, sol_pos_matriz)
    camino_fin = recuperador_camino(lista_fin, sol_pos_matriz)

    return sol_pos_matriz, camino_inicio, camino_fin


# - Tiene tres parámetros:
#    - una tupla (row, col).
#    - lista de vértices desde la entrada hasta el tesoro
#    - lista de vértices desde el tesoro hasta la salida
# - Muestra cuatro líneas por la salida estándar. Por orden:
#    - Fila del tesoro
#    - Columna del tesoro
#    - Longitud del camino desde la entrada hasta el tesoro (nº de vertices menos 1)
#    - Longitud del camino desde el tesoro hasta la salida (nº de vertices menos 1)
def show_results(pos: Pair, c1: Path, c2: Path):
    row, col = pos
    print(row)
    print(col)
    print(len(c1)-1)
    print(len(c2)-1)


# -----------------------------------------------------


if __name__ == '__main__':
    size, lab = read_data(sys.stdin)
    pos, path1, path2 = process(size, lab)
    show_results(pos, path1, path2)
