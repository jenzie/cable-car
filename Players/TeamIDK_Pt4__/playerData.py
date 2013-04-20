"""
Cable Car: Student Computer Player

A sample class you may use to hold your state data
Author: Adam Oest (amo9149@rit.edu)
Author: Jenny Zhen (jxz6853@rit.edu)
Author: Neil Zimmerman (nxz3937@gmail.com)
"""

class PlayerData(object):
    """A sample class for your player data"""
    
    # Add other slots as needed
    __slots__ = ('logger', 'playerId', 'currentTile', 'numPlayers',  'tiles', 'carList')
    
    def __init__(self, logger, playerId, currentTile, numPlayers):
        """
        __init__: PlayerData * Engine.Logger * int * NoneType * int -> None
        Constructs and returns an instance of PlayerData.
            self - new instance
            logger - the engine logger
            playerId - my player ID (0-5)
            currentTile - my current hand tile (initially None)
            numPlayers - number of players in game (1-6)
        """
        
        self.logger = logger
        self.playerId = playerId
        self.currentTile = currentTile
        self.numPlayers = numPlayers
        
        # initialize any other slots you require here
        self.getCars()
        self.tiles = {}         # dictionary of tile objects
        
    def __str__(self):
        """
        __str__: PlayerData -> string
        Returns a string representation of the PlayerData object.
            self - the PlayerData object
        """
        result = "PlayerData= " \
                    + "playerId: " + str(self.playerId) \
                    + ", currentTile: " + str(self.currentTile) \
                    + ", numPlayers:" + str(self.numPlayers)
                
        # add any more string concatenation for your other slots here
                
        return result
    
    def getCars(self):
        numPlayers = self.numPlayers
        self.carList = [None for i in range(numPlayers)]
        if numPlayers == 1:
            self.carList = [i for i in range(33)] # [0,32]
        elif numPlayers == 2:
            self.carList[0] = [i for i in range(1, 33, 2)] #odd numbers, [1,31]
            self.carList[1] = [i for i in range(2, 34, 2)] #even numbers, [2,32]
        elif numPlayers == 3:
            self.carList[0] = [1, 4, 6, 11, 15, 20, 23, 25, 28, 31]
            self.carList[1] = [2, 7, 9, 12, 14, 19, 22, 27, 29, 32]
            self.carList[2] = [3, 5, 8, 10, 13, 18, 21, 24, 26, 30]
        elif numPlayers == 4:
            self.carList[0] = [4, 7, 11, 16, 20, 23, 27, 32]
            self.carList[1] = [3, 8, 12, 15, 19, 24, 28, 31]
            self.carList[2] = [1, 6, 10, 13, 18, 21, 25, 30]
            self.carList[3] = [2, 5, 9, 14, 17, 22, 26, 29]
        elif numPlayers == 5:
            self.carList[0] = [1, 5, 10, 14, 22, 28]
            self.carList[1] = [6, 12, 18, 23, 27, 32]
            self.carList[2] = [3, 7, 15, 19, 25, 29]
            self.carList[3] = [2, 9, 13, 21, 26, 30]
            self.carList[4] = [4, 8, 11, 20, 24, 31]
        elif numPlayers == 6:
            self.carList[0] = [1, 5, 10, 19, 27]
            self.carList[1] = [2, 11, 18, 25, 29]
            self.carList[2] = [4, 8, 14, 21, 26]
            self.carList[3] = [6, 15, 20, 24, 31]
            self.carList[4] = [3, 9, 13, 23, 30]
            self.carList[5] = [7, 12, 22, 28, 32]
