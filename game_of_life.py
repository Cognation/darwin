
import numpy as np
import argparse
import time

def create_grid(size):
    return np.zeros(size, dtype=int)

def apply_rules(grid):
    new_grid = grid.copy()
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            neighbors = np.sum(grid[y-1:y+2, x-1:x+2]) - grid[y, x]
            if grid[y, x] == 1 and (neighbors < 2 or neighbors > 3):
                new_grid[y, x] = 0
            elif grid[y, x] == 0 and neighbors == 3:
                new_grid[y, x] = 1
    return new_grid

def parse_args():
    parser = argparse.ArgumentParser(description='Game of Life')
    parser.add_argument('--size', type=int, nargs=2, default=[10, 10], help='Grid size as two integers: rows cols')
    return parser.parse_args()

def main():
    args = parse_args()
    grid = create_grid((args.size[0], args.size[1]))
    while True:
        print(grid)
        grid = apply_rules(grid)
        time.sleep(1)

if __name__ == '__main__':
    main()
