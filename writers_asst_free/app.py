# app.py
import streamlit as st
import sys
import os
import google.generativeai as genai
import time
from branching import generate_alternatives, create_branch_visualization, preprocess_story, SimpleVectorDB
import io  # Needed for gTTS stream

api_key = "AIzaSyAyBjb3w-583rckUkuvQ9WrZEFxo3NFWhU"
genai.configure(api_key=api_key)

# Initialize Gemini model
gemini_model = genai.GenerativeModel('gemini-1.5-pro')

# Assuming llm_interface.py, utils.py, recommender.py, audio_generator.py are in the same directory
from llm_interface import start_chat_session, send_message, end_chat_session
from recommender import run_recommender
from audio_generator import synthesize_text_gtts as synthesize_text

# --- Configuration ---
PAGE_TITLE = "🖋️ AI Story Assistant"
st.set_page_config(page_title=PAGE_TITLE, layout="wide")

# --- State Management ---
# Initialize session state variables if they don't exist
if 'chat_session' not in st.session_state:
    st.session_state.chat_session = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"  # Default page
if 'global_story' not in st.session_state:
    st.session_state.global_story = ""  # Global story storage

# == Display State Variables ==
if 'gen_last_output' not in st.session_state: st.session_state.gen_last_output = ""
if 'chk_last_output_analysis' not in st.session_state: st.session_state.chk_last_output_analysis = ""
if 'exp_last_output' not in st.session_state: st.session_state.exp_last_output = ""
if 'style_last_output' not in st.session_state: st.session_state.style_last_output = ""
if 'rec_last_output' not in st.session_state: st.session_state.rec_last_output = ""
if 'ab_last_audio_bytes' not in st.session_state: st.session_state.ab_last_audio_bytes = None


# --- LLM Session Handling ---
def initialize_session():
    """Starts the LLM chat session and stores it in session_state."""
    if st.session_state.chat_session is None:
        with st.spinner("Initializing AI session..."):
            try:
                st.session_state.chat_session = start_chat_session()
                if st.session_state.chat_session:
                    st.success("AI Session started!")
                else:
                    st.error("Failed to initialize AI session. Check API key."); st.stop()
            except Exception as e:
                st.error(f"Init Error: {e}. Check API key/internet."); st.stop()

# Initialize session
initialize_session()


# --- UI Rendering Functions ---

def render_home():
    """Displays the main welcome/navigation page."""
    st.title(PAGE_TITLE)
    st.write("Welcome! Choose a feature below to get started.")
    features = {
        "Generator": "📝 Generate", "Checker": "🧐 Check Plot", "Explorer": "✨ Explore",
        "Transformer": "🎨 Transform", "Recommender": "📚 Recommend", "Audiobook": "🎧 Listen"
    }
    num_features = len(features)
    cols = st.columns(num_features)
    feature_keys = list(features.keys())
    for i, col in enumerate(cols):
        if i < len(feature_keys):
            key = feature_keys[i]; name = features[key]
            if col.button(name, key=f"nav_{key.lower()}"):
                st.session_state.current_page = key; st.rerun()


def render_story_generator():
    """Renders the Story Generator UI."""
    st.header("📝 Story Generator")
    st.caption("Provide details below and the AI will write a short story for you.")

    # Input Form
    with st.form("story_gen_form", clear_on_submit=True):
        genre = st.text_input("Story Genre (e.g., Fantasy, Sci-Fi, Mystery)")
        age_group = st.text_input("Target Age Group (e.g., Children, YA, Adult)")
        plot_outline = st.text_area("Plot Outline", height=100, placeholder="Briefly describe the main events...")
        character_details = st.text_area("Character Details", height=100, placeholder="Name, description, role...")
        submitted = st.form_submit_button("Generate Story")

        if submitted:
            if not all([genre, age_group, plot_outline, character_details]):
                st.warning("Please fill in all fields.")
            else:
                prompt = f"""Generate a complete short story based on:
                - Genre: {genre}
                - Age Group: {age_group}
                - Plot: {plot_outline}
                - Characters: {character_details}
                Provide: ## Title, Full story text, ### Actor Suggestions (with reasons). Ensure engaging, consistent, age-appropriate."""
                with st.spinner("Generating story..."):
                    response = send_message(st.session_state.chat_session, prompt)
                st.session_state.gen_last_output = response
                st.session_state.global_story = response  # Save the story globally

    # --- Display Area ---
    if st.session_state.get('gen_last_output'):
        st.subheader("Generated Story")
        st.markdown(st.session_state.gen_last_output)
        st.download_button("📥 Download Story", st.session_state.gen_last_output, file_name="generated_story.txt")


def render_plot_checker():
    """Renders the Plot Checker UI."""
    st.header("🧐 Plot Hole & Inconsistency Checker")
    st.caption("Analyze the story for plot holes and inconsistencies.")

    # Pre-fill the story input with the global story
    default_story = st.session_state.global_story

    with st.form("plot_check_form", clear_on_submit=True):
        user_story_input = st.text_area("Paste story here:", height=300, value=default_story)
        submitted = st.form_submit_button("Analyze Story")
        if submitted:
            if not user_story_input.strip():
                st.warning("Please paste a story.")
            else:
                prompt = f"""Analyze the following story for plot holes, inconsistencies, or unresolved arcs:
                {user_story_input}"""
                with st.spinner("Analyzing..."):
                    response = send_message(st.session_state.chat_session, prompt)
                st.session_state.chk_last_output_analysis = response

    # --- Display Area ---
    if st.session_state.get('chk_last_output_analysis'):
        st.subheader("Plot Analysis")
        st.markdown(st.session_state.chk_last_output_analysis)


def render_creative_explorer():
    """Renders the Creative Explorer UI."""
    st.header("✨ Creative Explorer")
    st.caption("Explore creative 'what if' scenarios for your story.")

    # Pre-fill the story input with the global story
    default_story = st.session_state.global_story

    with st.form("creative_explorer_form", clear_on_submit=True):
        user_story_input = st.text_area("Paste story here:", height=300, value=default_story)
        creative_request = st.text_input("Enter your creative request (e.g., 'Suggest alternate endings')")
        submitted = st.form_submit_button("Explore")
        if submitted:
            if not user_story_input.strip() or not creative_request.strip():
                st.warning("Please provide both the story and a creative request.")
            else:
                prompt = f"""Based on the following story, respond to the creative request:
                Story: {user_story_input}
                Request: {creative_request}"""
                with st.spinner("Exploring..."):
                    response = send_message(st.session_state.chat_session, prompt)
                st.session_state.exp_last_output = response

    # --- Display Area ---
    if st.session_state.get('exp_last_output'):
        st.subheader("Creative Exploration Result")
        st.markdown(st.session_state.exp_last_output)


def render_style_transformer():
    """Renders the Style Transformer UI."""
    st.header("🎨 Style Transformer")
    st.caption("Rewrite the story in a different style.")

    # Pre-fill the story input with the global story
    default_story = st.session_state.global_story

    with st.form("style_transform_form", clear_on_submit=True):
        user_story_input = st.text_area("Paste story here:", height=250, value=default_story)
        target_style = st.text_input("Target style (e.g., Hemingway, Jane Austen)")
        submitted = st.form_submit_button("Transform Style")
        if submitted:
            if not user_story_input.strip() or not target_style.strip():
                st.warning("Please provide both the story and a target style.")
            else:
                prompt = f"""Rewrite the following story in the style of {target_style}:
                {user_story_input}"""
                with st.spinner("Transforming..."):
                    response = send_message(st.session_state.chat_session, prompt)
                st.session_state.style_last_output = response

    # --- Display Area ---
    if st.session_state.get('style_last_output'):
        st.subheader("Transformed Story")
        st.markdown(st.session_state.style_last_output)
        st.download_button("📥 Download Transformed Story", st.session_state.style_last_output, file_name="transformed_story.txt")


def render_recommender():
    """Renders the Recommender UI."""
    st.header("📚 Recommender")
    st.caption("Get book and movie recommendations based on your story.")

    # Pre-fill the story input with the global story
    default_story = st.session_state.global_story

    with st.form("recommender_form", clear_on_submit=True):
        user_story_input = st.text_area("Paste story here:", height=300, value=default_story)
        submitted = st.form_submit_button("Get Recommendations")
        if submitted:
            if not user_story_input.strip():
                st.warning("Please paste a story.")
            else:
                response = run_recommender(st.session_state.chat_session, user_story_input)
                st.session_state.rec_last_output = response

    # --- Display Area ---
    if st.session_state.get('rec_last_output'):
        st.subheader("Recommendations")
        st.markdown(st.session_state.rec_last_output)


def render_audiobook_generator():
    """Renders the Audiobook Generator UI."""
    st.header("🎧 Audiobook Generator")
    st.caption("Convert your story into an audiobook.")

    # Pre-fill the story input with the global story
    default_story = st.session_state.global_story

    with st.form("audiobook_form", clear_on_submit=True):
        user_story_input = st.text_area("Paste story here:", height=300, value=default_story)
        submitted = st.form_submit_button("Generate Audiobook")
        if submitted:
            if not user_story_input.strip():
                st.warning("Please paste a story.")
            else:
                with st.spinner("Generating audiobook..."):
                    audio_bytes = synthesize_text(user_story_input)
                st.session_state.ab_last_audio_bytes = audio_bytes

    # --- Display Area ---
    if st.session_state.get('ab_last_audio_bytes'):
        st.audio(st.session_state.ab_last_audio_bytes, format="audio/mp3")
        st.download_button("📥 Download Audiobook", st.session_state.ab_last_audio_bytes, file_name="audiobook.mp3")


# --- Main App Logic ---
st.sidebar.title("Navigation")
st.sidebar.caption("Choose a feature")

AVAILABLE_PAGES = ["Home", "Generator", "Checker", "Explorer", "Transformer", "Recommender", "Audiobook"]

def change_page():
    """Callback function when the sidebar navigation changes."""
    st.session_state.current_page = st.session_state.sidebar_selection

st.sidebar.radio(
    "Features", AVAILABLE_PAGES, key="sidebar_selection",
    index=AVAILABLE_PAGES.index(st.session_state.current_page),
    on_change=change_page
)

# --- Render the selected page ---
page_to_render = st.session_state.current_page

if page_to_render == "Home": render_home()
elif page_to_render == "Generator": render_story_generator()
elif page_to_render == "Checker": render_plot_checker()
elif page_to_render == "Explorer": render_creative_explorer()
elif page_to_render == "Transformer": render_style_transformer()
elif page_to_render == "Recommender": render_recommender()
elif page_to_render == "Audiobook": render_audiobook_generator()
else: st.error("Page not found!")


# to run this: streamlit run app.py