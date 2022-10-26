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