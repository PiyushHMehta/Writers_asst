# llm_interface.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Please set it in a .env file.")

genai.configure(api_key=api_key)

# --- Model Configuration ---
# You might adjust "gemini-1.5-flash" to another model if needed
# See https://ai.google.dev/models/gemini
GENERATION_CONFIG = {
    "temperature": 0.7, # Controls randomness - adjust as needed
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192, # Adjust based on expected story length / analysis
    "response_mime_type": "text/plain",
}
SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

def start_chat_session():
    """Initializes and returns a new Gemini ChatSession."""
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash", # Or your preferred model
            safety_settings=SAFETY_SETTINGS,
            generation_config=GENERATION_CONFIG,
            # system_instruction="You are a helpful creative writing assistant.", # Optional: Set a system-level instruction
        )
        chat = model.start_chat(history=[]) # Start with empty history for a new session
        print("\n✨ New session started with Gemini. ✨")
        return chat
    except Exception as e:
        print(f"❌ Error initializing Gemini model: {e}")
        return None

def send_message(chat_session, prompt):
    """Sends a message to the Gemini chat session and returns the response."""
    if not chat_session:
        return "Error: Chat session not initialized."
    try:
        print("\n🤖 Thinking...")
        response = chat_session.send_message(prompt)
        print("✅ Response received.")
        return response.text
    except Exception as e:
        print(f"❌ Error sending message to Gemini: {e}")
        # Attempt to gracefully handle potential context length issues or other API errors
        if "context length" in str(e).lower():
             return "Error: The conversation history is too long. Please start a new session or shorten your input."
        elif "429" in str(e): # Rate limit likely
             return "Error: API rate limit exceeded. Please wait a bit and try again."
        elif "500" in str(e): # Server error
             return "Error: The AI service encountered an internal error. Please try again later."
        else:
             return f"An unexpected error occurred: {e}"
        
def end_chat_session(chat_session):
    """Ends the given Gemini ChatSession."""
    if not chat_session:
        print("No active session to end.")
        return
    try:
        # Assuming the chat session has a method to close or clean up
        chat_session.end_chat()  # Replace with the actual method if different
        print("✨ Chat session ended successfully.")
    except AttributeError:
        print("⚠️ The chat session does not support explicit termination. Assuming cleanup is automatic.")
    except Exception as e:
        print(f"❌ Error ending chat session: {e}")