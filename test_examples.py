"""Local test runner for Assignment 1 (NOT submitted).

Runs pathfinding() on every Examples/Examples/ExampleN/grid.txt and compares
the result with the expected .txt files that exist in that folder.

Usage (from the Assignment1 folder):
    python test_examples.py
"""

import ast
import os

from assignment1 import pathfinding

EXAMPLES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Examples", "Examples")


def read_expected(folder, name):
    """Return the parsed contents of `name` in `folder`, or None if missing."""
    path = os.path.join(folder, name)
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return ast.literal_eval(f.read().strip())


def main():
    for example in sorted(os.listdir(EXAMPLES_DIR)):
        folder = os.path.join(EXAMPLES_DIR, example)
        path, cost, explored = pathfinding(os.path.join(folder, "grid.txt"))

        exp_path = read_expected(folder, "optimal_path.txt")
        exp_cost = read_expected(folder, "optimal_path_cost.txt")
        exp_explored = read_expected(folder, "num_states_explored.txt")

        print(f"== {example}")
        print(f"  cost     : {cost}  (expected {exp_cost})  {'OK' if cost == exp_cost else 'DIFF'}")
        if exp_explored is not None:
            print(f"  explored : {explored}  (expected {exp_explored})  "
                  f"{'OK' if explored == exp_explored else 'DIFF'}")
        else:
            print(f"  explored : {explored}  (no expected file)")
        same_path = path == exp_path
        print(f"  path     : {'OK' if same_path else 'DIFF (may still be valid if cost matches)'}")
        if not same_path:
            print(f"    got      {path}")
            print(f"    expected {exp_path}")


if __name__ == "__main__":
    main()
