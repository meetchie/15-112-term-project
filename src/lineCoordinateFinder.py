from cmu_graphics import *

def onAppStart(app):
    app.width, app.height = 600, 600
    app.startX = None
    app.startY = None
    app.endX = None
    app.endY = None
    app.isDrawing = False
    app.lines = []

def redrawAll(app):
    drawRect(340,240,80,60, fill = 'pink')
    drawRect(240, 120, 120, 120, fill = 'blue')
    
    for line in app.lines:
        drawLine(line[0], line[1], line[2], line[3])
    
    if app.isDrawing and app.startX is not None and app.endX is not None:
        drawLine(app.startX, app.startY, app.endX, app.endY)

def onMousePress(app, mouseX, mouseY):
    app.startX = mouseX
    app.startY = mouseY
    app.endX = mouseX
    app.endY = mouseY
    app.isDrawing = True

def onMouseDrag(app, mouseX, mouseY):
    app.endX = mouseX
    app.endY = mouseY

def onMouseRelease(app, mouseX, mouseY):
    app.isDrawing = False
    if app.startX is not None and app.endX is not None:
        app.lines.append((app.startX, app.startY, app.endX, app.endY))
        print(f"Line coordinates: Start ({app.startX}, {app.startY}), End ({app.endX}, {app.endY})")
    
    app.startX = None
    app.startY = None
    app.endX = None
    app.endY = None

def main():
    runApp(width=400, height=400)

main()
