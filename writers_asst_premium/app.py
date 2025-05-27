# app.py
import streamlit as st
import os
import json
import time
from story_assistant import (
    get_api_key, 
    setup_llm_client, 
    generate_chapter, 
    analyze_plot, 
    generate_creative_branches, 
    export_story_context, 
    import_story_context,
    get_audience_guidelines,
    suggest_character_arc,
    generate_plot_outline,
    solve_plot_problem,
    generate_dialogue
)
from ui_components import (
    sidebar_content,
    story_setup_page,
    characters_page,
    settings_page,
    plot_elements_page,
    chapter_generator_page,
    plot_analysis_page,
    creative_branches_page,
    character_arc_page,
    plot_outline_page,
    dialogue_generator_page,
    plot_problem_solver_page,
    export_import_page
)
from translations import get_translations
# Add this new import
from storage_helper import add_storage_buttons, check_for_loaded_data

# Set page configuration
st.set_page_config(
    page_title="Author's AI Assistant",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if 'story_context' not in st.session_state:
    st.session_state.story_context = {
        "title": "",
        "genre": "fantasy",
        "target_age_group": "young_adult_13_17",
        "language": "english",  # Default language is English
        "characters": [],
        "plot_elements": [],
        "settings": [],
        "timeline_events": []
    }

if 'api_key' not in st.session_state:
    st.session_state.api_key = ""

if 'chapters' not in st.session_state:
    st.session_state.chapters = []

if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = []

if 'creative_branches' not in st.session_state:
    st.session_state.creative_branches = []

if 'character_arcs' not in st.session_state:
    st.session_state.character_arcs = []

if 'plot_outlines' not in st.session_state:
    st.session_state.plot_outlines = []

if 'dialogues' not in st.session_state:
    st.session_state.dialogues = []

# Set up language if it's not already in session state
if 'language' not in st.session_state:
    st.session_state.language = "english"

# Main app logic
def main():
    # Check for loaded data first
    check_for_loaded_data()
    
    # Display sidebar and get current page
    current_page = sidebar_content()
    
    # Add storage management buttons
    add_storage_buttons()
    
    # Display the appropriate page based on selection
    if current_page == "Story Setup":
        story_setup_page()
    elif current_page == "Characters":
        characters_page()
    elif current_page == "Settings":
        settings_page()
    elif current_page == "Plot Elements":
        plot_elements_page()
    elif current_page == "Chapter Generator":
        chapter_generator_page()
    elif current_page == "Plot Analysis":
        plot_analysis_page()
    elif current_page == "Creative Branches":
        creative_branches_page()
    elif current_page == "Character Arcs":
        character_arc_page()
    elif current_page == "Plot Outline":
        plot_outline_page()
    elif current_page == "Dialogue Generator":
        dialogue_generator_page()
    elif current_page == "Plot Problem Solver":
        plot_problem_solver_page()
    elif current_page == "Export/Import":
        export_import_page()

if __name__ == "__main__":
    main()