from algoritmia.datastructures.digraphs import UndirectedGraph
from algoritmia.datastructures.mergefindsets import MergeFindSet

from random import shuffle

def create_labyrinth(rows: int, cols: int, additional: int = 0):
    vertices = [(row, col)
                for row in range(rows)
                for col in range(cols)]

    mfs = MergeFindSet()

    for vertex in vertices:
        mfs.add(vertex)

    edges = [((row, col), (row+1, col))
              for row in range(rows - 1)
              for col in range(cols)]
    edges.extend([((row, col), (row, col+1))
              for row in range(rows)
              for col in range(cols - 1)])

    shuffle(edges)

    corridors = []

    for (u, v) in edges:
        if additional > 0 or mfs.find(u) != mfs.find(v):
            if mfs.find(u) != mfs.find(v):
                mfs.merge(u, v)
            else:
                additional -= 1
            corridors.append((u, v))

    return UndirectedGraph(E = corridors)
