from abc import ABC, abstractmethod
from features import *

"""
This is the traversal moduel, with the different searching algorithm classes
"""
 
class Pathfinder(ABC):
 
    @abstractmethod
    def find_path(self, start, target, traveller=None):
        """
        start:      [Node] of the start location
        target:     [Node] of the destination location
        traveller:  [User] who is traversing the graph
        @return:    [List] of the nodes that you must traverse to get from start
                    to the target inclusive.
        """
        pass

class Breadth_First_Search(Pathfinder):
    """
    A simple BFS algorithm, irrespective of the edge_length between nodes
    """

    def find_path(self, start, target, traveller=None):
        visited = []
        parent_map = {start: start}
        curr_node = None
        queue = [start] + start.expand(traveller)

        target_found = False
        while curr_node != target and queue:
            curr_node = queue.pop(0)
            visited.append(curr_node)
            
            for node in curr_node.expand(traveller):
                if node not in parent_map:
                    parent_map[node] = curr_node
                if node not in visited and node not in queue:
                    queue.append(node)
            
            if curr_node == target:
                target_found = True
            
        if not target_found:
            print("No possible path from {start} to {target} found.".format(start=start, target=target))
            return []
        
        ret_path = []
        while curr_node != start:
            ret_path = [curr_node] + ret_path
            curr_node = parent_map[curr_node]
        ret_path = [curr_node] + ret_path
        return ret_path

class A_Star_Search(Pathfinder):
    """
    Performs an A* search with the input algorithm, defaults to using the striaght_line distance
    assuming no user input. REQUIRES THAT ALL NODES HAVE A POSITION.

    Also note that A_Star search would be optimal as long as the preset edge lengths are not geometrically
    invalid relative to their actual layout.
    """

    def straight_line_heuristic(a, b):
        return a.calculate_distance(b)

    def find_path(self, start, target, traveller, heuristic=straight_line_heuristic):
        visited = []
        parent_map = {start: start}
        tr_parent_map = {start: start} #only keeps track of expanded nodes
        curr_node = None
        fringe = [start] + start.expand(traveller)
        cost_to_node = {start: 0}

        target_found = False
        while curr_node != target and fringe:
            curr_node = fringe.pop(0)
            tr_parent_map[curr_node] = parent_map[curr_node]
            cost_to_node[curr_node] = cost_to_node[parent_map[curr_node]] + curr_node.get_distance(parent_map[curr_node])
            visited.append(curr_node)
            
            for node in curr_node.expand(traveller):
                if node not in parent_map or node.get_distance(parent_map[node]) > node.get_distance(curr_node):
                    #This is in err, I am going to try remove it. Causing infinite loop
                    parent_map[node] = curr_node
                if node not in visited and node not in fringe:
                    fringe.append(node)
            fringe.sort(key=lambda node: heuristic(node, target) + parent_map[node].get_distance(node)  + cost_to_node[parent_map[node]])
            
            if curr_node == target:
                target_found = True
            
        if not target_found:
            print("No possible path from {start} to {target} found.".format(start=start, target=target))
            return []
        
        ret_path = []
        while curr_node != start:
            # print("whoops", repr(curr_node), repr(start), repr(target))
            ret_path = [curr_node] + ret_path
            curr_node = tr_parent_map[curr_node]
        ret_path = [curr_node] + ret_path
        return ret_path

class Dijkstras_algorithm(Pathfinder):
    """
    Basically A* search, except Dijkstras. I copied and pasted 95% of it, pretty sure it works though.
    I only really got rid of the heuristic :P
    """
    
    def find_path(self, start, target, traveller):
        visited = []
        parent_map = {start: start}
        curr_node = None
        fringe = [start] + start.expand(traveller)
        cost_to_node = {start: 0}

        target_found = False
        while curr_node != target and fringe:
            curr_node = fringe.pop(0)
            cost_to_node[curr_node] = cost_to_node[parent_map[curr_node]] + curr_node.get_distance(parent_map[curr_node])
            visited.append(curr_node)
            
            for node in curr_node.expand(traveller):
                if node not in parent_map or node.get_distance(parent_map[node]) > node.get_distance(curr_node):
                    parent_map[node] = curr_node
                if node not in visited and node not in fringe:
                    fringe.append(node)
            fringe.sort(key=lambda node: parent_map[node].get_distance(node) + cost_to_node[parent_map[node]])
            
            if curr_node == target:
                target_found = True
            
        if not target_found:
            print("No possible path from {start} to {target} found.".format(start=start, target=target))
            return []
        
        ret_path = []
        while curr_node != start:
            ret_path = [curr_node] + ret_path
            curr_node = parent_map[curr_node]
        ret_path = [curr_node] + ret_path
        return ret_path