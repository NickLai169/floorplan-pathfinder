import pygame
import sys
import time
import itertools

from pygame import sprite
from floors import *
# from features import *
# from traversal import *
from visualizer import *

"""
This is the main module, where the primary body of the program is executed.
"""

"""
<<<<[HELPER FUNCTIONS]>>>>
"""

"""
Creates the edge between the two nodes both for visuals and in logic
"""
def create_edge(a, b, edges):
    if (a, b) not in edges and a != b:
        edges.append((a, b))
        a.connect_nodes(b)

"""
<<<<[GLOBAL CONSTANTS]>>>>
"""
DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 720

def main():
    pygame.init()

    gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT), 32)
    pygame.display.set_caption('A bit Racey')

    # floorplan_image = pygame.image.load("assets/Phasmophobia-high school floorplan_image.jpg").convert()
    # floorplan_image = pygame.image.load("assets/Phasmophobia-high school floorplan_image 2.png").convert()
    # floorplan_image = pygame.image.load("assets/Phasmophobia-high school floorplan 3.png").convert()
    floorplan_image = pygame.image.load("assets/Brownstone high school first floor.png").convert()

    floorplan_image = scale_image(DISPLAY_WIDTH, DISPLAY_HEIGHT, floorplan_image)
    gameDisplay.fill((255, 255, 255))
    floor = Floor(floorplan_image)
    edge_surface = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))


    #Initialisation of groups
    all_nodes = []
    edges = []
    
    prev_node = None
    for _ in range(50):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break


            elif event.type == pygame.KEYDOWN:
                pos = pygame.mouse.get_pos()
                #if the keypress is "n"
                if event.key == 110:
                    new_node = Node(floor, x=pos[0], y=pos[1])
                    all_nodes.append(new_node)
                    new_node.display(gameDisplay)
            

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for node in all_nodes:
                    if node.collision(x, y):
                        if not prev_node:
                            prev_node = node
                            node.highlight()
                            break
                        else:
                            create_edge(prev_node, node, edges)

        display_center(gameDisplay, floor.get_display())
        [pygame.draw.line(gameDisplay, (186,225,255),a.get_pos(), b.get_pos(), 5) for a, b in edges]
        [n.display(gameDisplay) for n in all_nodes]
        # pygame.draw.line(gameDisplay, (186,225,255), (0,0), (200,400), 30)
        pygame.display.update()
        time.sleep(0.1)
    print(edges[0][0].get_edges())
    pygame.quit()
    quit()

main()