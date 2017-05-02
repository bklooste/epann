
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

def define_FOV(position, levels, heading):
    rows = range(position[0] - (levels), position[0] + (levels + 1))
    cols = range(position[1] - (levels), position[1] + (levels + 1))
    FOV = list(itertools.product(rows, cols))
    FOV = [(enforce_wrapping(i, world), enforce_wrapping(j, world)) for i, j in FOV]

    return FOV

world = np.zeros((100, 100))

location = [ 50, 50 ]
levels = 3

print 'Levels = ', levels

for heading in range(4):
    print '     - Heading: ', heading
    FOV = define_FOV(location, levels, heading)

    FOV_heading = []
    r = 2 * levels + 1
    tH = levels * r
    t = r ** 2

    for l in range(1, levels + 1):

        if not heading: # Heading = 0
            FOV_heading += range((levels - l) * r, (levels - l + 1) * r, 1)

        elif heading == 1: # Heading = 1
            FOV_heading += range( r - ( levels - l + 1 ), t, r )

        elif heading == 2: # Heading = 2
            FOV_heading += range( ( r - (levels - l) ) * r - 1 , (levels + l) * r - 1, -1  )

        elif heading == 3: # Heading = 3
            FOV_heading += range( 2 * tH + ( levels - l ), levels - l - 1, -1 * r )

    print FOV_heading


