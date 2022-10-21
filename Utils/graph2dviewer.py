"""
28/09/2021: Version 1.3. Añadidos canvas_width y canvas_height en el constructor
                         (reemplazan a window_size)
15/09/2021: Version 1.2. Permite poner el fondo transparente (en el IU es blanco, pero
                         en el eps se genera transparente).
24/09/2019: Version 1.1. Corregido modo ROW_COL para que funcione como LabyrinthViewer
02/10/2013: Version 1
@author: David Llorens dllorens@uji.es

Dos modos de funcionamiento según parámetro del constructor (vertexmode):

- Modo ROW_COL (8 filas, 14 columnas):
   (0,0)-----(0,14)
     |         |
   (8,0)-----(8,14)

- Modo X_Y (mismos puntos):
   (0,14)--(8,14)
     |       |
     |       |
     |       |
   (0,0)---(8,0)
"""

from easycanvas import EasyCanvas
from algoritmia.datastructures.digraphs import UndirectedGraph


class Graph2dViewer(EasyCanvas):
    X_Y = 0
    ROW_COL = 1

    def __init__(self, g: UndirectedGraph, canvas_width: int = 400, canvas_height: int = 300,
                 vertexmode=X_Y, transparent_bg=False):
        EasyCanvas.__init__(self)

        self.transparent_bg = transparent_bg

        if not isinstance(g, UndirectedGraph) or \
                any([type(p) != type((1, 1)) or
                     len(p) != 2 or
                     type(p[0]) != type(p[1]) for p in g.V]) or \
                any([type(p[0]) != type(1) and type(p[0]) != type(1.0) for p in g.V]):
            raise TypeError("The graph must be an UndirectedGraph. Vertices must be tuples of two integers or floats")

        if vertexmode == Graph2dViewer.ROW_COL:
            if any([type(p[0]) != type(1) for p in g.V]):
                raise TypeError("In this mode, vertices must be tuples of two integers")
            g = UndirectedGraph(V=[(v[1], -v[0]) for v in g.V], E=[((u[1], -u[0]), (v[1], -v[0])) for (u, v) in g.E])

        self.g = g
        self.max_y = max(p[1] for p in self.g.V)
        self.max_x = max(p[0] for p in self.g.V)
        self.min_y = min(p[1] for p in self.g.V)
        self.min_x = min(p[0] for p in self.g.V)
        self.window_size = (canvas_width, canvas_height)

    def main(self):
        sizex = self.max_x - self.min_x + 1
        sizey = self.max_y - self.min_y + 1
        cell_size = min(self.window_size[0] / sizex, self.window_size[1] / sizey)
        m = ((self.window_size[0] - cell_size * sizex) / 2 - self.min_x * cell_size,
             (self.window_size[1] - cell_size * sizey) / 2 - self.min_y * cell_size)
        self.easycanvas_configure(title='2D Graph Viewer',
                                  background='white',
                                  size=self.window_size,
                                  coordinates=(0, 0, self.window_size[0] - 1, self.window_size[1] - 1))

        if self.transparent_bg:
            # self.root.wm_attributes("-topmost", True)
            # Turn off the window shadow
            self.root.wm_attributes("-transparent", True)
            # Set the root window background color to a transparent color
            self.root.config(bg='systemTransparent')
            self.canvas.config(bg='systemTransparent')

        for u, v in self.g.E:
            self.create_line((u[0] + 0.5) * cell_size + m[0], (u[1] + 0.5) * cell_size + m[1],
                             (v[0] + 0.5) * cell_size + m[0], (v[1] + 0.5) * cell_size + m[1])

        for u in self.g.V:
            self.create_filled_circle((u[0] + 0.5) * cell_size + m[0], (u[1] + 0.5) * cell_size + m[1], cell_size / 8,
                                      relleno='palegreen')
        # Wait for a key   
        self.readkey(True)


if __name__ == '__main__':
    g = UndirectedGraph(E=[((-5, -1), (0, 0)), ((0, 0), (1, 1))])
    viewer = Graph2dViewer(g, canvas_width=400, canvas_height=300, transparent_bg=True)
    viewer.run()
