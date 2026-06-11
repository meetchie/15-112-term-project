import random as py_random
from cmu_graphics import *

def drawStalactite(app, x0, y0, color):
    # perplexity AId almost entire function
    # Random overall width and height for the stalactite
    total_width = py_random.randint(20, 25)
    total_height = py_random.randint(30, 40)
    
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
        drawRect(left, current_y, rect_width, rect_height, fill = color)
        current_y += rect_height