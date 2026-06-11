from cmu_graphics import *

class TextBox:
    def __init__(self, wCanvas, hCanvas, borderWidth, borderColor, fillColor):
        self.wCanvas = wCanvas
        self.hCanvas = hCanvas
        self.borderWidth = borderWidth
        self.borderColor = borderColor
        self.fillColor = fillColor

    # creates a text box at the bottom
    def drawBottomTextBox(self):
        height = self.hCanvas // 6
        width = self.wCanvas * 0.92 
        heightTall = height + 2 * self.borderWidth 
        widthWide = width + 2 * self.borderWidth
        
        centerX = self.wCanvas / 2
        bottomYTall = self.hCanvas - self.hCanvas * 0.025
        bottomYWide = self.hCanvas - self.hCanvas * 0.025 - self.borderWidth

        drawRect(centerX, bottomYTall, width, heightTall, align = 'bottom', fill = self.borderColor)
        drawRect(centerX, bottomYWide, widthWide, height, align = 'bottom', fill = self.borderColor)
        drawRect(centerX, bottomYWide, width, height, align = 'bottom', fill = self.borderColorfillColor)
    
    def drawTextBox(self, width, height):
        heightTall = height + 2 * self.borderWidth
        widthWide = width + 2 * self.borderWidth

        centerX = self.wCanvas / 2
        centerY = self.hCanvas / 2

        drawRect(centerX, centerY, width, heightTall, align = 'center', fill = self.borderColor)
        drawRect(centerX, centerY, widthWide, height, align = 'center', fill = self.borderColor)
        drawRect(centerX, centerY, width, height, align = 'center', fill = self.fillColor)

    def drawCustomTextBox(self, x0, y0, width, height):
        heightTall = height + 2 * self.borderWidth
        widthWide = width + 2 * self.borderWidth

        centerX = x0 + width / 2
        centerY = y0 + height / 2

        drawRect(centerX, centerY, width, heightTall, align = 'center', fill = self.borderColor)
        drawRect(centerX, centerY, widthWide, height, align = 'center', fill = self.borderColor)
        drawRect(centerX, centerY, width, height, align = 'center', fill = self.fillColor)


    @staticmethod
    def splitText(text, maxCharCount): # splits strings into shorter chunks 
        splitTextList = text.split(' ')
        lineList = []

        newString = ''
        charCount = 0
        for word in splitTextList:
            for char in word:
                charCount += 1
            newString += word + ' '

            if charCount > maxCharCount:
                lineList.append(newString[:-1])
                newString = ''
                charCount = 0
        
        lineList.append(newString[:-1])
        return lineList    

    @staticmethod
    def drawTextList(textList, x0, y0):
        for i in range(len(textList)):
            drawLabel(textList[i], x0, y0 + i * 30, font = 'monospace', size = 20, fill = 'white', align = 'left')
        