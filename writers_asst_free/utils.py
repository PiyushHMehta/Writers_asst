# utils.py
import re
import datetime
import os

def get_multiline_input(prompt="Enter text (type 'END_TEXT' on a new line to finish):"):
    """Gets multi-line input from the user via console."""
    print(prompt)
    lines = []
    while True:
        try:
            line = input()
            # Use a specific, less common marker like %%END%% or similar if END_TEXT is likely in the story
            if line.strip().upper() == "END_TEXT": 
                break
            lines.append(line)
        except EOFError: # Handle Ctrl+D or similar EOF signals
            break
    return "\n".join(lines)

def sanitize_filename(name):
    """Removes or replaces characters invalid for filenames."""
    # Remove characters that are definitely invalid on most systems
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    # Replace spaces with underscores (optional, but common)
    name = name.replace(" ", "_")
    # Limit length (optional)
    return name[:100] # Limit to 100 chars

def save_text_locally(content, base_filename="story_output"):
    """Saves the given text content to a local file."""
    try:
        # Sanitize and create a unique filename
        safe_base = sanitize_filename(base_filename)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_base}_{timestamp}.txt"

        # Ensure downloads directory exists
        download_dir = "downloaded_stories"
        os.makedirs(download_dir, exist_ok=True)
        filepath = os.path.join(download_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Content successfully saved to: {filepath}")
        return filepath # Return the path for confirmation
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return None

# --- No changes needed for llm_interface.py initially, but be aware ---
# --- Streamlit will manage the session differently (using st.session_state) ---
# --- We might need to slightly adapt how the session is passed later ---