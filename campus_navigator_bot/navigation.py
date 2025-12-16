"""
Navigation module with pathfinding algorithms for campus navigation
"""

import math
from typing import List, Dict, Tuple, Optional
from campus_data import get_location_by_name, get_all_locations, get_coordinates_map


class CampusGraph:
    """
    A graph representation of the campus with locations as nodes and connections as edges
    """
    
    def __init__(self):
        self.vertices = {}
        self.edges = {}
        self._initialize_graph()
    
    def _initialize_graph(self):
        """Initialize the graph with campus locations as vertices"""
        coordinates_map = get_coordinates_map()
        
        # Add all locations as vertices
        for location_name in coordinates_map.keys():
            self.vertices[location_name] = coordinates_map[location_name]
            self.edges[location_name] = []
        
        # Create connections between nearby locations
        # For now, connect locations that are within a certain distance
        locations = list(coordinates_map.keys())
        for i in range(len(locations)):
            for j in range(i + 1, len(locations)):
                loc1 = locations[i]
                loc2 = locations[j]
                
                # Calculate Euclidean distance
                coord1 = coordinates_map[loc1]
                coord2 = coordinates_map[loc2]
                distance = math.sqrt((coord1[0] - coord2[0])**2 + 
                                   (coord1[1] - coord2[1])**2 + 
                                   (coord1[2] - coord2[2])**2)
                
                # Connect if locations are reasonably close (adjust threshold as needed)
                # Using a threshold of 20 units to connect nearby locations
                if distance <= 20:
                    self.edges[loc1].append((loc2, distance))
                    self.edges[loc2].append((loc1, distance))
    
    def get_neighbors(self, vertex: str) -> List[Tuple[str, float]]:
        """Get neighbors of a vertex with their distances"""
        return self.edges.get(vertex, [])
    
    def get_vertex_count(self) -> int:
        """Get the number of vertices in the graph"""
        return len(self.vertices)


def dijkstra(graph: CampusGraph, start: str, end: str) -> Tuple[Optional[List[str]], float]:
    """
    Find shortest path using Dijkstra's algorithm
    
    Args:
        graph: CampusGraph instance
        start: Starting location name
        end: Destination location name
    
    Returns:
        Tuple of (path as list of location names, total distance) or (None, float('inf')) if no path
    """
    if start not in graph.vertices or end not in graph.vertices:
        return None, float('inf')
    
    # Initialize distances and previous nodes
    distances = {vertex: float('inf') for vertex in graph.vertices}
    previous = {vertex: None for vertex in graph.vertices}
    unvisited = set(graph.vertices.keys())
    
    # Set starting distance to 0
    distances[start] = 0
    
    while unvisited:
        # Find the unvisited node with smallest distance
        current = min(unvisited, key=lambda vertex: distances[vertex])
        
        # If we've reached the destination or the smallest distance is infinity, break
        if current == end or distances[current] == float('inf'):
            break
        
        # Update distances to neighbors
        for neighbor, weight in graph.edges[current]:
            if neighbor in unvisited:
                new_distance = distances[current] + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current
        
        unvisited.remove(current)
    
    # Reconstruct path
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    
    path.reverse()
    
    # Return path if it starts with the start location
    if path[0] == start:
        return path, distances[end]
    else:
        return None, float('inf')


def get_directions_with_pathfinding(start: str, end: str) -> Tuple[Optional[List[str]], float]:
    """
    Get directions between two locations using pathfinding algorithm
    
    Args:
        start: Starting location name
        end: Destination location name
    
    Returns:
        Tuple of (list of directions/steps, total distance) or (None, float('inf')) if no path
    """
    graph = CampusGraph()
    
    # Find shortest path
    path, distance = dijkstra(graph, start, end)
    
    if path is None:
        return None, float('inf')
    
    # Convert path to human-readable directions
    directions = []
    for i in range(len(path)):
        if i == 0:
            directions.append(f"Start at {path[i]}")
        elif i == len(path) - 1:
            directions.append(f"Arrive at {path[i]}")
        else:
            directions.append(f"Go from {path[i-1]} to {path[i]}")
    
    return directions, distance


def get_directions(start: str, end: str) -> Optional[List[str]]:
    """
    Get directions between two locations
    
    Args:
        start: Starting location name
        end: Destination location name
    
    Returns:
        List of directions/steps or None if no path exists
    """
    directions, _ = get_directions_with_pathfinding(start, end)
    return directions


def calculate_distance(start: str, end: str) -> float:
    """
    Calculate straight-line distance between two locations
    
    Args:
        start: Starting location name
        end: Destination location name
    
    Returns:
        Distance in coordinate units or float('inf') if location doesn't exist
    """
    start_info = get_location_by_name(start)
    end_info = get_location_by_name(end)
    
    if not start_info or not end_info:
        return float('inf')
    
    start_coord = start_info['coordinates']
    end_coord = end_info['coordinates']
    
    distance = math.sqrt(
        (start_coord[0] - end_coord[0])**2 +
        (start_coord[1] - end_coord[1])**2 +
        (start_coord[2] - end_coord[2])**2
    )
    
    return distance