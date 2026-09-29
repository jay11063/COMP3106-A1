"""
COMP 3106 A - Assignment 1
A* search for a grid path that collects treasure worth at least TREASURE_TARGET.

Name: Jaeyoon Lee
"""

import csv
import heapq

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
START = "S"
GOAL = "G"
WALL = "X"
TREASURE_TARGET = 5          # minimum total treasure value required
MOVE_COST = 1                # cost of moving to an adjacent tile
MOVES = ((-1, 0), (1, 0), (0, -1), (0, 1))  # up, down, left, right (no diagonals)


# ---------------------------------------------------------------------------
# 1. Input parsing
# ---------------------------------------------------------------------------
def read_grid(filepath):
    """Read the CSV file and return the grid as a list of rows (list of str).

    Each cell should be stripped of surrounding whitespace.
    Empty lines should be ignored.
    """
    # TODO: use csv.reader to read the file
    raise NotImplementedError


def parse_grid(grid):
    """Extract the important information from the grid.

    Returns:
        start     : (row, col) of the start tile
        goals     : set of (row, col) goal tiles
        walls     : set of (row, col) wall tiles
        treasures : dict mapping (row, col) -> treasure value (only values > 0)
    """
    # TODO: loop over every (row, col) and classify the cell
    raise NotImplementedError


# ---------------------------------------------------------------------------
# 2. State helpers
#    A state is (position, collected), where `collected` is a frozenset of
#    treasure positions already picked up (so a treasure is never counted twice).
# ---------------------------------------------------------------------------
def collected_value(collected, treasures):
    """Return the total value of the treasures in `collected`."""
    # TODO
    raise NotImplementedError


def is_goal(state, goals, treasures):
    """True if the agent is on a goal tile AND has collected >= TREASURE_TARGET."""
    # TODO
    raise NotImplementedError


def get_successors(state, grid_size, walls, treasures):
    """Return a list of successor states reachable in one move.

    - Stay inside the grid and do not enter walls.
    - If the new tile is a treasure not yet collected, add it to `collected`.
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# 3. Heuristic
# ---------------------------------------------------------------------------
def manhattan(a, b):
    """Manhattan distance between two (row, col) positions."""
    # TODO
    raise NotImplementedError


def heuristic(state, goals):
    """Estimated remaining cost: Manhattan distance to the nearest goal tile.

    (Must be admissible and consistent -- see Question 3 in the PDF.)
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# 4. A* search
# ---------------------------------------------------------------------------
def reconstruct_path(parents, goal_state):
    """Follow parent pointers back from `goal_state` to the start.

    Returns the list of (row, col) positions from start to goal, in order.
    """
    # TODO
    raise NotImplementedError


def a_star(start, goals, walls, treasures, grid_size):
    """Run A* search.

    Returns:
        path         : list of (row, col) from start to goal
        cost         : cost of that path
        num_explored : number of states popped from the frontier and expanded
                       (skip states already in the explored/closed set;
                       the goal state that is popped counts too)
    """
    # TODO:
    #   - frontier: heapq of (f, tie_breaker, g, state)
    #   - best_g:   dict state -> lowest g found so far
    #   - parents:  dict state -> previous state
    #   - explored: set of expanded states
    #   - goal test when a state is POPPED, not when it is pushed
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Required entry point (do not change the name or signature)
# ---------------------------------------------------------------------------
def pathfinding(filepath):
    """Find the optimal path for the grid stored in `filepath` (CSV).

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
