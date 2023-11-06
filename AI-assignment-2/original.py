from Map import Map_Obj
from queue import PriorityQueue
import numpy as np

def heuristic(a, b):
    return np.sqrt((b[0]-a[0])**2 + (b[1]-a[1])**2)

def heuristic_moving(a, b):
    return np.sqrt((b[0]-a[0]-0.25)**2 + (b[1]-a[1])**2)

# Initialization
start = map.get_start_pos()
goal = map.get_goal_pos()

parent = np.zeros((map.int_map.shape[0], map.int_map.shape[1], 2))-1
cost = np.zeros((map.int_map.shape[0], map.int_map.shape[1]))-1

cost[start[0], start[1]] = 0
frontier = PriorityQueue()

frontier.put((1, start))

# A-star algorithm
# Main algorithm loop:
while not frontier.empty():
    map.tick()
    goal = map.get_goal_pos()

    # Get next node from the Frontier
    current = frontier.get()[1]

    # Check if it is the goal
    if (current[0] == goal[0] and current[1] == goal[1]):
        print("Goal found!")
        break

    # For all Neighbors of Current
    for neighbor in map.get_cell_neighbors(current):

        # Calculate the cost of Neighbor from Current
        new_cost = cost[current[0], current[1]] + map.int_map[neighbor[0], neighbor[1]]

        # If Neighbor has not been visited, or if Current has a lower cost for the Neighbor 
        if (cost[neighbor[0], neighbor[1]] == -1) or new_cost < cost[neighbor[0], neighbor[1]]:
            map.str_map[neighbor[0], neighbor[1]] = ' - '
            
            # Update parent and cost of Neighbor
            parent[neighbor[0], neighbor[1]] = [current[0], current[1]]
            cost[neighbor[0], neighbor[1]] = new_cost

            # Calculate priority based on new cost and heuristic
            prio = new_cost + heuristic_moving(neighbor, goal)

            # Put Neighbor in the Frontier with the given priority
            frontier.put((prio, neighbor))

current = parent[int(goal[0]), int(goal[1])] # Get parent of Goal
path = [] # initialize path array

# Until we reach the start
while not (current[0] == start[0] and current[1] == start[1]):
    path.append( current )
    current = parent[int(current[0]), int(current[1])] # get parent

# Paint the map
for current in path:
    map.str_map[int(current[0]), int(current[1])] = ' x '
map.str_map[int(goal[0]), int(goal[1])] = ' G '
map.show_map()
image = map.show_map()



