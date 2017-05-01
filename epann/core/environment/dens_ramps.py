
import numpy as np

densities = [0.15, 0.30, 0.45, 0.60, 0.75, 0.90]


passes = 500
num_intervals = 10

intervals = [ int(interval) for interval in np.linspace(0, passes, num_intervals + 1) ]
intervals.pop(0)

flatten = True

# for density in densities:
#
#     dens_index = densities.index(density)
#     ramp = range(dens_index, dens_index + num_intervals)
#
#     while any( i > max(range(len(densities))) for i in ramp ):
#         if flatten:
#             ramp = [max(range(len(densities))) if val > max(range(len(densities))) else val for val in ramp]
#         else:
#             ramp = [ val - ( max(range(len(densities))) + 1 ) if val > max(range(len(densities))) else val for val in ramp]
#
#     ramp = [ densities[val] for val in ramp ]
#
#     print density, ramp

for density in densities:

    rev_densities = list(reversed(densities))
    dens_index = rev_densities.index(density)

    ramp = range(dens_index, dens_index + num_intervals)

    while any( i > max(range(len(densities))) for i in ramp ):
        if flatten:
            ramp = [max(range(len(densities))) if val > max(range(len(densities))) else val for val in ramp]
        else:
            ramp = [ val - ( max(range(len(densities))) + 1 ) if val > max(range(len(densities))) else val for val in ramp]

    ramp = [ rev_densities[val] for val in ramp ]

    print density, ramp