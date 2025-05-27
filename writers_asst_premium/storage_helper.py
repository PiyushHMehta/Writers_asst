# storage_helper.py
import streamlit as st
import streamlit.components.v1 as components
import json
import urllib.parse
from translations import get_translations

def add_storage_buttons():
    """Add save/load buttons to the sidebar"""
    # Get translations
    t = get_translations(st.session_state.language)
    
    st.sidebar.divider()
    st.sidebar.subheader(t.get("session_management", "Session Management"))
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button(f"💾 {t.get('save_button', 'Save')}", key="save_session"):
            save_to_storage()
            
    with col2:
        if st.button(f"📂 {t.get('load_button', 'Load')}", key="load_session"):
            load_component()

def save_to_storage():
    """Save current session state to browser storage"""
    # Collect the data we want to save
    save_data = {
        "story_context": st.session_state.story_context,
        "chapters": st.session_state.chapters,
        "analysis_results": st.session_state.analysis_results,
        "creative_branches": st.session_state.creative_branches,
        "character_arcs": st.session_state.character_arcs,
        "plot_outlines": st.session_state.plot_outlines,
        "dialogues": st.session_state.dialogues,
        "language": st.session_state.language,
        "api_key": st.session_state.api_key
    }
    
    # Convert to JSON string
    json_str = json.dumps(save_data)
    
    # Create component to save to localStorage
    save_component(json_str)

def save_component(json_str):
    """Create HTML component to save data to localStorage"""
    js_code = f"""
    <script>
        const data = {json_str};
        try {{
            localStorage.setItem('authorAssistantData', JSON.stringify(data));
            console.log('Session saved to localStorage');
            document.getElementById('save_result').innerText = 'Session saved successfully!';
        }} catch (e) {{
            console.error('Error saving to localStorage:', e);
            document.getElementById('save_result').innerText = 'Error saving session: ' + e.message;
        }}
    </script>
    <p id="save_result">Saving data...</p>
    """
    components.html(js_code, height=50)

def load_component():
    """Create HTML component to load data from localStorage"""
    js_code = """
    <script>
        try {
            const savedData = localStorage.getItem('authorAssistantData');
            if (savedData) {
                const searchParams = new URLSearchParams(window.location.search);
                searchParams.set('loadSession', encodeURIComponent(savedData));
                window.location.search = searchParams.toString();
            } else {
                console.log('No saved data found');
                document.getElementById('load_result').innerText = 'No saved data found';
            }
        } catch (e) {
            console.error('Error loading from localStorage:', e);
            document.getElementById('load_result').innerText = 'Error: ' + e.message;
        }
    </script>
    <p id="load_result">Checking for saved data...</p>
    """
    components.html(js_code, height=50)

def check_for_loaded_data():
    """Check URL parameters for loaded session data"""
    # Using st.query_params instead of the deprecated experimental_get_query_params
    query_params = st.query_params
    if 'loadSession' in query_params:
        try:
            # Decode the URL-encoded JSON string
            encoded_data = query_params['loadSession']
            decoded_data = urllib.parse.unquote(encoded_data)
            loaded_data = json.loads(decoded_data)
            
            # Restore session state from loaded data
            st.session_state.story_context = loaded_data.get('story_context', st.session_state.story_context)
            st.session_state.chapters = loaded_data.get('chapters', st.session_state.chapters)
            st.session_state.analysis_results = loaded_data.get('analysis_results', st.session_state.analysis_results)
            st.session_state.creative_branches = loaded_data.get('creative_branches', st.session_state.creative_branches)
            st.session_state.character_arcs = loaded_data.get('character_arcs', st.session_state.character_arcs)
            st.session_state.plot_outlines = loaded_data.get('plot_outlines', st.session_state.plot_outlines)
            st.session_state.dialogues = loaded_data.get('dialogues', st.session_state.dialogues)
            st.session_state.language = loaded_data.get('language', st.session_state.language)
            st.session_state.api_key = loaded_data.get('api_key', st.session_state.api_key)
            
            # Clean URL after loading - also updated to use the non-experimental version
            st.query_params.clear()
            
            # Show success message
            st.success("Session restored successfully!")
            
        except Exception as e:
            st.error(f"Error loading session data: {e}")
            st.query_params.clear()