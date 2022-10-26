# importing libraries
import pygame
import time
import random
import math

class Tile:

    def calculate(self, end, start):

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


snake_speed = 30

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

# defining first 4 blocks of snake body
snake_body = [[1, 1]]

# fruit position
fruit_position = [5, 5]

fruit_spawn = True

# setting default snake direction towards
# right
direction = 'RIGHT'
change_to = direction

# initial score
score = 0

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
	#pygame.display.flip()
	
	# after 2 seconds we will quit the program
	time.sleep(3)
	
	# deactivating pygame library
	pygame.quit()
	
	# quit the program
	quit()


def randomSnake(change_to):

	dir = change_to

	randDir = random.randint(0,3)
	if(randDir == 0):
		dir = 'UP'
	if(randDir == 1):
		dir = 'DOWN'
	if(randDir == 2):
		dir = 'LEFT'
	if(randDir == 3):
		dir = 'RIGHT'

	return dir

def playerSnake(change_to):

	dir = change_to

	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				dir = 'UP'
			if event.key == pygame.K_DOWN:
				dir = 'DOWN'
			if event.key == pygame.K_LEFT:
				dir = 'LEFT'
			if event.key == pygame.K_RIGHT:
				dir = 'RIGHT'
	return dir

def fastSnake(change_to,snake_position, fruit_position):

	distanceX = snake_position[0] - fruit_position[0]
	distanceY = snake_position[1] - fruit_position[1]


	if(change_to == 'RIGHT'):
		if(distanceX < 0):
			return 'RIGHT'
		else:
			if(distanceY < 0):
				return 'DOWN'
			else:
				return 'UP'

	if(change_to == 'LEFT'):
		if(distanceX > 0):
			return 'LEFT'
		else:
			if(distanceY < 0):
				return 'DOWN'
			else:
				return 'UP'

	if(change_to == 'DOWN'):
		if(distanceY < 0):
			return 'DOWN'
		else:
			if(distanceX < 0):
				return 'RIGHT'
			else:
				return 'LEFT'

	if(change_to == 'UP'):
		if(distanceY > 0):
			return 'UP'
		else:
			if(distanceX < 0):
				return 'RIGHT'
			else:
				return 'LEFT'
		
def aSnake(Start, End, walls):
	
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

def getDirections(newPath,snake_position):
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
	
	return change_to

def createPath(path):

    currentTile = path[len(path) - 1]
    newPath = []

    while(currentTile != path[0]):
        newPath.insert(0, currentTile)
        currentTile = currentTile.parent

        
    return newPath

def printPath(path,tileSize, color, speed):
    for tile in path:
        drawTile(tile, tileSize, color, speed)
	

	
def drawTile(tile,size, color, speed):

    pygame.draw.rect(game_window, color,
						pygame.Rect(tile.x*size, tile.y*size, size, size))
    

def initializeMapBoardrs():

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

def aSnakeOpen(Start, End, walls):
	
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
			return closedList

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

def findTail(headTile, snakeTiles, damageTiles):

	potentials = []
	i = len(snakeTiles) - 1
	while(i >= 0):
		potentials.append(Tile([snakeTiles[i].x - 1, snakeTiles[i].y], "self"))
		potentials.append(Tile([snakeTiles[i].x - 1, snakeTiles[i].y], "self"))
		potentials.append(Tile([snakeTiles[i].x, snakeTiles[i].y - 1], "self"))
		potentials.append(Tile([snakeTiles[i].x, snakeTiles[i].y - 1], "self"))
		i = i - 1


	

	i = len(potentials) - 1
	looping = True
	path = "NO PATH"
	while(looping and i >= 0):

		if potentials[i].x != snake_position[0] and potentials[i].y != snake_position[1]:
			path = aSnake(headTile, potentials[i],damageTiles)
		i = i - 1

		if path != "NO PATH":
			looping = False
			i = i + 1
			print(i)
		
	path = findLongestPath(headTile, potentials[i], damageTiles)

	return path



def findLongestPath(Start, End, walls):
	openList = [Start]
	closedList = []

	searching = True
	while(searching):
		best = 0
		for i in range(len(openList)):
			if(openList[i].f == 0):
				openList[i].calculate(End, Start)
			if openList[i].f > openList[best].f:
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




class Htile:
	
	def __init__(self,parent,direction):

		self.alive = True

		if parent == "NONE":
			self.parent = parent
			self.id = 0
		else:
			self.parent = parent
			self.id = parent.id + 1

		if direction == "RIGHT":
			self.x = parent.x + 1
			self.y = parent.y
		elif direction == "LEFT":
			self.x = parent.x - 1
			self.y = parent.y
		elif direction == "DOWN":
			self.x = parent.x
			self.y = parent.y + 1
		elif direction == "UP":
			self.x = parent.x
			self.y = parent.y - 1
		elif direction == "NONE":
			self.x = 0
			self.y = 0

class Hcycle:
	def __init__(self):
		
		self.cycle = [Htile("NONE","NONE")]

		for i in range(worldSize * 2):
			self.cycle.insert(Htile(self.cycle[i]))





# main function

walls = initializeMapBoardrs()
while True:

	#initiate everything maybe?
	pygame.event.get()

	snakeTiles = []
	wallTiles = []
	damageTiles = []
	fruitTile = Tile(fruit_position,"self")
	headTile = Tile(snake_position,"self")

	
	for wall in walls:
		wallTiles.append(Tile(wall,"wall"))
		damageTiles.append(Tile(wall,"wall"))
	for link in snake_body:
		snakeTiles.append(Tile(link,"wall"))
		damageTiles.append(Tile(link,"wall"))

	
	# handling key events
	path  = aSnake(headTile, fruitTile, damageTiles)

	if path != "NO PATH":
		newPath = createPath(path)

		change_to = getDirections(newPath, snake_position)
	else:
			
		path = LongestPath(headTile, fruitTile, damageTiles)

		if path == "NO PATH":
			game_over()



		newPath = createPath(path)
		if len(newPath) <=1:
			game_over()

		if not newPath:
			game_over()


		if newPath != "No PATH":
			if len(newPath) >=1:
				change_to = getDirections(newPath, snake_position)


	# If two keys pressed simultaneously
	# we don't want snake to move into twodsaw
	# directions simultaneously
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

	# Snake body growing mechanism
	# if fruits and snakes collide then scores
	# will be incremented by 10
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
	game_window.fill(black)
	
	for tile in snakeTiles:
		drawTile(tile, tileSize, green, 60)
	for tile in wallTiles:
		drawTile(tile,tileSize,white,60)
	drawTile(fruitTile,tileSize,red, 60)

	# Game Over conditions
	if snake_position[0] < 0 or snake_position[0] > window_x-tileSize:
			game_over()
	if snake_position[1] < 0 or snake_position[1] > window_y-tileSize:
			game_over()


	# Touching the snake body
	for block in snake_body[1:]:
		if snake_position[0] == block[0] and snake_position[1] == block[1]:
			game_over()


	# displaying score countinuously
	show_score(1, white, 'times new roman', 20)

	# Refresh game screen
	pygame.display.update()

	# Frame Per Second /Refres Rate
	fps.tick(snake_speed)


	




# aStarTest3(Start, End, Walls)

# need to make a function to turn all the snake_body into walls







#path tikes can be occupoied open and have a path nubmer value.



#Hamoltonian path snake 

# create a hamalotnian path starting fromt he top left of the screen.
# go right untill wall then go down untill wall then double back untill start.
# look at snakes current pose. find next pose in path.




# IMPROVED hamaltonian path

# snake can skip portions of the hamaltonian as long as the path 

# when 60% of map is covered follow hamaltonian cycle

# if apple in on a live tile use a* to get there favoring straight lines

# if apple in on dead tile follow hamaltonian cycle untill apple is on alive tile.






		



def hamaltonianSnake():
	pass