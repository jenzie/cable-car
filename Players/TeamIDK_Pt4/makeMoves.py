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
            if (push_edge(tempPlayer, move, 'us') == 1) or (push_ps(tempPlayer, move, 'them') == 1):
                priority = 1
            if (push_edge(tempPlayer, move, 'them') == 3) or (push_ps(tempPlayer, move, 'us') == 3):
                priority = 3
            if (_priorityZeroOrFour_(tempPlayer,move,'them') == 0) or (_priorityZeroOrFour_(tempPlayer,move,'us') == 4):
                priority = 4
            else:
                pass
            ##### END perform testing ####
            
            #place appropriate moves into 4
            if priority == 4:
                self.priorityQueue[4].append(move)
                break
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
        #print("### PRIORITY QUEUE ###")
        #for i in range(5):
        #    print str(4 - i) + " => " + str(self.priorityQueue[4 - i])
        
    
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
    moveClass = ['',None]
    x = move['position'][1]
    y = move['position'][0]
    if ((x == 0) or (x == 7)) and ((y == 0) or (y == 1) or (y == 2) or (y == 3) or (y == 4) or (y == 5) or (y == 6) or (y == 7)):
        #0's/7's column
        moveClass[0] = 'border'
    elif ((y == 0) or (y == 7)) and ((y == 0) or (x == 1) or (x == 2) or (x == 3) or (x == 4) or (x == 5) or (x == 6) or (x == 7)):
        #0's/7's row
        moveClass[0] = 'border'
    else:
        return False
    if moveClass[0] == 'border':
        if team == "us":
            if playerData.carList[playerData.playerId].count(moveClass[1]) > 0:
                return 1
        elif team == 'them':
            if playerData.carList[playerData.playerId].count(moveClass[1]) > 0:
                return 3

def push_ps(playerData, move, team):
    moveClass = ['',None]
    x = move['position'][1]
    y = move['position'][0]
    if ((x == 1) or (x == 6)) and ((y == 1) or (y == 2) or (y == 3) or (y == 4) or (y == 5) or (y == 6)):
        #1's/6's column
        moveClass[0] = 'ps'
    elif ((x == 2) or (x == 5)) and ((y == 1) or (y == 2) or (y == 5) or (y == 6)):
        #2's/5's column
        moveClass[0] = 'ps'
    elif ((x == 3) or (x == 4)) and ((y == 1) or (y == 6)):
        #'3's/4's column
        moveClass[0] = 'ps'
    else:
        return False
    if moveClass[0] == 'ps':
        if team == "us":
            if playerData.carList[playerData.playerId].count(moveClass[1]) > 0:
                return 3
        elif team == 'them':
            if playerData.carList[playerData.playerId].count(moveClass[1]) > 0:
                return 1
   
def _priorityZeroOrFour_(playerData,move,team):
    """
    _priorityZero_ : playerData move team
        
    """
    # moveclass = (type,origin)
    moveClass = ['',None]
    # dismiss if wrong position
    if (move['position'][0] == 0):
        #'nBorder'
        if (playerData.tiles[move['position']].routeMap[0] == 7) and (move['position'][1] != 0):
            if playerData.tiles[(move['position'][0],move['position'][1]-1)].routeMap[2] == 1:
                moveClass = ('border',playerData.tiles[move['position']].car)
        elif (playerData.tiles[move['position']].routeMap[0] == 3) and (move['position'][1] != 7):
            if playerData.tiles[(move['position'][0],move['position'][1]+1)].routeMap[6] == 1:
                moveClass = ('border',playerData.tiles[move['position']].car)
        elif (playerData.tiles[move['position']].routeMap[1] == 6) and (move['position'][1] != 0):
            if playerData.tiles[(move['position'][0],move['position'][1]-1)].routeMap[3] == 0:
                moveClass = ('border',playerData.tiles[(move['position'][0],move['position'][1]-1)].car)
        elif (playerData.tiles[move['position']].routeMap[1] == 2) and (move['position'][1] != 7):
            if playerData.tiles[(move['position'][0],move['position'][1]+1)].routeMap[7] == 0:
                moveClass = ('border',playerData.tiles[(move['position'][0],move['position'][1]+1)].car)
        else:
            return False
        
    elif (move['position'][0] == 7):
        #'sBorder'
        if (playerData.tiles[move['position']].routeMap[4] == 7) and (move['position'][1] != 0):
            if playerData.tiles[(move['position'][0],move['position'][1]-1)].routeMap[2] == 1:
                moveClass = ('border',playerData.tiles[move['position']].car)
        elif (playerData.tiles[move['position']].routeMap[4] == 3) and (move['position'][1] != 7):
            if playerData.tiles[(move['position'][0],move['position'][1]+1)].routeMap[6] == 1:
                moveClass = ('border',playerData.tiles[move['position']].car)
        elif (playerData.tiles[move['position']].routeMap[5] == 6) and (move['position'][1] != 0):
            if playerData.tiles[(move['position'][0],move['position'][1]-1)].routeMap[3] == 0:
                moveClass = ('border',playerData.tiles[(move['position'][0],move['position'][1]-1)].car)
        elif (playerData.tiles[move['position']].routeMap[5] == 2) and (move['position'][1] != 7):
            if playerData.tiles[(move['position'][0],move['position'][1]+1)].routeMap[6] == 1:
                moveClass = ('border',playerData.tiles[(move['position'][0],move['position'][1]+1)].car)
        else:
            return False
        
    elif (move['position'][1] == 0):
        #'wBorder'
        if (playerData.tiles[move['position']].routeMap[6] == 1) and (move['position'][0] != 0):
            if playerData.tiles[(move['position'][0]-1,move['position'][1])].routeMap[4] == 7:
                moveClass = ('border',playerData.tiles[move['position']].car)
        elif (playerData.tiles[move['position']].routeMap[6] == 5) and (move['position'][0] != 7):
            if playerData.tiles[(move['position'][0]+1,move['position'][1])].routeMap[0] == 7:
                moveClass = ('border',playerData.tiles[move['position']].car)
        elif (playerData.tiles[move['position']].routeMap[7] == 0) and (move['position'][0] != 0):
            if playerData.tiles[(move['position'][0]-1,move['position'][1])].routeMap[5] == 6:
                moveClass = ('border',playerData.tiles[(move['position'][0]-1,move['position'][1])].car)
        elif (playerData.tiles[move['position']].routeMap[7] == 4) and (move['position'][0] != 7):
            if playerData.tiles[(move['position'][0]+1,move['position'][1])].routeMap[1] == 6:
                moveClass = ('border',playerData.tiles[(move['position'][0]+1,move['position'][1])].car)
        else:
            return False
        
    elif (move['position'][1] == 7):
        #'eBorder'
        if (playerData.tiles[move['position']].routeMap[2] == 1) and (move['position'][0] != 0):
            if playerData.tiles[(move['position'][0]-1,move['position'][1])].routeMap[4] == 3:
                moveClass = ('border',playerData.tiles[move['position']].car)      
        elif (playerData.tiles[move['position']].routeMap[2] == 5) and (move['position'][0] != 7):
            if playerData.tiles[(move['position'][0]+1,move['position'][1])].routeMap[0] == 3:
                moveClass = ('border',playerData.tiles[move['position']].car)
        elif (playerData.tiles[move['position']].routeMap[3] == 0) and (move['position'][0] != 0):
            if playerData.tiles[(move['position'][0]-1,move['position'][1])].routeMap[5] == 2:
                moveClass = ('border',playerData.tiles[(move['position'][0]-1,move['position'][1])].car)     
        elif (playerData.tiles[move['position']].routeMap[3] == 4) and (move['position'][0] != 7):
            if playerData.tiles[(move['position'][0]+1,move['position'][1])].routeMap[5] == 2:
                moveClass = ('border',playerData.tiles[(move['position'][0]+1,move['position'][1])].car)
        else:
            return False
    elif (move['position'][0] == 2) and ((move['position'][1] == 3) or (move['position'][1] == 4)):
        #'nPS'
        moveClass[0] = 'ps'
        currNode = 5
    elif (move['position'][0] == 5) and ((move['position'][1] == 3) or (move['position'][1] == 4)):
        #'sPS'
        moveClass[0] = 'ps'
        currNode = 1
    elif (move['position'][1] == 2) and ((move['position'][0] == 3) or (move['position'][0] == 4)):
        #'wPS'
        moveClass[0] = 'ps'
        currNode = 3
    elif (move['position'][1] == 5) and ((move['position'][0] == 3) or (move['position'][0] == 4)):
        #'ePS'
        moveClass[0] = 'ps'
        currNode = 7
    else:
        return False
    
    # if ps, find root
    if moveClass[0] == 'ps':
        num = 0
        #print(move)
        # traverse route until complete or dead-end
        currTile = playerData.tiles[move['position']]
        while True:
            num += 1
            if num == 40:
                return False
            entNode = currTile.routeMap[currNode]
            if (currTile.position[0]==0) and (entNode == 0):
                moveClass[1] = currTile.car
                break
            elif (currTile.position[1]==7) and (entNode == 2):
                moveClass[1] = currTile.car
                break
            elif (currTile.position[0]==7) and (entNode == 4):
                moveClass[1] = currTile.car
                break
            elif (currTile.position[1]==0) and (entNode == 6):
                moveClass[1] = currTile.car
                break
            elif (entNode == None):
                return False
            elif (currTile.isPsNode(entNode)):
                return False
            elif (entNode == 0): 
                currNode = 5
                currTile = playerData.tiles[(currTile.position[0]-1,currTile.position[1])]
            elif (entNode == 2):
                currNode = 7
                currTile = playerData.tiles[(currTile.position[0],currTile.position[1]+1)]
            elif (entNode == 4):
                currNode = 1
                currTile = playerData.tiles[(currTile.position[0]+1,currTile.position[1])]
            elif (entNode == 6):
                currNode = 3
                currTile = playerData.tiles[(currTile.position[0],currTile.position[1]-1)]
    
    if moveClass[0] == 'border':
        if team == "us":
            if playerData.carList[playerData.playerId].count(moveClass[1]) > 0:
                return 0
            else:
                return 4
        elif team == 'them':
            if playerData.carList[playerData.playerId].count(moveClass[1]) > 0:
                return 4
            else:
                return 0
    if moveClass[0] == 'ps':
        if team == "us":
            if playerData.carList[playerData.playerId].count(moveClass[1]) > 0:
                return 4
            else:
                return 0
        elif team == 'them':
            if playerData.carList[playerData.playerId].count(moveClass[1]) > 0:
                return 0
            else:
                return 4
    
