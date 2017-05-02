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

    def __init__(self, data):
        self.fig = plt.figure()
        self.frames = [[plt.imshow(data[:, :, frame], animated=True)] for frame in range(data.shape[2])]

        # Set up formatting for saving an animation
        # self.save_animation = True
        # Writer = animation.writers['ffmpeg']
        # self.writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

    def animate(self):
        ani = animation.ArtistAnimation(self.fig, self.frames, interval=50, blit=True, repeat_delay=1000)
        plt.axis('off')
        plt.show()
        # if self.save_animation:
        #     ani.save('im.mp4', writer=self.writer)


##### EXAMPLE #####
# sample = np.random.randn(100, 100, 60)
# anim = Animation(sample)
# anim.animate()