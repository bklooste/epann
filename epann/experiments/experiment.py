
from epann.core.population.population import Population
from epann.core.environment.environment import Environment

from progressbar import ProgressBar, SimpleProgress, FormatLabel


class Experiment:

    '''
    General purpose experiment class.
    '''

    def __init__(self, num_generations=100, num_agents=36, verbose=False):

        self.num_generations = num_generations
        self.num_agents = num_agents

        self.verbose = verbose

        # Define the Environment object
        self.environment = Environment()

        self.history = dict.fromkeys( range(self.num_generations) )

    def run(self):

        innovation_number = 0

        if self.verbose:
            pbar = ProgressBar(widgets=[FormatLabel('  Generation: '), SimpleProgress()], maxval=self.num_generations).start()

            for generation in range(self.num_generations):

                innovation_number = self.main(generation, innovation_number)

                pbar.update(generation + 1)

            pbar.finish()

        else:

            for generation in range(self.num_generations):
                innovation_number = self.main(generation, innovation_number)


    def main(self, generation, innovation_number):

        if not generation:
            self.population = Population(self.num_agents)
        else:
            self.population = Population(self.population.children)

        if generation < (self.num_generations - 1):

            self.population.evaluate()
            innovation_number = self.population.breed( innovation_number)

        else:

            self.population.evaluate()

        self.history[generation] = self.population

        return innovation_number

    def save(self):
        pass