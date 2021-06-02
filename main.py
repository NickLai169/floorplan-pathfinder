import pygame
import sys
import time
import itertools
from floors import *
from features import *
from traversal import *
from visualizer import *

"""
This is the main module, where the primary body of the program is executed.
"""

"""
<<<<[GLOBAL CONSTANTS]>>>>
"""
DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 720

def main():
    pygame.init()

    gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT), 32)
    pygame.display.set_caption('A bit Racey')

    # floorplan = pygame.image.load("assets/Phasmophobia-high school floorplan.jpg").convert()
    # floorplan = pygame.image.load("assets/Phasmophobia-high school floorplan 2.png").convert()
    floorplan = pygame.image.load("assets/Phasmophobia-high school floorplan 3.png").convert()

    floorplan = scale_image(DISPLAY_WIDTH, DISPLAY_HEIGHT, floorplan)

    gameDisplay.fill((255, 255, 255))
    
    for i in range(100):
        display_center(gameDisplay, floorplan)
        pygame.display.update()
        time.sleep(0.1)

    pygame.quit()
    quit()

main()