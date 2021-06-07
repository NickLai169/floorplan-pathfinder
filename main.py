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
Takes care of the case where the input is a mouse_press. for creating nodes
"""
def mouse_press(event, all_nodes, highlight_order, edges, floor, gameDisplay):
    x, y = event.pos
    clicked_node = None
    #marker
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
<<<<[GLOBAL CONSTANTS]>>>>
"""
DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 720
EDGE_COLOUR = (186,225,255) #light blue
PATH_COLOUR = (255,255,186) #Light Yellow

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
    
    highlight_order = []
    start_node = None
    goal_nodes = []
    goal_paths = {}
    # while pygame.time.get_ticks() <= 50000:
    while True:
        #Previsualisations
        display_center(gameDisplay, floor.get_display())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


            elif event.type == pygame.KEYDOWN:
                pos = pygame.mouse.get_pos()
                if event.key == pygame.locals.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.locals.K_n:
                    new_node = Node(floor, x=pos[0], y=pos[1])
                    all_nodes.append(new_node)
                    new_node.display(gameDisplay)
                
                elif event.key == pygame.locals.K_s or event.key == pygame.locals.K_g:
                    #if the keypress is "s" or "g"
                    x, y = pygame.mouse.get_pos()
                    clicked_node = None
                    for node in all_nodes:
                        if node.collision(x, y):
                            clicked_node = node
                    if clicked_node:
                        if event.key == pygame.locals.K_s:
                            start_node = clicked_node
                        elif clicked_node not in goal_nodes:
                            goal_nodes.append(clicked_node)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_press(event, all_nodes, highlight_order, edges, floor, gameDisplay)
        #Postvisualizations
        [pygame.draw.line(gameDisplay, EDGE_COLOUR,a.get_pos(), b.get_pos(), 5) for a, b in edges]
        #show all goal paths
        if start_node:
            for goals in goal_nodes:
                search = A_Star_Search()
                path = search.find_path(start_node, goals, None)
                goal_paths[node] = path
                if len(path) > 1:
                    this = path.pop(0)
                    that = None
                    
                    while this != goals and len(path) > 0:
                        that = path.pop(0)
                        pygame.draw.line(gameDisplay, PATH_COLOUR, this.get_pos(), that.get_pos(), 8)
                        this = that
        [n.display(gameDisplay) for n in all_nodes]

        if start_node:
            start_s = pygame.image.load("assets/start.png").convert_alpha()
            width, height = start_s.get_size()
            gameDisplay.blit(start_s, (start_node.get_x() - round(width/2), start_node.get_y() - round(height/2)))
        if goal_nodes:
            goal_g = pygame.image.load("assets/goal.png").convert_alpha()
            width, height = goal_g.get_size()
            for goals in goal_nodes:
                gameDisplay.blit(goal_g, (goals.get_x() - round(width/2), goals.get_y() - round(height/2)))

        pygame.display.update()

        clock.tick(10)

main()