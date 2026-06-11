# Renders the game's fractal trees to standalone PNGs in images/
# Reuses drawTreeFractal and pixelManyLineClass from PILbackgroungPictures.py,
# the same functions that draw the forest level background in the game.

import math
import os
import random as py_random
from PIL import ImageDraw

from PILbackgroungPictures import drawTreeFractal, pixelManyLineClass, makePilImage

class TreeApp:
    # minimal stand-in for the cmu_graphics app object,
    # drawTreeFractal only uses app.treeLineClasss
    def __init__(self):
        self.treeLineClasss = []

def renderTrees(path, trees, bgColor, seed, width=600, height=600):
    py_random.seed(seed)
    app = TreeApp()
    for (x0, y0, length, lineWidth, fillColor, randomness) in trees:
        drawTreeFractal(app, x0, y0, length, lineWidth, 0.8, fillColor, math.pi / 2, randomness)
    image = makePilImage(width, height, bgColor)
    pixelManyLineClass(ImageDraw.Draw(image), app.treeLineClasss)
    image.save(path)
    print(f'saved {path}')

if __name__ == '__main__':
    outDir = os.path.join(os.path.dirname(__file__), '..', 'images')
    os.makedirs(outDir, exist_ok=True)

    white = (255, 255, 255)
    black = (0, 0, 0)

    # a single perfectly symmetric tree (no randomness)
    renderTrees(os.path.join(outDir, 'fractal-tree-symmetric.png'),
                [(300, 560, 110, 8, 'black', 0)], white, seed=112)

    # a single tree with the game's gaussian angle randomness
    renderTrees(os.path.join(outDir, 'fractal-tree-random.png'),
                [(300, 560, 110, 8, 'black', 0.2)], white, seed=112)

    # the forest level background exactly as the game generates it
    gameTrees = [(40, 500, 100, 8, 'black', 0.2),
                 (360, 360, 100, 8, 'black', 0.2)]
    renderTrees(os.path.join(outDir, 'forest-background.png'),
                gameTrees, white, seed=15112)

    # the flash-event version: same trees recolored white on black
    flashTrees = [(x0, y0, length, w, 'white', r) for (x0, y0, length, w, c, r) in gameTrees]
    renderTrees(os.path.join(outDir, 'forest-background-flash.png'),
                flashTrees, black, seed=15112)
