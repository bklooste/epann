
from __future__ import division
import numpy as np
import itertools

import matplotlib.pyplot as plt

class Environment:

    def __init__(self):
        self.current = Simple()

class Simple:

    def __init__(self):
        
        # Define what the agent can observe and the actions it can perform
        self.observation_space = 6
        self.action_space = 3