"""
COMP 3106 A - Assignment 1
A* search for a grid path that collects treasure worth at least TREASURE_TARGET.

Name: Jaeyoon Lee
"""

import csv


START = "S"
GOAL = "G"
WALL = "X"
TREASURE_TARGET = 5  # minimum total treasure value required
TARGET_MET = "TARGET_MET" # replaces 'collected' once the treasure target is reached
MOVE_COST = 1  # cost of moving to an adjacent tile
MOVES = ((-1, 0), (1, 0), (0, -1), (0, 1))  # up, down, left, right (no diagonals)


def read_grid(filepath):
    grid = []
    with open(filepath, newline='') as csvfile:
        grid = list(csv.reader(csvfile))
    return grid


def parse_grid(grid):
    """Extract the important information from the grid.

    Returns:
        start     : (row, col) of the start tile
        goals     : set of (row, col) goal tiles
        walls     : set of (row, col) wall tiles
        treasures : dict mapping (row, col) -> treasure value (only values > 0)
    """
    start = None
    goals = set()
    walls = set()
    treasures = {}

    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            cell = cell.strip() # remove whitespace
            if cell == START:
                start = (r, c)
            elif cell == GOAL:
                goals.add((r, c))
            elif cell == WALL:
                walls.add((r, c))
            else:
                try:
                    val = int(cell)
                    if val > 0:
                        treasures[(r, c)] = val
                except ValueError:
                    pass
    return start, goals, walls, treasures

# Return the total value of the treasures in collected
def get_collected_value(collected, treasures):
    if collected == TARGET_MET:
        return TREASURE_TARGET
    return sum(treasures[pos] for pos in collected)

# True if the agent is on a goal tile AND has collected >= TREASURE_TARGET.
def is_goal(state, goals, treasures):
    position, collected = state
    collected_value = get_collected_value(collected, treasures)
    return (position in goals) and (collected_value >= TREASURE_TARGET)

# Return a list of successor states reachable in one move
def get_successors(state, grid_size, walls, treasures):
    position, collected = state
    r,c = position
    n_rows, n_cols = grid_size

    successors = []

    for dr, dc in MOVES:
        next_r, next_c = r+dr, c+dc
        next_pos = (next_r, next_c)

        # Stay inside the grid and do not enter walls
        if not (0 <= next_r < n_rows and 0 <= next_c < n_cols) or (next_pos in walls):
            continue

        # If the new tile is a treasure not yet collected, add it to collected
        if collected == TARGET_MET:
            next_collected = TARGET_MET
        elif (next_pos in treasures) and (next_pos not in collected):
            next_collected = collected | frozenset([next_pos])
            if get_collected_value(next_collected, treasures) >= TREASURE_TARGET:
                next_collected = TARGET_MET
        else:
            next_collected = collected

        successors.append((next_pos, next_collected))

    return successors


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def heuristic(state, goals):
    position, collected = state
    if not goals:
        return 0
    return min(manhattan(position, g) for g in goals)


# Returns the list of (row, col) positions from start to goal, in order.
def reconstruct_path(parents, goal_state):
    path = []
    current = goal_state
    
    while current is not None:
        position = current[0]
        path.append(position)
        current = parents.get(current)

    return path[::-1]


def a_star(start, goals, walls, treasures, grid_size):
    """Run A* search.

    Returns:
        path         : list of (row, col) from start to goal
        cost         : cost of that path
        num_explored : number of states popped from the frontier and expanded
                       (skip states already in the explored/closed set;
                       the goal state that is popped counts too)
    """
    start_state = (start, frozenset())
    frontier = {}
    f_start = 0 + heuristic(start_state, goals)
    frontier[start_state] = {
        'g': 0,
        'h': heuristic(start_state, goals)
    }
    
    best_g = {start_state: 0}
    parents = {start_state: None}
    explored = set()
    
    num_explored = 0

    while frontier:
        # extract based on the combined value of cost (g(n)) and heuristic (h(n))
        current_state = min(frontier.keys(), key=lambda k: frontier[k]['g'] + frontier[k]['h'])
        
        node_data = frontier.pop(current_state)
        g = node_data['g']

        # if already explored this node
        if current_state in explored:
            continue

        num_explored += 1
        explored.add(current_state)

        if is_goal(current_state, goals, treasures):
            path = reconstruct_path(parents, current_state)
            return path, g, num_explored
    
        for next_state in get_successors(current_state, grid_size, walls, treasures):
            if next_state in explored:
                continue

            new_g = g + 1
            if ((next_state not in best_g) or (new_g < best_g[next_state])):
                best_g[next_state] = new_g
                parents[next_state] = current_state
                frontier[next_state] = {
                    'g': new_g,
                    'h': heuristic(next_state, goals)
                }
    # if exploring fails
    return [], float('inf'), num_explored



# The pathfinding function must implement A* search to find the goal state
def pathfinding(filepath):
    """Find the optimal path for the grid stored in 'filepath' (CSV).
    Returns:
        optimal_path        : list of (row, col) tuples visited in order
        optimal_path_cost   : cost of the optimal path
        num_states_explored : number of states explored during A* search
    """

    grid = read_grid(filepath)
    start, goals, walls, treasures = parse_grid(grid)
    grid_size = (len(grid), len(grid[0]))

    optimal_path, optimal_path_cost, num_states_explored = a_star(
        start, goals, walls, treasures, grid_size
    )
    return optimal_path, optimal_path_cost, num_states_explored