from drop_needle.Needle import Needle
import numpy as np

class Table:
    def __init__(self, distance_lines: float) -> None:
        '''Initialize a table with a certain distance between the parallel lines on it.
        
        Input:
            distance_lines [float]: distance between the parallel lines on the table

        Output:
            None
        '''
        self.distance_lines = distance_lines
        # Variable for probability that a needle of a certain length crosses a line on the table after it fell on it.
        self.probability: float = None
        # Number of needles that should fall on the table for the experiment
        self.n_needles = 0
        # Number of needles crossing a line on the table
        self.n_crossing = 0
        # Length of the needles
        self.needle_length = None

    def __repr__(self) -> str:
        '''Print information about the table and the simulation experiment.
        
        Input:
            None

        Output:
            [str] Information about table and experiment.
        '''
        return "Distance between lines: {0}\nNumber of needles: {1}\nNeedle length: {2}\nProbability: {3}".format(self.distance_lines, self.n_needles, self.needle_length, self.probability)
    
    def simulate(self, n_needles: int, needle_length: float) -> float:
        '''Method to let fall n needles on the table to observe how many of them cross a line on the table.
        Then it is possible to estimate the probability that a needle crosses a line following the law of large numbers.
        
        Input:
            n_needles [int]: number of needles to fall on the table.
            neede_length [float]: the length of the needles.

        Output:
            [float] the relative number of needles that cross a line or in other words the probability of it.
        '''
        # Update variables
        self.n_needles = n_needles
        self.needle_length = needle_length
        
        angle = np.array([])
        dist_next = np.array([])

        # Drop needles on the table
        for iteration in range(self.n_needles):
            needle = Needle(self.needle_length)
            # Let needle fall
            angle = np.append(angle, needle.fall(self.distance_lines)[1])

            # Get distnace between the needle's middle and the next line on the table
            dist_next = np.append(dist_next, needle.dist_next)

        # Elementwise calculation of the hypotenuse's length
        len_h = dist_next / np.cos(angle)
        # Needle crosses line if the length of the hypotenuse is less or equal to half of the length of th needle
        n_crossing = len(len_h[len_h <= self.needle_length/2])

        self.n_crossing = n_crossing

        # Update probability
        self.probability = self.n_crossing / self.n_needles

        return self.probability