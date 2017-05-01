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
        self.data = array
        self.frames = []

    def update_frame(self, frame):
        return self.data[:, :, frame]

    def build_frames(self):
        for frame in range(self.data.shape[2]):
            im = plt.imshow(self.update_frame(frame), animated=True)
            self.frames.append([im])

    def run(self):
        self.build_frames()
        ani = animation.ArtistAnimation(self.fig, self.frames, interval=50, blit=True, repeat_delay=1000)
        plt.axis('off')
        plt.show()

##### EXAMPLE #####
sample = np.random.randn(100, 100, 60)
anim = Animation(sample)
anim.run()