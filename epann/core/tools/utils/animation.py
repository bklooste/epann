# """
# =================
# General Purpose Animation
# =================
#
# Creates an animation figure out of a 3D array, animating over axis=2.
# """

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Animation:

    def __init__(self, array):
        self.fig = plt.figure()
        self.frames = [[plt.imshow(array[:, :, frame], animated=True)] for frame in range(array.shape[2])]

    def run(self):
        ani = animation.ArtistAnimation(self.fig, self.frames, interval=50, blit=True, repeat_delay=1000)
        plt.axis('off')
        plt.show()

# ##### EXAMPLE #####
# sample = np.random.randn(100, 100, 60)
# anim = Animation(sample)
# anim.run()