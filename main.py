import pygame
import sys
import time
import itertools

from pygame import sprite
from pygame.locals import *
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
    clock = pygame.time.Clock()

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

    new_node = Node(floor, x=200, y=200)
    all_nodes.append(new_node)
    new_node.display(gameDisplay)
    
    prev_node = None
    highlight_order = []
    while pygame.time.get_ticks() <= 50000:
        #Previsualisations
        display_center(gameDisplay, floor.get_display())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


            elif event.type == pygame.KEYDOWN:
                pos = pygame.mouse.get_pos()
                #if the keypress is "n"
                if event.key == pygame.locals.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.locals.K_n:
                    new_node = Node(floor, x=pos[0], y=pos[1])
                    all_nodes.append(new_node)
                    new_node.display(gameDisplay)
            

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                clicked_node = None
                for node in all_nodes:
                    if node.collision(x, y):
                        clicked_node = node
                if event.button == 1:
                    #Left-click
                    if clicked_node:
                        highlighted = clicked_node.highlighted
                        if highlighted:
                            #Left-click Highlighted-node
                            clicked_node.unhighlight()
                            highlight_order.remove(clicked_node)
                        else:
                            #Left-click Unhighlighted-node
                            curr_highlighted = [n for n in all_nodes if n.highlighted]
                            if curr_highlighted:
                                for n in curr_highlighted:
                                    create_edge(n, clicked_node, edges)
                            else:
                                clicked_node.highlight()
                                highlight_order.append(clicked_node)
                    else:
                        #Left-click Blank-spot
                        new_node = Node(floor, x=x, y=y)
                        all_nodes.append(new_node)
                        new_node.display(gameDisplay)
                
                elif event.button == 3:
                    #Right-click
                    if clicked_node:
                        highlighted = clicked_node.highlighted
                        if highlighted:
                            #Right-click Highlighted-node
                            #Haven't quite decided what to do here yet
                            pass
                        else:
                            #Right-click Unhighlighted-node
                            curr_highlighted = [n for n in all_nodes if n.highlighted]
                            if curr_highlighted:
                                #If there exists a previously highlighted node, unhighlight it
                                prev_node = curr_highlighted.pop()
                                create_edge(prev_node, clicked_node, edges)
                                prev_node.unhighlight()
                            clicked_node.highlight()
                            highlight_order.append(clicked_node)
                    else:
                        #Right-click Blank-spot
                        curr_highlighted = [n for n in all_nodes if n.highlighted]
                        found = False
                        while not found and len(highlight_order) > 0:
                            prev_node = highlight_order.pop()
                            if prev_node.highlighted:
                                found = True
                                prev_node.unhighlight()
                        if len(highlight_order) > 0:
                            highlight_order[-1].highlight()
                
                """
                for node in all_nodes:
                    if node.collision(x, y):
                        if not prev_node:
                            prev_node = node
                            node.highlight()
                            break
                        else:
                            create_edge(prev_node, node, edges)
                """
        
        #Postvisualizations
        [pygame.draw.line(gameDisplay, (186,225,255),a.get_pos(), b.get_pos(), 5) for a, b in edges]
        [n.display(gameDisplay) for n in all_nodes]
        pygame.display.update()

        clock.tick(10)
    
    pygame.quit()
    quit()

main()