import pygame
import sys
import time
import itertools
from floors import *
from traversal import *
from visualizer import *
from main import *





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