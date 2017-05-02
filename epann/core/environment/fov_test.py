
import numpy as np
import itertools


def enforce_wrapping(position, world):
    if position == world.shape[0]:
        wrapped_position = 0
    elif position < 0:
        wrapped_position = world.shape[0] - 1
    else:
        wrapped_position = position
    return wrapped_position

def define_FOV(position, levels):
    rows = range(position[0] - (levels), position[0] + (levels + 1))
    cols = range(position[1] - (levels), position[1] + (levels + 1))
    FOV = list(itertools.product(rows, cols))
    FOV = [(enforce_wrapping(i, world), enforce_wrapping(j, world)) for i, j in FOV]
    return FOV



world = np.zeros((100, 100))

location = [ 50, 50 ]
levels = 1

FOV = define_FOV(location, levels)
print FOV