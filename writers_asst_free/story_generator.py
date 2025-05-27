# story_generator.py
from llm_interface import start_chat_session, send_message

def run_story_generator(chat_session):
    """Handles the story generation feature."""
    print("\n--- 📝 Story Generator ---")
    if not chat_session:
        print("No active session. Exiting.")
        return # Stop if session failed to start

    # 1. Get User Input
    genre = input("Enter the story genre (e.g., Fantasy, Sci-Fi, Mystery): ")
    age_group = input("Enter the target age group (e.g., Children, Young Adult, Adult): ")
    print("\nEnter the plot outline:")
    plot_outline = input("> ") # Could use get_multiline_input for longer plots
    print("\nEnter character details (name, description, role):")
    character_details = input("> ") # Could use get_multiline_input

    # 2. Construct Initial Prompt
    prompt = f"""
    Generate a complete short story based on the following details:
    - Genre: {genre}
    - Target Age Group: {age_group}
    - Plot Outline: {plot_outline}
    - Character Details: {character_details}

    Please provide:
    1. A suitable title for the story.
    2. The full story text.
    3. Suggestions for 2-3 actors who could play the main character(s) if this were adapted into a film or series, briefly explaining why.

    Ensure the story is engaging and appropriate for the specified age group.
    """

    # 3. Get Initial Story
    story_response = send_message(chat_session, prompt)
    print("\n--- Generated Story ---")
    print(story_response)
    print("----------------------")

    # 4. Follow-up Interaction Loop
    print("\nYou can now ask follow-up questions about the story (e.g., 'Expand on scene X', 'Change character Y's motivation', 'Describe the setting more') or type 'quit' to end.")
    while True:
        user_input = input("\nYour request ('quit' to exit): ")
        if user_input.lower() == 'quit':
            print("Ending story generator session.")
            break
        if not user_input:
            continue

        follow_up_response = send_message(chat_session, user_input)
        print("\n--- Response ---")
        print(follow_up_response)
        print("---------------")