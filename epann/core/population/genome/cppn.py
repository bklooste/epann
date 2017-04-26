
from epann.core.tools.utils.structs import Structs

from epann.core.tools.constants.cppn import *

import numpy as np

class CPPN:

    '''
    Class for creating single Compositional Pattern Producing Network (CPPN) genomes.
    '''

    def __init__(self):

        self.num_inputs = num_inputs
        self.num_outputs = num_outputs

        self.modify = Structs()

        self.nodes, self.connections = self.initialize()

        self.score = 0

    def initialize(self):

        # --- Construct the initial node genome

        nodes = dict((key, self.modify.generate_node('input')) for key in range(self.num_inputs))

        additional_output_nodes = dict((key, self.modify.generate_node('output')) for key in range(self.num_inputs, self.num_inputs + self.num_outputs))

        nodes.update(additional_output_nodes)

        # --- Construct the initial connection genome

        connections = dict((key, self.modify.generate_connection([key % self.num_inputs, self.num_inputs - 1 + (key / self.num_inputs + 1)])) for key in range(self.num_inputs * self.num_outputs))

        return nodes, connections

    def evaluate(self):
        self.score = np.random.randn() * 200


