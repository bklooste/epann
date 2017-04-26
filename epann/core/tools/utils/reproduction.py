

from epann.core.tools.utils.structs import Structs
from epann.core.tools.utils.child import Child

from epann.core.tools.constants.cppn import *
from epann.core.tools.constants.hyperNEAT import *

import numpy as np
from random import shuffle
from copy import deepcopy, copy



class SexualReproduction():

    def __init__(self):
        pass

    def speciation(self):

        # Speciation - Computing the Compatibility Distance Delta

        agent_list = self.genomes.keys()

        shuffle( agent_list )

        current_species = 0

        for agent in agent_list:

            self.species[ current_species ] = [ agent ]

            match_ups = deepcopy( agent_list )
            shuffle(match_ups)
            match_ups.remove(agent)

            agent_list.remove( agent )

            primary_agent_connections, primary_agent_nodes = self.genomes[agent].connections, self.genomes[agent].nodes

            for match in match_ups:

                matched_agent_connections, matched_agent_nodes = self.genomes[match].connections, self.genomes[match].nodes

                # Set the longer genome length for our N value
                if len( primary_agent_connections.keys() ) > len( matched_agent_connections.keys() ):
                    N = len( primary_agent_connections.keys() )
                else:
                    N = len( matched_agent_connections.keys() )

                difference = list( set(primary_agent_connections.keys()) - set(matched_agent_connections.keys()) )
                matching = list( set(primary_agent_connections.keys()) - set(difference))

                # Find the disjoint and excess connection genes
                disjoint = filter( lambda  a: a <= max( matched_agent_connections.keys() ), difference )
                excess = filter( lambda  b: b > max( matched_agent_connections.keys() ), difference )

                # Calculate their variables
                D, E = len(disjoint), len(excess)

                weights_agent = [ primary_agent_connections[ connection ][ 'weight' ] for connection in matching ]
                weights_match = [ matched_agent_connections[ connection ][ 'weight' ] for connection in matching ]

                avg_weight_diff = np.mean(np.array(weights_agent) - np.array(weights_match))

                delta = self.compatability_distance_delta(E, D, N, avg_weight_diff)

                # If compatability distance delta is less than threshold, add it to the current species and remove it from pool
                if delta < C_t:
                    self.species[ current_species ].append( match )
                    agent_list.remove( match )

            current_species += 1


    def compatability_distance_delta(self, excess, disjoint, longer_genome_length_N, average_weight_difference):
        return ((c_1 * excess) / longer_genome_length_N) + ((c_2 * disjoint) / longer_genome_length_N) + c_3 * average_weight_difference

    def fitness_sharing(self):

        # Fitness Sharing

        # --- Calculate the current number of agents in each species
        num_agents_per_species = [ len( self.species[ current_species ] ) for current_species in self.species.keys() ]

        per_species_adjusted_fitness_sum = dict.fromkeys( self.species.keys(), 0 )

        # --- Adjust the fitness score for the current generation (post-evaluation): fitness_individual / num_agents in species
        for species in range( len( self.species.keys() ) ):
            for agent in self.species[ species ]:

                # --- Calculate the adjusted fitness for each agent
                value = round( 1. * self.scores[ agent ] / num_agents_per_species[ species ], 4 )

                # --- Update the adjusted fitness for each agent
                self.scores[ agent ] = value

                # --- Sum the adjusted fitnesses within each species
                per_species_adjusted_fitness_sum[ species ] += value

        # --- Calculate the average adjusted fitness across the entire population
        avg_adjusted_fitness_population = np.mean( np.array( self.scores.values() ) )

        # --- Calculate the new number of parent genomes from each species to seed the next generation
        self.new_num_agents_per_species = self.calculate_new_num_agents(per_species_adjusted_fitness_sum, avg_adjusted_fitness_population)

    def calculate_new_num_agents(self, per_species_adjusted_fitnesss_sum, avg_adjusted_fitness_population):

        # --- Calculate the new number of parent genomes from each species to seed the next generation
        new_num_agents_per_species = [ int(round((  per_species_adjusted_fitnesss_sum[ species ] / avg_adjusted_fitness_population ))) for species in self.species.keys() ]

        # See if our calculation of the new number of agents results in more/less new agents than our self.num_agents constant. Adjust accordingly; prioritize diversity.
        difference = len(self.genomes.keys()) - sum(new_num_agents_per_species)

        if difference < 0:
            # The number of calculated new agents > self.num_agents constant
            max_index = new_num_agents_per_species.index( max(new_num_agents_per_species) )
            new_num_agents_per_species[ max_index ] += difference

        elif difference > 0:
            # The number of calculated new agents < self.num_agents constant
            max_index = new_num_agents_per_species.index( min(new_num_agents_per_species) )
            new_num_agents_per_species[ max_index ] += difference

        return new_num_agents_per_species



    def recombination(self):

        # Cross-over

        # --- A randomly selected proportion of each species is selected in order to build the desired number of agents for the next generation
        species_parent_seeds = dict.fromkeys(self.species.keys())

        child_index_start = 0

        self.children = {}

        for species in self.species.keys():

            seeds = copy(self.species[species])
            shuffle(seeds)

            percent_index = int(round(cx_percentage * len(seeds)))
            seeds = seeds[:percent_index]

            species_parent_seeds[species] = seeds

            # --- Perform cross-over on a random pairing of the randomly selected genomes
            for child in range(child_index_start, child_index_start + self.new_num_agents_per_species[species]):

                a, b = np.random.randint(len(species_parent_seeds[species])), np.random.randint(len(species_parent_seeds[species]))

                parent_a_index, parent_b_index = species_parent_seeds[species][a], species_parent_seeds[species][b]

                # --- Match up parent genomes according to innovation number, keeping all innovation numbers and the genes from the more fit individual

                # --- Breed connection genomes
                current_child_connections = self.breed_connections( parent_a_index, parent_b_index )

                # --- Breed node genomes
                current_child_nodes = self.genomes[ parent_a_index ].nodes

                current_child = Child( current_child_connections, current_child_nodes )

                self.children[child] = current_child

            child_index_start += child


        #   3b) In rare cases when the fitness of the entire population does not improve for more than 20 generations, only the top two
        #       species are allowed to reproduce, refocusing the search into the most promising spaces.


    def breed_connections(self, parent_a_index, parent_b_index):

        # Input: two parent genome indices; Output: single child connection genome, single child node genome

        parent_a_conn, parent_a_nod = self.genomes[ parent_a_index ].connections, self.genomes[ parent_a_index ].nodes
        parent_b_conn, parent_b_nod = self.genomes[ parent_b_index ].connections, self.genomes[ parent_b_index ].nodes

        shared_connections = list(( set( parent_a_conn.keys() ) & set( parent_b_conn.keys() )  ))
        extra_parent_a_conn = list(( set( parent_a_conn.keys() ) - set( parent_b_conn.keys() )  ))
        extra_parent_b_conn = list(( set( parent_b_conn.keys() ) - set( parent_a_conn.keys() )  ))

        # Create the connection genome
        child_connection_genome = {}

        for connection in shared_connections:

            if self.scores[ parent_a_index ] > self.scores[ parent_b_index ]:
                child_connection_genome[ connection ] = parent_a_conn[ connection ]
            elif self.scores[ parent_b_index ] > self.scores[ parent_a_index ]:
                child_connection_genome[ connection ] = parent_b_conn[ connection ]
            else:
                if np.random.rand() < 0.5:
                    child_connection_genome[connection] = parent_a_conn[connection]
                else:
                    child_connection_genome[connection] = parent_b_conn[connection]

        for connection in extra_parent_a_conn:
            child_connection_genome[ connection ] = parent_a_conn[ connection ]

        for connection in extra_parent_b_conn:
            child_connection_genome[ connection ] = parent_b_conn[ connection ]

        # Create the node genome
        if self.scores[ parent_a_index ] > self.scores[ parent_b_index ]:
            child_node_genome = parent_a_nod

            difference = list( set(parent_b_nod.keys()) - set(parent_a_nod.keys()) )
            for missing_node in difference:
                child_node_genome[ missing_node ] = parent_b_nod[ missing_node ]

        else:
            child_node_genome = parent_b_nod

            difference = list( set(parent_a_nod.keys()) - set(parent_b_nod.keys()) )
            for missing_node in difference:
                child_node_genome[ missing_node ] = parent_a_nod[ missing_node ]

        return child_connection_genome

    def crossover(self, genomes, scores):

        self.genomes = genomes
        self.scores = scores

        # Keep track of individual agents' species
        self.species = {}

        # Speciation - localize agents within population into smaller competing species wrt their similar histories
        self.speciation()

        # print [ len(sub_pop) for sub_pop in self.species.values()]


        # Explicit Fitness Sharing wrt species
        self.fitness_sharing()

        # Reproduction
        self.recombination()


        return self.children