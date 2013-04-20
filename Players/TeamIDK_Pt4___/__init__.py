"""
Cable Car: Student Computer Player

Complete these function stubs in order to implement your AI.
Author: Adam Oest (amo9149@rit.edu)
Author: Jenny Zhen (jxz6853@rit.edu)
Author: Neil Zimmerman (nxz3937@gmail.com)
"""

from Model.interface import PlayerMove
from playerData import PlayerData
from tileData import TileData
from carData import CarData
from makeMoves import MakeMove

def init(playerId, numPlayers, startTile, logger, arg = "None"):
    """The engine calls this function at the start of the game in order to:
        -tell you your player id (0 through 5)
        -tell you how many players there are (1 through 6)
        -tell you what your start tile is (a letter a through i)
        -give you an instance of the logger (use logger.write("str") 
            to log a message) (use of this is optional)
        -inform you of an additional argument passed 
            via the config file (use of this is optional)
        
    Parameters:
        playerId - your player id (0-5)
        numPlayers - the number of players in the game (1-6)
        startTile - the letter of your start tile (a-j)
        logger - and instance of the logger object
        arg - an extra argument as specified via the config file (optional)

    You return:
        playerData - your player data, which is any data structure
                     that contains whatever you need to keep track of.
                     Consider this your permanent state.
    """
    
    # Put your data in here.
    # This will be permanently accessible by you in all functions.
    # It can be an object, list, or dictionary
    playerData = PlayerData(logger, playerId, startTile, numPlayers)

    # This is how you write data to the log file
    playerData.logger.write("Player %s starting up" % playerId)
    
    # This is how you print out your data to standard output (not logged)
    print(playerData)
    
    # initialize dictionary of tile objects
    for row in range(8):
        for col in range(8):
            if ((row == 3 or row == 4) and (col == 3 or col == 4)):
                playerData.tiles[(row,col)] = TileData(row, col, 'ps', 0)
            else:
                playerData.tiles[(row,col)] = TileData(row, col)
    
    return playerData

def move(playerData):  
    """The engine calls this function when it wants you to make a move.
    
    Parameters:
        playerData - your player data, 
            which contains whatever you need to keep track of
        
    You return:
        playerData - your player data, 
            which contains whatever you need to keep track of
        playerMove - your next move
    """
    
    playerData.logger.write("move() called")
    
    # generate next move
    thisMove = MakeMove(playerData)

    # Populate these values
    playerId = playerData.playerId # 0-5 accesses ID stored with playerData
    position = thisMove.move['position'] # (row, column)
    tileName = thisMove.move['tileName'] # a-j
    rotation = thisMove.move['rotation'] # 0-3 (0 = north, 1 = east, 2 = south, 3 = west)
    
    playerMove = PlayerMove(playerId, position, tileName, rotation)
    
    # setTile() for my move
    playerData.tiles[playerMove.position].setTile(playerMove.tileName,playerMove.rotation)
    
    return playerData, playerMove

def move_info(playerData, playerMove, nextTile):
    """The engine calls this function to notify you of:
        -other players' moves
        -your and other players' next tiles
        
    The function is called with your player's data, as well as the valid move of
    the other player.  Your updated player data should be returned.
    
    Parameters:
        playerData - your player data, 
            which contains whatever you need to keep track of
        playerMove - the move of another player in the game, or None if own move
        nextTile - the next tile for the player specified in playerMove, 
                    or if playerMove is None, then own next tile
                    nextTile can be none if we're on the last move
    You return:
        playerData - your player data, 
            which contains whatever you need to keep track of
    """
    
    
    
    # setTile() for appropriate object
    if playerMove != None:
        playerData.tiles[playerMove.position].setTile(playerMove.tileName,playerMove.rotation)
    else:
        playerData.currentTile = nextTile
    
    playerData.logger.write("move_info() called")
    
    return playerData


################################# PART ONE FUNCTIONS #######################
# These functions are called by the engine during part 1 to verify your board 
# data structure
# If logging is enabled, the engine will tell you exactly which tests failed
# , if any

def tile_info_at_coordinates(playerData, row, column):
    """The engine calls this function during 
        part 1 to validate your board state.
    
    Parameters:
        playerData - your player data as always
        row - the tile row (0-7)
        column - the tile column (0-7)
    
    You return:
        tileName - the letter of the tile at the given coordinates (a-j), 
            or 'ps' if power station or None if no tile
        tileRotation - the rotation of the tile 
            (0 is north, 1 is east, 2 is south, 3 is west.
            If the tile is a power station, it should be 0.  
            If there is no tile, it should be None.
    """      
    
    # return data from appropriate tile object, stored in PlayerData.tiles
    ## dictionary
    tileName = playerData.tiles[(row,column)].tileId
    tileRotation = playerData.tiles[(row,column)].rotation
    
    return tileName, tileRotation

def route_complete(playerData, carId):
    """The engine calls this function 
        during part 1 to validate your route checking
    
    Parameters:
        playerData - your player data as always
        carId - the id of the car where the route starts (1-32)
        
    You return:
        isComplete - true or false depending on whether or not this car
             connects to another car or power station"""
    
    # get position of first tile
    myCar = CarData(carId)
    currTile = playerData.tiles[myCar.entryTile]
    currNode = myCar.entryNode
    # traverse route until complete or dead-end
    while True:
        exitNode = currTile.routeMap[currNode]
        if (exitNode == None):
            return False
        elif (currTile.isTerminalNode(exitNode) is True):
            myCar.complete = True
            return True
        elif (currTile.isPsNode(exitNode) is True):
            myCar.complete = True
            return True
        elif (exitNode == 1):
            currNode = 4
            currTile = playerData.tiles[(currTile.position[0]-1,currTile.position[1])]
        elif (exitNode == 3): 
            currNode = 6
            currTile = playerData.tiles[(currTile.position[0],currTile.position[1]+1)]
        elif (exitNode == 5): 
            currNode = 0
            currTile = playerData.tiles[(currTile.position[0]+1,currTile.position[1])]
        elif (exitNode == 7): 
            currNode = 2
            currTile = playerData.tiles[(currTile.position[0],currTile.position[1]-1)]


def route_score(playerData, carId):
    """The engine calls this function 
        during route 1 to validate your route scoring
    
    Parameters:
        playerData - your player data as always
        carId - the id of the car where the route starts (1-32)
        
    You return:
        score - score is the length of the current route from the carId.
                if it reaches the power station, 
                the score is equal to twice the length.
    """
    
    # get position of first tile
    myCar = CarData(carId)
    currTile = playerData.tiles[myCar.entryTile]
    currNode = myCar.entryNode
    
    # initialize score
    score = 1
    
    # traverse route until complete or dead-end
    while True:
        exitNode = currTile.routeMap[currNode]
        
        if (exitNode == None):
            score -= 1
            myCar.score = score
            return score
        elif (currTile.isTerminalNode(exitNode) is True):
            myCar.score = score
            return score
        elif (currTile.isPsNode(exitNode) is True):
            score *=2
            myCar.score = score
            return score
        elif (exitNode == 1): 
            score += 1
            currNode = 4
            currTile = playerData.tiles[(currTile.position[0]-1,currTile.position[1])]
        elif (exitNode == 3):
            score += 1
            currNode = 6
            currTile = playerData.tiles[(currTile.position[0],currTile.position[1]+1)]
        elif (exitNode == 5):
            score += 1
            currNode = 0
            currTile = playerData.tiles[(currTile.position[0]+1,currTile.position[1])]
        elif (exitNode == 7):
            score += 1
            currNode = 2
            currTile = playerData.tiles[(currTile.position[0],currTile.position[1]-1)]
    
    myCar.score = score
    return score

def game_over(playerData, historyFileName = None):
    """The engine calls this function after the game is over 
        (regardless of whether or not you have been kicked out)

    You can use it for testing purposes or anything else you might need to do...
    
    Parameters:
        playerData - your player data as always       
        historyFileName - name of the current history file, 
            or None if not being used 
    """
    # Test things here, changing the function calls...
    print "History File: %s" % historyFileName
    print "If it says False below, you are doing something wrong"
    
    if historyFileName == "example_complete_start.data":
        print tile_info_at_coordinates(playerData, 5, 2) == ('e', 0)
        print route_complete(playerData, 1) == True
        print route_score(playerData, 1) == 3
    elif historyFileName == "SECOND_HISTORY_FILE_NAME":
        print "Second history file test cases here..."
    elif historyFileName == "THIRD_HISTORY_FILE_NAME":
        print "Third history file test cases here..."
    
    #print scores and get highest
    scores = getScores(playerData)
    playerNum = 0
    highestScore = [(None, 0)]
    
    for score in scores:
        print('Player ' + str(playerNum) + ": score = " + str(scores[playerNum]) )
        if (scores[playerNum] > highestScore[0][1]):
            highestScore = [(playerNum, score)]
        elif (scores[playerNum] == highestScore[0][1]):
            highestScore.append((playerNum, score))
        playerNum += 1
    
    # print winner
    if len(highestScore) == 1:
        print("\nPlayer #" + str(highestScore[0][0]) + " has won.")
    else:
        result = "\nPlayers "
        j = 1
        for player in highestScore:
            result += "#" + str(player[0])
            if j != len(highestScore):
                result += ','
            j+=1
        result += " have won."
        print(result)

def getCars(playerData):
    numPlayers = playerData.numPlayers
    carList = [None for i in range(numPlayers)]
    if numPlayers == 1:
        carList = [i for i in range(33)] # [0,32]
    elif numPlayers == 2:
        carList[0] = [i for i in range(1, 33, 2)] #odd numbers, [1,31]
        carList[1] = [i for i in range(2, 34, 2)] #even numbers, [2,32]
    elif numPlayers == 3:
        carList[0] = [1, 4, 6, 11, 15, 20, 23, 25, 28, 31]
        carList[1] = [2, 7, 9, 12, 14, 19, 22, 27, 29, 32]
        carList[2] = [3, 5, 8, 10, 13, 18, 21, 24, 26, 30]
    elif numPlayers == 4:
        carList[0] = [4, 7, 11, 16, 20, 23, 27, 32]
        carList[1] = [3, 8, 12, 15, 19, 24, 28, 31]
        carList[2] = [1, 6, 10, 13, 18, 21, 25, 30]
        carList[3] = [2, 5, 9, 14, 17, 22, 26, 29]
    elif numPlayers == 5:
        carList[0] = [1, 5, 10, 14, 22, 28]
        carList[1] = [6, 12, 18, 23, 27, 32]
        carList[2] = [3, 7, 15, 19, 25, 29]
        carList[3] = [2, 9, 13, 21, 26, 30]
        carList[4] = [4, 8, 11, 20, 24, 31]
    elif numPlayers == 6:
        carList[0] = [1, 5, 10, 19, 27]
        carList[1] = [2, 11, 18, 25, 29]
        carList[2] = [4, 8, 14, 21, 26]
        carList[3] = [6, 15, 20, 24, 31]
        carList[4] = [3, 9, 13, 23, 30]
        carList[5] = [7, 12, 22, 28, 32]
    return carList

def getScores( playerData ):
    """
    getScores( playerData ) -> list
    returns list of each player's score, indexed by player #
    """
    score = 0
    scores = []
    numPlayers = playerData.numPlayers
    carList = getCars(playerData)
    
    for player in range(numPlayers):
        for car in carList[player]:
            score += int(route_score(playerData, int(car)))
        scores.append(score)
        score = 0
    
    return scores
    