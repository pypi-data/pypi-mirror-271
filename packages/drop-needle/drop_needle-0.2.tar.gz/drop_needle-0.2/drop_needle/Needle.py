import random
import math
from typing import Tuple

class Needle:
    def __init__(self, length: float) -> None:
        '''Method to initialize a needle with a certain length.
        
        Input:
            length [float]: lenth of the needle.

        Output:
            None
        '''
        self.length = length

        # Variable for the position of the needle's middle between the lines on the table
        self.position = None
        # Variable for the angle the needle has to the next line on the table after it fell.
        self.angle = None
        # Distance to the next line on the table
        self.dist_next = None

    def __repr__(self) -> str:
        '''Print information about the needle
        
        Input:
            None

        Output:
            [str] Information about the needle
        '''
        return "Length: {0}\nPosition: {1}\nAngle: {2}".format(self.length, self.position, self.angle)
    
    def fall(self, distance_lines: float) -> Tuple[float]:
        '''Method to let the needle fall n the table.
        Afterwards the needle has a position between two lines and an angle to the next line.
        
        Input:
            distance_lines [float]: the distance between two parallel lines on the table.

        Output:
            Tuple[float] position of the middle of the needle between two lines and the angle to the next line.
        '''

        # Randomly define the position between two lines for a needle
        self.position = random.uniform(0, distance_lines)
        # Randomly define an angle the needle has to the next line between 0 and 90 degrees
        self.angle = random.uniform(0, math.pi/2)

        # Update distance to next line
        self.dist_next = self.get_distance_to_next_line(distance_lines)

        return (self.position, self.angle)
    
    def get_distance_to_next_line(self, distance_lines: float) -> float:
        '''Method to determine the distance between the needle's middle and the next line on the table.
        
        Input:
            distance_lines [float]: the distance between two parallel lines on the table.

        Output:
            dist_next [float]: distance to the next line on the table
        '''

        min_distance = min(distance_lines - self.position, self.position)
        self.dist_next = min_distance
        return self.dist_next