import json
from typing import Dict, List, Optional, Tuple


def load_campus_data():
    """Load campus data from JSON file"""
    with open('data/campus_data.json', 'r') as f:
        return json.load(f)


def get_coordinates_map() -> Dict[str, List[float]]:
    """
    Get a dictionary mapping location names to coordinates
    Returns: dict with location names as keys and [x, y, z] coordinates as values
    """
    data = load_campus_data()
    coordinates_map = {}
    
    for location_id, location_info in data['locations'].items():
        coordinates_map[location_info['name']] = location_info['coordinates']
    
    return coordinates_map


def get_location_by_id(location_id: str) -> Optional[Dict]:
    """
    Get location details by its ID
    Args:
        location_id: The ID of the location
    Returns:
        Dictionary with location details or None if not found
    """
    data = load_campus_data()
    return data['locations'].get(location_id)


def get_location_by_name(location_name: str) -> Optional[Dict]:
    """
    Get location details by its name
    Args:
        location_name: The name of the location
    Returns:
        Dictionary with location details or None if not found
    """
    data = load_campus_data()
    
    for location_id, location_info in data['locations'].items():
        if location_info['name'].lower() == location_name.lower():
            return location_info
    
    return None


def get_all_locations() -> List[str]:
    """
    Get all location names
    Returns:
        List of all location names
    """
    data = load_campus_data()
    return [location_info['name'] for location_info in data['locations'].values()]


def location_exists(location_name: str) -> bool:
    """
    Check if a location name exists
    Args:
        location_name: The name to check
    Returns:
        True if location exists, False otherwise
    """
    return get_location_by_name(location_name) is not None


def get_locations_by_category(category: str) -> List[Dict]:
    """
    Get all locations that belong to a specific category
    Args:
        category: The category to filter by
    Returns:
        List of location dictionaries that match the category
    """
    data = load_campus_data()
    matching_locations = []
    
    for location_id, location_info in data['locations'].items():
        if location_info['category'].lower() == category.lower():
            matching_locations.append({
                'id': location_id,
                'name': location_info['name'],
                'category': location_info['category'],
                'coordinates': location_info['coordinates']
            })
    
    return matching_locations