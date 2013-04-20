"""
Cable Car: carData

A class that holds data about cable car positions and routes
Author: Jenny Zhen (jxz6853@rit.edu)
Author: Neil Zimmerman (nxz3937@gmail.com)
"""

class CarData(object):
    '''
    Class used to create cablecar objects
    '''
    
    __slots__ = ['carId','entryTile','entryNode','complete', 'score']

    def __init__(self, carId):
        """
        __init__: carData
        Constructs an instance of carData
            self - the carData object
            carId - the position number (1-32)
        """
        
        # set carId
        self.carId = carId
        
        # initialize route completion variables
        self.complete = False
        self.score = 0
        
        # set entry information
        if ((self.carId >= 1) & (self.carId <= 8)):
            self.entryTile = (0,carId-1)
            self.entryNode = 0
        elif ((self.carId >= 9) & (self.carId <= 16)):
            self.entryTile = ((carId%8+7)%8,7)
            self.entryNode = 2
        elif ((self.carId >= 17) & (self.carId <= 24)):
            self.entryTile = (7,7-((carId%8)+7)%8)
            self.entryNode = 4
        elif ((self.carId >= 25) & (self.carId <= 32)):
            self.entryTile = (7-((carId%8)+7)%8,0)
            self.entryNode = 6
    