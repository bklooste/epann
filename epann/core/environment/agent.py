
import numpy as np
from copy import copy
import itertools

class Agent:

    def __init__(self, world, num_decisions, world_vals):

        # Observation parameters
        self.levels_FOV = 2
        self.conical_FOV = False

        # Action parameters
        self.action_space = 5
        self.actions = self.build_actions()

        # Define the world the agent will interact with
        self.num_decisions = num_decisions
        self.world = world
        self.world_history = np.zeros((self.world.shape[0], self.world.shape[1], self.num_decisions))
        [ self.metabolic_cost, self.nutrient_value, self.visualize ] = world_vals

        # Dynamic global parameters changed by actions
        self.location = [ int(self.world.shape[0]/2), int(self.world.shape[1]/2) ]
        self.heading = 0

        # Place initial agent location in world history
        self.agent_value = 2

        self.world[ self.location[0], self.location[1]] = self.metabolic_cost

        if self.visualize:
            self.step_tick = 0
            self.world_history[:, :, 0] = copy(self.world)
            FOV = self.define_FOV()
            self.world_history[ self.location[0], self.location[1], 0 ] = self.agent_value
            self.world_history[:, :, 1] = copy(self.world)

        self.step_tick = 1

        # Keep track of rewards
        self.cumulative_reward = 0
        self.reward_history = []

    def build_actions(self):

        # Position adjustments
        empty_position_adjust = [ [0,0], [0,0], [0,0], [0,0] ]
        straight = [ [-1,0], [0,1], [1,0], [0,-1] ]
        diagonal_right = [ [-1,1], [1,1], [1,-1], [-1,-1] ]
        diagonal_left = [ [-1,-1], [-1,1], [1,1], [1,-1] ]

        actions = {}

        # Heading changes
        actions[0] = { 'heading_adjust': -1, 'position_adjust': empty_position_adjust }
        actions[1] = { 'heading_adjust': 1, 'position_adjust': empty_position_adjust }

        # Position changes
        actions[2] = { 'heading_adjust': 0, 'position_adjust': straight }
        actions[3] = { 'heading_adjust': 0, 'position_adjust': diagonal_right }
        actions[4] = { 'heading_adjust': 0, 'position_adjust': diagonal_left }

        return actions

    def enforce_wrapping(self, position):
        if position >= self.world.shape[0]:
            wrapped_position = 0
        elif position < 0:
            wrapped_position = self.world.shape[0] - 1
        else:
            wrapped_position = position
        return wrapped_position

    def cyclical_heading(self, heading):
        if heading < 0:
            heading = 3
        elif heading > 3:
            heading = 0
        return heading

    def define_FOV(self):
        rows = range(self.location[0] - (self.levels_FOV), self.location[0] + (self.levels_FOV + 1))
        cols = range(self.location[1] - (self.levels_FOV), self.location[1] + (self.levels_FOV + 1))
        FOV = list(itertools.product(rows, cols))
        FOV = [(self.enforce_wrapping(i), self.enforce_wrapping(j)) for i, j in FOV]

        if self.visualize:
            self.visualize_FOV(FOV)

        return FOV

    def visualize_FOV(self, FOV):
        for receptor in FOV:
            self.world_history[ receptor[0], receptor[1], self.step_tick ] = 0.75 * self.agent_value

    def act(self, observation):

        # Execute a random action
        action = self.actions[np.random.randint(self.action_space)]

        # Update heading
        self.heading = self.cyclical_heading( self.heading + action['heading_adjust'] )

        # Update location
        self.location[0] = self.enforce_wrapping( self.location[0] + action['position_adjust'][self.heading][0] )
        self.location[1] = self.enforce_wrapping( self.location[1] + action['position_adjust'][self.heading][1] )

        # Define the agent FOV
        FOV = self.define_FOV()

    def observe(self):
        observation = 0
        return observation

    def step(self):

        if not (self.step_tick > (self.num_decisions - 1)):

            if not (self.step_tick > (self.num_decisions - 2)) and self.visualize:

                # Copy the current world to the subsequent frame
                self.world_history[:, :, (self.step_tick + 1)] = copy(self.world)

            # Perform an observation
            observation = self.observe()

            # Act on that observation
            self.act(observation)

            # Remove consumed nutrients
            self.world[self.location[0], self.location[1]] = self.metabolic_cost

            if self.visualize:
                # Draw the agent onto the world
                self.world_history[self.location[0], self.location[1], self.step_tick] = self.agent_value

        self.step_tick += 1