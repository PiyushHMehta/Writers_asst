# plot_checker.py
from llm_interface import send_message # Removed start_chat_session import
from utils import get_multiline_input # Keep for potential future CLI use

# Note: In Streamlit version, get_multiline_input won't be used directly
# The function signature will change to accept story_text from Streamlit UI

def run_plot_checker(chat_session, user_story): # Accept story as argument
    """
    Handles the plot hole detection and correction feature.
    Returns the analysis text.
    """
    print("\n--- 🧐 Plot Hole & Inconsistency Checker ---") # Keep for logging if needed
    if not chat_session:
        print("Error: No active session.")
        return "Error: No active chat session."
    if not user_story.strip():
        print("Error: No story provided.")
        return "Error: No story provided to analyze."

    # Modified Prompt: Focus on significant issues
    prompt = f"""
    Please carefully analyze the following story for **significant** plot holes, major logical inconsistencies, critical continuity errors, or clearly unresolved character arcs/motivations that undermine the core narrative.

    Minor stylistic choices or interpretations are less critical unless they create genuine confusion. Acknowledge if the story is generally consistent but point out areas that *could* be strengthened for clarity or impact.

    For each significant issue found:
    1. Clearly identify the problem (e.g., "Major Plot Hole: Character X couldn't have known Y at this point based on previous events.").
    2. Explain *why* it's a significant issue for the story's coherence.
    3. Suggest specific corrections or ways to rewrite the problematic sections to resolve the issue. If possible, provide the corrected text directly.

    Story to analyze:
    ---
    {user_story}
    ---

    Provide a comprehensive analysis. If no major issues are found, state that clearly, perhaps offering minor suggestions for polish if appropriate.
    """

    analysis_response = send_message(chat_session, prompt)
    print("\n--- Analysis & Corrections ---") # Keep for logging
    print(analysis_response) # Keep for logging
    print("-----------------------------")
    return analysis_response # Return the result for Streamlit

# Note: The follow-up loop logic will be handled within the Streamlit app's structure

# --- Similar modifications needed for other modules ---
# story_generator.py, creative_explorer.py, style_transformer.py
# They should be refactored to:
# 1. Accept necessary inputs (like prompts, story text) as function arguments.
# 2. Return the LLM's response string.
# 3. Remove input() calls and direct print() statements meant for CLI display.
# 4. Keep print() for logging/debugging if desired.
# We'll do this refactoring directly within the Streamlit app file for simplicity.