# importing libraries
import pygame
import math
import random

class Tile:

    def calculate(self, end, start):

        self.g = self.parent.g + abs(self.parent.x - self.x)+ abs(self.parent.y - self.y)
        self.h = abs(self.x - end.x) + abs(self.y - end.y) #Make 0 for dejkarts
        self.f = self.g + self.h

    def getChildren(self):
        self.children.append(Tile([self.x - 1,self.y],self))
        self.children.append(Tile([self.x + 1,self.y],self))
        self.children.append(Tile([self.x,self.y - 1],self))
        self.children.append(Tile([self.x,self.y + 1],self))

	
    def __init__(self,pos,parent):
        self.children = []
        self.wall = False

        self.f = 0
        self.g = 0
        self.h = 0

        self.generation = 0

        self.x = pos[0]
        self.y = pos[1]

        if parent == "wall":
            self.wall = True

        if parent == "self":
            self.parent = self
        else:
            self.parent = parent
        
        if parent != "self" and parent != "wall":
            self.generation = parent.generation + 1


# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Initialising pygame
pygame.init()

# Initialise game window
pygame.display.set_caption('Astar Generator')

# FPS (frames per second) controller
fps = pygame.time.Clock()

# defining snake default Tile
windowSize = 900
game_window = pygame.display.set_mode((windowSize, windowSize))
worldmin = 30
worldmax = 50

# game over function
def game_over():
	
    time.sleep(4)
	
	# deactivating pygame library
    pygame.quit()
	
	# quit the program
    quit()


def drawTile(tile,size, color, speed):

    pygame.draw.rect(game_window, color,
						pygame.Rect(tile.x*size, tile.y*size, size, size))
    
    pygame.display.update()

    fps.tick(speed)



def aStarTest(Start):
    drawTile(Start,worldData[0],green, 5)
    Start.getChildren()

    for i in range(4):
        drawTile(Start.children[i],worldData[0],red, 5)

    game_over()

def aStartTest2(Start,End):
    drawTile(End, worldData[0], red, 5)
    drawTile(Start, worldData[0], green, 5)

    openList = [Start]
    closedList = []

    searching = True
    while(searching):
        best = 0
        for i in range(len(openList)):
            openList[i].calculate(End, Start)
            if openList[i].f < openList[best].f:
                best = i
        if(openList[best].f == 1):
            searching = False
            closedList.append(openList.pop(best))
            return closedList

        closedList.append(openList.pop(best))

        closedList[len(closedList) - 1].getChildren()

        for i in range(len(closedList[len(closedList) - 1].children)):
            openList.insert(0,closedList[len(closedList) - 1].children[i])


# its 2:00am and im attempting to add breadth search... god help me
# sorry if i fuck up future matt but you know cant sleep lmao.
# annyway checking for
# when you run into a situation where you can no longer make a child search closedList for a tile witht he lowest f value. continue from there
# if a path is making children and the child appears on the open list with a smaller f value then do not make the child.
# if a path is making a child and the path appears on the closed List do not make the child
# also check to see if a child is a wall


# Dev log. it fucking works bois lets go!!!! 
# also cool test case idea. randomly generate seeds that create random walls from 0 to 30. 
# then if the pathfinder fails log the seeds in terminal to veiw. run 100 times. also create a wayy to load seeds. 
# not too hard right?

#its fuckin 6:00am breh... sleep? maybe?

#cya

def aStarTest3(Start, End, walls):

    openList = [Start]
    closedList = []

    searching = True
    while(searching):
        best = 0
        for i in range(len(openList)):
            if(openList[i].f == 0):
                openList[i].calculate(End, Start)
            if openList[i].f < openList[best].f:
                best = i
        if openList:
            if(openList[best].x == End.x and openList[best].y == End.y):
                searching = False
                closedList.append(openList.pop(best))
                return closedList
        else:
            return "NO PATH"

        closedList.append(openList.pop(best))

        closedList[len(closedList) - 1].getChildren()
        
        #for i in range(len(closedList[len(closedList) - 1].children)):
        for tile in closedList[len(closedList) - 1].children:
            tile.calculate(End, Start)
            create = True
            if closedList:
                for closedTile in closedList:
                    if(tile.x == closedTile.x and tile.y == closedTile.y):
                        create = False
            if openList:
                for openTile in openList:
                    if(tile.x == openTile.x and tile.y == openTile.y and tile.f >= openTile.f):
                        create = False
            for wall in walls:
                if tile.x == wall.x and tile.y == wall.y:
                    create = False
                

            if(create):
                openList.insert(0,tile)


# decide how big i want the world
# use window size to decide tile size
# window size SET
# use seed to generate values
# generate start and end at random
# generate wall at random up to 30 walls
# if path could not get to the end or it takes over 5 seconds to do so return the seed to a list of FailedRuns

def randomWorldGen():

    #create seed

    seed = random.randint(0,999999)

    random.seed(seed)

    worldSize = random.randint(worldmin,worldmax)

    wallPos = initializeMapBoardrs(worldSize)
    startPos = [random.randint(1, (worldSize-2)), random.randint(1, (worldSize-2))]

    endPos = startPos

    if endPos == startPos:
        endPos = [random.randint(1, (worldSize-2)), random.randint(1, (worldSize-2))]

    wallAmmount = random.randint((math.floor((worldSize-1) / .1)), (math.floor((worldSize-1) / .05)))

    for i in range(wallAmmount):
        validWall = False
        while not validWall:
            wall = [random.randint(0, (worldSize-1)),random.randint(0, (worldSize-1))]

            if((wall != startPos) and (wall != endPos)):
                if wallPos:
                    for walls in wallPos:
                        if(wall != walls):
                            validWall = True  
                else:
                    validWall = True
            
            else:
                validWall = False

            if validWall:
                wallPos.append(wall)
    
    tileSize = windowSize / worldSize

    packet = [tileSize,startPos,endPos,wallPos,wallAmmount,seed]

    return packet


def printPath(path,tileSize, color, speed):
    for tile in path:
        drawTile(tile, tileSize, color, speed)

def createPath(path):

    currentTile = path[len(path) - 1]
    newPath = []

    while(currentTile != path[0]):
        newPath.insert(0, currentTile)
        currentTile = currentTile.parent

        
    return newPath

def worldInit(start, end, walls, worldData):

    drawTile(start, worldData[0], blue, 600)
    drawTile(end, worldData[0], red, 600)

    for wall in walls:
        drawTile(wall, worldData[0], white, 600)

def aStarFailTest(loop):

    failedSeeds = []

    for i in range(loop):
        print(i)
        worldData = randomWorldGen()
        seed = worldData[5]


        Start = Tile(worldData[1],"self")
        End = Tile(worldData[2],"self")
        walls = []

        for wall in worldData[3]:
            walls.append(Tile(wall,"wall"))

        pygame.event.get()

        path = aStarTest3(Start, End, walls)

        if path == "NO PATH":
            failedSeeds.append(seed)
        
    return failedSeeds

def aStarStart(loop):

    for i in range(loop):

        worldData = randomWorldGen()


        Start = Tile(worldData[1],"self")
        End = Tile(worldData[2],"self")
        walls = []

        for wall in worldData[3]:
            walls.append(Tile(wall,"wall"))

        worldInit(Start, End, walls,worldData)

        pygame.event.get()

        path = aStarTest3(Start, End, walls)

        if path != "NO PATH":
            newPath = createPath(path)

            printPath(path, worldData[0], blue, 60)

            printPath(newPath, worldData[0], green, 30)
        
        game_window.fill(black)

    game_over
    

def loadSeed(seed):

    random.seed(seed)

    worldSize = random.randint(worldmin,worldmax)

    startPos = [random.randint(0, (worldSize-1)), random.randint(0, (worldSize-1))]

    endPos = startPos

    while(startPos == endPos):

        endPos = [random.randint(0, worldSize-1), random.randint(0, worldSize-1)]


        #################### TO DO ###############

        # when initialize map boarder gets called it will cover up the start of end node.
        # need to call boarder before declaring the start / end node
        # check if the start or end node will be placed on a boparder
        # if so create new start loacation
        

    wallPos = initializeMapBoardrs(worldSize)

    wallAmmount = random.randint((math.floor((worldSize-1) / .2)), (math.floor((worldSize-1) / .1)))

    for i in range(wallAmmount):
        validWall = False
        while not validWall:
            wall = [random.randint(0, (worldSize-1)),random.randint(0, (worldSize-1))]

            if((wall != startPos) and (wall != endPos)):
                if wallPos:
                    for walls in wallPos:
                        if(wall != walls):
                            validWall = True  
                else:
                    validWall = True
            
            else:
                validWall = False

            if validWall:
                wallPos.append(wall)
    
    tileSize = windowSize / worldSize

    packet = [tileSize,startPos,endPos,wallPos,wallAmmount,seed]

    return packet

def LongestPath(Start, End, walls):

    openList = [Start]
    closedList = []

    searching = True
    while(searching):
        worst = 0
        for i in range(len(openList)):
            if(openList[i].f == 0):
                openList[i].calculate(End, Start)
            if openList[i].f > openList[worst].f:
                worst = i
        if not openList:
            oldest = 0
            counter = 0
            for Tile in closedList:
                if Tile.generation > closedList[oldest].generation:
                    oldest = counter
                counter = counter + 1
            
            closedList.append(closedList[oldest])

            return closedList
                

        closedList.append(openList.pop(worst))

        closedList[len(closedList) - 1].getChildren()
        
        #for i in range(len(closedList[len(closedList) - 1].children)):
        for tile in closedList[len(closedList) - 1].children:
            tile.calculate(End, Start)
            create = True
            if closedList:
                for closedTile in closedList:
                    if(tile.x == closedTile.x and tile.y == closedTile.y):
                        create = False
            if openList:
                for openTile in openList:
                    if(tile.x == openTile.x and tile.y == openTile.y and tile.f <= openTile.f):
                        create = False
            for wall in walls:
                if tile.x == wall.x and tile.y == wall.y:
                    create = False

            if(create):
                openList.insert(0,tile)







# Main Function

	#initiate everything maybe?

#main loop

def test1():
    loop = 5

    failedSeeds = aStarFailTest(loop)

    if failedSeeds:
        
        #load seed

        #initialie vars
        for seed in failedSeeds:
            worldData = loadSeed(seed)

            Start = Tile(worldData[1],"self")
            End = Tile(worldData[2],"self")
            walls = []

            for wall in worldData[3]:
                walls.append(Tile(wall,"wall"))

            worldInit(Start, End, walls,worldData)

            time.sleep(4)

            game_window.fill(black)
    
    else: 
        print("no failed seeds")
    
    print("Finished checking seeds on batch ", loop)
    game_over()

def initializeMapBoardrs(worldSize):

    walls = []

    for x in range(worldSize):
        wall = [x, 0]
        walls.append(wall)
        wall = [x, (worldSize - 1)]
        walls.append(wall)


    for y in range(worldSize):
        wall = [0, y]
        walls.append(wall)
        wall = [(worldSize - 1), y]
        walls.append(wall)
    
    return walls

while True:

    aStarStart(100)
    




