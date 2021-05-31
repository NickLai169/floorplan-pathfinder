import sys
import time
import pygame



"""
Floors represent each individual floorplan, they do not necessarily have to be based on an image.
"""
class Floor:
    name = "Unamed floorplan"
    
    def __init__(self):
        """
        node_count:         [Integer] denoting the number of "nodes" in the floorplan
        nodes:              [Integer] denoting the number of "passage points" in the floorplan, these are
                                things inpasssageways like intersections, corners, in front of doors.
        doors:              [Dictionary] mapping of all the doors to the nodes they connect to
        door_count:         [Integer] denoting the number of doors in the floor
        connections:        [Dictionary] mapping of all the connections to the other Floor objects that 
                                they connect to
        connections_count:  [Integer] denoting the number of connecting points to other floors
        scale:              [Float] distance (in meters) per pixel of the floorplan
        
        """
        self.nodes = {}
        self.node_count = 0
        self.doors = {}
        self.door_count = 0
        self.connections = {}
        self.connections_count = 0
        self.scale = 1
    
    def __repr__(self):
        return self.name
    
    
    """
    Connects this Floor to another Floor by adding a connection
    """
    def connect_floor(self, other_floor,connection):
        self.connections[connection] = other_floor
        self.connections_count += 1
    
    """
    Disconnect this Floor to the target other Floor
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
    [GET and SET METHODS]
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
