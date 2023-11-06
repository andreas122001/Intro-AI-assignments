from Map import Map_Obj
import numpy as np
from a_star import AStar

# Changes in Map.py
# - added new colors for '-' and 'x'
# - added functions:
#   - get_cell_neighbors(self, cell: tuple[int, int]) -> list[tuple[int, int]]
#   - get_cell_neighbors_8(self, cell: tuple[int, int]) -> list[tuple[int, int]]
#   - _filter_cells(self, cells: list) -> list[tuple[int, int]]
# - Added function get_map_image() that returns the image-obj instead of showing it

# Heuristic functions
def heuristic(a, b):
    return np.sqrt((b[0]-a[0])**2 + (b[1]-a[1])**2)

def heuristic_moving(a, b):
    return np.sqrt((b[0]-a[0]-0.25)**2 + (b[1]-a[1])**2)

astar = AStar(Map_Obj(task = 1))
astar.find_shortest_path(heuristic, 1.0)
# astar.find_shortest_path(heuristic_moving, 1.0) # uncomment to use this instead
astar.show_path()






