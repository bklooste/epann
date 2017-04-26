
from epann.core.tools.utils.activations import Activation
import numpy as np


class Structs:

    def __init__(self):

        # Node activation related global variables
        self.act = Activation()
        self.activation_tags = self.act.tags

    def generate_connection(self, connection):
        weight = np.random.randn()
        enable_bit = 1
        return {'in_node': connection[1], 'out_node': connection[0], 'weight': weight, 'enable_bit': enable_bit}

    def generate_node(self, type):
        if type == 'input':
            activation = 'linear'
        else:
            activation = self.activation_tags[ np.random.randint( len(self.activation_tags) )]
        return {'type': type, 'activation': activation}

    def generate_history(self, population):
        return { 'population': population }