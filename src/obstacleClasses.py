from cmu_graphics import *

class Obstacle:
    def __init__(self, x0, y0, width, height):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x0 + width
        self.y1 = y0 + height
        
        self.width = width
        self.height = height

    def coorQuadruple(self):
        return self.x0, self.y0, self.width, self.height
    
    @staticmethod
    def distance(x0, y0, x1, y1):
        return ((x1 - x0)**2 + (y1 - y0)**2)**(1/2) 

class SafeSpot(Obstacle):
    def __init__(self, app, x0, y0, width, height):
        super().__init__(x0, y0, width, height)
        self.app = app

    def coorQuadruple(self):
        return self.x0, self.y0, self.width, self.height

class Air(Obstacle):
    def __init__(self, app, x0, y0, width, height):
        super().__init__(x0, y0, width, height)
        self.app = app

    def coorQuadruple(self):
        return self.x0, self.y0, self.width, self.height

class Water(Obstacle):
    def __init__(self, app, x0, y0, width, height):
        super().__init__(x0, y0, width, height)
        self.app = app

    def coorQuadruple(self):
        return self.x0, self.y0, self.width, self.height
  
class ObstacleHolder:
    def __init__(self, app):
        self.app = app
        self.terrainObstacles = ['T']
        self.nonObstacles = [' ', '~', 'S', 'W']
        self.airObstacles = ['T', ' ']
        self.waterObstacles = ['S']
        self.safetyObstacles = ['~', ' ', 'T']
        self.airSafe = ['S']

    def createObstacleClassList(self):
        self.app.obstacles = []

        rows, cols = len(self.app.terrain), len(self.app.terrain[0])
        width, height = ObstacleHolder.getCellSize(self.app, rows, cols)

        for row in range(rows):
            for col in range(cols):
            
                if self.app.levelClass.getLevel() == 'water':
                    # adds air "obstacles"
                    if self.app.terrain[row][col] == 'S': 
                        if ObstacleHolder.shouldAddObstacle(self, 'S', ['W'], row, col, rows, cols):
                            top, left = ObstacleHolder.getPixelTL(self.app, row, col, rows, cols)
                            self.app.obstacles.append(Air(self.app, left, top, width, height))

                    elif self.app.terrain[row][col] == 'W':
                        if ObstacleHolder.shouldAddObstacle(self, 'W', self.waterObstacles, row, col, rows, cols):
                            top, left = ObstacleHolder.getPixelTL(self.app, row, col, rows, cols)
                            self.app.obstacles.append(Water(self.app, left, top, width, height))
                
                if self.app.terrain[row][col] in self.terrainObstacles:
                    if ObstacleHolder.shouldAddObstacle(self, 'T', self.nonObstacles, row, col, rows, cols):
                        top, left = ObstacleHolder.getPixelTL(self.app, row, col, rows, cols)
                        self.app.obstacles.append(Obstacle(left, top, width, height))
                elif self.app.terrain[row][col] == ' ':
                    if ObstacleHolder.shouldAddObstacle(self, ' ', ['S'], row, col, rows, cols):
                        top, left = ObstacleHolder.getPixelTL(self.app, row, col, rows, cols)
                        self.app.obstacles.append(Air(self.app, left, top, width, height))
                    elif row == rows - 1 or col == cols - 1 or row == 0 or col == 0:
                        top, left = ObstacleHolder.getPixelTL(self.app, row, col, rows, cols)
                        self.app.obstacles.append(Air(self.app, left, top, width, height))
                elif self.app.terrain[row][col] == 'S':
                    if ObstacleHolder.shouldAddObstacle(self, 'S', self.safetyObstacles, row, col, rows, cols):
                        top, left = ObstacleHolder.getPixelTL(self.app, row, col, rows, cols)
                        self.app.obstacles.append(SafeSpot(self.app, left, top, width, height))
                    elif row == rows - 1 or col == cols - 1 or row == 0 or col == 0:
                        top, left = ObstacleHolder.getPixelTL(self.app, row, col, rows, cols)
                        self.app.obstacles.append(SafeSpot(self.app, left, top, width, height))

    @staticmethod
    def shouldAddObstacle(self, obstacle, obstacleList, row, col, rows, cols):
        if self.app.terrain[row][col] == obstacle: 
            if (row == rows - 1) and (col == cols - 1): #if on the bottom right corner
                if ((row > 0 and self.app.terrain[row - 1][col] in obstacleList) or 
                    (col > 0 and self.app.terrain[row][col - 1] in obstacleList)):
                        return True
                    
            elif row == rows - 1: # if on the very bottom
                if ((row > 0 and self.app.terrain[row - 1][col] in obstacleList) or 
                    (col < cols - 1 and self.app.terrain[row][col + 1] in obstacleList) or 
                    (col > 0 and self.app.terrain[row][col - 1] in obstacleList)):
                        return True

            elif col == cols - 1: #if on the very right
                if ((row < rows - 1 and self.app.terrain[row + 1][col] in obstacleList) or 
                    (row > 0 and self.app.terrain[row - 1][col] in obstacleList) or 
                    (col > 0 and self.app.terrain[row][col - 1] in obstacleList)):
                        return True

            elif (-1 < row < rows - 1) and (-1 < col < cols - 1): #rest of the platform
                if (self.app.terrain[row + 1][col] in obstacleList or 
                    self.app.terrain[row - 1][col] in obstacleList or 
                    self.app.terrain[row][col + 1] in obstacleList or 
                    self.app.terrain[row][col - 1] in obstacleList):
                        return True
        else: 
            return False
    
    @staticmethod
    def getPixelTL(app, row, col, rows, cols):
        width, height = ObstacleHolder.getCellSize(app, rows, cols)
        top = row * height 
        left = col * width 
        return top, left

    @staticmethod
    def getCellSize(app, rows, cols):
        width = app.width / cols
        height = app.height / rows 

        return width, height

def ifPlayerCenterInside(cx, cy, obstacleList, Class):
        for obstacle in obstacleList:
            if isinstance(obstacle, Class):
                if (obstacle.x0 < cx < obstacle.x0 + obstacle.width and
                    obstacle.y0 < cy < obstacle.y0 + obstacle.height):
                        return True
        return False

class Spiderweb:
    def __init__(self, app, x0, y0, width, height, level):
        self.app = app
        self.x0 = x0
        self.y0 = y0
        self.width = width
        self.height = height
        self.level = level

    def coorQuadruple(self):
        return self.x0, self.y0, self.width, self.height
    
    def ifSameLevel(self, currLevel):
        return self.level == currLevel
    
    def drawSpiderweb(self):
        drawRect(self.x0, self.y0, self.width, self.height, fill = 'pink')

    @staticmethod
    def distance(x0, y0, x1, y1):
        return ((x1 - x0)**2 + (y1 - y0)**2)**(1/2) 

def indexOfNearbySpiderweb(spiderwebList):
    for i in range(len(spiderwebList)):
        spiderweb = spiderwebList[i]
        closestX = max(spiderweb.x0, min(app.player.cx, spiderweb.x0 + spiderweb.width))
        closestY = max(spiderweb.y0, min(app.player.cy, spiderweb.y0 + spiderweb.height))

        distanceX = app.player.cx - closestX
        distanceY = app.player.cy - closestY
        distance = (distanceX**2 + distanceY**2) ** (1/2)

        if distance < 20:
            return i
    return None