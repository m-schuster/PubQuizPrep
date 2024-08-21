# PubQuizPrep

PubQuizPrep is an application designed to help you prepare for pub quizzes on demand. It includes features such as summarizing the news of the last week, providing historical summaries of specific days, and creating rounds for images and music. This app leverages various services to gather and process information, making quiz preparation efficient and comprehensive.

As of now, this app only supports the German language, i.e. inputs must be German and all outputs will be generated in German. 

## Features

- **News Summary**: Summarizes the most significant news events from the past week.
- **Day Summary**: Provides a historical summary of significant events, births, deaths, and holidays for a specific day.
- **Image Round**: Generates a list of significant images related to a given topic.
- **Music Round**: Creates a playlist of significant songs related to a given theme.
- **PDF Generation**: Compiles all the gathered information into a PDF document for easy distribution and use.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/PubQuizPrep.git
    cd PubQuizPrep
    ```

2. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up your configuration**:
    - Create a `config.py` file with your API keys and other necessary configurations.
