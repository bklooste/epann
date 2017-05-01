
from __future__ import division
import numpy as np
import itertools

import matplotlib.pyplot as plt

class Environment:

    def __init__(self):
        self.current = SimpleOcean()


class SimpleOcean:

    def __init__(self):

        # Define what the agent can observe and the actions it can perform
        self.observation_space = 6
        self.action_space = 3

    def reset(self, density):

        # Build the thing with a certain nutrient density
        self.world_size = [ 100, 100 ]
        self.world = np.random.rand( self.world_size[0], self.world_size[1] )

        self.metabolic_cost = -0.2
        self.nutrient_value = 3 * -1 * self.metabolic_cost

        self.nut_density = density
        self.world[ self.world > self.nut_density ] = self.metabolic_cost
        self.world[ self.world > self.metabolic_cost ] = self.nutrient_value

        # Place the agent in the world
        self.agent_location = [ int(self.world_size[0]/2), 0 ]

        self.cumulative_reward = 0
        self.reward_history = []

    def reset_density(self, density):
        # For resetting nutrient density within a single pass (dynamically changing environment)

        # Build the thing with a certain nutrient density
        self.world_size = [ 100, 100 ]
        self.world = np.random.rand( self.world_size[0], self.world_size[1] )

        self.metabolic_cost = -0.2
        self.nutrient_value = 3 * -1 * self.metabolic_cost

        self.nut_density = density
        self.world[ self.world > self.nut_density ] = self.metabolic_cost
        self.world[ self.world > self.metabolic_cost ] = self.nutrient_value

    def make_observation(self):

        rows = [ self.enforce_wrapping(row, 'row') for row in range( self.agent_location[0] - 1, self.agent_location[0] + 2 ) ]
        cols = [ self.enforce_wrapping(col, 'col') for col in range( self.agent_location[1] + 1, self.agent_location[1] + 3 ) ]

        return np.array( [ self.world[loc[0], loc[1]] for loc in list(itertools.product(rows, cols)) ] ).reshape(self.observation_space, )

    def make_decision(self, current_observation):

        # Update the agent location
        self.agent_location[1] = self.enforce_wrapping(self.agent_location[1] + 1, 'col')

        chance_decision = np.random.rand()

        if chance_decision < (1. / 3):
            self.agent_location[0] = self.enforce_wrapping( self.agent_location[0] - 1, 'row' )
            action = 'up'
        elif chance_decision > (2. / 3):
            self.agent_location[0] = self.enforce_wrapping( self.agent_location[0] + 1, 'row' )
            action = 'down'
        else:
            action = 'stay'

        # Return the current agent reward
        reward = self.world[self.agent_location[0], self.agent_location[1]]

        return reward, action

    def enforce_wrapping(self, position, tag):
        if position < 0 and tag == 'row':
            position = self.world_size[0]-1
        elif position >= self.world_size[0] and tag == 'row':
            position = 0
        elif position < 0 and tag == 'col':
            position = self.world_size[1]-1
        elif position >= self.world_size[1] and tag == 'col':
            position = 0
        return position

    def step(self):

        state = self.make_observation()

        reward, action = self.make_decision(state)

        self.cumulative_reward += reward
        self.reward_history.append(self.cumulative_reward)

        self.world[ self.agent_location[0], self.agent_location[1]] = self.metabolic_cost


def simulation(pattern):

    env = Environment()

    if not pattern:
        ## PATTERN 0: Decreasing density over time wrt agent consumption

        # Different densities to be viewed
        densities = [ 0.15, 0.30, 0.45, 0.60, 0.75, 0.90 ]

        num_repetitions = 5
        num_passes = 500  # for a world size of 100,

        plot_count = 1

        for density in densities:
            print 'Nutrient Density: ', density

            plot_track = {}

            for rep in range(num_repetitions):
                print '     - Repetition', rep + 1

                env.current.reset(density)

                env.current.world[env.current.agent_location[0], env.current.agent_location[1]] = env.current.metabolic_cost

                passes = num_passes-1

                for single_pass in range(passes):

                    for decision in range(env.current.world_size[1]):
                        env.current.step()

                plot_track[rep] = env.current.reward_history


            avg_rewards = [sum(e)/len(e) for e in zip(*plot_track.values())]
            x = range(len(avg_rewards))
            xaxis = np.zeros((len(x), ))

            plt.subplot(2, 3, plot_count)
            plt.title('Nutrient Density: ' + str(density))
            plt.plot(x, avg_rewards)
            plt.plot(x, xaxis)
            plt.xlabel('Time')
            plt.ylabel('Cumulative Reward')

            plot_count += 1

        plt.show()

    if pattern == 1:
        ## PATTERN 1: Pass reset to original density for periodic density/clustering

        # Different densities to be viewed
        densities = [ 0.15, 0.30, 0.45, 0.60, 0.75, 0.90 ]

        num_repetitions = 5
        num_passes = 500  # for a world size of 100,

        num_reset_intervals = 3 # environment regrows/agent enters new environment ever pri * 100 decisions

        intervals = [int(interval) for interval in np.linspace(0, num_passes, num_reset_intervals + 1)]
        intervals.pop(0)

        plot_count = 1

        for density in densities:
            print 'Nutrient Density: ', density

            plot_track = {}

            for rep in range(num_repetitions):
                print '     - Repetition', rep + 1

                env.current.reset(density)

                env.current.world[env.current.agent_location[0], env.current.agent_location[1]] = env.current.metabolic_cost

                passes = num_passes-1

                for single_pass in range(passes):

                    # Reset to initial nutrient density at pass interval
                    if single_pass in intervals:
                        env.current.reset_density(density)

                    for decision in range(env.current.world_size[1]):
                        env.current.step()

                plot_track[rep] = env.current.reward_history


            avg_rewards = [sum(e)/len(e) for e in zip(*plot_track.values())]
            x = range(len(avg_rewards))
            xaxis = np.zeros((len(x), ))

            plt.subplot(2, 3, plot_count)
            plt.title('Nutrient Density: ' + str(density))
            plt.plot(x, avg_rewards)
            plt.plot(x, xaxis)
            plt.xlabel('Time')
            plt.ylabel('Cumulative Reward')

            plot_count += 1

        plt.show()

    if pattern == 2 or pattern == 3 or pattern == 4 or pattern == 5:

        if pattern == 2 or pattern == 4:
            flatten = True
        elif pattern == 3 or pattern == 5:
            flatten = False

        ## PATTERN 2: Pass reset to increasing cycle through densities

        # Different densities to be viewed
        densities = [0.15, 0.30, 0.45, 0.60, 0.75, 0.90]

        num_repetitions = 5
        num_passes = 500  # for a world size of 100,

        num_reset_intervals = 10  # environment regrows/agent enters new environment ever pri * 100 decisions

        intervals = [int(interval) for interval in np.linspace(0, num_passes, num_reset_intervals + 1)]
        intervals.pop(0)

        plot_count = 1

        for density in densities:
            print 'Nutrient Density: ', density

            if pattern == 4 or pattern == 5:
                rev_densities = list(reversed(densities))
                dens_index = rev_densities.index(density)
            else:
                dens_index = densities.index(density)

            ramp = range(dens_index, dens_index + num_reset_intervals)

            while any(i > max(range(len(densities))) for i in ramp):
                if flatten:
                    ramp = [max(range(len(densities))) if val > max(range(len(densities))) else val for val in ramp]
                else:
                    ramp = [val - (max(range(len(densities))) + 1) if val > max(range(len(densities))) else val for val
                            in
                            ramp]

            if pattern == 4 or pattern == 5:
                ramp = [rev_densities[val] for val in ramp]
            else:
                ramp = [densities[val] for val in ramp]



            # ramp_index = 0

            plot_track = {}

            for rep in range(num_repetitions):
                print '     - Repetition', rep + 1

                ramp_index = 0

                env.current.reset(ramp[ramp_index])

                env.current.world[
                    env.current.agent_location[0], env.current.agent_location[1]] = env.current.metabolic_cost

                passes = num_passes - 1

                for single_pass in range(passes):

                    # Reset to initial nutrient density at pass interval
                    if single_pass in intervals:
                        ramp_index += 1
                        env.current.reset_density(ramp[ramp_index])

                    for decision in range(env.current.world_size[1]):
                        env.current.step()

                plot_track[rep] = env.current.reward_history

            avg_rewards = [sum(e) / len(e) for e in zip(*plot_track.values())]
            x = range(len(avg_rewards))
            xaxis = np.zeros((len(x),))

            plt.subplot(2, 3, plot_count)
            plt.title('Nutrient Density: ' + str(ramp))
            plt.plot(x, avg_rewards)
            plt.plot(x, xaxis)
            plt.xlabel('Time')
            plt.ylabel('Cumulative Reward')

            plot_count += 1

        plt.show()


# Run the simulation - wouldn't a square wrap around world that a track could be written on to be a better general purpose environment? How would it relate to eventual object classes? to OpenAI Universe?
simulation(4)


