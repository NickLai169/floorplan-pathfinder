import pygame
import sys
import time
import itertools
from floors import *
from traversal import *

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
Takes in an image and displayes it on the centre of the screen
"""
def display_center(gameDisplay, image):
    display_width = gameDisplay.get_width()
    display_height = gameDisplay.get_height()
    image_width, image_height = image.get_size()
    x = round((display_width - image_width) / 2)
    y = round((display_height - image_height) / 2)
    gameDisplay.blit(image, (x, y))

class Rightclick_Dropdown():
    """
    This is just the little drop-down menu that happens when you right click on the screen.
    """

    def __init__(self, display_width, display_height):
        self.invisible = True
        self.x = display_width
        self.y = 0
        self.display_width = display_width
        self.display_height = display_height
        self.image = pygame.image.load("assets/dropdown menu 3.png").convert_alpha()
        self.blue_box = pygame.image.load("assets/dropdown blue box 3.png").convert_alpha()
        self.goto((self.x, self.y))
    
    def goto(self, mouse_pos):
        if self.invisible:
            self.x = self.display_width
            self.y = 0
        else:
            self.x, self.y = mouse_pos
    
    def command(self, mouse_pos):
        if self.invisible:
            return None
        commands = ["Move_Node", "Copy", "Paste", "Delete", "Highlight", "Unhighlight", "Change_Attribute", "Delete_Edge"]
        x, y = mouse_pos
        if x - self.x > 257 or x < self.x or y - self.y > 288 or y < self.y:
            return None
        return commands[(y - self.y)//self.blue_box.get_size()[1]]
    
    def render(self, display):
        display.blit(self.image, (self.x, self.y))
        x, y = pygame.mouse.get_pos()
        if self.collision((x, y)):
            blue_width, blue_height = self.blue_box.get_size()
            display.blit(self.blue_box, (self.x, self.y + blue_height * ((y - self.y)//blue_height)))
    
    def collision(self, pos):
        x, y = pos
        width, height = self.image.get_size()
        if x < self.x or y < self.y or x > self.x + width or y > self.y + height:
            return False
        return True
    
    def make_invisible(self):
        self.invisible = True
        self.goto((self.display_width, 0))
    
    def make_visible(self):
        self.invisible = False
    
    def is_invisible(self):
        return self.invisible
