from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")  # Or another suitable model

def chat_with_gemini(user_input):
    """Sends user input to Gemini and returns the response."""
    try:
        response = model.generate_content(user_input)
        return response.text
    except genai.APIError as e:
        print(f"API Error: {e}")
        return "An error occurred while communicating with Gemini."
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.form["user_message"]
    bot_response = chat_with_gemini(user_message)
    return jsonify({"bot_response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)