from random import random, seed
from binpacking import process

if __name__ == "__main__":
    seed(42)
    w = [int(random() * 1000) + 1 for i in range(1000)]
    c = 1100

    print(f"Como líquido: {(sum(w) + c - 1) // c}")

    for algorithm, sol in [(0, 637), (1, 497), (2, 474)]:
        res = process(algorithm, c, w)
        nc = max(res) + 1
        print(f"Algoritmo {algorithm}: {nc}", end=" ")
        if nc != sol:
            print(f"Error: esperado {sol}")
        else:
            print("OK")
