import sys
from entregable1 import *
from labyrinthviewer import LabyrinthViewer


if len(sys.argv) != 2:
    print('Use:')
    print(f'    python3 {sys.argv[0]} <instance_file_name>')
    sys.exit(1)

with open(sys.argv[1]) as f:
    try:
        size, lab = read_data(f)
    except Exception as e:
        print("Exception running 'read_data':", e)
        sys.exit(1)

entry = (0, 0)
exit = (size[0] - 1, size[1] - 1)

try:
    treasure_pos, path1, path2 = process(size, lab)
except Exception as e:
    print("Exception running 'process':", e)
    sys.exit(1)

lv = LabyrinthViewer(lab, canvas_width=1024, canvas_height=768, margin=10)

lv.set_input_point(entry)
lv.set_output_point(exit)
lv.add_marked_cell(treasure_pos, 'yellow')
lv.add_path(path1, 'red', -1)
lv.add_path(path2, 'blue', 1)

lv.run()  # Muestra la ventana gráfica
