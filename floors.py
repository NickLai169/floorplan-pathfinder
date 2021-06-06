import sys
import time
import pygame
from features import *



class Floor:
    """
    Floors represent each individual floorplan, they do not necessarily have to be based on an image.
    """
    name = "Unamed floorplan"
    
    def __init__(self, display):
        """
        node_count:         [Integer] denoting the number of "nodes" in the [Floor]
        nodes:              [List] of all the "passage points" in the floorplan, these are things like
                                passsageways, intersections, corners, in front of doors.
        doors:              [Dictionary] mapping of all the doors to the nodes they connect to
        door_count:         [Integer] denoting the number of doors in the [Floor]
        connections:        [Dictionary] mapping of all the connecting [Nodes] to the other Floor objects that 
                                they connect to
        connections_count:  [Integer] denoting the number of connecting points to other [Floors]
        scale:              [Float] distance (in meters) per pixel of the floorplan
        
        """
        self.nodes = []
        self.node_count = 0
        self.doors = {}
        self.door_count = 0
        self.connections = {}
        self.connections_count = 0
        self.scale = 1
        self.display = display
    
    def __repr__(self):
        return "{}: {}".format(self.name, self.connections)
    
    
    """
    Connects this [Floor] to another [Floor] by adding a connection
    """
    def connect_floor(self, other_floor, my_connection, their_connection, distance=0):
        self.connections[my_connection] = other_floor
        self.connections_count += 1

        my_connection.set_distance(distance, their_connection)


    

    """
    Disconnect this [Floor] to the target other [Floor]
    """
    def disconnect_floor(self, other_floor):
        deletion = False
        for connection in self.connections:
            if self.connections[connection] == other_floor:
                del self.connection
                deletion == True

        if not deletion:
            print("No such connection to", other_floor, "exists")
            

    """
    Sets the image for the Floor for which the Floor is based on
    """
    def set_floorplan_image(self, image_name):
        """
        image:      [pygame.image] object that represents the image of the floorplan
        name:       [String] name of the floorplan
        """
        self.image = pygame.image.load(image_name).convert()
        if self.name == "Unamed floorplan":
            self.name = image_name
    

    """
    Creates a new node on the Floor
    """
    def make_node(self, name="Unamed Node", x=None, y=None):
        new_node = Node(self, name, x, y)
        self.nodes.append(new_node)
        self.node_count += 1

        return new_node


    """
    <<<<<<<<<<[GET and SET METHODS]>>>>>>>>>>
    """
    def get_nodes(self):
        return self.get_nodes

    def get_node_count(self):
        return self.node_count
    
    def get_doors(self):
        return self.doors
    
    def get_door_count(self):
        return self.door_count
    
    def get_connections(self):
        return self.connections
    
    def get_connections_count(self):
        return self.connections_count
    
    def get_scale(self):
        return self.scale
    
    def get_image(self):
        return self.image
    
    def get_display(self):
        return self.display