import os
import json
import streamlit as st
import google.generativeai as genai
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv  # <-- Add this import

load_dotenv()  # <-- Load environment variables from .env

# LLM configuration
def get_api_key():
    """Get Gemini API key from environment or Streamlit secrets"""
    api_key = os.getenv('GOOGLE_API_KEY', '')
    if api_key:
        return api_key
    else:
        return st.session_state.get('api_key', '')

def setup_llm_client():
    """Initialize and configure Gemini API"""
    api_key = get_api_key()
    if not api_key:
        return None
    
    genai.configure(api_key=api_key)
    return True

# Define prompt templates and guidelines
PROMPTS = {
    "audience_tailoring": {
        "children_5_8": {
            "vocabulary_level": "simple, concrete nouns and verbs, limited adjectives",
            "sentence_structure": "short, direct sentences with simple syntax",
            "thematic_elements": "friendship, kindness, overcoming small fears, learning lessons",
            "content_boundaries": "no violence, mild peril only, resolution of conflicts through communication",
            "narrative_style": "third-person, clear descriptions, frequent dialogue, repetition of key phrases"
        },
        "middle_grade_9_12": {
            "vocabulary_level": "expanded vocabulary, introduction of figurative language",
            "sentence_structure": "varied sentence length, introduction of complex sentences",
            "thematic_elements": "friendship, family challenges, school life, early identity questions, adventure",
            "content_boundaries": "mild peril, non-graphic conflicts, emotional challenges",
            "narrative_style": "mix of dialogue and description, character internal thoughts"
        },
        "young_adult_13_17": {
            "vocabulary_level": "rich vocabulary, metaphors, word play, emotional language",
            "sentence_structure": "diverse sentence structures, stylistic variations",
            "thematic_elements": "identity, belonging, challenging authority, relationships, social issues",
            "content_boundaries": "moderate peril, emotional intensity, some mature themes handled sensitively",
            "narrative_style": "strong voice, internal character development, varied pacing"
        },
        "adult_18+": {
            "vocabulary_level": "sophisticated vocabulary, nuanced language, literary techniques",
            "sentence_structure": "complex, varied structures, stylistic flexibility",
            "thematic_elements": "full range of human experience, philosophical questions, complex relationships",
            "content_boundaries": "all themes appropriate, graphic content used purposefully",
            "narrative_style": "diverse approaches, experimental techniques allowed"
        }
    },
    "chapter_generation": """
    Generate a chapter for a {genre} story targeting {age_group} readers.
    
    Story Context:
    Title: {title}
    Main Characters: {characters}
    Setting: {settings}
    Previous Events: {previous_events}
    Current Situation: {current_situation}
    
    Chapter Guidance:
    - Use vocabulary and sentence structure appropriate for {age_group}
    - Focus on the following plot elements: {plot_focus}
    - Maintain the established tone: {tone}
    - Chapter should be approximately {word_count} words
    
    Stylistic Reference:
    Write in a style similar to {author_reference} but with your own unique voice.
    
    Language: 
    Write this chapter in {language}
    """,
    "plot_analysis": """
    Analyze the following story excerpt for plot coherence, character consistency, and pacing.
    
    Story Context:
    Genre: {genre}
    Target Age Group: {age_group}
    Established Characters: {characters}
    Previous Plot Points: {plot_points}
    
    Story Excerpt:
    {story_excerpt}
    
    Provide analysis on:
    1. Plot Consistency: Are there any contradictions or plot holes?
    2. Character Consistency: Do characters act in line with established traits?
    3. Pacing: Does the scene move too quickly or slowly?
    4. Unresolved Threads: Are there dangling plot elements that need addressing?
    5. Suggestions: Provide specific recommendations for improvement.
    
    Language: 
    Write this analysis in {language}
    """,
    "creative_expansion": """
    Generate {num_branches} possible story branches from the current narrative point.
    
    Current Situation:
    {current_situation}
    
    Key Decision Point:
    {decision_point}
    
    Character Motivations:
    {character_motivations}
    
    For each branch:
    1. Provide a brief summary of the direction
    2. Explain the cause-and-effect relationship
    3. Outline potential consequences for the overall plot
    4. Generate a short sample passage (100-200 words) demonstrating this branch
    
    Ensure each branch feels distinct and offers meaningful narrative divergence.
    
    Language: 
    Write these story branches in {language}
    """
}

# Reference databases
AUTHOR_REFERENCES = {
    "fantasy": {
        "children_5_8": "J.K. Rowling's early Harry Potter chapters",
        "middle_grade_9_12": "Rick Riordan's Percy Jackson series",
        "young_adult_13_17": "Leigh Bardugo's Shadow and Bone",
        "adult_18+": "N.K. Jemisin's The Fifth Season"
    },
    "science_fiction": {
        "children_5_8": "Louis Sachar's Sideways Stories",
        "middle_grade_9_12": "Madeleine L'Engle's A Wrinkle in Time",
        "young_adult_13_17": "Suzanne Collins' The Hunger Games",
        "adult_18+": "Andy Weir's The Martian"
    },
    "mystery": {
        "children_5_8": "Ron Roy's A to Z Mysteries",
        "middle_grade_9_12": "Trenton Lee Stewart's The Mysterious Benedict Society",
        "young_adult_13_17": "Karen M. McManus' One of Us Is Lying",
        "adult_18+": "Gillian Flynn's Gone Girl"
    },
    "romance": {
        "young_adult_13_17": "Jenny Han's To All the Boys I've Loved Before",
        "adult_18+": "Emily Henry's Beach Read"
    },
    "historical": {
        "middle_grade_9_12": "Christopher Paul Curtis's The Watsons Go to Birmingham",
        "young_adult_13_17": "Ruta Sepetys's Salt to the Sea",
        "adult_18+": "Hilary Mantel's Wolf Hall"
    },
    "thriller": {
        "young_adult_13_17": "April Henry's Girl, Stolen",
        "adult_18+": "Gillian Flynn's Gone Girl"
    },
    "horror": {
        "middle_grade_9_12": "R.L. Stine's Goosebumps series",
        "young_adult_13_17": "Stephanie Perkins's There's Someone Inside Your House",
        "adult_18+": "Stephen King's The Shining"
    },
    "adventure": {
        "children_5_8": "Mac Barnett's Mac B., Kid Spy series",
        "middle_grade_9_12": "Erin Hunter's Warriors series",
        "young_adult_13_17": "James Dashner's The Maze Runner",
        "adult_18+": "Clive Cussler's Dirk Pitt series"
    },
    "dystopian": {
        "young_adult_13_17": "Veronica Roth's Divergent",
        "adult_18+": "Margaret Atwood's The Handmaid's Tale"
    },
    "literary": {
        "young_adult_13_17": "John Green's The Fault in Our Stars",
        "adult_18+": "Donna Tartt's The Goldfinch"
    }
}

# Helper functions 
def get_audience_guidelines(age_group: str) -> Dict:
    """Get writing guidelines for a specific age group"""
    return PROMPTS["audience_tailoring"].get(age_group, {})

def get_author_reference(genre: str, age_group: str) -> str:
    """Return appropriate author reference based on genre and age group"""
    try:
        return AUTHOR_REFERENCES[genre][age_group]
    except KeyError:
        return "bestselling authors in this genre"

def call_llm(prompt: str, max_tokens: int = 1500, temperature: float = 0.7) -> str:
    """Call the Gemini language model API with the given prompt"""
    if not setup_llm_client():
        return "API key not configured."
    
    try:
        # Configure the generation model
        generation_config = {
            "temperature": temperature,
            "max_output_tokens": max_tokens,
            "top_p": 0.95,
            "top_k": 40,
        }
        
        # Add a system instruction as part of the prompt
        system_instruction = "You are an expert literary assistant helping to write and analyze fiction."
        full_prompt = f"{system_instruction}\n\n{prompt}"
        
        # Get Gemini Pro model
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro", 
            generation_config=generation_config
        )
        
        # Generate the response directly
        response = model.generate_content(full_prompt)
        
        # Return the text content
        return response.text
        
    except Exception as e:
        # In real implementation, properly handle API errors
        return f"Error generating content: {str(e)}"

# Core functionality functions
def generate_chapter(story_context: Dict, chapter_title: str, plot_focus: str, 
                    tone: str, word_count: int, previous_events: str, 
                    current_situation: str) -> str:
    """Generate a chapter based on the story context and parameters"""
    
    # Extract character information for the prompt
    characters_str = ", ".join([f"{c['name']} ({c['role']})" for c in story_context["characters"]])
    
    # Extract settings information
    settings_str = ", ".join([s["name"] for s in story_context["settings"]])
    
    # Format the prompt with all necessary context
    prompt = PROMPTS["chapter_generation"].format(
        genre=story_context["genre"],
        age_group=story_context["target_age_group"],
        title=story_context["title"],
        characters=characters_str,
        settings=settings_str,
        previous_events=previous_events,
        current_situation=current_situation,
        plot_focus=plot_focus,
        tone=tone,
        word_count=word_count,
        author_reference=get_author_reference(
            story_context["genre"], 
            story_context["target_age_group"]
        ),
        language=story_context.get("language", "english")
    )
    
    # Call the LLM API
    return call_llm(prompt, max_tokens=2000)

def analyze_plot(story_context: Dict, story_excerpt: str) -> str:
    """Analyze plot coherence, character consistency, and pacing"""
    
    # Extract character information for the prompt
    characters_str = ", ".join([f"{c['name']} ({c['role']}): {c['motivation']}" 
                              for c in story_context["characters"]])
    
    # Extract plot points
    plot_points = ", ".join([p["description"] for p in story_context["plot_elements"]])
    
    # Format the prompt with context
    prompt = PROMPTS["plot_analysis"].format(
        genre=story_context["genre"],
        age_group=story_context["target_age_group"],
        characters=characters_str,
        plot_points=plot_points,
        story_excerpt=story_excerpt,
        language=story_context.get("language", "english")
    )
    
    # Call the LLM API
    return call_llm(prompt)

def generate_creative_branches(story_context: Dict, current_situation: str, 
                              decision_point: str, num_branches: int = 3) -> str:
    """Generate multiple potential plot branches from a decision point"""
    
    # Extract character motivations
    character_motivations = "\n".join([f"{c['name']}: {c['motivation']}" 
                                     for c in story_context["characters"]])
    
    # Format the prompt
    prompt = PROMPTS["creative_expansion"].format(
        num_branches=num_branches,
        current_situation=current_situation,
        decision_point=decision_point,
        character_motivations=character_motivations,
        language=story_context.get("language", "english")
    )
    
    # Call the LLM API
    return call_llm(prompt, max_tokens=2000)

def export_story_context(story_context: Dict) -> str:
    """Export the current story context as JSON string"""
    return json.dumps(story_context, indent=2)

def import_story_context(json_data: str) -> Dict:
    """Import a story context from JSON string"""
    try:
        return json.loads(json_data)
    except json.JSONDecodeError:
        return {}

# Advanced functionality
def suggest_character_arc(story_context: Dict, character_name: str) -> str:
    """Generate a character arc suggestion for a specific character"""
    
    # Find the character in the story context
    character = None
    for c in story_context["characters"]:
        if c["name"].lower() == character_name.lower():
            character = c
            break
    
    if not character:
        return f"Character '{character_name}' not found in story context."
    
    # Create a prompt for character arc suggestion
    prompt = f"""
    Based on the character information below, suggest a compelling character arc for {character_name} 
    in a {story_context["genre"]} story for {story_context["target_age_group"].replace('_', ' ')} readers.
    
    Character Details:
    Name: {character["name"]}
    Role: {character["role"]}
    Description: {character["description"]}
    Current Motivation: {character["motivation"]}
    
    Story Context:
    Title: {story_context["title"]}
    Genre: {story_context["genre"]}
    
    Include:
    1. Starting point - the character's initial state, beliefs, or situation
    2. Key transformation moments - 2-3 pivotal experiences that could change them
    3. Final state - how they might be different by the end of the story
    4. Thematic relevance - how this arc connects to potential themes of the story
    5. Specific scene ideas (1-2) that would be powerful moments in this character's journey
    
    Language: 
    Write this character arc in {story_context.get("language", "english")}
    """
    
    return call_llm(prompt, max_tokens=1500)

def generate_plot_outline(story_context: Dict, num_chapters: int = 10) -> str:
    """Generate a plot outline based on story context"""
    
    # Extract key story elements
    characters_str = "\n".join([f"- {c['name']} ({c['role']}): {c['motivation']}" 
                              for c in story_context["characters"]])
    
    settings_str = "\n".join([f"- {s['name']}: {s['significance']}" 
                            for s in story_context["settings"]])
    
    plot_elements_str = "\n".join([f"- {p['type']} ({p['importance']}): {p['description']}" 
                                 for p in story_context["plot_elements"]])
    
    # Create prompt for plot outline
    prompt = f"""
    Create a {num_chapters}-chapter plot outline for a {story_context["genre"]} story 
    titled "{story_context["title"]}" aimed at {story_context["target_age_group"].replace('_', ' ')} readers.
    
    Story Elements:
    
    Characters:
    {characters_str}
    
    Settings:
    {settings_str}
    
    Key Plot Elements:
    {plot_elements_str}
    
    Create a well-structured plot following the three-act structure (setup, confrontation, resolution),
    with a compelling narrative arc. For each chapter, provide:
    
    1. Chapter title
    2. Brief summary (2-3 sentences)
    3. Key character developments or revelations
    
    Ensure the plot has a clear progression, rising action, climax, and resolution appropriate
    for the target age group. Include chapter titles that evoke interest without revealing too much.
    
    Language: 
    Write this plot outline in {story_context.get("language", "english")}
    """
    
    return call_llm(prompt, max_tokens=2000)

def solve_plot_problem(problem_description: str, story_context: Dict) -> str:
    """Generate solutions for a specific plot problem"""
    
    # Extract relevant context
    characters_str = "\n".join([f"- {c['name']} ({c['role']}): {c['motivation']}" 
                              for c in story_context["characters"]])
    
    plot_elements_str = "\n".join([f"- {p['type']} ({p['importance']}): {p['description']}" 
                                 for p in story_context["plot_elements"]])
    
    # Create prompt for plot problem-solving
    prompt = f"""
    Help solve the following plot problem in a {story_context["genre"]} story 
    for {story_context["target_age_group"].replace('_', ' ')} readers:
    
    Problem: {problem_description}
    
    Story Context:
    Title: {story_context["title"]}
    
    Characters:
    {characters_str}
    
    Established Plot Elements:
    {plot_elements_str}
    
    Please provide:
    1. Three different approaches to solving this problem
    2. For each approach, explain:
       - How it would work within the established story
       - Its narrative strengths and weaknesses
       - How it might affect character development
       - Any new opportunities it creates for future plot developments
    3. Recommend which solution you think works best and why
    
    Language: 
    Write these solutions in {story_context.get("language", "english")}
    """
    
    return call_llm(prompt, max_tokens=1800)

def generate_dialogue(story_context: Dict, character1: str, character2: str, 
                     situation: str, tone: str) -> str:
    """Generate dialogue between two characters"""
    
    # Find the characters in the story context
    char1 = None
    char2 = None
    for c in story_context["characters"]:
        if c["name"].lower() == character1.lower():
            char1 = c
        elif c["name"].lower() == character2.lower():
            char2 = c
    
    if not char1 or not char2:
        missing = []
        if not char1:
            missing.append(character1)
        if not char2:
            missing.append(character2)
        return f"Character(s) not found: {', '.join(missing)}"
    
    # Create prompt for dialogue generation
    prompt = f"""
    Write a dialogue scene between {char1["name"]} and {char2["name"]} in a {story_context["genre"]} story 
    for {story_context["target_age_group"].replace('_', ' ')} readers.
    
    Character Information:
    - {char1["name"]}: {char1["description"]}
    - Motivation: {char1["motivation"]}
    
    - {char2["name"]}: {char2["description"]}
    - Motivation: {char2["motivation"]}
    
    Situation: {situation}
    
    The tone of the conversation should be: {tone}
    
    Guidelines:
    - Make the dialogue reveal character traits and advance the plot
    - Include appropriate body language and brief action descriptions
    - Keep the dialogue natural and age-appropriate
    - Ensure distinct voice for each character
    - Include subtext where appropriate
    
    Language: 
    Write this dialogue in {story_context.get("language", "english")}
    """
    
    return call_llm(prompt, max_tokens=1500, temperature=0.75)
