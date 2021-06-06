import math
import pygame

"""
This is the features module, containing all the objects that a floorplan is composed of.
"""

class Node:
    """
    Nodes are feature objects, they can be connections, doors, or just simply nodes
    """
    node_type = "Node"
    name = "Unamed Node"

    def __init__(self, parent_floor, name="Unamed Node", x=None, y=None):
        """
        x:              [Integer] Pixel x position of this node on the [Floor]
        y:              [Integer] Pixel y position of this node of the [Floor]
        edges:          [Dictionary] mapping neighbouring [Node] to [Float] distance between the two
        parent_floor:   [Floor] of which this node belongs to
        name:           [Strong] name of this node
        image           [pygame.Surface] image/surface which hosts the png of this node
        highlighted     [Boolean] representing whether this node is in it's highlightes state
        high_image      [pygame.Surface] image/surface which hosts the png of the highlighted node
        """
        self.x = x
        self.y = y
        self.edges = {}
        self.parent_Floor = parent_floor
        self.name = name
        self.image = pygame.image.load("assets/Node.png").convert_alpha()
        self.high_image = pygame.image.load("assets/Node highlighted.png").convert_alpha()
        self.highlighted = False

    def __repr__(self):
        node_type = self.node_type
        if self.highlighted:
            node_type = node_type.capitalize()
        return "[{node_type}] {name} | Position: {position}".format(
                node_type=node_type, name=self.name, position=self.get_pos()
            )
    
    def __str__(self):
        ret_str = "[{node_type}] {name} | Position: {position}\nEdges: ".format(
                node_type=self.node_type, name=self.name, position=self.get_pos()
            )
        edges_string = ""
        count = 1
        for other_node in self.edges:
            name = other_node.get_name()
            if name == "Unamed Node":
                name = other_node.get_pos()
            
            edges_string += "({name} -> [{other_type}]{other_name}: {distance}) ".format(
                    name=self.name,other_type=other_node.get_type(), other_name=other_node.get_name(), distance=self.edges[other_node]
                )
            if not count%5:
                edges_string += "\n"
        
        return ret_str + edges_string
    
    
    """
    Connectes two nodes by adding an edge going from each way
    """
    def connect_nodes(self, other_node, distance=None):
        if not distance:
            distance = self.calculate_distance(other_node)
        self.edges[other_node] = distance
        other_node.edges[self] = distance


    """
    Calculates the distance in meters between two nodes, assuming no obstacles between them
    """
    def calculate_distance(self, other_node):
        if any([i == None for i in [self.x, self.y, other_node.get_x(), other_node.get_y()]]):
            return None 
        scaling = self.parent_Floor.get_scale()
        x_diff = self.x - other_node.get_x()
        y_diff = self.y - other_node.get_y()
        return (x_diff**2 + y_diff**2)**0.5 * scaling
    
    
    """
    Sets the distance between two nodes irrespective of their actual positions. Creating this
    connection if it didn't exist before.
    """
    def set_distance(self, distance, other_node):
        self.edges[other_node] = distance
        other_node.get_edges()[self] = distance
    

    """
    Gets the distance between two nodes
        - returns the length of the edge
        - If there is no preset distance, it calculates the distance
        - If any node is missing coordinates then it errors
    """
    def get_distance(self, other_node):
        if other_node in self.get_edges():
            return self.get_edges()[other_node]
        elif all([i != None for i in [self.x, self.y, other_node.get_x(), other_node.get_y()]]):
            return self.calculate_distance(other_node)
        else:
            print(self.x, self.y, other_node.get_x(), other_node.get_y())
            raise Exception("missing coordinates") 
    

    """
    Simply removes a connection, throwing print statements if this connection didn't exist.
    """
    def remove_connection(self, other_node):
        failed = self.edges.pop(other_node, None)
        if not failed:
            print("No such edge from", self, "to", other_node)
        failed = other_node.get_edges().pop(self, None)
        if not failed:
            print("No such edge from", other_node, "to", self)
            print("WARNING THAT EDGE FROM SELF TO OTHER_NODE WAS DELETED")
    

    """
    Expands a node by returning all the accessible neighbours
    """
    def expand(self, traveller):
        return [neighbour for neighbour in self.get_edges()]
    

    """
    Displays the node on the screen
    """
    def display(self, display):
        image = self.image
        if self.highlighted:
            image = pygame.image.load("assets/Node highlighted.png").convert_alpha()
        width, height = image.get_size()
        display.blit(image, (self.x - round(width/2), self.y - round(height/2)))

    
    """
    Returns True or False depending on whether there is a collision between 
    self and (x,y) on display
    """
    def collision(self, x, y):
        width, height = self.image.get_size()
        distance = ((x - self.x)**2 + (y - self.y)**2 )**(1/2)
        if distance < width/2:
            return True
        return False
    

    """
    Highlights the current node by setting self.highlighted = True
    """
    def highlight(self):
        self.highlighted = True
    

    """
    Unhighlights the current node by setting self.highlighted = False
    """
    def unhighlight(self):
        self.highlighted = False
    

    """
    <<<<<<<<<<[GET and SET METHODS]>>>>>>>>>>
    """
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_pos(self):
        return (self.x, self.y)
    
    def get_edges(self):
        return self.edges
    
    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name
    
    def get_type(self):
        return self.node_type
    
    def get_image(self):
        return self.image
    
    def highlighted(self):
        return self.highlight