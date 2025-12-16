import streamlit as st
import json
import re
from difflib import get_close_matches
from utils import load_campus_data, find_best_match, get_location_info, get_timing_info, get_directions, IntentClassifier
from campus_data import get_all_locations, location_exists
from navigation_3d import show_campus_3d_map
import time

# Load campus data
campus_data = load_campus_data()

# Set page configuration
st.set_page_config(
    page_title="Campus Navigator Bot",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for chat interface
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        text-align: center;
        color: #1e3a8a;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #4b5563;
        margin-bottom: 2rem;
    }
    
    .user-message {
        background-color: #dbeafe;
        padding: 10px 15px;
        border-radius: 15px;
        margin: 10px 0;
        text-align: right;
        border-left: 4px solid #3b82f6;
    }
    
    .bot-message {
        background-color: #f3f4f6;
        padding: 10px 15px;
        border-radius: 15px;
        margin: 10px 0;
        text-align: left;
        border-left: 4px solid #6b7280;
    }
    
    .chat-container {
        height: 60vh;
        overflow-y: auto;
        padding: 15px;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        background-color: #f9fafb;
        margin-bottom: 20px;
    }
    
    .input-container {
        display: flex;
        gap: 10px;
        margin-top: 20px;
    }
    
    .send-button {
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        cursor: pointer;
        font-size: 16px;
    }
    
    .send-button:hover {
        background-color: #2563eb;
    }
    
    .welcome-box {
        background-color: #eff6ff;
        border: 1px solid #dbeafe;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    .feature-list {
        background-color: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

def sanitize_input(user_input):
    """Sanitize user input to prevent malicious input"""
    # Remove any potentially harmful characters/sequences
    import re
    sanitized = re.sub(r'[<>"\'\\]', '', user_input)
    return sanitized.strip()


def guess_destination(destination_keyword):
    """Guess the intended destination from simple keywords like 'library' or 'cafeteria'"""
    # Dictionary mapping common keywords to actual location names in the dataset
    keyword_to_location = {
        'library': ['Ibaan Building', 'Taal Building', 'Sto. Tomas Building'],  # Academic buildings that might house libraries
        'cafeteria': ['Rosario Canteen', 'Lian Cafeteria'],
        'canteen': ['Rosario Canteen', 'Lian Cafeteria'],
        'dining': ['Rosario Canteen', 'Lian Cafeteria'],
        'food': ['Rosario Canteen', 'Lian Cafeteria'],
        'admin': ['Apacible Museum', 'Ermita Building'],
        'administration': ['Apacible Museum', 'Ermita Building'],
        'gym': ['Joson Gymnasium'],
        'gymnasium': ['Joson Gymnasium'],
        'infirmary': ['Infirmary'],
        'clinic': ['Infirmary'],
        'medical': ['Infirmary'],
        'museum': ['Apacible Museum'],
        'research': ['VIP Corals - Nasugbu Marine Research Station'],
        'student': ['Student Council Building'],
        'services': ['Student Council Building', 'Batangan Student Services Center'],
        'hostel': ['Nasugbu Hostel'],
        'accommodation': ['Nasugbu Hostel'],
        'academic': ['Ibaan Building', 'Taal Building', 'Sto. Tomas Building', 'Joson Gymnasium', 'Lobo Building', 'Lipa Building', 'Calatagan Building', 'Lemery Building', 'San Juan Building'],
        'classroom': ['Ibaan Building', 'Taal Building', 'Sto. Tomas Building', 'Joson Gymnasium', 'Lobo Building', 'Lipa Building', 'Calatagan Building', 'Lemery Building', 'San Juan Building'],
        'building': ['Ibaan Building', 'Taal Building', 'Sto. Tomas Building', 'Joson Gymnasium', 'Lobo Building', 'Lipa Building', 'Calatagán Building', 'Lemery Building', 'San Juan Building'],
        'gate': ['Entrance-Exit (Guardhouse)'],
        'entrance': ['Entrance-Exit (Guardhouse)'],
        'exit': ['Entrance-Exit (Guardhouse)'],
        'guard': ['Entrance-Exit (Guardhouse)'],
        'maintenance': ['Maintenance Building'],
        'powerhouse': ['Villadolid Ground Powerhouse'],
        'forest': ['Talisay Mini Forest'],
        'court': ['Open Court']
    }
    
    # Convert the keyword to lowercase for comparison
    keyword_lower = destination_keyword.lower().strip()
    
    # Check if the keyword matches any known mappings
    for keyword, possible_locations in keyword_to_location.items():
        if keyword in keyword_lower:
            # Return the first matching location from the list
            return possible_locations[0]
    
    # If no match is found, return None
    return None

# Sidebar
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
        
        # If still no match, try to guess the destination from simple keywords
        guessed_destination = guess_destination(user_input)
        if guessed_destination:
            location_info = get_location_info(guessed_destination, campus_data)
            if location_info:
                return f"Did you mean **{location_info['name']}**? It is located at {location_info['location']}.\\n\\nDescription: {location_info['description']}\\n\\nBuildings: {', '.join(location_info['buildings'])}\\n\\nFloors: {', '.join(location_info['floors'])}"

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
            # If not enough locations found, try to guess destinations from simple keywords
            # Split the user input to identify potential start and end locations
            words = user_input_lower.split()
            
            # Try to find potential start and end locations using the guessing function
            start_guessed = None
            end_guessed = None
            
            # Look for phrases like "from X to Y" to identify start and end
            import re
            from_to_match = re.search(r'from\s+(.+?)\s+to\s+(.+)', user_input_lower)
            if from_to_match:
                start_part = from_to_match.group(1).strip()
                end_part = from_to_match.group(2).strip()
                
                # Try exact match first
                for loc in possible_locations:
                    if start_part in loc.lower():
                        start_guessed = loc
                        break
                    if end_part in loc.lower():
                        end_guessed = loc
                        break
                
                # If no exact match, try guessing
                if not start_guessed:
                    start_guessed = guess_destination(start_part)
                if not end_guessed:
                    end_guessed = guess_destination(end_part)
            else:
                # If no "from X to Y" pattern, try to guess from the whole input
                # First try to guess the start location
                start_guessed = guess_destination(user_input_lower)
                # For end location, we'll try a different approach by splitting the input
                if not start_guessed:
                    # Try to extract potential locations from keywords in the input
                    for keyword in ['library', 'cafeteria', 'canteen', 'dining', 'food', 'admin', 'gym', 'infirmary', 'museum', 'research', 'student', 'hostel', 'gate', 'entrance', 'exit']:
                        if keyword in user_input_lower:
                            potential_guessed = guess_destination(keyword)
                            if potential_guessed and not start_guessed:
                                start_guessed = potential_guessed
                            elif potential_guessed and start_guessed and potential_guessed != start_guessed:
                                end_guessed = potential_guessed
                                break
            
            if start_guessed and end_guessed:
                directions = get_directions(start_guessed, end_guessed, campus_data)
                if directions:
                    return f"**Directions from {start_guessed} to {end_guessed}:**\\n\\n" + "\\n".join([f"{i+1}. {step}" for i, step in enumerate(directions)])
                else:
                    return f"Sorry, I don't have directions from {start_guessed} to {end_guessed}. Try asking for directions between major locations."
            elif start_guessed:
                # Only start location was guessed, ask for destination
                return f"I found your starting location as **{start_guessed}**. Please specify your destination. For example: 'How do I get from {start_guessed} to [destination]'"
            
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
            
            # If still no match, try to guess the destination from simple keywords
            guessed_destination = guess_destination(user_input)
            if guessed_destination:
                location_info = get_location_info(guessed_destination, campus_data)
                if location_info:
                    return f"Did you mean **{location_info['name']}**? It is located at {location_info['location']}.\\n\\nDescription: {location_info['description']}\\n\\nBuildings: {', '.join(location_info['buildings'])}\\n\\nFloors: {', '.join(location_info['floors'])}"

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
                # If not enough locations found, try to guess destinations from simple keywords
                # Split the user input to identify potential start and end locations
                words = user_input_lower.split()
                
                # Try to find potential start and end locations using the guessing function
                start_guessed = None
                end_guessed = None
                
                # Look for phrases like "from X to Y" to identify start and end
                import re
                from_to_match = re.search(r'from\s+(.+?)\s+to\s+(.+)', user_input_lower)
                if from_to_match:
                    start_part = from_to_match.group(1).strip()
                    end_part = from_to_match.group(2).strip()
                    
                    # Try exact match first
                    for loc in possible_locations:
                        if start_part in loc.lower():
                            start_guessed = loc
                            break
                        if end_part in loc.lower():
                            end_guessed = loc
                            break
                    
                    # If no exact match, try guessing
                    if not start_guessed:
                        start_guessed = guess_destination(start_part)
                    if not end_guessed:
                        end_guessed = guess_destination(end_part)
                else:
                    # If no "from X to Y" pattern, try to guess from the whole input
                    # First try to guess the start location
                    start_guessed = guess_destination(user_input_lower)
                    # For end location, we'll try a different approach by splitting the input
                    if not start_guessed:
                        # Try to extract potential locations from keywords in the input
                        for keyword in ['library', 'cafeteria', 'canteen', 'dining', 'food', 'admin', 'gym', 'infirmary', 'museum', 'research', 'student', 'hostel', 'gate', 'entrance', 'exit']:
                            if keyword in user_input_lower:
                                potential_guessed = guess_destination(keyword)
                                if potential_guessed and not start_guessed:
                                    start_guessed = potential_guessed
                                elif potential_guessed and start_guessed and potential_guessed != start_guessed:
                                    end_guessed = potential_guessed
                                    break
                
                if start_guessed and end_guessed:
                    directions = get_directions(start_guessed, end_guessed, campus_data)
                    if directions:
                        return f"**Directions from {start_guessed} to {end_guessed}:**\\n\\n" + "\\n".join([f"{i+1}. {step}" for i, step in enumerate(directions)])
                    else:
                        return f"Sorry, I don't have directions from {start_guessed} to {end_guessed}. Try asking for directions between major locations."
                elif start_guessed:
                    # Only start location was guessed, ask for destination
                    return f"I found your starting location as **{start_guessed}**. Please specify your destination. For example: 'How do I get from {start_guessed} to [destination]'"
                
                return "I can provide directions between locations. Try asking 'How do I get from Ibaan Building to Sto. Tomas Building?' or 'Directions from Apacible Museum to Joson Gymnasium.'"

        else:
            return "I'm not sure I understand. You can ask me about locations, get 3D visualizations, or directions on campus. For example:\\n\\n• 'Where is the Ibaan Building?'\\n• 'Show 3D map'\\n• 'How do I get from Ibaan Building to Sto. Tomas Building?'"

with st.sidebar:
    st.title("📍 Campus Navigator")
    st.markdown("---")
    st.header("About")
    st.markdown("""
    Welcome to the Campus Navigator Bot! This chatbot helps you find your way around campus by providing:
    
    - **Location Information**: Find buildings and facilities
    - **Operating Hours**: Check when places are open
    - **Directions**: Get step-by-step navigation
    """)
    
    st.header("How to Use")
    st.markdown("""
    - Type your question in the input box below
    - Examples:
        - "Where is the library?"
        - "When does the cafeteria open?"
        - "How do I get from Gate 2 to Admin Block?"
    """)
    
    st.markdown("---")
    st.markdown("**💡 Pro Tips:**")
    st.markdown("- Be specific with your queries")
    st.markdown("- You can ask for directions between locations")
    st.markdown("- Ask about timings for various facilities")

# Main content
st.markdown('<div class="main-header">📍 Campus Navigator Bot</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Your friendly guide to navigating the campus</div>', unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize ML classifier
if 'classifier' not in st.session_state:
    st.session_state.classifier = IntentClassifier()

# Initialize 3D map state variables
if 'waiting_for_3d_current' not in st.session_state:
    st.session_state.waiting_for_3d_current = None
if 'waiting_for_3d_target' not in st.session_state:
    st.session_state.waiting_for_3d_target = None

# Display welcome message if chat is empty
if not st.session_state.messages:
    welcome_message = (
        "Hello! 👋 I'm your Campus Navigator. I can help you find locations, get 3D visualizations, "
        "and get directions around campus. What can I help you with today?\n\n"
        "Try asking things like:\n"
        "- Where is the Ibaan Building?\n"
        "- Show 3D map\n"
        "- How do I get from Ibaan Building to Sto. Tomas Building?"
    )
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})

# Create chat container
chat_container = st.container()

# Display chat history
with chat_container:
    for message in st.session_state.messages:

        if message["role"] == "user":
            st.markdown(f'<div class="user-message">You: {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message">Bot: {message["content"]}</div>', unsafe_allow_html=True)

# Input area
col1, col2 = st.columns([4, 1])
with st.form(key="input_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here...", key="input")
    with col1:
        submit_button = st.form_submit_button("Send", type="primary")
    with col2:
        clear_button = st.form_submit_button("Clear Chat", type="secondary")

# Process clear button
if clear_button:
    st.session_state.messages = []
    # Add a new welcome message
    welcome_message = (
        "Hello! 👋 I'm your Campus Navigator. I can help you find locations, get 3D visualizations, "
        "and get directions around campus. What can I help you with today?\n\n"
        "Try asking things like:\n"
        "- Where is the Ibaan Building?\n"
        "- Show 3D map\n"
        "- How do I get from Ibaan Building to Sto. Tomas Building?"
    )
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})
    st.rerun()

# Process user input
if submit_button and user_input:
    # Sanitize user input
    sanitized_input = sanitize_input(user_input)
    
    if sanitized_input.strip():
        # Check if we're waiting for 3D map locations
        if st.session_state.waiting_for_3d_current is None:
            # Normal processing - check if it's a 3D map request
            # Add user message to history
            st.session_state.messages.append({"role": "user", "content": sanitized_input})
            
            # Show user message immediately
            st.markdown(f'<div class="user-message">You: {sanitized_input}</div>', unsafe_allow_html=True)
            
            # Generate bot response
            with st.spinner("Bot is thinking..."):
                response = generate_response(sanitized_input)
                
                # Check if the response indicates a 3D map request
                if response == "3D_MAP_REQUEST":
                    # Ask for current location
                    current_loc_response = "To create a 3D visualization, please provide your current location."
                    st.session_state.waiting_for_3d_current = True
                    st.session_state.current_3d_input = sanitized_input
                    response = current_loc_response
                else:
                    # Normal response
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.markdown(f'<div class="bot-message">Bot: {response}</div>', unsafe_allow_html=True)
                    st.rerun()
        else:
            # We're waiting for 3D location information
            if st.session_state.waiting_for_3d_current:
                # This is the current location
                if location_exists(sanitized_input):
                    st.session_state.waiting_for_3d_current_loc = sanitized_input
                    st.session_state.waiting_for_3d_current = False
                    st.session_state.waiting_for_3d_target = True
                    
                    # Add user message to history
                    st.session_state.messages.append({"role": "user", "content": sanitized_input})
                    st.markdown(f'<div class="user-message">You: {sanitized_input}</div>', unsafe_allow_html=True)
                    
                    # Ask for target location
                    target_request_msg = f"Current location set to '{sanitized_input}'. Now please provide your destination/target location."
                    st.session_state.messages.append({"role": "assistant", "content": target_request_msg})
                    st.markdown(f'<div class="bot-message">Bot: {target_request_msg}</div>', unsafe_allow_html=True)
                    st.rerun()
                else:
                    # Location doesn't exist, ask again
                    st.session_state.messages.append({"role": "user", "content": sanitized_input})
                    st.markdown(f'<div class="user-message">You: {sanitized_input}</div>', unsafe_allow_html=True)
                    
                    error_msg = f"Location '{sanitized_input}' doesn't exist. Please provide a valid location from the campus."
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    st.markdown(f'<div class="bot-message">Bot: {error_msg}</div>', unsafe_allow_html=True)
                    st.rerun()
            elif st.session_state.waiting_for_3d_target:
                # This is the target location
                if location_exists(sanitized_input):
                    st.session_state.waiting_for_3d_target_loc = sanitized_input
                    st.session_state.waiting_for_3d_target = False
                    
                    # Add user message to history
                    st.session_state.messages.append({"role": "user", "content": sanitized_input})
                    st.markdown(f'<div class="user-message">You: {sanitized_input}</div>', unsafe_allow_html=True)
                    
                    # Show confirmation and generate 3D map
                    confirmation_msg = f"Generating 3D map from '{st.session_state.waiting_for_3d_current_loc}' to '{st.session_state.waiting_for_3d_target_loc}'..."
                    st.session_state.messages.append({"role": "assistant", "content": confirmation_msg})
                    st.markdown(f'<div class="bot-message">Bot: {confirmation_msg}</div>', unsafe_allow_html=True)
                    
                    # Show the 3D map (this will open in a new tab)
                    try:
                        show_campus_3d_map(st.session_state.waiting_for_3d_current_loc, st.session_state.waiting_for_3d_target_loc)
                        success_msg = f"3D map visualization created successfully! Check your browser for the interactive 3D map."
                        st.session_state.messages.append({"role": "assistant", "content": success_msg})
                        st.markdown(f'<div class="bot-message">Bot: {success_msg}</div>', unsafe_allow_html=True)
                    except Exception as e:
                        error_msg = f"Error creating 3D map: {str(e)}"
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
                        st.markdown(f'<div class="bot-message">Bot: {error_msg}</div>', unsafe_allow_html=True)
                    
                    # Reset 3D state
                    st.session_state.waiting_for_3d_current_loc = None
                    st.session_state.waiting_for_3d_target_loc = None
                    st.rerun()
                else:
                    # Location doesn't exist, ask again
                    st.session_state.messages.append({"role": "user", "content": sanitized_input})
                    st.markdown(f'<div class="user-message">You: {sanitized_input}</div>', unsafe_allow_html=True)
                    
                    error_msg = f"Location '{sanitized_input}' doesn't exist. Please provide a valid location from the campus."
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    st.markdown(f'<div class="bot-message">Bot: {error_msg}</div>', unsafe_allow_html=True)
                    st.rerun()
    else:
        st.warning("Please enter a valid message.")

# Add a footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #6b7280; padding: 10px;'>Campus Navigator Bot &copy; 2025 - Helping you navigate campus with ease</div>", unsafe_allow_html=True)