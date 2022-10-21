import time

from entregable1 import *

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Use:')
        print(f'    python3 {sys.argv[0]} <instance_file_name> <solution_file_name>')
        sys.exit(1)

    pos = (-1, 1)
    lc1 = -1
    lc2 = -1
    try:
        with open(sys.argv[2]) as f:
            ls = [int(line.strip()) for line in f.readlines()]
            pos, lc1, lc2 = (ls[0], ls[1]), ls[2], ls[3]
    except Exception as e:
        print("Exception parsing '{sys.argv[2]}':", e)
        sys.exit(1)

    try:
        with open(sys.argv[1]) as f:
            size, lab = read_data(f)
    except Exception as e:
        print("Exception running 'read_data':", e)
        sys.exit(1)

    entry = (0, 0)
    exit = (size[0] - 1, size[1] - 1)
    try:
        t1 = time.process_time()
        treasure_pos, path1, path2 = process(size, lab)
        t2 = time.process_time()
    except Exception as e:
        print("Exception running 'process':", e)
        sys.exit(1)

    t = t2 - t1

    if (treasure_pos, len(path1)-1, len(path2)-1) == (pos, lc1, lc2):
        if t <= 1:
            print (f"SOLUTION OK - TIME OK ({t:.3f})")
        else:
            print(f"SOLUTION OK - TIME ERROR ({t:.3f})")
    else:
        if t <= 1:
            print (f"SOLUTION ERROR - TIME OK ({t:.3f})")
        else:
            print(f"SOLUTION ERROR - TIME ERROR ({t:.3f})")

