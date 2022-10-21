from shortest_path import process
from labyrinthviewer import LabyrinthViewer

g, path1, path2 = process(40, 60)

lv = LabyrinthViewer(g, canvas_width=800, canvas_height=600, margin=10)

lv.add_path(path1)
lv.add_path(path2, offset=2, color ='blue')

lv.run()