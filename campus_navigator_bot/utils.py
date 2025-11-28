import json
import re
from difflib import get_close_matches
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import numpy as np

def load_campus_data():
    """Load campus data from JSON file"""
    with open('data/campus_data.json', 'r') as f:
        return json.load(f)

def find_best_match(user_input, possible_matches, threshold=0.3):
    """Find the best match for user input from possible matches using difflib"""
    matches = get_close_matches(user_input.lower(), possible_matches, n=1, cutoff=threshold)
    return matches[0] if matches else None

def get_location_info(location_name, data):
    """Get information about a specific location"""
    locations = data.get('locations', {})
    for location_key, location_info in locations.items():
        if location_key.lower() == location_name.lower():
            return location_info
    return None

def get_timing_info(timing_query, data):
    """Get timing information based on query"""
    timings = data.get('timings', {})
    for key, timing_info in timings.items():
        if timing_query.lower() in key.lower():
            return timing_info
    return None

def get_directions(start, end, data):
    """Get directions between two points"""
    directions = data.get('directions', {})
    # Try direct path
    path_key = f"{start.lower()} to {end.lower()}"
    if path_key in directions:
        return directions[path_key]
    
    # Try reverse path
    reverse_path_key = f"{end.lower()} to {start.lower()}"
    if reverse_path_key in directions:
        return directions[reverse_path_key]
    
    return None

class IntentClassifier:
    """Simple ML model to classify user intents using Naive Bayes"""
    
    def __init__(self):
        self.model = None
        self.is_trained = False
        
    def train_model(self):
        """Train the intent classification model"""
        # Training data - intent examples
        training_data = [
            # Location queries
            ("where is the library", "location"),
            ("library location", "location"),
            ("where is the computer lab", "location"),
            ("computer lab location", "location"),
            ("where is the cafeteria", "location"),
            ("cafeteria location", "location"),
            ("where is the admin block", "location"),
            ("admin block location", "location"),
            ("where is the sports complex", "location"),
            ("sports complex location", "location"),
            ("where is the parking", "location"),
            ("parking location", "location"),
            ("where is the medical center", "location"),
            ("medical center location", "location"),
            ("where is the bookstore", "location"),
            ("bookstore location", "location"),
            ("where is the", "location"),
            ("show me the", "location"),
            ("find the", "location"),
            ("location of", "location"),
            
            # Timing queries
            ("when does the library open", "timing"),
            ("library hours", "timing"),
            ("when does the cafeteria open", "timing"),
            ("cafeteria hours", "timing"),
            ("what time does the library close", "timing"),
            ("library timing", "timing"),
            ("timing for cafeteria", "timing"),
            ("hours for computer lab", "timing"),
            ("when is the library open", "timing"),
            ("library open hours", "timing"),
            ("timing", "timing"),
            ("hours", "timing"),
            ("when does", "timing"),
            ("what time", "timing"),
            ("open close", "timing"),
            
            # Direction queries
            ("how do i get to", "direction"),
            ("direction to", "direction"),
            ("navigate to", "direction"),
            ("how to reach", "direction"),
            ("directions from gate 2 to admin block", "direction"),
            ("get from library to cafeteria", "direction"),
            ("how to go from", "direction"),
            ("path to", "direction"),
            ("route to", "direction"),
            ("navigate from", "direction"),
            ("directions to", "direction"),
            ("get directions", "direction"),
            ("how to get from", "direction"),
            
            # General queries
            ("hello", "greeting"),
            ("hi", "greeting"),
            ("help", "greeting"),
            ("what can you do", "greeting"),
            ("who are you", "greeting"),
            ("what are you", "greeting"),
            ("thank you", "greeting"),
            ("thanks", "greeting"),
            ("bye", "greeting"),
            ("goodbye", "greeting"),
            ("good morning", "greeting"),
            ("good afternoon", "greeting"),
            ("good evening", "greeting"),
            
            # Unknown queries
            ("random text", "unknown"),
            ("this is not related", "unknown"),
            ("completely unrelated", "unknown"),
            ("what is the meaning of life", "unknown"),
            ("tell me a joke", "unknown"),
            ("weather today", "unknown"),
            ("news", "unknown"),
            ("anything else", "unknown")
        ]
        
        # Separate texts and labels
        texts, labels = zip(*training_data)
        
        # Create and train the pipeline
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(lowercase=True, stop_words='english', ngram_range=(1, 2))),
            ('classifier', MultinomialNB())
        ])
        
        self.model.fit(texts, labels)
        self.is_trained = True
        
    def predict_intent(self, text):
        """Predict the intent of the user's text"""
        if not self.is_trained:
            self.train_model()
        
        if self.model is None:
            return "unknown"
        
        # Predict the intent
        predicted_intent = self.model.predict([text])[0]
        confidence = max(self.model.predict_proba([text])[0])
        
        # Only return prediction if confidence is above threshold
        if confidence > 0.1:
            return predicted_intent
        else:
            return "unknown"
    
    def save_model(self, filepath):
        """Save the trained model to a file"""
        if self.is_trained:
            with open(filepath, 'wb') as f:
                pickle.dump(self.model, f)
    
    def load_model(self, filepath):
        """Load a pre-trained model from a file"""
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                self.model = pickle.load(f)
                self.is_trained = True