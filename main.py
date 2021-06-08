import pygame
import sys
import time
import itertools

from pygame import sprite
from pygame.locals import *
from floors import *
# from features import *
# from traversal import *
from interface import *

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
def mouse_press(event, rightclick_dropdown, all_nodes, highlight_order, edges, floor, gameDisplay, clicked_node):
    x, y = event.pos
    #marker
    target_node = None
    for node in all_nodes:
        if node.collision(x, y):
            target_node = node
    if event.button == 1:
        #Left-click
        if target_node:
            highlighted = target_node.highlighted
            if highlighted:
                #Left-click Highlighted-node
                target_node.unhighlight()
                highlight_order.remove(target_node)
            else:
                #Left-click Unhighlighted-node
                curr_highlighted = [n for n in all_nodes if n.highlighted]
                if curr_highlighted:
                    for n in curr_highlighted:
                        create_edge(n, target_node, edges)
                else:
                    target_node.highlight()
                    highlight_order.append(target_node)
        else:
            #Left-click Blank-spot
            new_node = Node(floor, x=x, y=y)
            all_nodes.append(new_node)
            new_node.display(gameDisplay)

    elif event.button == 3:
        #Right-click
        if target_node:
            highlighted = target_node.highlighted
            if highlighted:
                #Right-click Highlighted-node
                rightclick_dropdown.make_visible()
                rightclick_dropdown.goto(event.pos)
                clicked_node[0] = target_node
            else:
                #Right-click Unhighlighted-node
                curr_highlighted = [n for n in all_nodes if n.highlighted]
                if curr_highlighted:
                    #If there exists a previously highlighted node, unhighlight it
                    prev_node = curr_highlighted.pop()
                    create_edge(prev_node, target_node, edges)
                    prev_node.unhighlight()
                target_node.highlight()
                highlight_order.append(target_node)
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
Takes care of the case of keypress being "s" or "g" where a start/goal node is created
"""
def s_or_g_keypress(event, all_nodes, goal_nodes):
    x, y = pygame.mouse.get_pos()
    target_node = None
    for node in all_nodes:
        if node.collision(x, y):
            target_node = node
    if target_node:
        if event.key == pygame.locals.K_s:
            return target_node
        elif target_node not in goal_nodes:
            goal_nodes.append(target_node)
        else:
            goal_nodes.remove(target_node)


"""
Takes care of deleting highlighted nodes when "Backspace" or "Del" is pressed
"""
def delete_highlighted_nodes(goal_nodes, goal_paths, all_nodes, highlight_order, edges):
    highlighted_nodes = [] #in case we decide to make highlighting multiple nodes possible
    for node in all_nodes:
        if node.highlighted:
            highlighted_nodes.append(node)
    
    for node in highlighted_nodes:
        all_nodes.remove(node)
        neighbours = [i for i in node.get_edges()]
        for neighbour in neighbours:
            node.remove_connection(neighbour)
            if (node, neighbour) in edges:
                edges.remove((node, neighbour))
            elif (neighbour, node) in edges:
                edges.remove((neighbour, node))
        if node in highlight_order:
            highlight_order.remove(node)
        if start_node == node:
            start_node = None
        if node in goal_nodes:
            goal_nodes.remove(node)
        if node in goal_paths:
            goal_paths.pop(node)

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
    rightclick_dropdown = Rightclick_Dropdown(DISPLAY_WIDTH, DISPLAY_HEIGHT)
    pygame.display.set_caption('A bit Racey')

    # floorplan_image = pygame.image.load("assets/Phasmophobia-high school floorplan_image.jpg").convert()
    # floorplan_image = pygame.image.load("assets/Phasmophobia-high school floorplan_image 2.png").convert()
    # floorplan_image = pygame.image.load("assets/Phasmophobia-high school floorplan 3.png").convert()
    floorplan_image = pygame.image.load("assets/Brownstone high school first floor.png").convert()

    floorplan_image = scale_image(DISPLAY_WIDTH, DISPLAY_HEIGHT, floorplan_image)
    gameDisplay.fill((255, 255, 255))
    floor = Floor(floorplan_image)

    #Initialisation of groups
    all_nodes = []
    edges = []
    
    highlight_order = []
    start_node = None
    goal_nodes = []
    goal_paths = {}
    # while pygame.time.get_ticks() <= 50000:
    held_node = None
    command = None
    clicked_node = [None] #list for mutability properties
    while True:
        #Previsualisations
        display_center(gameDisplay, floor.get_display())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if event.key == pygame.locals.K_ESCAPE:
                    #if the keypress is "esc" and quits the game
                    pygame.quit()
                    sys.exit()
                
                elif event.key == pygame.locals.K_s or event.key == pygame.locals.K_g:
                    #if the keypress is "s" or "g"
                    temp = s_or_g_keypress(event, all_nodes, goal_nodes)
                    if temp:
                        start_node = temp
                
                elif event.key == pygame.locals.K_DELETE or event.key == pygame.locals.K_BACKSPACE:
                    delete_highlighted_nodes(goal_nodes, goal_paths, all_nodes, highlight_order, edges)
                        

                elif (keys[pygame.locals.K_RCTRL] or keys[pygame.locals.K_LCTRL]) and keys[pygame.locals.K_z]:
                    #ctrl+z pressed
                    pass
                
                
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if command:
                    if "Move_Node" == command:
                        print("I made it here")
                        held_node.move_to((x, y))
                        command = None
                        held_node = None
                        clicked_node = [None]
                    elif "Copy" == command:
                        pass
                    elif "Paste" == command:
                        pass
                    elif "Delete" == command:
                        pass
                    elif "Highlight" == command:
                        pass
                    elif "Unhighlight" == command:
                        pass
                    elif "Change_Attribute" == command:
                        pass
                    elif "Delete_Edge" == command:
                        pass
                elif not rightclick_dropdown.is_invisible():
                    if rightclick_dropdown.collision(event.pos):
                        #Clicked the dropdown menu
                        command = rightclick_dropdown.command(event.pos)
                        x, y = pygame.mouse.get_pos()
                        if "Move_Node" == command:
                            held_node = clicked_node[0]
                        elif "Copy" == command:
                            pass
                        elif "Paste" == command:
                            pass
                        elif "Delete" == command:
                            pass
                        elif "Highlight" == command:
                            pass
                        elif "Unhighlight" == command:
                            pass
                        elif "Change_Attribute" == command:
                            pass
                        elif "Delete_Edge" == command:
                            pass
                    rightclick_dropdown.make_invisible()
                    # elif not rightclick_dropdown.is_invisible():
                        #clicked off the dropdown menue while it was visible
                        # rightclick_dropdown.make_invisible()
                        # for node in all_nodes:
                        #     if node.collision(x, y):
                                # clicked_node[0] = node
                    #marker
                else:
                    mouse_press(event, rightclick_dropdown, all_nodes, highlight_order, edges, floor, gameDisplay, clicked_node)
        if command:
            if "Move_Node" == command:
                x, y = pygame.mouse.get_pos()
                held_node.move_to((x, y))
            elif "Copy" == command:
                pass
            elif "Paste" == command:
                pass
            elif "Delete" == command:
                pass
            elif "Highlight" == command:
                pass
            elif "Unhighlight" == command:
                pass
            elif "Change_Attribute" == command:
                pass
            elif "Delete_Edge" == command:
                pass
        
        #Postvisualizations
        [pygame.draw.line(gameDisplay, EDGE_COLOUR,a.get_pos(), b.get_pos(), 5) for a, b in edges]
        #show all goal paths
        if start_node:
            for goals in goal_nodes:
                search = A_Star_Search()
                path = search.find_path(start_node, goals, None)
                goal_paths[goals] = path
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

        rightclick_dropdown.render(gameDisplay)
        pygame.display.update()

        print("command", command)
        print("clicked_node", repr(clicked_node))
        clock.tick(10)

main()