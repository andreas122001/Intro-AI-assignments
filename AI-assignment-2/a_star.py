from Map import Map_Obj
from queue import PriorityQueue
from typing import Callable
import numpy as np
from PIL import Image


class AStar:
    def __init__(self, map: Map_Obj) -> None:
        """
        Initializes the A*-algorithm, using a Map_Obj. \\
        params:
            - map:
                - the Map_Obj to find the shortest path of, given a start and a goal.
        """
        # Get start and stop from map
        self.start = map.get_start_pos()
        self.stop = map.get_goal_pos()

        # Setup cost and parent matrices
        self.parent = np.zeros((map.int_map.shape[0], map.int_map.shape[1], 2))-1
        self.cost = np.zeros((map.int_map.shape[0], map.int_map.shape[1]))-1

        # Start should have 0 accumulative cost
        self.cost[self.start[0], self.start[1]] = 0

        # Initialize queue and add starting cell
        self.frontier = PriorityQueue()
        self.frontier.put((1, self.start))

        self.map = map

    def find_shortest_path(self, heuristic: Callable, heuristic_weight: float = 1.0):
        """
        Finds the shortest path of the map, and draws it on the map. \\
        params:
            - heuristic: 
                - the heuristic function to use. Must take in two cells, e.g. heuristic(cellA, cellB).
            - heuristic_weight: 
                - a float value specifying how much to weight the heuristic (compared to the cell cost)
        """
        # Main algorithm loop:
        while not self.frontier.empty():
            # Update goal for task 5
            self.map.tick() 
            self.stop = self.map.get_goal_pos()

            # Get next node from the Frontier
            current = self.frontier.get()[1]

            # Check if it is the goal
            if (current[0] == self.stop[0] and current[1] == self.stop[1]):
                print("Goal found!")
                break

            # For all Neighbors of Current
            for neighbor in self.map.get_cell_neighbors(current):

                # Calculate the cost of Neighbor from Current
                new_cost = self.cost[current[0], current[1]] + self.map.int_map[neighbor[0], neighbor[1]]

                # If Neighbor has not been visited, or if Current has a lower cost for the Neighbor 
                if (self.cost[neighbor[0], neighbor[1]] == -1) or new_cost < self.cost[neighbor[0], neighbor[1]]:
                    self.map.str_map[neighbor[0], neighbor[1]] = ' - '

                    # Update parent and cost of Neighbor
                    self.parent[neighbor[0], neighbor[1]] = [current[0], current[1]]
                    self.cost[neighbor[0], neighbor[1]] = new_cost

                    # Calculate priority based on new cost and heuristic
                    prio = new_cost + heuristic(neighbor, self.stop)*heuristic_weight

                    # Put Neighbor in the Frontier with the given priority
                    self.frontier.put((prio, neighbor))

        # When goal is found
        path = []
        current = self.parent[int(self.stop[0]), int(self.stop[1])] # get parent of goal
        # Until we reach the start, add current to path and set current to parent
        while not (current[0] == self.start[0] and current[1] == self.start[1]):
            path.append( current )
            current = self.parent[int(current[0]), int(current[1])] # get parent of current
        
        # Paint the path of the map
        for current in path:
            self.map.str_map[int(current[0]), int(current[1])] = ' x '
        self.map.str_map[int(self.stop[0]), int(self.stop[1])] = ' G '

    def show_path(self):
        """Shows the current state of the map as an image."""
        self.map.show_map()

    def get_image(self) -> Image.Image:
        """Returns the image-object of the map."""
        return self.map.get_map_image()