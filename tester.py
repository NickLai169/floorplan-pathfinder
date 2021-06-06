import pygame
import sys
import time
import itertools
from floors import *
from traversal import *
from visualizer import *
from main import *

class Ball(pygame.sprite.Sprite):
    """A ball that will move across the screen
    Returns: ball object
    Functions: update, calcnewpos
    Attributes: area, vector"""

    def __init__(self, vector):
        pygame.sprite.Sprite.__init__(self)
        ball = pygame.image.load('assets/cursor.PNG')
        self.image = ball
        self.rect = ball.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.vector = vector

    def update(self):
        newpos = self.calcnewpos(self.rect,self.vector)
        self.rect = newpos

    def calcnewpos(self,rect,vector):
        (angle,z) = vector
        (dx,dy) = (z*math.cos(angle),z*math.sin(angle))
        return rect.move(dx,dy)

def tester_main():
    pygame.init()

    gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT), 32)
    pygame.display.set_caption('Where does the caption actually go?')
    gameDisplay.fill((255, 255, 255))

    # [create new object as instance of ball class]
    edge_surface = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    line = pygame.draw.line(gameDisplay, (186,225,255), (0,0), (200,400), 30)
    # gameDisplay.blit(line, (0,0))
    
    pygame.display.update()
    time.sleep(3)
    
    print("ORAORAROROAROA")
    pygame.quit()
    quit()

tester_main()


# first_floor = Floor()

# a = first_floor.make_node(name="a", x=0, y=0)
# b = first_floor.make_node(name="b", x=1, y=0)
# c = first_floor.make_node("c", x=1, y=1)
# d = first_floor.make_node(name="d", x=2, y=1)
# e = first_floor.make_node(name="e", x=1, y=2)
# f = first_floor.make_node(name="f", x=2, y=2)
# g = first_floor.make_node(name="g", x=3, y=2)

# a.connect_nodes(b)
# b.connect_nodes(c)
# b.connect_nodes(d)
# c.connect_nodes(e)
# d.connect_nodes(f)
# e.connect_nodes(g)
# e.connect_nodes(f)

# # for pair in itertools.combinations([a, b, c, d, e, f, g], 2):
# #     print(repr(pair[0]), "->", repr(pair[1]), ":", pair[0].get_distance(pair[1]))

# bfs_search = A_Star_Search()
# print(bfs_search.find_path(a, g, None))