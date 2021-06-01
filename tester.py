import pygame
import sys
import time
from floors import *

"""
<<<<[GLOBAL CONSTANTS]>>>>
"""
DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 720



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


def main():
    pygame.init()

    gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT), 32)
    pygame.display.set_caption('A bit Racey')

    floorplan = pygame.image.load("assets/Phasmophobia-high school floorplan.jpg").convert()
    # floorplan = pygame.image.load("assets/Phasmophobia-high school floorplan 2.png").convert()
    # floorplan = pygame.image.load("assets/Phasmophobia-high school floorplan 3.png").convert()

    floorplan = scale_image(DISPLAY_WIDTH, DISPLAY_HEIGHT, floorplan)

    gameDisplay.fill((255, 255, 255))
    
    for i in range(100):
        display_center(gameDisplay, floorplan)
        pygame.display.update()
        time.sleep(0.1)

    pygame.quit()
    quit()

# main()




first_floor = Floor()

print(first_floor)

a = first_floor.make_node(name="a", x=0, y=0)
b = first_floor.make_node(name="b", x=1, y=1)
c = first_floor.make_node("c", 1, 0)
d = first_floor.make_node(x=0, y=1)

a.connect_nodes(b)
b.connect_nodes(c)
a.connect_nodes(c)
d.connect_nodes(a)

print(a)
print(b)
print(c)
print(d)