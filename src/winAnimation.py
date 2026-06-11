from cmu_graphics import *

class GrowingCircle:
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.r = 1
        self.increase = 10
    
    def growLarger(self):
        self.r += self.increase
    
    def drawGrowingCircle(self):
        drawCircle(self.cx, self.cy, self.r, fill = 'white')
    
