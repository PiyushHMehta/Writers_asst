# creative_explorer.py
from llm_interface import start_chat_session, send_message
from utils import get_multiline_input

def run_creative_explorer(chat_session):
    """Handles the creative expansion and 'what if' scenarios."""
    print("\n--- ✨ Creative Explorer ---")
    if not chat_session:
        print("No active session. Exiting.")
        return # Stop if session failed to start

    # 1. Get User's Story
    user_story = get_multiline_input("Paste your base story below (type 'END_TEXT' on a new line to finish):")

    if not user_story.strip():
        print("No story provided. Exiting creative explorer.")
        return

    # 2. Send initial story to establish context (but don't ask for specific action yet)
    initial_prompt = f"""
    I have the following story that I'd like to explore creatively. Please keep this story in mind for subsequent questions:

    --- STORY START ---
    {user_story}
    --- STORY END ---

    Okay, I've read the story. What creative exploration would you like to try first?
    (Examples: 'Suggest 3 different endings.', 'What if Character A made decision Z instead of Y in scene 5?', 'How would the story change if the setting was futuristic instead of medieval?')
    """
    # Send the story and the introductory message
    initial_response = send_message(chat_session, initial_prompt)
    print("\n--- Gemini Confirmation ---")
    print(initial_response) # Print the LLM's confirmation/readiness message
    print("--------------------------")


    # 3. Follow-up Interaction Loop for Exploration
    print("\nEnter your creative exploration requests (e.g., suggest endings, 'what if' scenarios) or type 'quit' to end.")
    while True:
        user_input = input("\nYour request ('quit' to exit): ")
        if user_input.lower() == 'quit':
            print("Ending creative explorer session.")
            break
        if not user_input:
            continue

        # Construct prompt for the specific exploration, relying on chat history for story context
        exploration_prompt = f"""
        Based on the story provided earlier, please respond to the following creative request:

        '{user_input}'

        Provide a detailed and imaginative response, considering the implications for the plot, characters, and themes.
        """
        follow_up_response = send_message(chat_session, exploration_prompt) # Use exploration_prompt or just user_input if the LLM handles context well enough
        print("\n--- Exploration Response ---")
        print(follow_up_response)
        print("--------------------------")