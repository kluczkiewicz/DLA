import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def init_grid(box_size = 101, start_point = 'center', full_edge = False):
    # initialize grid with zeros
    global N 
    N = box_size
    global grid
    grid = np.zeros((N, N), dtype=int)
    # place seed in the center
    if start_point == 'center':
        grid[N//2][N//2] = 1
        return N//2, N//2
    elif start_point == 'left':
        if full_edge:
            grid[:][0] = 1
        else:
            grid[N//2][0] = 1
        return N//2, 0
    elif start_point == 'right':
        if full_edge:
            grid[:][N-1] = 1
        else:
            grid[N//2][N-1] = 1
        return N//2, N-1
    elif start_point == 'up':
        if full_edge:
            grid[0][:] = 1
        else:
            grid[0][N//2] = 1
        return 0, N//2
    elif start_point == 'down':
        if full_edge:
            grid[N-1][:] = 1
        else:
            grid[N-1][N//2] = 1
        return N-1, N//2
    

def is_neighbour(i, j):
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            if x == y == 0:
                continue
            elif i+x < 0 or i+x >= N or j+y < 0 or j+y >= N:
                continue
            elif grid[i+x][j+y] == 1:
                return True
    return False

def random_walker(edges):
    # starting the walker at a random position at the edge
    edge = random.choice(edges)
    if edge == 'up':
        i, j = 0, random.randint(0, N-1)
    elif edge == 'down':
        i, j = N-1, random.randint(0, N-1)
    elif edge == 'left':
        i, j = random.randint(0, N-1), 0
    else:  # edge == 'right'
        i, j = random.randint(0, N-1), N-1

    # keep walking until the walker sticks or goes off the edge
    while True:
        direction = random.choice(['up', 'down', 'left', 'right'])
        if direction == 'up':
            i -= 1
        elif direction == 'down':
            i += 1
        elif direction == 'left':
            j -= 1
        else:  # direction == 'right'
            j += 1

        # if the walker has left the grid, start a new walker
        if i < 0 or i >= N or j < 0 or j >= N:
            return

        # if the walker is neighbouring a part of the aggregate, add it to the aggregate and start a new walker
        if is_neighbour(i, j):
            grid[i][j] = 1
            return

def visualize(n):
    plt.figure(figsize=(6, 6))
    plt.imshow(grid, cmap='gray')
    plt.title('Step ' + str(n))
    plt.show()

def generate_dla(k, m, edges):
    grids = []
    for n in range(k):  # number of walkers
        random_walker(edges)
        if n % m == 0:  # change this to control frequency of visualizations
            #visualize(n)
            grids.append(np.copy(grid))
            if np.all(grids[-1][0:2, :] == 1) and np.all(grids[-1][-2:, :] == 1) and np.all(grids[-1][:, 0:2] == 1) and np.all(grids[-1][:, -2:] == 1):
                break
    return np.array(grids), n

def power_law(R, A, alpha):
    """Power-law function."""
    return A * R**alpha

def calculate_dim(grid, R_values, distances):
    N_values = np.array([np.sum(grid[distances <= R]) for R in R_values])
    # fit N(R) to a power law
    popt, pcov = curve_fit(power_law, R_values, N_values)
    
    return N_values, popt, pcov


