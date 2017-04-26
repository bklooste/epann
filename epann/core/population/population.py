
from epann.core.population.genome.cppn import CPPN
from epann.core.population.ga.hyperNEAT import HyperNEAT

import numpy as np



class Population:

    def __init__(self, initials):

        '''
        Class for generating a population of agents.
        '''

        self.num_agents, self.genomes = self.initialize(initials)

        self.brains = dict.fromkeys( range( self.num_agents) )

        self.scores = dict.fromkeys( range( self.num_agents) )

        self.ga = HyperNEAT()

        self.children = {}

    def initialize(self, initials):
        if isinstance( initials, int ):
            num_agents = initials
            genomes = self.build( num_agents )
        else:
            genomes = initials
            num_agents = len( genomes.keys() )
        return num_agents, genomes


    def build(self, num_agents):
        # Building a population dictionary
        return dict((key, self.build_cppn()) for key in range(num_agents))

    def build_cppn(self):
        # Initializing a CPPN object for a given agent
        return CPPN()

    def evaluate(self):

        for agent in self.genomes.keys():

            # --- Evaluate the current agent's substrate in order to build the ANN

            # Build the current agent's neural network
            self.build_brain(self.genomes[agent])

            # Evaluate the ANN on the Environment
            # (4/12 - Dummy)
            self.scores[ agent ] = np.random.randint(20)



    def breed(self, innovation_number):

        new_innovation_number = self.ga.run( innovation_number, self.genomes, self.scores )

        self.children = self.ga.children

        return new_innovation_number

    def build_brain(self, genome):
        pass
