# recommender.py
from llm_interface import send_message

def run_recommender(chat_session, user_text):
    """
    Asks the LLM to suggest similar books and movies based on user text.

    Args:
        chat_session: The active Gemini chat session.
        user_text: The story summary, theme, or text provided by the user.

    Returns:
        A string containing the LLM's recommendations, or an error message.
    """
    if not chat_session:
        return "Error: Chat session not initialized."
    if not user_text or not user_text.strip():
        return "Error: No text provided to analyze."

    prompt = f"""
    Analyze the following story text, summary, or theme description:
    --- TEXT START ---
    {user_text}
    --- TEXT END ---

    Based on the core themes, plot elements, genre, tone, and overall feeling evoked by this text, please suggest:

    1.  **Books (3-5 suggestions):** List relevant books that explore similar ideas, share plot structures, or have a comparable style/tone. For each book, provide:
        *   Title and Author.
        *   A brief (1-2 sentences) explanation of *why* it's a relevant suggestion (e.g., "similar dystopian theme focusing on rebellion," "features a complex anti-hero protagonist like the one described," "shares the melancholic, reflective tone").

    2.  **Movies (3-5 suggestions):** List relevant movies that explore similar ideas, belong to a similar genre, or have a comparable visual style or atmosphere. For each movie, provide:
        *   Title and Director (if commonly known).
        *   A brief (1-2 sentences) explanation of *why* it's a relevant suggestion (e.g., "similar sci-fi mystery plot involving memory loss," "visual style matches the described dark fantasy setting," "deals with the theme of found family in a post-apocalyptic world").

    Format the response clearly with distinct sections for Books and Movies. Provide well-known examples where possible, but also consider less common works if they are a strong match. Focus on providing helpful inspiration for a writer exploring these themes/ideas.
    """

    try:
        print(f"\n🤖 Requesting recommendations based on: {user_text[:100]}...") # Log request
        response = send_message(chat_session, prompt)
        print("✅ Recommendations received.")
        return response
    except Exception as e:
        print(f"❌ Error getting recommendations: {e}")
        # Use the error handling from send_message if it returns specific strings,
        # otherwise return a generic error.
        if "Error:" in str(response): # Check if send_message returned an error string
             return response
        else:
             return f"An unexpected error occurred while getting recommendations: {e}"