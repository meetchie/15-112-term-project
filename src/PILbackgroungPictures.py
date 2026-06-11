from cmu_graphics import *
import math
import random as py_random
from PIL import Image, ImageDraw
from terrain2DLists import *

class BackgroundDrawer:
    def __init__(self, app, color, bgColor):
        self.cachedTerrain = []
        self.app = app
        self.color = color
        self.bgColor = bgColor
        self.terrainRendered = False
    
    def renderBackgroundTerrain(self):
        if self.terrainRendered == False:
            rows, cols = len(self.app.terrain), len(self.app.terrain[0])
            width, height = getCellSize(self.app, rows, cols)

            for row in range(rows):
                newRow = []

                for col in range(cols):
                    top, left = getPixelTL(self.app, row, col, rows, cols)
                    terColor = None
                    if self.app.terrain[row][col] == 'T':
                        terColor = self.color
                        newRow.append((top, left, width, height, terColor))
            
                self.cachedTerrain.append(newRow)
        self.terrainRendered = True

    def resetTerrainRender(self):
        self.terrainRendered = False
        self.cachedTerrain = []

    def drawTerrain(self, draw):
        if self.terrainRendered:
            for row in self.cachedTerrain:
                for (top, left, width, height, terColor) in row:
                    if terColor != None:
                        right = left + width
                        bottom = top + height
                        
                        if terColor == 'black':
                            rgba_color = (0, 0, 0, 255)  # Fully opaque black
                        elif terColor == 'white':
                            rgba_color = (255, 255, 255, 255)  # Fully opaque white
                        else:
                            rgba_color = terColor if len(terColor) == 4 else terColor + (255,)
                        
                        draw.rectangle([left, top, right, bottom], fill=rgba_color)
                        
class LineClass:
    def __init__(self,x0, y0, x1, y1, fill, width):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.fill = fill
        self.width = width
        self.xDistance = x1 - x0
        self.yDistance = y1 - y0
        self.partitions = 3 #number of dividing lines there will be per platform (1 makes the block itself wiggle)
        self.opacity = 100 
    
    def coorStartEnd(self):
        return self.x0, self.y0, self.x1, self.y1
        
    def changeColorOpacity(self, color, opacity):
        self.fill = color
        self.opacity = opacity
    
    def getLength(self):
        return LineClass.distance(self.x0, self.y0, self.x1, self.y1)

    @staticmethod
    def distance(x0, y0, x1, y1):
        return ((x1 - x0)**2 + (y1 - y0)**2)**(1/2) 

def pixelManyLineClass(draw, lineList):
    for line in lineList:
        x0, y0, x1, y1 = line.x0, line.y0, line.x1, line.y1 
        dx = x1 - x0
        dy = y1 - y0
        pixelSize = line.getLength() // 3
        length = math.sqrt(dx**2 + dy**2)
        numPixels = max(int(length // pixelSize), 1)
        
        for i in range(numPixels + 1):
            t = i / numPixels 
            px0, py0 = x0 + (t * dx), y0 + (t * dy)
            px1, py1 = px0 + pixelSize, py0 + pixelSize       
            draw.rectangle([px0, py0, px1, py1], line.fill, None, width = 1)   

def drawSafeSpots(draw, terrainList, app):
    # perplexity AI tool was heavily referenced here -- ran into problems with transparent rectangles and Pillow making them opaque
    rows, cols = len(terrainList), len(terrainList[0])
    width, height = getCellSize(app, rows, cols)
    for row in range(rows):
        for col in range(cols):
            if terrainList[row][col] == 'S':  # Check for a safe spot
                top, left = getPixelTL(app, row, col, rows, cols)
                bottom, right = top + height, left + width
                draw.rectangle([left, top, right, bottom], (128, 128, 128, 255))
                
                # Create a separate image for the glow effect
                glow_image = Image.new('RGBA', (app.width, app.height), (0, 0, 0, 0))
                glow_draw = ImageDraw.Draw(glow_image)
                
                # Draw glow effect
                for i in range(10, 0, -1):
                    alpha = int(255 - 25.5 * i)  # Increase alpha for inner circles
                    glow_color = (100, 100, 100, alpha)
                    glow_draw.ellipse([left - 2*i, top - 2*i, right + 2*i, bottom + 2*i], 
                                      fill=glow_color)
                
                # Composite the glow effect onto the main image
                
                draw._image.paste(glow_image, (0, 0), glow_image)
                
def drawTreeFractal(app, x0, y0, length, width, decrease, fillColor, angle, random=0):
    if length > 10: 
        x1 = x0 + length * math.cos(angle)
        y1 = y0 - length * math.sin(angle)

        app.treeLineClasss.append(LineClass(x0, y0, x1, y1, fillColor, width))

        newLength = length * decrease
        newWidth = width * decrease

        if random > 0:
            newLength *= py_random.uniform(0.9, 1.1)
        newAngle = angle + py_random.gauss(0, random)

        drawTreeFractal(app, x1, y1, newLength, newWidth, decrease, fillColor, newAngle - math.pi / 6, random)
        drawTreeFractal(app, x1, y1, newLength, newWidth, decrease, fillColor, newAngle + math.pi / 6, random)

def drawStalactite(app, x0, y0):
    # perplexity AId almost entire function
    # Random overall width and height for the stalactite
    total_width = py_random.randint(20, 50)
    total_height = py_random.randint(40, 100)
    
    # Random number of rectangles (2 to 4)
    num_rectangles = py_random.randint(2, 4)
    
    # Calculate height and width proportions for each rectangle
    heights = [total_height // num_rectangles] * num_rectangles
    widths = [total_width - (i * (total_width // num_rectangles)) for i in range(num_rectangles)]
    
    current_y = y0
    
    for i in range(num_rectangles):
        # Use calculated width and height for each rectangle
        rect_width = widths[i]
        rect_height = heights[i]
        left = x0 - rect_width // 2
        drawRect(app, left, current_y, rect_width, rect_height)
        current_y += rect_height

def getPixelTL(app, row, col, rows, cols):
    width, height = getCellSize(app, rows, cols)
    top = row * height 
    left = col * width 
    return top, left

def getCellSize(app, rows, cols):
    width = app.width / cols
    height = app.height / rows 

    return width, height

def makePilImage(width, height, bgColor):
    mode = "RGBA" if len(bgColor) == 4 else "RGB"
    return Image.new(mode, (width, height), bgColor)

def startImages(app):
    imageWidth, imageHeight = app.width, app.height

    app.blackMinusRGB = 255
    app.color = (0,0,0)
    app.bgColor = (255, 255, 255)
    
    # BACKGROUND PICTURES
    # forest bg
    # picture with white background and black trees
    bgColor1 = (255, 255, 255) # white background
    forestBackground = makePilImage(imageWidth, imageHeight, bgColor1)
    drawFB = ImageDraw.Draw(forestBackground)
    app.treeLineClasss = []
    drawTreeFractal(app, 40, 500, 100, 8, 0.8, 'black', math.pi / 2, random=0.2)
    drawTreeFractal(app, 360, 360, 100, 8, 0.8, 'black', math.pi / 2, random=0.2)
    pixelManyLineClass(drawFB, app.treeLineClasss)

    # picture with black background and white trees
    bgColor2 = (0, 0, 0)  # black background
    flashForestBackground = makePilImage(imageWidth, imageHeight, bgColor2)
    drawFFB = ImageDraw.Draw(flashForestBackground)
    for line in app.treeLineClasss:
        line.changeColorOpacity( 'white', 100)
    pixelManyLineClass(drawFFB, app.treeLineClasss)

    # NORMAL FOREGROUND
    transparent = (0, 0, 0, 0)  # Fully transparent color
    # transparent forest terrain with the black foreground 
    blackForestForeground = makePilImage(imageWidth, imageHeight, transparent)
    drawBFF = ImageDraw.Draw(blackForestForeground)
    app.terrain = forestTerrain2DList
    app.terrainCache = BackgroundDrawer(app, (0, 0, 0, 255), None)  # Fully opaque black
    app.terrainCache.renderBackgroundTerrain()
    app.terrainCache.drawTerrain(drawBFF)

    # transparent cave terrain with the black foreground 
    blackCaveForeground = makePilImage(imageWidth, imageHeight, transparent)
    drawBCF = ImageDraw.Draw(blackCaveForeground)
    app.terrain = caveTerrain2DList
    app.terrainCache.resetTerrainRender()
    app.terrainCache.renderBackgroundTerrain()
    app.terrainCache.drawTerrain(drawBCF)

    # transparent water terrain with the black foreground 
    blackWaterForeground = makePilImage(imageWidth, imageHeight, transparent)
    drawBWF = ImageDraw.Draw(blackWaterForeground)
    app.terrain = waterTerrain2DList
    app.terrainCache.resetTerrainRender()
    app.terrainCache.renderBackgroundTerrain()
    app.terrainCache.drawTerrain(drawBWF)

    # transparent forest terrain with the white foreground 
    flashForestForeground = makePilImage(imageWidth, imageHeight, transparent)
    drawFFF = ImageDraw.Draw(flashForestForeground)
    app.terrain = forestTerrain2DList
    app.terrainCache = BackgroundDrawer(app, (255, 255, 255, 255), None)  # Fully opaque black
    app.terrainCache.renderBackgroundTerrain()
    app.terrainCache.drawTerrain(drawFFF)

    # transparent cave terrain with the white foreground 
    flashCaveForeground = makePilImage(imageWidth, imageHeight, transparent)
    drawFCF = ImageDraw.Draw(flashCaveForeground)
    app.terrain = caveTerrain2DList
    app.terrainCache.resetTerrainRender()
    app.terrainCache.renderBackgroundTerrain()
    app.terrainCache.drawTerrain(drawFCF)

    # transparent water terrain with the white foreground 
    flashWaterForeground = makePilImage(imageWidth, imageHeight, transparent)
    drawFWF = ImageDraw.Draw(flashWaterForeground)
    app.terrain = waterTerrain2DList
    app.terrainCache.resetTerrainRender()
    app.terrainCache.renderBackgroundTerrain()
    app.terrainCache.drawTerrain(drawFWF)

    spiderwebImage = makePilImage(imageWidth, imageHeight, transparent)
    drawCI = ImageDraw.Draw(spiderwebImage)

    #line tuples found using lineCoordinateFinder.py
    lineTuples = [(240, 121, 210, 242),(243, 125, 251, 240),(240, 125, 286, 243),(242, 123, 350, 239),(243, 125, 405, 241),(360, 120, 312, 237),(360, 122, 268, 239),(260, 178, 278, 165),(250, 181, 260, 179),(226, 176, 249, 181),(281, 163, 287, 158),(217, 205, 250, 213),(250, 213, 271, 208),(271, 208, 301, 188),(300, 188, 309, 173),(352, 205, 338, 224),(338, 224, 287, 243),(293, 208, 317, 222),(326, 169, 338, 174),(360, 120, 379, 244),(339, 177, 368, 172),(317, 222, 374, 221)]
    for coords in lineTuples:
        drawCI.line((coords), fill='black', width = 2)
    
    caveSpiderwebImage = makePilImage(imageWidth, imageHeight, transparent)
    drawCSI = ImageDraw.Draw(caveSpiderwebImage)
    caveLineTuples = [(419, 237, 339, 273), (417, 237, 333, 305), (417, 237, 375, 304), (414, 237, 410, 307), (416, 238, 437, 306), (414, 239, 416, 238), (380, 256, 384, 263), (384, 263, 397, 269), (397, 269, 412, 271), (412, 271, 426, 268), (350, 264, 357, 286), (357, 286, 379, 296), (379, 296, 407, 302), (351, 264, 353, 238), (379, 252, 379, 238)]
    for coords in caveLineTuples:
        drawCSI.line((coords), fill = 'black', width = 2)
    
    flashCaveSpiderwebImage = makePilImage(imageWidth, imageHeight, transparent)
    drawFCSI = ImageDraw.Draw(flashCaveSpiderwebImage)
    for coords in caveLineTuples:
        drawFCSI.line((coords), fill = 'white', width = 2)

    # safespots
    safeSpotsForest = makePilImage(imageWidth, imageHeight, transparent)
    drawSSF = ImageDraw.Draw(safeSpotsForest, 'RGBA')
    drawSafeSpots(drawSSF, forestTerrain2DList, app)

    safeSpotsCave = makePilImage(imageWidth, imageHeight, transparent)
    drawSSC = ImageDraw.Draw(safeSpotsCave, 'RGBA')
    drawSafeSpots(drawSSC, caveTerrain2DList, app)

    safeSpotsWater = makePilImage(imageWidth, imageHeight, transparent)
    drawSSW = ImageDraw.Draw(safeSpotsWater, 'RGBA')
    drawSafeSpots(drawSSW, waterTerrain2DList, app)

    app.forestBackground = CMUImage(forestBackground)
    app.flashForestBackground = CMUImage(flashForestBackground)
    
    app.forestForeground = CMUImage(blackForestForeground)
    app.caveForeground = CMUImage(blackCaveForeground)
    app.waterForeground = CMUImage(blackWaterForeground)
    app.flashForestForeground = CMUImage(flashForestForeground)
    app.flashCaveForeground = CMUImage(flashCaveForeground)
    app.flashWaterForeground = CMUImage(flashWaterForeground)

    app.forestSafeSpots = CMUImage(safeSpotsForest)
    app.caveSafeSpots = CMUImage(safeSpotsCave)
    app.waterSafeSpots = CMUImage(safeSpotsWater)
    
    app.waterSpiderwebImage = CMUImage(spiderwebImage)
    app.caveSpiderwebImage = CMUImage(caveSpiderwebImage)
    app.flashCaveSpiderwebImage = CMUImage(flashCaveSpiderwebImage)

