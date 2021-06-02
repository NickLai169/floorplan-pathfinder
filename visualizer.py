import pygame
import sys
import time
import itertools
from floors import *
from traversal import *
from main import DISPLAY_HEIGHT, DISPLAY_WIDTH

"""
This is the visualization moduel, condtaing helper functions to help visualise and interact
with the floorplan.
"""


"""
Takes in a display dimension and returns a scaled image to fit
"""
def scale_image(display_width, display_height, image):
    image_width, image_height = image.get_size()
    display_ratio = display_width/display_height
    image_ratio = image_width/image_height

    if display_ratio > image_ratio:
        #The display is "wider" than the image
        return pygame.transform.scale(image, (round(image_width * (display_height/image_height)), display_height))
    else:
        #The dispaly is "Narrower" than the image
        return pygame.transform.scale(image, (display_width, round(image_height * (display_width/image_width))))


"""
Takes in an image and displayes it on the center of the screen
"""
def display_center(gameDisplay, image):
    image_width, image_height = image.get_size()
    x = round((DISPLAY_WIDTH - image_width) / 2)
    y = round((DISPLAY_HEIGHT - image_height) / 2)
    gameDisplay.blit(image, (x, y))