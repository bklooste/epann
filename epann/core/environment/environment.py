
import numpy as np
from animation import Animation
from agent import Agent

class Environment:

    def __init__(self):

        self.num_decisions = 500

        self.visualize = True
        self.current = Simple(self.visualize)

    def run(self):

        self.current.reset(self.num_decisions)

        for decision in range(self.num_decisions):
            self.current.step()

        if self.visualize:
            self.animate()

    def animate(self):

        anim = Animation(self.current.agent.world_history)
        anim.animate()

class Simple:

    def __init__(self, visualize):

        self.world_size = 30

        # Reward parameters
        self.nutrient_density = 0.25
        self.metabolic_cost = -0.2
        self.nutrient_value = 3 * -1 * self.metabolic_cost
        self.world_vals = [ self.metabolic_cost, self.nutrient_value, visualize ]

    def reset(self, num_decisions):

        # Define a world with a certain nutrient density
        self.world = np.random.rand( self.world_size, self.world_size)
        self.world[ self.world > self.nutrient_density ] = self.metabolic_cost
        self.world[ self.world > self.metabolic_cost ] = self.nutrient_value

        # Define an agent
        self.agent = Agent( self.world, num_decisions, self.world_vals )

    def step(self):

        self.agent.step()

env = Environment()
env.run()