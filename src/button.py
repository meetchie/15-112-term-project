from cmu_graphics import *

class Button:
    def __init__(self, app, centerX, centerY, width, height, borderWidth, text, borderColor, fillColor):
        self.app = app
        self.centerX = centerX
        self.centerY = centerY
        self.width = width
        self.height = height
        self.borderWidth = borderWidth
        self.borderColor = borderColor
        self.fillColor = fillColor
        self.text = text
    
    def drawButton(self):
        heightTall = self.height + 2 * self.borderWidth 
        widthWide = self.width + 2 * self.borderWidth

        drawRect(self.centerX, self.centerY, self.width, heightTall, align = 'center', fill = self.borderColor)
        drawRect(self.centerX, self.centerY, widthWide, self.height, align = 'center', fill = self.borderColor)
        drawRect(self.centerX, self.centerY, self.width, self.height, align = 'center', fill = self.fillColor)
        drawLabel(self.text, self.centerX, self.centerY, size = 30, font = 'monospace', align = 'center', fill = self.borderColor)
        drawLabel(self.text, self.centerX, self.centerY, size = 30, font = 'monospace', align = 'center', fill = self.borderColor, opacity = 30, bold = True)
    
    def checkButtonPressed(self, mouseX, mouseY):
        minTallX = self.centerX - self.width / 2
        minTallY = self.centerY - self.height / 2 - self.borderWidth

        minWideX = self.centerX - self.width / 2 - self.borderWidth
        minWideY = self.centerY - self.height / 2

        if (minTallX < mouseX < (minTallX + self.width) and
            minTallY < mouseY < (minTallY + self.height + self.borderWidth * 2)): # if it's in the taller part of the button
            return True
        elif (minWideX < mouseX < (minWideX + self.width + self.borderWidth * 2) and 
              minWideX < mouseY < (minWideX + self.height)): # if it's in the wider part of the button
            return True
        else:
            return False





