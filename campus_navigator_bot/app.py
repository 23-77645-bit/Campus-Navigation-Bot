import streamlit as st
import json
import re
from difflib import get_close_matches
from utils import load_campus_data, find_best_match, get_location_info, get_timing_info, get_directions, IntentClassifier
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

def generate_response(user_input):
    """Generate a response based on user input using ML classification"""
    # Use the ML classifier to determine intent
    intent = st.session_state.classifier.predict_intent(user_input)
    
    user_input_lower = user_input.lower()
    
    # Use ML classification to determine the type of query
    if intent == 'location':
        # Extract possible location names
        possible_locations = list(campus_data['locations'].keys())
        # Try to find a match in the user input
        for loc in possible_locations:
            if loc.lower() in user_input_lower:
                location_info = get_location_info(loc, campus_data)
                if location_info:
                    return f"**{location_info['name']}** is located at {location_info['location']}.\n\nDescription: {location_info['description']}\n\nBuildings: {', '.join(location_info['buildings'])}\n\nFloors: {', '.join(location_info['floors'])}"
        
        # If no direct match, try fuzzy matching
        best_match = find_best_match(user_input_lower, possible_locations, threshold=0.3)
        if best_match:
            location_info = get_location_info(best_match, campus_data)
            if location_info:
                return f"**{location_info['name']}** is located at {location_info['location']}.\n\nDescription: {location_info['description']}\n\nBuildings: {', '.join(location_info['buildings'])}\n\nFloors: {', '.join(location_info['floors'])}"
        
        return "I'm sorry, I couldn't find information about that location. Try asking about specific places like 'library', 'cafeteria', or 'admin block'."
    
    elif intent == 'timing':
        # Check for specific timing information
        if 'library' in user_input_lower:
            timing_info = get_timing_info('library', campus_data)
            if timing_info:
                return f"The library is open from {timing_info['open']} to {timing_info['close']}.\n\nAdditional info: {timing_info['additional_info']}"
        elif 'cafeteria' in user_input_lower:
            timing_info = get_timing_info('cafeteria', campus_data)
            if timing_info:
                return f"The cafeteria is open from {timing_info['open']} to {timing_info['close']}.\n\nAdditional info: {timing_info['additional_info']}"
        elif 'computer lab' in user_input_lower:
            timing_info = get_timing_info('computer_lab', campus_data)
            if timing_info:
                return f"The computer lab is open from {timing_info['open']} to {timing_info['close']}.\n\nAdditional info: {timing_info['additional_info']}"
        
        return "I can provide information about operating hours. Ask about specific places like 'library hours' or 'cafeteria timing'."
    
    elif intent == 'direction':
        # Extract possible start and end locations
        possible_locations = list(campus_data['locations'].keys())
        found_locations = []
        
        for loc in possible_locations:
            if loc.lower() in user_input_lower:
                found_locations.append(loc)
        
        if len(found_locations) >= 2:
            start = found_locations[0]
            end = found_locations[1]
            directions = get_directions(start, end, campus_data)
            if directions:
                return f"**Directions from {start.title()} to {end.title()}:**\n\n" + "\n".join([f"{i+1}. {step}" for i, step in enumerate(directions)])
            else:
                return f"Sorry, I don't have directions from {start.title()} to {end.title()}. Try asking for directions between major locations like 'gate to library' or 'admin block to cafeteria'."
        else:
            return "I can provide directions between locations. Try asking 'How do I get from the library to the cafeteria?' or 'Directions from gate 2 to admin block.'"
    
    elif intent == 'greeting':
        return "Hello! I'm your Campus Navigator Bot. I can help you find:\n\n• **Locations** - Ask 'Where is the library?' or 'Find the cafeteria'\n• **Timings** - Ask 'When does the library open?' or 'Cafeteria hours'\n• **Directions** - Ask 'How do I get from the gate to the admin block?'\n\nJust type your question and I'll help you navigate the campus!"
    
    elif intent == 'unknown':
        # Fallback for unknown queries - use keyword-based detection
        if any(keyword in user_input_lower for keyword in ['where is', 'location', 'find', 'locate', 'at']):
            # Extract possible location names
            possible_locations = list(campus_data['locations'].keys())
            # Try to find a match in the user input
            for loc in possible_locations:
                if loc.lower() in user_input_lower:
                    location_info = get_location_info(loc, campus_data)
                    if location_info:
                        return f"**{location_info['name']}** is located at {location_info['location']}.\n\nDescription: {location_info['description']}\n\nBuildings: {', '.join(location_info['buildings'])}\n\nFloors: {', '.join(location_info['floors'])}"
            
            # If no direct match, try fuzzy matching
            best_match = find_best_match(user_input_lower, possible_locations, threshold=0.3)
            if best_match:
                location_info = get_location_info(best_match, campus_data)
                if location_info:
                    return f"**{location_info['name']}** is located at {location_info['location']}.\n\nDescription: {location_info['description']}\n\nBuildings: {', '.join(location_info['buildings'])}\n\nFloors: {', '.join(location_info['floors'])}"
            
            return "I'm sorry, I couldn't find information about that location. Try asking about specific places like 'library', 'cafeteria', or 'admin block'."
        
        # Check for timing queries
        elif any(keyword in user_input_lower for keyword in ['when', 'open', 'close', 'hours', 'timing', 'time']):
            # Check for specific timing information
            if 'library' in user_input_lower:
                timing_info = get_timing_info('library', campus_data)
                if timing_info:
                    return f"The library is open from {timing_info['open']} to {timing_info['close']}.\n\nAdditional info: {timing_info['additional_info']}"
            elif 'cafeteria' in user_input_lower:
                timing_info = get_timing_info('cafeteria', campus_data)
                if timing_info:
                    return f"The cafeteria is open from {timing_info['open']} to {timing_info['close']}.\n\nAdditional info: {timing_info['additional_info']}"
            elif 'computer lab' in user_input_lower:
                timing_info = get_timing_info('computer_lab', campus_data)
                if timing_info:
                    return f"The computer lab is open from {timing_info['open']} to {timing_info['close']}.\n\nAdditional info: {timing_info['additional_info']}"
            
            return "I can provide information about operating hours. Ask about specific places like 'library hours' or 'cafeteria timing'."
        
        # Check for direction queries
        elif any(keyword in user_input_lower for keyword in ['how do i get', 'direction', 'navigate', 'go to', 'reach', 'path', 'route']):
            # Extract possible start and end locations
            possible_locations = list(campus_data['locations'].keys())
            found_locations = []
            
            for loc in possible_locations:
                if loc.lower() in user_input_lower:
                    found_locations.append(loc)
            
            if len(found_locations) >= 2:
                start = found_locations[0]
                end = found_locations[1]
                directions = get_directions(start, end, campus_data)
                if directions:
                    return f"**Directions from {start.title()} to {end.title()}:**\n\n" + "\n".join([f"{i+1}. {step}" for i, step in enumerate(directions)])
                else:
                    return f"Sorry, I don't have directions from {start.title()} to {end.title()}. Try asking for directions between major locations like 'gate to library' or 'admin block to cafeteria'."
            else:
                return "I can provide directions between locations. Try asking 'How do I get from the library to the cafeteria?' or 'Directions from gate 2 to admin block.'"
        
        else:
            return "I'm not sure I understand. You can ask me about locations, timings, or directions on campus. For example:\n\n• 'Where is the library?'\n• 'When does the cafeteria open?'\n• 'How do I get from the gate to the admin block?'"

# Sidebar
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

# Display welcome message if chat is empty
if not st.session_state.messages:
    welcome_message = (
        "Hello! 👋 I'm your Campus Navigator. I can help you find locations, check timings, "
        "and get directions around campus. What can I help you with today?\n\n"
        "Try asking things like:\n"
        "- Where is the library?\n"
        "- When does the cafeteria open?\n"
        "- How do I get from Gate 2 to Admin Block?"
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
with st.form(key="input_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here...", key="input")
    submit_button = st.form_submit_button("Send", type="primary")

# Process user input
if submit_button and user_input:
    # Sanitize user input
    sanitized_input = sanitize_input(user_input)
    
    if sanitized_input.strip():
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": sanitized_input})
        
        # Show user message immediately
        st.markdown(f'<div class="user-message">You: {sanitized_input}</div>', unsafe_allow_html=True)
        
        # Generate bot response
        with st.spinner("Bot is thinking..."):
            response = generate_response(sanitized_input)
        
        # Add bot response to history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Show bot response
        st.markdown(f'<div class="bot-message">Bot: {response}</div>', unsafe_allow_html=True)
        
        # Rerun to update the chat display
        st.rerun()
    else:
        st.warning("Please enter a valid message.")

# Add a footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #6b7280; padding: 10px;'>Campus Navigator Bot &copy; 2025 - Helping you navigate campus with ease</div>", unsafe_allow_html=True)