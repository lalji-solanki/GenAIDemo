import os

import google.generativeai as genai

from dotenv import load_dotenv

import chromadb

import hashlib

import logging

from chromadb.config import Settings

from flask import Flask, render_template, request, jsonify

from flask_socketio import SocketIO



load_dotenv()



app = Flask(__name__)

socketio = SocketIO(app)



# Configure logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



# Initialize the API key for Google Gemini

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:

    logging.error("GOOGLE_API_KEY not found in .env file.")

    raise ValueError("GOOGLE_API_KEY not found in .env file.")



genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")



# --- ChromaDB Initialization ---

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

CHROMA_PERSIST_DIRECTORY = os.path.join(PROJECT_DIR, "chroma_db")



def init_chromadb():

    """Initialize ChromaDB client and collection."""

    try:

        logging.info(f"Initializing ChromaDB with directory: {CHROMA_PERSIST_DIRECTORY}")

        settings = Settings(persist_directory=CHROMA_PERSIST_DIRECTORY)

        client = chromadb.Client(settings)

        collection = client.get_or_create_collection(name="gemini_chat_history")

        logging.info("ChromaDB initialized successfully!")

        return client, collection

    except Exception as e:

        logging.error(f"Error initializing ChromaDB: {e}")

        return None, None



# Initialize ChromaDB client and collection

client, collection = init_chromadb()



def hash_text(text):

    """Hashes text using SHA-256 for consistent IDs."""

    return hashlib.sha256(text.encode()).hexdigest()



def chat_with_gemini(user_input):

    """Sends user input to Gemini or retrieves from DB."""

    if client is None or collection is None:

        logging.warning("ChromaDB is not available. Using Gemini directly.")

        try:

            response = model.generate_content(user_input)

            logging.info(f"Gemini Response: {response.text}")  # Log the full response

            return response.text

        except genai.APIError as e:

            logging.error(f"Gemini API Error: {e}")

            return "An error occurred while communicating with Gemini."

        except Exception as e:

            logging.exception(f"An unexpected error occurred: {e}")

            return "An unexpected error occurred."



    query_hash = hash_text(user_input)



    results = collection.get(ids=[query_hash])

    if results["ids"]:

        logging.info("Retrieving response from database...")

        logging.info(f"Retrieved from database: Question: {user_input}, Answer: {results['documents'][0]}")

        return results["documents"][0]



    try:

        response = model.generate_content(user_input)

        response_text = response.text



        collection.upsert(

            ids=[query_hash],

            documents=[response_text],

            metadatas=[{"question": user_input}]

        )

        logging.info("Storing response in database...")

        logging.info(f"Stored in database: Question: {user_input}, Answer: {response_text}")

        return response_text

    except genai.APIError as e:

        logging.error(f"Gemini API Error: {e}")

        return "An error occurred while communicating with Gemini."

    except Exception as e:

        logging.exception(f"An unexpected error occurred: {e}")

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

    socketio.run(app, debug=True)

