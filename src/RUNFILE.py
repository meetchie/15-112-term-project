from cmu_graphics import *
import random as py_random
import math
from terrain2DLists import *
from playerClasses import *
from button import *
from textBox import *
from obstacleClasses import *
from PILbackgroungPictures import *
from winAnimation import *
from stalactites import *

class Gravity:
    def falling(y, v, g, dt):
        v += g * dt  # gravity accelerates the ball
        y += v * dt  # gravity moves the ball
        return (y, v)
    
    def moveXDir(x, v, dt):
        x += v * dt
        return x

class Level:
    def __init__(self, app):
        self.app = app
        self.app.level = 'start'
    
    def restart(self):
        self.app.isPaused = False
        self.app.isDead = False
        self.app.isWon = False
        self.app.isTutorial = False

        self.app.blankTerrain = []
        
        self.app.forestTerrain = forestTerrain2DList
        self.app.caveTerrain =  caveTerrain2DList
        self.app.waterTerrain = waterTerrain2DList

        self.app.terrain = self.app.forestTerrain
        self.app.inWater = False
        self.app.inEdgeWater = False
        self.app.inSpiderweb = False
        self.app.canDie = True

        self.app.isFlashing = False
        self.app.isFlashFrame = False
        self.app.minFlashCountRange, self.app.maxFlashCountRange = 500, 2000
        self.app.flashingCounter = py_random.randint(self.app.minFlashCountRange,self.app.maxFlashCountRange)
        self.app.currFlashCount = 0
        self.app.flashCountGoal = 40
        self.app.spotlightSize = 1

        self.app.counter = 0
        self.app.fireCounter = 0 #slower counter
        self.app.flashCounter = 0
        self.app.stepsPerSecond = 1000
        self.app.width = 600
        self.app.height = 600
        
        # colors
        self.app.blackMinusRGB = 255
        self.app.color = rgb(255-self.app.blackMinusRGB, 255-self.app.blackMinusRGB, 255-self.app.blackMinusRGB)
        self.app.bgColor = rgb(128, 128, 128)
        self.app.flashBgColor = rgb(255, 255, 255)
        
        self.app.r = 5
        self.app.player = Player(300, 300, self.app.r, 0, 0)
        self.app.obstacles = []

        self.app.wonButtonText1Pressed = False
        self.app.wonButtonText2Pressed = False

        # pause screen text box
        self.app.pauseTextBox = TextBox(self.app.width, self.app.height, 10, 'white', 'black')

        # death screen text box
        self.app.deadTextBox = TextBox(self.app.width, self.app.height, 10, 'white', 'black')

        self.app.startFireflies = []
        startFirefly1 = Firefly(py_random.randint(0,30), py_random.randint(0,20), 470, 250, 'start')
        startFirefly2 = Firefly(py_random.randint(10,40), py_random.randint(10,40), 470, 250, 'start')
        self.app.startFireflies.extend([startFirefly1, startFirefly2])

        # fireflies
        self.app.forestFireflies = []
        forestFirefly1 = Firefly(py_random.randint(0,30), py_random.randint(0,20), 250, 470, 'forest')
        forestFirefly2 = Firefly(py_random.randint(10,30), py_random.randint(10,30), 550, 340, 'forest')
        self.app.forestFireflies.extend([forestFirefly1, forestFirefly2])

        self.app.waterSpiderweb = Spiderweb(self.app, 240, 120, 120, 120, 'water')

        self.app.caveFireflies = []
        caveFirefly1 = Firefly(py_random.randint(0,40), py_random.randint(0,40), 220, 100, 'cave')
        caveFirefly2 = Firefly(py_random.randint(10,20), py_random.randint(10,40), 540, 350, 'cave')
        self.app.caveFireflies.extend([caveFirefly1, caveFirefly2])
        self.app.caveSpiderweb = Spiderweb(self.app, 340, 240, 80, 60, 'cave')
        self.app.caveSpiderwebList = [self.app.caveSpiderweb]
        self.app.caveStalactiteLocations = [(450,220),(300,400),(200,420)]

        self.app.waterFireflies = []
        waterFirefly1 = Firefly(py_random.randint(10,30), py_random.randint(10,30), 230, 200, 'water')
        waterFirefly2 = Firefly(py_random.randint(0,20), py_random.randint(0,40), 65, 300, 'water')
        self.app.waterFireflies.extend([waterFirefly1, waterFirefly2])
        self.app.waterSpiderwebList = [self.app.waterSpiderweb]

        self.app.spiderwebList = []
        self.app.spiderwebList.extend([self.app.caveSpiderweb, self.app.waterSpiderweb])
        
        self.app.levelClass.switchForest()
        self.app.createObstacles.createObstacleClassList()

    def switchForest(self):
        self.app.level = 'forest'
        self.app.terrain = self.app.forestTerrain
        self.app.createObstacles.createObstacleClassList()
        self.app.inWater = False
        self.app.canDie = True

    def switchCave(self):
        self.app.level = 'cave'
        self.app.terrain = self.app.caveTerrain
        self.app.createObstacles.createObstacleClassList()
        self.app.inWater = False
        self.app.canDie = True

    def switchWater(self):
        self.app.level = 'water'
        self.app.terrain = self.app.waterTerrain
        self.app.createObstacles.createObstacleClassList()
        self.app.inWater = True
        self.app.canDie = True
    
    def switchStart(self):
        self.app.level = 'start'

    def getLevel(self):
        if self.app.isPaused: return 'paused'
        elif self.app.isDead: return 'dead'
        elif self.app.isWon: return 'won'
        elif self.app.isTutorial: return 'tutorial'
        return self.app.level

def onAppStart(app):
    app.width = 600
    app.height = 600
    app.flashWhite = False

    startImages(app)

    app.isPaused = False
    app.isDead = False
    app.isWon = False
    app.isTutorial = False

    app.blankTerrain = []
    
    app.forestTerrain = forestTerrain2DList
    app.caveTerrain =  caveTerrain2DList
    app.waterTerrain = waterTerrain2DList

    app.terrain = app.forestTerrain
    app.inWater = False
    app.inEdgeWater = False
    app.inSpiderweb = False
    app.canDie = True

    app.isFlashing = False
    app.isFlashFrame = False
    app.minFlashCountRange, app.maxFlashCountRange = 500, 2000
    app.flashingCounter = py_random.randint(app.minFlashCountRange,app.maxFlashCountRange)
    app.currFlashCount = 0
    app.flashCountGoal = 40
    app.spotlightSize = 1

    app.counter = 0
    app.fireCounter = 0 #slower counter
    app.flashCounter = 0
    app.stepsPerSecond = 1000
    app.width = 600
    app.height = 600
    
    # colors
    app.blackMinusRGB = 255
    app.color = rgb(255-app.blackMinusRGB, 255-app.blackMinusRGB, 255-app.blackMinusRGB)
    app.bgColor = rgb(128, 128, 128)
    app.flashBgColor = rgb(255, 255, 255)
    
    app.r = 5
    app.player = Player(300, 300, app.r, 0, 0)
    app.obstacles = []

    app.winLightCircle = GrowingCircle(0,0)

    # starting screen buttons
    app.startButton = Button(app, 200, 400, 250, 100, 10, 'start', 'white', 'black')
    app.tutorialButton = Button(app, 450, 400, 150, 100, 10, 'tutorial', 'white', 'black')
    app.returnButton = Button(app, 300, 540, 200, 70, 10, 'return', 'white', 'black')
    app.wonButtonText1 = Button(app, 300, 500, 550, 130, 10, '', 'white', 'black')
    app.wonButtonText2 = Button(app, 300, 500, 550, 130, 10, '', 'white', 'black')
    app.wonButtonText1Pressed = False
    app.wonButtonText2Pressed = False

    # make class for text boxes in tutorial
    app.generalTutorialText = TextBox(app.width, app.height, 10, 'white', 'black')
    app.arrowList = [LineClass(540, 190, 515, 210, 'white', 1), LineClass(540, 190, 515, 170, 'white', 1),
                     LineClass(400, 190, 425, 210, 'white', 1), LineClass(400, 190, 425, 170, 'white', 1),
                     LineClass(470, 120, 495, 145, 'white', 1), LineClass(470, 120, 445, 145, 'white', 1)]

    # pause screen text box
    app.pauseTextBox = TextBox(app.width, app.height, 10, 'white', 'black')

    # death screen text box
    app.deadTextBox = TextBox(app.width, app.height, 10, 'white', 'black')

    app.startFireflies = []
    startFirefly1 = Firefly(py_random.randint(0,30), py_random.randint(0,20), 470, 250, 'start')
    startFirefly2 = Firefly(py_random.randint(10,40), py_random.randint(10,40), 470, 250, 'start')
    app.startFireflies.extend([startFirefly1, startFirefly2])

    # fireflies
    app.forestFireflies = []
    forestFirefly1 = Firefly(py_random.randint(0,30), py_random.randint(0,20), 250, 470, 'forest')
    forestFirefly2 = Firefly(py_random.randint(10,30), py_random.randint(10,30), 550, 340, 'forest')
    app.forestFireflies.extend([forestFirefly1, forestFirefly2])

    app.caveFireflies = []
    caveFirefly1 = Firefly(py_random.randint(0,40), py_random.randint(0,40), 220, 100, 'cave')
    caveFirefly2 = Firefly(py_random.randint(10,20), py_random.randint(10,40), 540, 350, 'cave')
    app.caveFireflies.extend([caveFirefly1, caveFirefly2])
    app.caveSpiderweb = Spiderweb(app, 340, 240, 80, 60, 'cave')
    app.caveSpiderwebList = [app.caveSpiderweb]
    app.caveStalactiteLocations = [(450,220),(300,400),(200,420)]

    app.waterFireflies = []
    waterFirefly1 = Firefly(py_random.randint(10,30), py_random.randint(10,30), 230, 200, 'water')
    waterFirefly2 = Firefly(py_random.randint(0,20), py_random.randint(0,40), 65, 300, 'water')
    app.waterFireflies.extend([waterFirefly1, waterFirefly2])
    app.waterSpiderweb = Spiderweb(app, 240, 120, 120, 120, 'water')
    app.waterSpiderwebList = [app.waterSpiderweb]
    app.waterStalactiteLocations = [(60,60), (120,40), (520, 150), (250,250),(300,230),(300,500)]

    app.spiderwebList = []
    app.spiderwebList.extend([app.caveSpiderweb, app.waterSpiderweb])

    app.levelClass = Level(app)
    app.createObstacles = ObstacleHolder(app)
    
    app.createObstacles.createObstacleClassList()
        
def redrawAll(app):
    if app.levelClass.getLevel() == 'start':
        # background
        drawRect(0,0, app.width, app.height, fill = 'black')

        # title text
        drawLabel('LIGHT', 75, 250, align = 'left', size = 100, font = 'monospace', fill = 'white')
        drawLabel('LIGHT', 75, 250, align = 'left', size = 100, font = 'monospace', fill = 'white', bold = True, opacity = 30)

        app.startButton.drawButton()
        app.tutorialButton.drawButton()

        for firefly in app.startFireflies:
            drawCircle(firefly.fx, firefly.fy, 3, fill = app.bgColor) # dark circle 
            drawCircle(firefly.fx, firefly.fy, 6, fill = app.bgColor, opacity = 30) # glow around circle

    elif app.levelClass.getLevel() == 'tutorial':
        # background
        drawRect(0,0, app.width, app.height, fill = 'black')
        
        drawLabel('tutorial', 300, 50, align = 'center', size = 50, font = 'monospace', fill = 'white')
        drawLabel('tutorial', 300, 50, align = 'center', size = 50, font = 'monospace', fill = 'white', bold = True, opacity = 30)

        app.returnButton.drawButton()
        app.generalTutorialText.drawCustomTextBox(25, 95, 300, 230)
        app.generalTutorialText.drawCustomTextBox(25, 370, 300, 90)
        app.generalTutorialText.drawCustomTextBox(375, 95, 190, 365)

        firefliesText = 'collect 6 fireflies across 3 different levels. once you collect them all, you escape. when flashing, escape to the light spots'
        firefliesTextList = app.generalTutorialText.splitText(firefliesText, 12)
        app.generalTutorialText.drawTextList(firefliesTextList, 45, 115)
        
        waterText = 'the underwater cave is safe. you cannot die.'
        waterTextList = app.generalTutorialText.splitText(waterText, 16)
        app.generalTutorialText.drawTextList(waterTextList, 45, 390)

        controlsText = "use arrow keys to move, press 'c' to cut spiderwebs, and 'p' to pause"
        controlsTextList = app.generalTutorialText.splitText(controlsText, 5)
        app.generalTutorialText.drawTextList(controlsTextList, 395, 260)

        normalPixelManyLineClasss(app.arrowList)
    elif app.isWon: #HERE

        drawRect(0,0, app.width, app.height, fill = 'black', opacity = 80)
        if app.wonButtonText1Pressed == False:
            app.wonButtonText1.drawButton()
            drawLabel('you found all the fireflies !', 70, 470, fill = 'white', font = 'monospoace', size = 25, align = 'left')
            drawLabel('you were able to bring light to', 70, 500, fill = 'white', font = 'monospoace', size = 25, align = 'left')
            drawLabel('the world again.', 70, 530, fill = 'white', font = 'monospoace', size = 25, align = 'left')
        elif app.wonButtonText2Pressed == False:
            app.wonButtonText2.drawButton()
            drawLabel('thank you for playing this game !', 70, 470, fill = 'white', font = 'monospoace', size = 25, align = 'left')
            drawLabel('enjoy your world with light :)', 70, 500, fill = 'white', font = 'monospoace', size = 25, align = 'left')
        else:
            drawRect(0,0, app.width, app.height, fill = 'white')
            drawLabel('LIGHT', 75, 250, align = 'left', size = 100, font = 'monospace', fill = 'black')
            drawLabel('LIGHT', 75, 250, align = 'left', size = 100, font = 'monospace', fill = 'black', bold = True, opacity = 30)

            drawLabel("press 'r' to restart", 75, 340, align = 'left', size = 30, font = 'monospace', fill = 'black', bold = True, opacity = 30)
    else: 
        # draw background
        drawRect(0,0, app.width, app.height, fill = app.bgColor)
        
        # background images
        if app.levelClass.getLevel() == 'forest':
            if app.isFlashFrame == False:
                drawImage(app.forestBackground, app.width / 2, app. height / 2, align = 'center')
            else:
                drawImage(app.flashForestBackground, app.width / 2, app. height / 2, align = 'center')
                
        # gradients between levels
        if app.levelClass.getLevel() == 'cave':
            grad = gradient( app.bgColor, app.color, start = 'bottom')
            drawRect(app.width - 160, 0, 80, 120, fill = grad)
        elif app.levelClass.getLevel() == 'water':
            grad = gradient(app.bgColor, app.color, start = 'bottom')
            drawRect(app.width-320, 0, 260, 60, fill = grad)
        
        if app.levelClass.getLevel() == 'cave':
            if app.isFlashFrame == False:
                for loc in app.caveStalactiteLocations:
                    drawStalactite(app, *loc, 'black')
            else:
                for loc in app.caveStalactiteLocations:
                    drawStalactite(app, *loc, 'white')
        if app.levelClass.getLevel() == 'water':
            if app.isFlashFrame == False:
                for loc in app.waterStalactiteLocations:
                    drawStalactite(app, *loc, 'black')
            else:
                for loc in app.waterStalactiteLocations:
                    drawStalactite(app, *loc, 'white')
            

        # dark overlay
        if app.blackMinusRGB == 255:
            drawRect(0,0, app.width, app.height, fill = app.color, opacity = 90)
        
        # spotlight that follows player
        for i in range(10):
            drawCircle(app.player.cx, app.player.cy, app.spotlightSize * 30 + i*2, fill = app.bgColor, opacity = 10 - i )

        # safe spots
        if app.levelClass.getLevel() == 'forest':
            drawImage(app.forestSafeSpots, app.width / 2, app. height / 2, align = 'center')
        elif app.levelClass.getLevel() == 'cave':
            drawImage(app.caveSafeSpots, app.width / 2, app. height / 2, align = 'center')
        elif app.levelClass.getLevel() == 'water':
            drawImage(app.waterSafeSpots, app.width / 2, app. height / 2, align = 'center')
        
        # general drawings between level objects (player, platforms, trail, fireflies)
        
        # spiderwebs
        if app.levelClass.getLevel() == 'cave':
            if len(app.caveSpiderwebList) != 0:
                if app.isFlashFrame:
                    drawImage(app.flashCaveSpiderwebImage, app.width / 2, app. height / 2, align = 'center')
                else:
                    drawImage(app.caveSpiderwebImage, app.width / 2, app. height / 2, align = 'center')
        elif app.levelClass.getLevel() == 'water':
            if len(app.waterSpiderwebList) != 0:
                drawImage(app.waterSpiderwebImage, app.width / 2, app. height / 2, align = 'center')

        # draw player
        drawCircle(app.player.cx, app.player.cy, app.player.r)
        
        # platforms
        for p in app.obstacles:
            if isinstance(p, Air):
                pass
            elif isinstance(p, Water):
                pass
            elif isinstance(p, SafeSpot):
                pass
            elif isinstance(p, Obstacle):

                # aligns the rectangle to the center, and then makes the width and height either 0, 1, or 2 pixels bigger than normal every step
                # creates a wiggling illusion
                randX, randY = py_random.randint(0, 2), py_random.randint(0, 2)
                x0, y0, width, height = p.coorQuadruple()
                
                x0, y0 = x0 + (width / 2), y0 + (height / 2)
                width += randX
                height += randY
                
                drawRect(x0, y0, width, height, align = 'center', fill=app.color)
            else:
                print('KYS')
        
        # why fat FIX
        for firefly in app.player.fireflies:
            drawCircle(firefly.fx, firefly.fy, 2, fill = app.bgColor) # dark circle 
            drawCircle(firefly.fx, firefly.fy, 4, fill = app.bgColor, opacity = 30) # glow around circle
            
        # draw trail
        for i, (x, y, alpha) in enumerate(app.player.trail):
            drawCircle(x, y, app.r, fill=app.color, opacity=alpha)
                
        # foreground images
        if app.levelClass.getLevel() == 'forest':
            if app.isFlashFrame == False:
                drawImage(app.forestForeground, app.width / 2, app. height / 2, align = 'center')
            else:
                drawImage(app.flashForestForeground, app.width / 2, app. height / 2, align = 'center')
        elif app.levelClass.getLevel() == 'cave':
            if app.isFlashFrame == False:
                drawImage(app.caveForeground, app.width / 2, app. height / 2, align = 'center')
            else:
                drawImage(app.flashCaveForeground, app.width / 2, app. height / 2, align = 'center')
        else:
            if app.isFlashFrame == False:
                drawImage(app.waterForeground, app.width / 2, app. height / 2, align = 'center')
            else:
                drawImage(app.flashWaterForeground, app.width / 2, app. height / 2, align = 'center')

        # fireflies in each level
        if app.levelClass.getLevel() == 'forest':
            for firefly in app.forestFireflies:
                drawCircle(firefly.fx, firefly.fy, 3, fill = app.bgColor) # dark circle 
                drawCircle(firefly.fx, firefly.fy, 6, fill = app.bgColor, opacity = 30) # glow around circle
            
        elif app.levelClass.getLevel() == 'cave':
            for firefly in app.caveFireflies:
                drawCircle(firefly.fx, firefly.fy, 3, fill = app.bgColor) # dark circle 
                drawCircle(firefly.fx, firefly.fy, 6, fill = app.bgColor, opacity = 30) # glow around circle

        elif app.levelClass.getLevel() == 'water':
            for firefly in app.waterFireflies:
                drawCircle(firefly.fx, firefly.fy, 3, fill = app.bgColor) # dark circle 
                drawCircle(firefly.fx, firefly.fy, 6, fill = app.bgColor, opacity = 30) # glow around circle

        # when app is paused have the pause screen placed above everything else
        if app.isPaused:
            drawRect(0,0, app.width, app.height, fill = 'black', opacity = 80)
            app.pauseTextBox.drawTextBox(400, 300)
            
            drawRect(270,190,20,80, fill = 'white')
            drawRect(310,190,20,80, fill = 'white')

            # FIX w buttons and pictures eventually :")
            drawLabel('press \'p\' to unpause', 125, 320, fill = 'white', font = 'monospoace', size = 25, align = 'left')
            drawLabel('press \'r\' to restart', 125, 350, fill = 'white', font = 'monospoace', size = 25, align = 'left')
        
        if app.isDead:
            drawRect(0,0, app.width, app.height, fill = 'black', opacity = 100)
            app.deadTextBox.drawTextBox(400, 300)

            # FIX w buttons and pictures eventually :")
            drawLabel('try again !', 125, 200, fill = 'white', font = 'monospoace', size = 25, align = 'left')
            drawLabel('press \'r\' to restart', 125, 230, fill = 'white', font = 'monospoace', size = 25, align = 'left')
    
def onKeyPress(app, key):
    # when app is paused, can either unpause or restart nd nothing else
    if app.levelClass.getLevel() == 'start':
        return

    if app.isPaused == True:
        if key == 'p': app.isPaused = False
        elif key == 'r': 
            app.isPaused = False
            app.levelClass.restart()

    elif app.isDead == True:
        if key == 'r':
            app.levelClass.restart()
    
    elif app.isWon == True:
        if key == 'r' and app.wonButtonText2Pressed == True:
            app.levelClass.restart()

    else:
        # (REMOVE FOR FINAL)
        if key == 't':
            app.player.cx, app.player.cy = 560, 570
        if key == 'e':
            app.player.cx, app.player.cy = 450, 300
        if key == 'w':
            app.player.fireflies.extend(app.forestFireflies)
            app.player.fireflies.extend(app.caveFireflies)
            app.player.fireflies.extend(app.waterFireflies)

        # pause
        if key == 'p': app.isPaused = True
        # jump
        if key == 'up' and (app.player.canJump or app.inEdgeWater): 
            if app.inEdgeWater:
                app.player.yv = -250
            elif app.inWater:
                app.player.yv = -30
            elif app.inSpiderweb:
                app.player.yv = -30
            else:
                app.player.yv = -250
                app.player.canJump = False
        
        if key == 'c':
            print('claw')
            if app.levelClass.getLevel() == 'cave':
                indexOfSpiderweb = indexOfNearbySpiderweb(app.caveSpiderwebList)
                if indexOfSpiderweb != None:
                    app.caveSpiderwebList.pop(indexOfSpiderweb)
            elif app.levelClass.getLevel() == 'water':
                indexOfSpiderweb = indexOfNearbySpiderweb(app.waterSpiderwebList)
                if indexOfSpiderweb != None:
                    app.waterSpiderwebList.pop(indexOfSpiderweb)

def onKeyHold(app,keys):
    if app.isPaused == True:
        return
    else:
        if 'right' in keys:
            if app.inWater: app.player.xv = 30
            elif app.inSpiderweb: app.player.xv = 20
            else: app.player.xv = 100
        if 'left' in keys:
            if app.inWater: app.player.xv = -30
            elif app.inSpiderweb: app.player.xv = -20
            else: app.player.xv = -100

def onMousePress(app, mouseX, mouseY):
    if app.levelClass.getLevel() == 'start':
        if app.startButton.checkButtonPressed(mouseX, mouseY):
            app.levelClass.switchForest()
        elif app.tutorialButton.checkButtonPressed(mouseX, mouseY):
            app.isTutorial = True
    elif app.levelClass.getLevel() == 'tutorial':
        if app.returnButton.checkButtonPressed(mouseX, mouseY):
            app.levelClass.restart()
            app.isTutorial = False
    elif app.isWon:
        if app.wonButtonText1Pressed == False and app.wonButtonText1.checkButtonPressed(mouseX, mouseY):
            app.wonButtonText1Pressed = True
        elif app.wonButtonText2.checkButtonPressed(mouseX, mouseY) and app.wonButtonText1Pressed:
            app.wonButtonText2Pressed = True

def onStep(app):

    if app.counter % 2 == 0:
        app.fireCounter += 1
    app.counter += 1

    # GENERAL
    if len(app.player.fireflies) == 6:
        app.winLightCircle = GrowingCircle(app.player.cx,app.player.cy)
        app.isWon = True

    if app.levelClass.getLevel() == 'start': # game doesn't start till play
        for firefly in app.startFireflies:
                firefly.updatePosition(app.fireCounter)
    elif app.levelClass.getLevel() == 'dead':
        pass
    elif app.levelClass.getLevel() == 'paused': # game doesn't update or move when paused 
        pass

    elif app.levelClass.getLevel() == 'tutorial':
        pass
    else:
        #updates colors
        app.color = rgb(255-app.blackMinusRGB, 255-app.blackMinusRGB, 255-app.blackMinusRGB)
        app.bgColor = rgb(0+app.blackMinusRGB, 0+app.blackMinusRGB, 0+app.blackMinusRGB)

        if app.levelClass.getLevel() == 'forest':
            if app.inSpiderweb:
                app.player.canJump = False
                app.player.cy, app.player.yv = Gravity.falling(app.player.cy, app.player.yv, 30, 0.02) 
                app.player.cx = Gravity.moveXDir(app.player.cx, app.player.xv, 0.02)
            else:
                app.player.canJump = False
                app.player.cy, app.player.yv = Gravity.falling(app.player.cy, app.player.yv, 500, 0.02) 
                app.player.cx = Gravity.moveXDir(app.player.cx, app.player.xv, 0.02)

            if app.player.cy >= app.height - app.player.r - 1: # friction on ground
                app.player.xv *= 0.9  
                app.player.cy = app.height - app.player.r 
            
            # catches fireflies 
            i = 0
            while i < len(app.forestFireflies):
                firefly = app.forestFireflies[i]
                if firefly.isColliding(app.player.cx, app.player.cy, app.player.r):
                    app.player.fireflies.append(app.forestFireflies.pop(i))
                else:
                    i += 1

            for firefly in app.forestFireflies:
                firefly.updatePosition(app.fireCounter)
        
        elif app.levelClass.getLevel() == 'cave':
            if app.inSpiderweb:
                app.player.canJump = False
                app.player.cy, app.player.yv = Gravity.falling(app.player.cy, app.player.yv, 30, 0.02) 
                app.player.cx = Gravity.moveXDir(app.player.cx, app.player.xv, 0.02)
            else:
                app.player.canJump = False
                app.player.cy, app.player.yv = Gravity.falling(app.player.cy, app.player.yv, 500, 0.02) 
                app.player.cx = Gravity.moveXDir(app.player.cx, app.player.xv, 0.02)

            if app.player.cy >= app.height - app.player.r - 1: # friction on ground
                app.player.xv *= 0.9  
                app.player.cy = app.height - app.player.r 
            
            # catches fireflies 
            i = 0
            while i < len(app.caveFireflies):
                firefly = app.caveFireflies[i]
                if firefly.isColliding(app.player.cx, app.player.cy, app.player.r):
                    app.player.fireflies.append(app.caveFireflies.pop(i))
                else:
                    i += 1

            for firefly in app.caveFireflies:
                firefly.updatePosition(app.fireCounter)

        elif app.levelClass.getLevel() == 'water':
            if app.inWater:
                app.player.canJump = True
                app.player.cy, app.player.yv = Gravity.falling(app.player.cy, app.player.yv, 20, 0.02) 
                app.player.cx = Gravity.moveXDir(app.player.cx, app.player.xv, 0.02)

                app.player.xv *= 0.95 #friction in water
            elif app.inSpiderweb:
                app.player.canJump = False
                app.player.cy, app.player.yv = Gravity.falling(app.player.cy, app.player.yv, 30, 0.02) 
                app.player.cx = Gravity.moveXDir(app.player.cx, app.player.xv, 0.02)
            else:
                app.player.canJump = False
                app.player.cy, app.player.yv = Gravity.falling(app.player.cy, app.player.yv, 500, 0.02) 
                app.player.cx = Gravity.moveXDir(app.player.cx, app.player.xv, 0.02)
                
                if app.player.cy >= app.height - app.player.r - 1: # friction on ground
                    app.player.xv *= 0.9  
                    app.player.cy = app.height - app.player.r 
                
            #jump 
            if ifPlayerCenterInside(app.player.cx, app.player.cy, app.obstacles, Water): # if it's on the edge water, can jump high to get out
                app.inWater = True
                app.player.canJump = True
                app.inEdgeWater = True

                if app.player.yv > 0: # FIX (shoots down into the water and doesn't slow down)
                    if app.player.yv > 200:
                        app.player.yv *= 0.6
                    else:
                        app.player.yv *= 0.9
            else:
                app.inEdgeWater = False
            
            if ifPlayerCenterInside(app.player.cx, app.player.cy, app.obstacles, Air):
                app.inWater = False

            # catches fireflies 
            i = 0
            while i < len(app.waterFireflies):
                firefly = app.waterFireflies[i]
                if firefly.isColliding(app.player.cx, app.player.cy, app.player.r):
                    app.player.fireflies.append(app.waterFireflies.pop(i))
                else:
                    i += 1

            for firefly in app.waterFireflies:
                firefly.updatePosition(app.fireCounter)

        # spotlight size
        app.spotlightSize = 1 + len(app.player.fireflies)

        # update caught fireflies positions
        for firefly in app.player.fireflies:
                firefly.fxc = app.player.cx - 30
                firefly.fyc = app.player.cy - 30

                firefly.updatePosition(app.fireCounter)

        #flashing mechanic: occurs randomly and then makes the screen flash to represent danger
        if (app.levelClass.getLevel() != 'start' and
            app.levelClass.getLevel() != 'water'): 
            app.flashCounter += 1

        if app.isFlashing:
            if app.flashCounter % 7 == 0:
                if app.blackMinusRGB == 255: 
                    app.blackMinusRGB = 0
                    app.isFlashFrame = True
                else: 
                    app.blackMinusRGB = 255
                    app.isFlashFrame = False
                app.currFlashCount += 1

            if app.currFlashCount >= app.flashCountGoal:
                app.isFlashing = False
                app.currFlashCount = 0

                if app.canDie: #if the flashing ends and the player still ins't in a safe spot, they die
                    app.isDead = True

        if app.flashCounter % app.flashingCounter == 0:
            app.isFlashing = True
            app.flashCounter = 0
            app.flashingCounter = py_random.randint(app.minFlashCountRange,app.maxFlashCountRange)

        # CAN DIE IF NOT IN SAFE SPOT
        if ifPlayerCenterInside(app.player.cx, app.player.cy, app.obstacles, SafeSpot): 
            app.canDie = False
        elif (ifPlayerCenterInside(app.player.cx, app.player.cy, app.obstacles, Air) or 
              ifPlayerCenterInside(app.player.cx, app.player.cy, app.obstacles, Water)): 
                app.canDie = True

        # collisions
        for p in app.obstacles:
            if isinstance(p, Air) or isinstance(p, Water) or isinstance(p, SafeSpot): pass
            elif isinstance(p, Obstacle):
                # Find closest point on obstacle to ball's center
                closestX = max(p.x0, min(app.player.cx, p.x0 + p.width))
                closestY = max(p.y0, min(app.player.cy, p.y0 + p.height))
                
                distanceX = app.player.cx - closestX
                distanceY = app.player.cy - closestY
                distance = (distanceX**2 + distanceY**2) ** (1/2)

                if distance < app.player.r:
                    if abs(distanceX) > abs(distanceY):  # horizontal collision
                        app.player.xv = 0 
                        if distanceX > 0: # to the right
                            app.player.cx = closestX + app.player.r
                        else: # to the left
                            app.player.cx = closestX - app.player.r
                    else:  # vertical collision
                        if distanceY > 0:  # below obstacle
                            app.player.cy = closestY + app.player.r
                            app.player.yv = max(0, app.player.yv) # 0 if it is below the obstacle & hits, and remain its prev velocity if its falling down

                            app.player.canJump = True
                        else:  # above obstacle
                            app.player.cy = closestY - app.player.r
                            app.player.yv = min(0, app.player.yv) # 0 if it is on the top of the obstacle, and remain its prev velocity if it is going up
                            app.player.canJump = True
                        app.player.xv *= 0.9  # apply friction when on platform
        
        if app.levelClass.getLevel() == 'cave':
            if ifPlayerCenterInside(app.player.cx, app.player.cy, app.caveSpiderwebList, Spiderweb):
                app.inSpiderweb = True
            else:
                app.inSpiderweb = False
        elif app.levelClass.getLevel() == 'water':
            if ifPlayerCenterInside(app.player.cx, app.player.cy, app.waterSpiderwebList, Spiderweb):
                app.inSpiderweb = True
            else:
                app.inSpiderweb = False

        # drawing the trail behind the player
        fade(app)
        
        # check for boundaries (top, bottom, left, right)
        if app.player.cy <= app.player.r:
            app.player.cy = app.player.r
            app.player.yv = 0
        if app.player.cy >= app.height - app.player.r:
            app.cy = app.height - app.player.r
            app.player.canJump = True
        if app.player.cx >= app.width - app.player.r:
            app.player.cx = app.width - app.player.r
            app.player.xv = 0
        if app.player.cx <= app.player.r:
            app.player.cx = app.player.r
            app.player.xv = 0
        
        #switching levels
        if app.levelClass.getLevel() == 'forest':
            if app.player.cy > (580):
                app.player.cy = 20
                app.levelClass.switchCave()

        elif app.levelClass.getLevel() == 'cave':
            if app.player.cy > (580):
                app.player.cy = 20
                app.levelClass.switchWater()
            elif app.player.cy < (20):
                app.player.cx, app.player.cy = 530, 580
                app.levelClass.switchForest()

        elif app.levelClass.getLevel() == 'water':
            if app.player.cy < (20):
                app.player.cx, app.player.cy = 530, 580
                app.levelClass.switchCave()

def getPixelTL(app, row, col, rows, cols):
    width, height = getCellSize(app, rows, cols)
    top = row * height 
    left = col * width 
    return top, left

def getCellSize(app, rows, cols):
    width = app.width / cols
    height = app.height / rows 

    return width, height

def fade(app):
    # apply fade
    app.player.trail.append((app.player.cx, app.player.cy, 100)) 

    # fade out trail as it goes on
    for i in range(len(app.player.trail)):
        x, y, alpha = app.player.trail[i]
        app.player.trail[i] = (x, y, alpha * 0.5)

    # limit trail 
    if len(app.player.trail) > 10: 
        app.player.trail.pop(0)

def normalPixelManyLineClasss(lineList):
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
            drawRect(px0, py0, abs(px1 - px0), abs(py1 - py0), fill = line.fill)  

def distance(x0, y0, x1, y1):
    return ((x1 - x0)**2 + (y1 - y0)**2)**(1/2) 

def main():
    runApp()

main()
