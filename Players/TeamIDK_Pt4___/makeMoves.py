"""
Cable Car: Part 1a

Class used to make moves (place tiles)
Author: Jenny Zhen (jxz6853@rit.edu)
Author: Neil Zimmerman (nxz3937@rit.edu)
"""

from copy import deepcopy

class MakeMove(object):
    """
    Class used to make a move / place a tile
    """
    
    #define slots
    __slots__ = ('validPos','allMoves','validMoves','priorityQueue','move')
    
    def __init__(self, playerData):
        """
        __init__: MakeMove
            self - the MakeMove object
            playerData - the PlayerData object
        Constructs an instance of MakeMove
        """

        # populate position/move queues
        self.createValidPos(playerData)
        self.createAllMoves(playerData)
        self.createValidMoves(playerData)
        self.createPriorityQueue(playerData)
        self.createMove()


    def __str__(self):
        """
        __str__: MakeMove
            self - the MakeMove object
        Returns the string representation of the MakeMove object
        """
        
        string =  "Valid Moves: " + str(self.validMoves)
        string += "\nNext Move:   " + str(self.move)
        
        return string


    def createValidPos(self, playerData):
        """
        createValidPos: MakeMove
            self - the MakeMove object
            playerData - the PlayerData object
        Stores all valid positions on the game board into MakeMove.validPos (List of tuples)
        """
        
        self.validPos = []
        
        # Get all valid positions from board
        
        # Add border spaces that have not been placed
        for row in range(8):
            for col in range(8):
                if (( row == 0 ) or ( row == 7 ) or ( col == 0 ) or ( col == 7 )):
                    if playerData.tiles[(row, col)].tileId == None:
                        self.validPos.append((row, col))
        
        # Add neighbor positions of any placed tile
        for row in range(8):
            for col in range(8):
                # If tile is placed
                if playerData.tiles[(row, col)].tileId != None:
                    
                    if playerData.tiles[(row, col)].tileId == 'ps':
                        continue
                    
                    # Check north neighbor
                    if row > 0:
                        if playerData.tiles[(row - 1, col)].tileId == None:
                            self.validPos.append((row - 1, col))
                    # Check east neighbor
                    if col < 7:
                        if playerData.tiles[(row, col + 1)].tileId == None:
                            self.validPos.append((row, col + 1))
                    # Check south neighbor
                    if row < 7:
                        if playerData.tiles[(row + 1, col)].tileId == None:
                            self.validPos.append((row + 1, col))
                    # Check west neighbor
                    if col > 0:
                        if playerData.tiles[(row, col - 1)].tileId == None:
                            self.validPos.append((row, col - 1))
        
        # remove duplicates
        self.validPos = list(set(self.validPos))


    def createAllMoves(self, playerData):
        """
        createAllMoves: MakeMove
            self - the MakeMove object
            playerData - the PlayerData object
        Stores all available into MakeMove.allMoves (<Data type>), based on MakeMove.validPos
            and playerData.currentTile
        """
        
        self.allMoves = []
        
        # for each valid position
        for position in self.validPos:
            # for each rotation
            for rotation in range(4):
                move = {'position': position, 'tileName': playerData.currentTile, 'rotation': rotation}
                self.allMoves.append(move)
                


    def createValidMoves(self, playerData):
        """
        createAllMoves: MakeMove
            self - the MakeMove object
            playerData - the PlayerData object
        Stores all available into MakeMove.validMoves (<Data type>), based on MakeMove.allMoves
            and data on already placed tiles (playerData.getBoard().getTileAt(row, col))
        """
        
        self.validMoves = []
        
        # create copy of playerData to test placement
        childData = deepcopy(playerData)
        
        # check for each valid position
        for move in self.allMoves:

            # bool for if move is valid
            moveIsValid = True
            
            # create duplicate playerData
            childData.tiles[move['position']].setTile(move['tileName'], move['rotation'])
                        
            # Moves are valid if they do not create a path of 1
            # If tiles in top row connect north (0) to north (1), then invalid
            if move['position'][0] == 0:
                if childData.tiles[move['position']].routeMap[0] == 1:
                    moveIsValid = False
                if move['position'][1] == 0:
                    if childData.tiles[move['position']].routeMap[0] == 7:
                        moveIsValid = False
                    if childData.tiles[move['position']].routeMap[6] == 1:
                        moveIsValid = False
                if move['position'][1] == 7:
                    if childData.tiles[move['position']].routeMap[0] == 3:
                        moveIsValid = False
                    if childData.tiles[move['position']].routeMap[2] == 1:
                        moveIsValid = False
            
            # If tiles in right column connect east (2) to east (3), then invalid
            if move['position'][1] == 7:
                if childData.tiles[move['position']].routeMap[2] == 3:
                    moveIsValid = False
            
            # If tiles in bottom row connect south (4) to south (5), then invalid
            if move['position'][0] == 7:
                if childData.tiles[move['position']].routeMap[4] == 5:
                    moveIsValid = False
                if move['position'][1] == 0:
                    if childData.tiles[move['position']].routeMap[4] == 7:
                        moveIsValid = False
                    if childData.tiles[move['position']].routeMap[6] == 5:
                        moveIsValid = False
                if move['position'][1] == 7:
                    if childData.tiles[move['position']].routeMap[2] == 5:
                        moveIsValid = False
                    if childData.tiles[move['position']].routeMap[4] == 3:
                        moveIsValid = False
            
            # If tiles in right column connect west (6) to west (7), then invalid
            if move['position'][1] == 0:
                if childData.tiles[move['position']].routeMap[6] == 7:
                    moveIsValid = False
            
            # if move is valid, append it to self.validMoves
            if moveIsValid == True:
                self.validMoves.append(move)
            
        # if no valid moves, all moves are valid
        if len(self.validMoves) == 0:
            print('No valid moves found!')
            self.validMoves = self.allMoves


    def createPriorityQueue(self, playerData):
        """
        createPriorityQueue: MakeMove
            self - the MakeMove object
            playerData - the PlayerData object
        Store valid moves into priorityQueue based on strategy
            priorityQueue[0] contains worst moves
            ...
            priorityQueue[4] contains optimal moves
        """
        
        #declare queue (4 = optimal, 0 = worst)
        self.priorityQueue = [[],[],[],[],[]]
        
        
        # place moves into priorityQueue
        for move in self.validMoves:
            # assign default priority
            priority = 2
            
            #create board with move
            tempPlayer = deepcopy(playerData)
            tempPlayer.tiles[move['position']].setTile(move['tileName'], move['rotation'])
            
            
            ##### BEGIN perform testing ####
            if (_priorityZeroOrFour_(tempPlayer,move,'us') == 0) or (_priorityZeroOrFour_(tempPlayer,move,'them') == 4): 
                priority = 0
            if push_edge(tempPlayer, move, 'us') or push_ps(tempPlayer, move, 'them'):
                priority = 1
            if push_edge(tempPlayer, move, 'them') or push_ps(tempPlayer, move, 'us'):
                priority = 3
            if (_priorityZeroOrFour_(tempPlayer,move,'us') == 0) or (_priorityZeroOrFour_(tempPlayer,move,'them') == 4):
                priority = 4
            else:
                pass
                
            ##### END perform testing ####
            
            #place appropriate moves into 4
            if priority == 4:
                self.priorityQueue[4].append(move)
            #place appropriate moves into 3
            elif priority == 3:
                self.priorityQueue[3].append(move)
            #place appropriate moves into 2
            elif priority == 2:
                self.priorityQueue[2].append(move)
            #place appropriate moves into 1
            elif priority == 1:
                self.priorityQueue[1].append(move)
            #place appropriate moves into 0
            elif priority == 0:
                self.priorityQueue[0].append(move)
        
        # print priority queue for testing
        print("### PRIORITY QUEUE ###")
        for i in range(5):
            print str(4 - i) + " => " + str(self.priorityQueue[4 - i])
        
    
    def createMove(self):
        """
        createMove: MakeMove
            self - the MakeMove object
        Stores the next move to be made into MakeMove.move (Dictionary)
        """
        
        #self.move = {'position': None, 'tileName': None, 'rotation': None}
        #declare priority queue
        
        if len(self.priorityQueue[4]) > 0:
            self.move = self.priorityQueue[4][0]
        elif len(self.priorityQueue[3]) > 0:
            self.move = self.priorityQueue[3][0]
        elif len(self.priorityQueue[2]) > 0:
            self.move = self.priorityQueue[2][0]
        elif len(self.priorityQueue[1]) > 0:
            self.move = self.priorityQueue[1][0]
        elif len(self.priorityQueue[0]) > 0:
            self.move = self.priorityQueue[0][0]
        
        
        # store next move into MakeMove.move
        #self.move = self.validMoves[0]
        
def push_edge(playerData, move, team):
    pass

def push_ps(playerData, move, team):
    #if playerData.tiles[move[]]
    if (move['position'][0] == 2) and ((move['position'][1] == 3) or (move['position'][1] == 4)):
        #moveType = 'ps'
        return True
    elif (move['position'][0] == 5) and ((move['position'][1] == 3) or (move['position'][1] == 4)):
        #moveType = 'ps'
        return True
    elif (move['position'][1] == 2) and ((move['position'][0] == 3) or (move['position'][0] == 4)):
        #moveType = 'ps'
        return True
    elif (move['position'][1] == 5) and ((move['position'][0] == 3) or (move['position'][0] == 4)):
        #moveType = 'ps'
        return True
    else:
        return False
    pass
    
def _priorityZeroOrFour_(playerData,move,team):
    """
    _priorityZero_ : playerData move team
        
    """
    #moveType = ''
    # dismiss if wrong position
    if (move['position'][0] == 0):
        #moveType = 'nBorder'
        if (playerData.tiles[move['position']].routeMap[0] == 7) or (playerData.tiles[move['position']].routeMap[0] == 3):
            pass
        elif (playerData.tiles[move['position']].routeMap[1] == 6) or (playerData.tiles[move['position']].routeMap[1] == 2):
            pass
        else:
            return False 
    elif (move['position'][0] == 7):
        #moveType = 'sBorder'
        if (playerData.tiles[move['position']].routeMap[4] == 7) or (playerData.tiles[move['position']].routeMap[4] == 3):
            pass
        elif (playerData.tiles[move['position']].routeMap[5] == 6) or (playerData.tiles[move['position']].routeMap[5] == 2):
            pass
        else:
            return False 
    elif (move['position'][1] == 0):
        #moveType = 'wBorder'
        if (playerData.tiles[move['position']].routeMap[6] == 1) or (playerData.tiles[move['position']].routeMap[6] == 5):
            pass
        elif (playerData.tiles[move['position']].routeMap[7] == 0) or (playerData.tiles[move['position']].routeMap[1] == 4):
            pass
        else:
            return False 
    elif (move['position'][1] == 7):
        #moveType = 'eBorder'
        if (playerData.tiles[move['position']].routeMap[2] == 1) or (playerData.tiles[move['position']].routeMap[2] == 5):
            pass
        elif (playerData.tiles[move['position']].routeMap[3] == 0) or (playerData.tiles[move['position']].routeMap[3] == 4):
            pass
        else:
            return False 
    elif (move['position'][0] == 2) and ((move['position'][1] == 3) or (move['position'][1] == 4)):
        #moveType = 'ps'
        return True
    elif (move['position'][0] == 5) and ((move['position'][1] == 3) or (move['position'][1] == 4)):
        #moveType = 'ps'
        return True
    elif (move['position'][1] == 2) and ((move['position'][0] == 3) or (move['position'][0] == 4)):
        #moveType = 'ps'
        return True
    elif (move['position'][1] == 5) and ((move['position'][0] == 3) or (move['position'][0] == 4)):
        #moveType = 'ps'
        return True
    else:
        return False
    
