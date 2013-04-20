"""
Cable Car: Part 1a

Class used to create tile object
Author: Jenny Zhen (jxz6853@rit.edu)
Author: Neil Zimmerman (nxz3937@rit.edu)
"""

class TileData(object):
    """
    Class used to create tile object
    """
    
    #define slots
    __slots__ = ('position','tileId','rotation','routeMap')
    
    def __init__(self, row, col, tileId = None, rotation = None):
        """
        __init__: TileData
        Constructs an instance of TileData
            self - the TileData object
            row - (int) row position of tile
            col - (int) column position of the tile
            tileId - (string) tile ID (a-j, ps)
        """
        
        self.position = (row, col)
        self.tileId = tileId
        self.rotation = rotation
        self.routeMap = [None for n in range(8)]
        for i in range(8):
            self.routeMap.append(i)
            
    def __str__(self):
        """
        __str__: TileData
        Returns a string representation of the PlayerData object.
            self - the TileData object
        """
        
        result = "TileData " + str(self.position) + " => " \
                    + str(self.tileId) + "," + str(self.rotation) + "\n"
        
        for i in range(8):
            result += "\t" + str(i) + " -> " + str(self.routeMap[i]) + "\n"
        
        return result
                    
    
    def setTile(self, tileId, rotation = 0):
        """
        setTile: TileData
        Generate routeMap based on tileId and rotation
            self - the TileData object
            tileId - tile ID (a-j)
            rotation - rotation of the placed tile (0-3)
        """
        
        self.tileId = tileId
        self.rotation = rotation
        
        #store initial route map ( at 0 degree rotation )
        if (tileId == 'a'):
            self.routeMap = [1,0,7,6,5,4,3,2]
        elif (tileId == 'b'):
            self.routeMap = [3,4,7,0,1,6,5,2]
        elif (tileId == 'c'):
            self.routeMap = [3,4,5,0,1,2,7,6]
        elif (tileId == 'd'):
            self.routeMap = [1,0,7,4,3,6,5,2]
        elif (tileId == 'e'):
            self.routeMap = [1,0,3,2,7,6,5,4]
        elif (tileId == 'f'):
            self.routeMap = [5,4,7,6,1,0,3,2]
        elif (tileId == 'g'):
            self.routeMap = [1,0,3,2,5,4,7,6]
        elif (tileId == 'h'):
            self.routeMap = [7,2,1,4,3,6,5,0]
        elif (tileId == 'i'):
            self.routeMap = [3,6,5,0,7,2,1,4]
        elif (tileId == 'j'):
            self.routeMap = [7,6,5,4,3,2,1,0]
        
        # rotate routeMap accordingly
        ## create map of relative routes
        relMap = []
        for i in range(8):
                relMap.append((self.routeMap[i] - i) % 8)
                
        ## apply rotation to relative map
        tempMap = list(relMap)
        if (rotation == 1):
            for i in range(8):
                relMap[i] = tempMap[(i+6)%8]
        elif (rotation == 2):
            for i in range(8):
                relMap[i] = tempMap[(i+4)%8]
        elif (rotation == 3):
            for i in range(8):
                relMap[i] = tempMap[(i+2)%8]
        
        ## apply new relative map to routeMap
        for i in range(8):
            self.routeMap[i] = (i + relMap[i]) % 8
            
        # return success
        return 0
    
    def isTerminalNode(self, node):
        """
        isTerminalNode: TileData
        Returns True if the exit node in question would complete
        a route; otherwise returns false.
            self - the TileData object
            node - node to be checked (0-7)
        """
        # return true if (row == 0) & (node == 1)
        if ((self.position[0] == 0) & (node == 1)):
            return True
        # return true if (row == 7) & (node == 5)
        elif ((self.position[0] == 7) & (node == 5)):
            return True
        # return true if (column == 0) & (node == 7)
        elif ((self.position[1] == 0) & (node == 7)):
            return True
        # return true if (column == 7) & (node == 3)
        elif ((self.position[1] == 7) & (node == 3)):
            return True
        # else return false
        else:
            return False
        
    def isPsNode(self, node):
        """
        isPsNode: TileData
        Returns True if the exit node connects to the power station
            self - the TileData object
            node - node to be checked (0-7)
        """
        # return true if (row == 2) & (column == 3|4) & (node == 5)
        if ((self.position[0] == 2) & ((self.position[1] == 3) or (self.position[1] == 4)) & (node == 5)):
            return True
        # return true if (row == 5) & (column == 3|4) & (node == 1)
        elif ((self.position[0] == 5) & ((self.position[1] == 3) or (self.position[1] == 4)) & (node == 1)):
            return True
        # return true if (column == 2) & (row == 3|4) & (node == 3)
        elif ((self.position[1] == 2) & ((self.position[0] == 3) or (self.position[0] == 4)) & (node == 3)):
            return True
        # return true if (column == 5) & (row == 3|4) & (node == 7)
        elif ((self.position[1] == 5) & ((self.position[0] == 3) or (self.position[0] == 4)) & (node == 7)):
            return True
        # else return false
        else:
            return False
        
        