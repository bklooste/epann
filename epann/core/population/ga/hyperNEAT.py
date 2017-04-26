
from epann.core.tools.utils.mutations import Mutations
from epann.core.tools.utils.reproduction import SexualReproduction

from epann.core.tools.constants.hyperNEAT import *
from epann.core.tools.constants.cppn import *

from copy import deepcopy



class HyperNEAT:

    def __init__(self):

        self.allow_self_connections = allow_self_connections

        # Speciation parameters - Explicit Fitness Sharing
        self.c_1, self.c_2, self.c_3, self.C_t = c_1, c_2, c_3, C_t

        # Cross-over parameters
        self.reproduction = SexualReproduction()
        self.cx_percentage = cx_percentage

        # Mutation parameters
        self.mutation = Mutations()

        self.prob_add_node = prob_add_node
        self.prob_add_connection = prob_add_connection
        self.prob_perturb_weight = prob_perturb_weight
        self.prob_delete_connection = prob_delete_connection
        self.prob_flip_enable_bit = prob_flip_enable_bit

    def run(self, innovation_number, genomes, scores):

        self.genomes = genomes
        self.scores = scores

        # Update the innovation number for the first generation
        if not innovation_number:
            self.innovation_number = num_inputs + num_outputs

        # Reproduce if not asexual agents
        if sex:
            self.reproduce()

        # Mutate
        new_innovation = self.mutate(innovation_number)


        self.children = deepcopy( self.genomes )

        return new_innovation

    def mutate(self, innovation_number):

        innovation = dict.fromkeys(self.genomes.keys(), innovation_number)

        for agent in self.genomes.keys():

            # If these mutations are instead applied randomly to every connection in every agent,
            # this random number selection should be done inside individual mutation functions
            # instead of in this main mutate() agent loop.

            mutated_genome = deepcopy(self.genomes[agent])

            # --- Structural Mutations

            # Mutations 1 - Add connection mutation
            mutated_genome.connections, mutated_genome.nodes, innov = self.mutation.add_connection(mutated_genome, self.prob_add_connection, innovation[agent])
            innovation[agent] = innov

            # # Mutations 2 - Add node mutations
            mutated_genome.connections, mutated_genome.nodes, innov = self.mutation.add_node(mutated_genome, self.prob_add_node, innovation[agent])
            innovation[agent] = innov

            # --- Functional Mutations

            # Mutations 3 - Perturb weight mutations
            mutated_genome = self.mutation.perturb_weight(mutated_genome, self.prob_perturb_weight)

            # Mutations 4 - Delete connection mutations
            self.mutation.delete_connection(mutated_genome, self.prob_delete_connection)

            # Mutations 5 - Flip enable bit mutations
            self.mutation.flip_enable_bit(mutated_genome, self.prob_flip_enable_bit)

            # Mutations 6 - Mutate node activation function



            # Genome update
            self.genomes[agent] = mutated_genome


        # INNOVATION NUMBER UPDATE

        return max(innovation.values())

    def reproduce(self):

        self.genomes = self.reproduction.crossover(self.genomes, self.scores)








