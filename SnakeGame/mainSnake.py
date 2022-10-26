# importing libraries
import pygame
import time
import random
import math
import Tile

snake_speed = 20

# Window size
window_x = 900
window_y = window_x
worldSize = 30
tileSize = math.floor(window_y / worldSize)

# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Initialising pygame
pygame.init()

# Initialise game window
pygame.display.set_caption('Snake Algo')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS (frames per second) controller
fps = pygame.time.Clock()

# defining snake default position
snake_position = [1, 1]
snake_body = [[1, 1]]
fruit_position = [5, 5]
wall_positions = []

fruit_spawn = True

alive = True

# setting default snake direction towards
# right
direction = 'RIGHT'
change_to = direction

# initial score
score = 0

class Tile:

    def calculate(self, end):

        self.g = self.parent.g + abs(self.parent.x - self.x)+ abs(self.parent.y - self.y)
        self.h = abs(self.x - end.x) + abs(self.y - end.y)
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

def drawTile(tile,size,color):

    pygame.draw.rect(game_window, color,
						pygame.Rect(tile[0]*size, tile[1]*size, size, size))

def show_score(choice, color, font, size):
	pass

	# creating font object score_font
	score_font = pygame.font.SysFont(font, size)
	
	# create the display surface object
	# score_surface
	score_surface = score_font.render('Score : ' + str(score), True, color)
	
	# create a rectangular object for the text
	# surface object
	score_rect = score_surface.get_rect()
	
	# displaying text
	game_window.blit(score_surface, score_rect)

def gameUpdate():

    global fps, snake_speed
    game_window.fill(black)

    for link in snake_body:
        drawTile(link, tileSize, green)
    for wall in wall_positions:
        drawTile(wall,tileSize,white)

    drawTile(fruit_position,tileSize,red)


    # displaying score countinuously
    show_score(1, white, 'times new roman', 20)

    # Refresh game screen
    pygame.display.update()

    # Frame Per Second /Refres Rate
    fps.tick(snake_speed)

def moveSnake():
    # If two keys pressed simultaneously
    # we don't want snake to move into twodsaw
    # directions simultaneously
    global direction, score,fruit_position, fruit_spawn, snake_position

    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_position[1] -= 1
    if direction == 'DOWN':
        snake_position[1] += 1
    if direction == 'LEFT':
        snake_position[0] -= 1
    if direction == 'RIGHT':
        snake_position[0] += 1


    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 1
        fruit_spawn = False
    else:
        snake_body.pop()
        
    if not fruit_spawn:
        invalid = True
        while invalid:
            invalid = False
            fruit_position = [random.randrange(1, ((window_x//tileSize) - 1)),
                        random.randrange(1, ((window_y//tileSize) - 1))]
            for pos in snake_body:
                if pos == fruit_position:
                    invalid = True
    fruit_spawn = True

def game_over():

	# creating font object my_font
	my_font = pygame.font.SysFont('times new roman', 50)
	
	# creating a text surface on which text
	# will be drawn
	game_over_surface = my_font.render(
		'Your Score is : ' + str(score), True, red)
	
	# create a rectangular object for the text
	# surface object
	game_over_rect = game_over_surface.get_rect()
	
	# setting position of the text
	game_over_rect.midtop = (window_x/2, window_y/4)
	
	# blit wil draw the text on screen
	game_window.blit(game_over_surface, game_over_rect)
	pygame.display.flip()
	
	# after 2 seconds we will quit the program
	time.sleep(3)
	
	# deactivating pygame library
	pygame.quit()
	
	# quit the program
	quit()

def checkGameOver():
    # Game Over conditions

    global snake_position, window_x, tileSize, snake_body
    if snake_position[0] < 0 or snake_position[0] > window_x-tileSize:
            game_over()
    if snake_position[1] < 0 or snake_position[1] > window_y-tileSize:
            game_over()


    # Touching the snake body
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

def playerGetDirection():

    global change_to

    dir = change_to

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                dir = 'UP'
            elif event.key == pygame.K_DOWN:
                dir = 'DOWN'
            elif event.key == pygame.K_LEFT:
                dir = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                dir = 'RIGHT'

    change_to = dir

def fastSnakeGetDirection():

    pygame.event.get()

    global change_to, snake_position, fruit_position

    distanceX = snake_position[0] - fruit_position[0]
    distanceY = snake_position[1] - fruit_position[1]


    if(change_to == 'RIGHT'):
        if(distanceX < 0):
            change_to = 'RIGHT'
        else:
            if(distanceY < 0):
                change_to = 'DOWN'
            else:
                change_to = 'UP'

    elif(change_to == 'LEFT'):
        if(distanceX > 0):
            change_to = 'LEFT'
        else:
            if(distanceY < 0):
                change_to = 'DOWN'
            else:
                change_to = 'UP'

    elif(change_to == 'DOWN'):
        if(distanceY < 0):
            change_to = 'DOWN'
        else:
            if(distanceX < 0):
                change_to = 'RIGHT'
            else:
                change_to = 'LEFT'

    elif(change_to == 'UP'):
        if(distanceY > 0):
            change_to = 'UP'
        else:
            if(distanceX < 0):
                change_to = 'RIGHT'
            else:
                change_to = 'LEFT'

def createPath(path):

    currentTile = path[len(path) - 1]
    newPath = []

    while(currentTile != path[0]):
        newPath.insert(0, currentTile)
        currentTile = currentTile.parent

        
    return newPath

def LongestPath(Start, End, walls):

    openList = [Start]
    closedList = []

    searching = True
    while(searching):
        worst = 0
        for i in range(len(openList)):
            if(openList[i].f == 0):
                openList[i].calculate(End)
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
            tile.calculate(End)
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

def getDirections(newPath):

    global change_to, snake_position
    if newPath[0].x == snake_position[0]:
        if newPath[0].y > snake_position[1]:
            change_to = "DOWN"
        else:
            change_to = "UP"
    else:
        if newPath[0].x > snake_position[0]:
            change_to = "RIGHT"
        else:
            change_to = "LEFT"
	
def aStarSnakeGetDirection():

    pygame.event.get()
    Start = []
    End = []
    walls = []

    Start = Tile(snake_position, "self")
    End = Tile(fruit_position, "self")

    for link in snake_body:
        walls.append(Tile(link,"wall"))


    path = aSnake(Start,End,walls)

    if path != "NO PATH":

        path = createPath(path)

        getDirections(path)  
        
    else:
            
        path = LongestPath(Start, End, walls)

        if path == "NO PATH":
            game_over()



        newPath = createPath(path)
        if len(newPath) <=1:
            game_over()

        if not newPath:
            game_over()


        if newPath != "No PATH":
            if len(newPath) >=1:
                getDirections(newPath)

def aSnake(Start, End, walls):

    openList = [Start]
    closedList = []

    searching = True
    while(searching):
        best = 0
        for i in range(len(openList)):
            if(openList[i].f == 0):
                openList[i].calculate(End)
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
            tile.calculate(End)
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


### SNAKE FUNCTIONS ###
def playerSnake():

    while alive:

        playerGetDirection()

        moveSnake()

        gameUpdate()

        checkGameOver()

def fastSnake():

    while alive:

        fastSnakeGetDirection()

        moveSnake()

        gameUpdate()

        checkGameOver()

def aStarSnake():

    while alive:

        aStarSnakeGetDirection()

        moveSnake()

        gameUpdate()

        checkGameOver()


# CHOOSE SNAKE #
def chooseSnake():
    snake = 0

    while snake == 0:

        print("What Snake simulation would you like to play?")
        print(" 1. Human Snake")
        print(" 2. fast Snake")
        print(" 3. A* Snake")
        print(" 4. Hamaltonian Snake")
        print(" 5. Hamaltonian skip Snake")
        print(" 6. Hamaltonian repair snake")

        snake = int(input("Enter number: "))


    if snake == 1:
        playerSnake()
    elif snake == 2:
        fastSnake()
    elif snake == 3:
        aStarSnake()
    elif snake == 4:
        pass
    elif snake == 5:
        pass
    elif snake == 6:
        pass


########### START MAIN FUNCTION ###########
while True:

    chooseSnake()












