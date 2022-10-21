from typing import List
import sys


def read_weights(name) -> List[int]:
    f = open(name)
    f.readline()
    return [int(i) for i in f.readlines()]


def read_data(f) -> List[int]:
    return [int(i) for i in f.readlines()]


def process(positions: List[int], weights: List[int]) -> List[List[int]]:
    d = {}
    for it, p in enumerate(positions):
        if p not in d:
            d[p] = []
        d[p].append(weights[it])
    return [sorted(d[p]) for p in sorted(d.keys())]


def show_results(bins: List[List[int]]):
    for i, b in enumerate(bins):
        print(f"{i:3}: {', '.join(str(it) for it in b)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("Error: necesito el nombre el fichero del problema")
        sys.exit(1)
    weights = read_weights(sys.argv[1])
    positions = read_data(sys.stdin)
    bins = process(positions, weights)
    show_results(bins)

