# Campus Navigator Bot

A graphical, user-friendly chatbot application that helps students, faculty, and visitors navigate the college campus. This application features a clean, responsive web-style interface where users can type natural-language questions and instantly receive helpful, location-specific answers.

## 🎯 Features

- **Graphical User Interface**: Built with Streamlit for an intuitive chat experience
- **Location Queries**: Find buildings and facilities on campus
- **Timing Information**: Check operating hours of various facilities
- **Direction Guidance**: Get step-by-step navigation between locations
- **Fuzzy Matching**: Handles typos and synonyms in user queries
- **Responsive Design**: Works well on both desktop and mobile devices

## 🛠️ Technologies Used

- **Python 3.8+**
- **Streamlit**: For the web interface
- **JSON**: For storing campus data
- **difflib**: For fuzzy string matching
- **re**: For regular expression pattern matching

## 📁 Project Structure

```
campus_navigator_bot/
│
├── app.py                  # Main Streamlit application (UI + logic)
├── utils.py                # Helper functions (text matching, response generation)
├── requirements.txt        # List of Python libraries to install
├── README.md               # Project documentation (setup, usage, features)
│
└── data/
    └── campus_data.json    # Campus buildings, timings, directions, etc
```

## 🚀 Setup Instructions

1. **Clone the repository** (or download the project files)
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**:
   ```bash
   streamlit run app.py
   ```
4. **Access the application**: Open your browser and go to `http://localhost:8501`

## 💡 Usage Examples

Once the application is running, you can ask questions like:

- "Where is the library?"
- "When does the cafeteria open?"
- "How do I get from Gate 2 to Admin Block?"
- "What time does the gym close?"
- "Find the CS lab for me"
- "Directions from main entrance to library"

## 🏗️ Data Structure

The `campus_data.json` file contains three main sections:

1. **Locations**: Information about campus buildings and facilities
2. **Timings**: Operating hours for various facilities
3. **Directions**: Predefined routes with step-by-step directions

## 🔧 Customization

To customize the bot for your specific campus:

1. Update the `data/campus_data.json` file with your campus information
2. Modify the response templates in `utils.py` if needed
3. Adjust the styling in `app.py` to match your college's theme colors

## 🌐 Deployment

The application can be easily deployed to platforms like:

- Streamlit Cloud
- Heroku
- Any cloud platform that supports Python web applications

## 🤝 Contributing

Feel free to fork this repository and submit pull requests for improvements. Some potential enhancements include:

- Adding a campus map visualization
- Integrating with real-time data sources
- Adding multilingual support
- Implementing voice input/output

## 📄 License

This project is available for educational and personal use.