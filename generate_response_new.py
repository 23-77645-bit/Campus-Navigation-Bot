def generate_response(user_input):
    """Generate a response based on user input using ML classification"""
    # Use the ML classifier to determine intent
    intent = st.session_state.classifier.predict_intent(user_input)

    user_input_lower = user_input.lower()

    # Check for 3D map request
    if any(keyword in user_input_lower for keyword in ['3d map', 'visualize', 'navigate 3d', '3d visualization', '3d view', 'show 3d']):
        return "3D_MAP_REQUEST"
    
    # Use ML classification to determine the type of query
    if intent == 'location':
        # Extract possible location names
        possible_locations = get_all_locations()
        # Try to find a match in the user input
        for loc in possible_locations:
            if loc.lower() in user_input_lower:
                location_info = get_location_info(loc, campus_data)
                if location_info:
                    return f"**{location_info['name']}** is located at {location_info['location']}.\\n\\nDescription: {location_info['description']}\\n\\nBuildings: {', '.join(location_info['buildings'])}\\n\\nFloors: {', '.join(location_info['floors'])}"

        # If no direct match, try fuzzy matching
        best_match = find_best_match(user_input_lower, possible_locations, threshold=0.3)
        if best_match:
            location_info = get_location_info(best_match, campus_data)
            if location_info:
                return f"**{location_info['name']}** is located at {location_info['location']}.\\n\\nDescription: {location_info['description']}\\n\\nBuildings: {', '.join(location_info['buildings'])}\\n\\nFloors: {', '.join(location_info['floors'])}"

        return "I'm sorry, I couldn't find information about that location. Try asking about specific places like 'Ibaan Building', 'Sto. Tomas Building', or 'Apacible Museum'."

    elif intent == 'timing':
        # Timing information is not available in the new data
        return "I can provide information about locations and directions. For 3D visualization, try asking 'Show 3D map' or 'Visualize campus'."

    elif intent == 'direction':
        # Extract possible start and end locations
        possible_locations = get_all_locations()
        found_locations = []

        for loc in possible_locations:
            if loc.lower() in user_input_lower:
                found_locations.append(loc)

        if len(found_locations) >= 2:
            start = found_locations[0]
            end = found_locations[1]
            directions = get_directions(start, end, campus_data)
            if directions:
                return f"**Directions from {start.title()} to {end.title()}:**\\n\\n" + "\\n".join([f"{i+1}. {step}" for i, step in enumerate(directions)])
            else:
                return f"Sorry, I don't have directions from {start.title()} to {end.title()}. Try asking for directions between major locations."
        else:
            return "I can provide directions between locations. Try asking 'How do I get from Ibaan Building to Sto. Tomas Building?' or 'Directions from Apacible Museum to Joson Gymnasium.'"

    elif intent == 'greeting':
        return "Hello! I'm your Campus Navigator Bot. I can help you find:\\n\\n• **Locations** - Ask 'Where is the Ibaan Building?' or 'Find the Sto. Tomas Building'\\n• **3D Visualization** - Ask 'Show 3D map' or 'Visualize campus'\\n• **Directions** - Ask 'How do I get from the Ibaan Building to the Sto. Tomas Building?'\\n\\nJust type your question and I'll help you navigate the campus!"

    elif intent == 'unknown':
        # Fallback for unknown queries - use keyword-based detection
        if any(keyword in user_input_lower for keyword in ['where is', 'location', 'find', 'locate', 'at']):
            # Extract possible location names
            possible_locations = get_all_locations()
            # Try to find a match in the user input
            for loc in possible_locations:
                if loc.lower() in user_input_lower:
                    location_info = get_location_info(loc, campus_data)
                    if location_info:
                        return f"**{location_info['name']}** is located at {location_info['location']}.\\n\\nDescription: {location_info['description']}\\n\\nBuildings: {', '.join(location_info['buildings'])}\\n\\nFloors: {', '.join(location_info['floors'])}"

            # If no direct match, try fuzzy matching
            best_match = find_best_match(user_input_lower, possible_locations, threshold=0.3)
            if best_match:
                location_info = get_location_info(best_match, campus_data)
                if location_info:
                    return f"**{location_info['name']}** is located at {location_info['location']}.\\n\\nDescription: {location_info['description']}\\n\\nBuildings: {', '.join(location_info['buildings'])}\\n\\nFloors: {', '.join(location_info['floors'])}"

            return "I'm sorry, I couldn't find information about that location. Try asking about specific places like 'Ibaan Building', 'Sto. Tomas Building', or 'Apacible Museum'."

        # Check for timing queries
        elif any(keyword in user_input_lower for keyword in ['when', 'open', 'close', 'hours', 'timing', 'time']):
            return "I can provide information about locations and directions. For 3D visualization, try asking 'Show 3D map' or 'Visualize campus'."

        # Check for direction queries
        elif any(keyword in user_input_lower for keyword in ['how do i get', 'direction', 'navigate', 'go to', 'reach', 'path', 'route']):
            # Extract possible start and end locations
            possible_locations = get_all_locations()
            found_locations = []

            for loc in possible_locations:
                if loc.lower() in user_input_lower:
                    found_locations.append(loc)

            if len(found_locations) >= 2:
                start = found_locations[0]
                end = found_locations[1]
                directions = get_directions(start, end, campus_data)
                if directions:
                    return f"**Directions from {start.title()} to {end.title()}:**\\n\\n" + "\\n".join([f"{i+1}. {step}" for i, step in enumerate(directions)])
                else:
                    return f"Sorry, I don't have directions from {start.title()} to {end.title()}. Try asking for directions between major locations."
            else:
                return "I can provide directions between locations. Try asking 'How do I get from Ibaan Building to Sto. Tomas Building?' or 'Directions from Apacible Museum to Joson Gymnasium'."

        else:
            return "I'm not sure I understand. You can ask me about locations, get 3D visualizations, or directions on campus. For example:\\n\\n• 'Where is the Ibaan Building?'\\n• 'Show 3D map'\\n• 'How do I get from Ibaan Building to Sto. Tomas Building?'"