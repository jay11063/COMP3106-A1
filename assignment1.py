"""
COMP 3106 A - Assignment 1
A* search for a grid path that collects treasure worth at least TREASURE_TARGET.

Name: Jaeyoon Lee
"""

import csv
import heapq


START = "S"
GOAL = "G"
WALL = "X"
TREASURE_TARGET = 5  # minimum total treasure value required
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


# ---------------------------------------------------------------------------
# 2. State helpers
#    A state is (position, collected), where `collected` is a frozenset of
#    treasure positions already picked up (so a treasure is never counted twice).
# ---------------------------------------------------------------------------
def get_collected_value(collected, treasures):
    """Return the total value of the treasures in `collected`."""
    return sum(treasures[pos] for pos in collected)


def is_goal(state, goals, treasures):
    """True if the agent is on a goal tile AND has collected >= TREASURE_TARGET."""
    position, collected = state
    collected_value = get_collected_value(collected, treasures)
    return (position in goals) and (collected_value >= TREASURE_TARGET)


def get_successors(state, grid_size, walls, treasures):
    """Return a list of successor states reachable in one move.

    - Stay inside the grid and do not enter walls.
    - If the new tile is a treasure not yet collected, add it to `collected`.
    """
    position, collected = state
    r,c = position
    n_rows, n_cols = grid_size

    successors = []

    for dr, dc in MOVES:
        next_r, next_c = r+dr, c+dc
        next_pos = (next_r, next_c)

        if not (0 <= next_r < n_rows and 0 <= next_c < n_cols) or (next_pos in walls):
            continue

        if next_pos in treasures and next_pos not in collected:
            next_collected = collected | frozenset([next_pos])
        else:
            next_collected = collected

        successors.append((next_pos, next_collected))

    return successors


# ---------------------------------------------------------------------------
# 3. Heuristic
# ---------------------------------------------------------------------------
def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def heuristic(state, goals):
    """Estimated remaining cost: Manhattan distance to the nearest goal tile.

    (Must be admissible and consistent -- see Question 3 in the PDF.)
    """
    position, collected = state
    return min(manhattan(position, g) for g in goals)


# ---------------------------------------------------------------------------
# 4. A* search
# ---------------------------------------------------------------------------
def reconstruct_path(parents, goal_state):
    """Follow parent pointers back from `goal_state` to the start.

    Returns the list of (row, col) positions from start to goal, in order.
    """
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
    # TODO:
    #   - frontier: heapq of (f, tie_breaker, g, state)
    #   - best_g:   dict state -> lowest g found so far
    #   - parents:  dict state -> previous state
    #   - explored: set of expanded states
    #   - goal test when a state is POPPED, not when it is pushed
    # 초기 상태: (시작 위치, 빈 frozenset)
    start_state = (start, frozenset())
    
    # frontier: (f, tie_breaker, g, state) 형태의 튜플을 담는 힙
    # 동일한 f 값일 때 상태(state) 객체 간 비교 연산 에러를 막기 위해 tie_breaker 카운터를 씁니다.
    frontier = []
    tie_breaker = 0
    
    # 시작 노드의 f score 계산 (g=0 + h)
    f_start = 0 + heuristic(start_state, goals)
    heapq.heappush(frontier, (f_start, tie_breaker, 0, start_state))
    
    # 탐색 기록 관리용 자료구조
    best_g = {start_state: 0}
    parents = {start_state: None}
    explored = set()
    
    num_explored = 0

    while frontier:
        # 가장 f 값이 작은 상태를 꺼냅니다.
        f, _, g, current_state = heapq.heappop(frontier)
        
        # 이미 확장(Pop)된 상태라면 중복 처리를 위해 건너뜁니다.
        if current_state in explored:
            continue
            
        # 탐색(확장)된 유효 노드 카운트 추가 (목적지 노드도 포함)
        num_explored += 1
        explored.add(current_state)
        
        # 🎯 Goal test when a state is POPPED
        if is_goal(current_state, goals, treasures):
            path = reconstruct_path(parents, current_state)
            return path, g, num_explored
            
        # 인접 노드(이동 가능한 후속 상태) 탐색
        for next_state in get_successors(current_state, grid_size, walls, treasures):
            # 격자 내 이동 비용은 항상 1입니다.
            tentative_g = g + 1
            
            # 더 짧은 경로로 해당 상태에 도달할 수 있는 경우에만 업데이트합니다.
            if next_state not in best_g or tentative_g < best_g[next_state]:
                best_g[next_state] = tentative_g
                parents[next_state] = current_state
                
                # f = g + h 계산 후 frontier에 삽입
                f_next = tentative_g + heuristic(next_state, goals)
                tie_breaker += 1
                heapq.heappush(frontier, (f_next, tie_breaker, tentative_g, next_state))
                
    # 목적지에 도달하지 못하고 모든 경로 탐색이 끝난 경우
    return [], float('inf'), num_explored



# The pathfinding function must implement A* search to find the goal state
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