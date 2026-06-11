import math

class Player:
    def __init__(self, cx, cy, r, xv, yv):
        self.cx = cx
        self.cy = cy
        self.r = r
        self.xv = xv
        self.yv = yv
        self.canJump = True
        self.trail = []
        self.fireflies = []

class Cat(Player):
    def __init__(self, cx, cy, r, xv, yv):
        super().__init__(cx,cy,r,xv,yv)
        self.jump = 250 #large jump
        self.r = 30
        self.color = "orange"

        #abilities
        self.canClaw = True
        self.canSwim = False

class Firefly:
    numFly = 0
    def __init__(self, rx, ry, cx, cy, level):
        self.rx = rx  
        self.ry = ry 
        self.cx = cx # location of the player
        self.cy = cy  
        self.level = level

        self.fxc = cx - 10  # location of the center of the elipse
        self.fyc = cy - 10  
        self.fx = self.fxc  
        self.fy = self.fyc  
        self.angle = 0
        self.speed = 0.05  
        self.ID = Firefly.numFly

        self.isCaught = False
        
        Firefly.numFly += 1

    def updatePosition(self, counter):
        self.angle = self.ID + (counter * self.speed)

        self.fx = self.fxc + self.rx * math.cos(self.angle)
        self.fy = self.fyc + self.ry * math.sin(self.angle)  

    def isColliding(self, cx, cy, r):
        if (Firefly.distance(self.fx, self.fy, cx, cy) < (3 + r)):
            return True     
    
    @staticmethod
    def distance(x0, y0, x1, y1):
        return ((x1 - x0)**2 + (y1 - y0)**2)**(1/2) 