"""
Search functionality for campus locations
"""

from typing import List, Dict, Optional
from difflib import get_close_matches
from campus_data import get_all_locations, get_location_by_name, get_locations_by_category


def search_locations(query: str, limit: int = 10) -> List[Dict]:
    """
    Search for locations based on a query string
    
    Args:
        query: Search query string
        limit: Maximum number of results to return
    
    Returns:
        List of location dictionaries matching the query
    """
    all_locations = get_all_locations()
    query_lower = query.lower().strip()
    
    # Direct matches first
    direct_matches = []
    partial_matches = []
    category_matches = []
    
    for location_name in all_locations:
        location_info = get_location_by_name(location_name)
        if not location_info:
            continue
            
        # Direct name match
        if query_lower == location_name.lower():
            direct_matches.append({
                'name': location_name,
                'category': location_info['category'],
                'coordinates': location_info['coordinates']
            })
        # Partial name match
        elif query_lower in location_name.lower() or location_name.lower() in query_lower:
            partial_matches.append({
                'name': location_name,
                'category': location_info['category'],
                'coordinates': location_info['coordinates']
            })
        # Category match
        elif query_lower in location_info['category'].lower():
            category_matches.append({
                'name': location_name,
                'category': location_info['category'],
                'coordinates': location_info['coordinates']
            })
    
    # If we don't have enough results, use fuzzy matching
    if len(direct_matches) + len(partial_matches) == 0:
        fuzzy_matches = get_close_matches(
            query_lower, 
            [name.lower() for name in all_locations], 
            n=limit, 
            cutoff=0.3
        )
        
        for fuzzy_match in fuzzy_matches:
            # Find the original case name
            original_name = next(name for name in all_locations if name.lower() == fuzzy_match)
            if original_name not in [m['name'] for m in direct_matches + partial_matches]:
                location_info = get_location_by_name(original_name)
                if location_info:
                    partial_matches.append({
                        'name': original_name,
                        'category': location_info['category'],
                        'coordinates': location_info['coordinates']
                    })
    
    # Combine results in order of relevance
    results = direct_matches + partial_matches + category_matches
    
    # Return up to the limit
    return results[:limit]


def get_locations_by_partial_match(query: str) -> List[str]:
    """
    Get location names that partially match the query
    
    Args:
        query: Search query string
    
    Returns:
        List of location names that match the query
    """
    all_locations = get_all_locations()
    query_lower = query.lower().strip()
    
    matches = []
    for location_name in all_locations:
        if query_lower in location_name.lower() or location_name.lower() in query_lower:
            matches.append(location_name)
    
    return matches


def get_locations_by_category_search(category: str) -> List[Dict]:
    """
    Get locations by category
    
    Args:
        category: Category to search for
    
    Returns:
        List of location dictionaries in the category
    """
    return get_locations_by_category(category)


def get_all_categories() -> List[str]:
    """
    Get all unique categories in the campus data
    
    Returns:
        List of unique category names
    """
    from campus_data import load_campus_data
    data = load_campus_data()
    
    categories = set()
    for location_id, location_info in data['locations'].items():
        categories.add(location_info['category'])
    
    return sorted(list(categories))