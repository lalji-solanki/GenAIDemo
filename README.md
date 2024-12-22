# Gemini Chatbot

This is a simple chatbot application that uses the Gemini AI model (via the `google-generativeai` library) to generate responses to user input. It provides a web-based user interface using Flask.

## Features

*   Chat with Gemini AI in a web browser.
*   Responsive UI that adapts to different screen sizes.
*   "Generating response..." message to provide user feedback during processing.
*   Error handling for API requests and other potential issues.
*   Enter key support for sending messages.
*   Button disabling during processing.

## Prerequisites

*   Python 3.7+
*   pip (Python package installer)
*   A Google Cloud project with the Gemini API enabled and a valid API key.

## Installation

1.  **Clone the repository (optional):**

    ```bash
    git clone [invalid URL removed] # Replace with your repo URL
    cd gemini-chatbot
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Linux/macOS
    .venv\Scripts\activate      # On Windows
    ```

3.  **Install required packages:**

    ```bash
    pip install Flask google-generativeai python-dotenv
    ```

4.  **Create a `.env` file:** Create a file named `.env` in the root directory of the project and add your Google Cloud API key:

    ```
    GOOGLE_API_KEY=YOUR_ACTUAL_API_KEY
    ```

    **Important:** Never commit your `.env` file to version control. It should be added to your `.gitignore` file.

## Usage

1.  **Run the Flask application:**

    ```bash
    python app.py
    ```

2.  **Open your web browser:** Go to `http://127.0.0.1:5000/`.

3.  **Start chatting:** Type your messages in the input field and press Enter or click the "Send" button.

## Project Structure

gemini-chatbot/
├── app.py          # Flask application code
├── templates/
│   └── index.html  # HTML template for the UI
├── .env            # Environment variables (API key)
└── .gitignore      # Git ignore file
└── README.md       # This file


## Error Handling

The application includes error handling for API requests and other potential issues. If an error occurs, an appropriate message will be displayed in the chat area.

## Responsive Design

The UI is designed to be responsive and adapt to different screen sizes using CSS media queries.

## Deployment (Optional)

To deploy this application to a production environment, you would typically use a platform like:

*   **Google App Engine:** Well-suited for Google Cloud projects.
*   **Heroku:** Easy to deploy Flask applications.
*   **Other cloud platforms:** AWS, Azure, etc.

You would need to configure the deployment environment to set the `GOOGLE_API_KEY` environment variable securely (using platform-specific secret management tools).

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

[Choose a license, e.g., MIT License](LICENSE)

## Acknowledgements

*   [Google Cloud](https://cloud.google.com/)
*   [Gemini API](https://developers.generativeai.google/) (When more public documentation is available)
*   [Flask](https://flask.palletsprojects.com/)
