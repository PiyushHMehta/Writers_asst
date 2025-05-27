# style_transformer.py
from llm_interface import start_chat_session, send_message
from utils import get_multiline_input

def run_style_transformer(chat_session):
    """Handles transforming the story's writing style."""
    print("\n--- 🎨 Style Transformer ---")
    if not chat_session:
        print("No active session. Exiting.")
        return # Stop if session failed to start

    # 1. Get User's Story
    user_story = get_multiline_input("Paste your story below (type 'END_TEXT' on a new line to finish):")
    if not user_story.strip():
        print("No story provided. Exiting style transformer.")
        return

    # 2. Get Target Style
    target_style = input("Enter the target writing style (e.g., 'Jane Austen', 'Ernest Hemingway', 'Shakespearean', 'Cyberpunk Noir'): ")
    if not target_style.strip():
        print("No target style provided. Exiting.")
        return

    # 3. Construct Initial Prompt
    prompt = f"""
    Please rewrite the following story in the distinct writing style of **{target_style}**.
    Capture the typical tone, vocabulary, sentence structure, and common themes or focuses associated with that style. Maintain the core plot and characters of the original story as much as possible while adapting the narration and dialogue.

    Original Story:
    ---
    {user_story}
    ---

    Rewrite the entire story in the style of {target_style}:
    """

    # 4. Get Transformed Story
    transformed_response = send_message(chat_session, prompt)
    print(f"\n--- Story Transformed (Style: {target_style}) ---")
    print(transformed_response)
    print("-------------------------------------------------")

    # 5. Follow-up Interaction Loop
    print("\nYou can now ask for refinements (e.g., 'Make the dialogue more formal', 'Focus more on internal thoughts') or type 'quit' to end.")
    while True:
        user_input = input("\nYour request ('quit' to exit): ")
        if user_input.lower() == 'quit':
            print("Ending style transformer session.")
            break
        if not user_input:
            continue

        follow_up_response = send_message(chat_session, user_input)
        print("\n--- Refinement Response ---")
        print(follow_up_response)
        print("--------------------------")