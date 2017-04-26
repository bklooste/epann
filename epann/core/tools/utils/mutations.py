
from epann.core.tools.utils.structs import Structs

from epann.core.tools.constants.cppn import *
from epann.core.tools.constants.hyperNEAT import *

import numpy as np



class Mutations:

    def __init__(self):

        self.modify = Structs()

    # ----- Structural Mutations

    def add_connection(self, genome, prob, innovation):
        connections = genome.connections
        nodes = genome.nodes

        # Mutations applied ONCE over the entire CPPN genome wrt prob
        if not connectionwise_mutations and np.random.rand() < prob:

            current_out_nodes = [ connections[connection]['out_node'] for connection in connections.keys() ]
            current_in_nodes = [ connections[connection]['in_node'] for connection in connections.keys() ]

            existing_connections = zip( current_out_nodes, current_in_nodes )
            # print '\nExisting connections:', existing_connections

            # Select the connection to add
            inputs = range(num_inputs)
            outputs = range(num_inputs, num_inputs + num_outputs)

            hiddens = list( set(nodes.keys()) - set( inputs + outputs ) )

            possible_starts = inputs + hiddens
            possible_ends = hiddens + outputs

            chosen_start = possible_starts[np.random.randint(len(possible_starts))]
            chosen_end = possible_ends[np.random.randint(len(possible_ends))]

            chosen_connection = (chosen_start, chosen_end)
            # print '     - Chosen connection:', chosen_connection, chosen_connection in existing_connections

            # print chosen_connection, existing_connections, chosen_connection in existing_connections

            # Check to make sure if the connection already exists - still getting duplicates
            if not (chosen_connection in existing_connections): # and connection's addition would not create a cycle

                # Check to make sure that the connection is not a self connection

                if allow_self_connections:  # Self-connections allowed

                    # Make the connection
                    connections[innovation] = self.modify.generate_connection(chosen_connection)

                else:  # Self-connections not allowed

                    if not (chosen_start == chosen_end):

                        # Make the connection
                        connections[innovation] = self.modify.generate_connection(chosen_connection)

            innovation += 1

        elif connectionwise_mutations:
            pass


        return connections, nodes, innovation

    def add_node(self, genome, prob, innovation):

        connections = genome.connections
        nodes = genome.nodes

        # Mutations applied ONCE over the entire CPPN genome wrt prob
        if not connectionwise_mutations and np.random.rand() < prob:

            # Choose the existing connection the new node will bisect - select this first, and only mutate if it hasnt already been DISABLED
            new_node_bisection = np.random.randint(len(connections))
            possible_nodes = connections.keys()
            new_node_bisection = possible_nodes[new_node_bisection]

            if connections[new_node_bisection]['enable_bit']: # checks to see if the connection is still ENABLED

                # Add the node to the node genome
                new_node_ID = len(nodes)
                nodes[ new_node_ID ] = self.modify.generate_node('hidden')

                # # Choose the existing connection the new node will bisect - select this first, and only mutate if it hasnt already been DISABLED
                # new_node_bisection = np.random.randint(len(connections))
                # possible_nodes = connections.keys()
                # new_node_bisection = possible_nodes[new_node_bisection]

                # Disable that previous connection
                connections[new_node_bisection]['enable_bit'] = 0

                # Instantiate the two new connections coming into and out of the newly introduced node
                previous_out_node = connections[new_node_bisection]['out_node']
                previous_in_node = connections[new_node_bisection]['in_node']

                # Outgoing connection
                connections[innovation] = self.modify.generate_connection([previous_out_node, new_node_ID])

                innovation += 1

                # Incoming connection
                connections[innovation] = self.modify.generate_connection([new_node_ID, previous_in_node])

                innovation += 1

        elif connectionwise_mutations:
            pass

        return connections, nodes, innovation



    # ----- Functional Mutations -----

    def perturb_weight(self, genome, prob):
        connections = genome.connections
        nodes = genome.nodes

        # Mutations applied ONCE over the entire CPPN genome wrt prob
        if not connectionwise_mutations and np.random.rand() < prob:

            chosen_connection = np.random.randint(len(connections.keys()))
            chosen_connection = connections.keys()[chosen_connection]

            # Update the weight - SHOULD THIS BE REPLACED BY A CAUCHY CHANGE AS IN THE DPPNs?

            # --- Either adjust the weight by a small amount
            if np.random.rand() < prob_replace_weight:
                current_weight = connections[chosen_connection]['weight']
                connections[chosen_connection]['weight'] = np.random.normal(current_weight, 0.1)

            # --- Or replace it entirely with a new weight value
            else:
                connections[chosen_connection]['weight'] = np.random.randn()

        elif connectionwise_mutations:
            pass

        # Update
        genome.connections = connections
        genome.nodes = nodes

        return genome


    def delete_connection(self, genome, prob):
        connections = genome.connections
        nodes = genome.nodes

        return connections, nodes

    def flip_enable_bit(self, genome, prob):
        connections = genome.connections
        nodes = genome.nodes

        return connections, nodes

    def mutate_activation_func(self, genome, prob):
        connections = genome.connections
        nodes = genome.nodes

        return connections, nodes


