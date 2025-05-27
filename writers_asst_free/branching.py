import google.generativeai as genai
from sentence_transformers import SentenceTransformer
import numpy as np
import plotly.graph_objects as go
from typing import List, Dict, Any
import json
import uuid

# Initialize Sentence Transformer for embeddings
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Set up Google Gemini API
# api_key = st.secrets["GEMINI_API_KEY"] if "GEMINI_API_KEY" in st.secrets else os.environ.get("GEMINI_API_KEY")
api_key = "AIzaSyAyBjb3w-583rckUkuvQ9WrZEFxo3NFWhU"
genai.configure(api_key=api_key)

# Initialize Gemini model
gemini_model = genai.GenerativeModel('gemini-1.5-pro')

# Create a simple in-memory vector database
class SimpleVectorDB:
    def __init__(self):
        self.vectors = []
        self.metadata = []
        
    def add(self, text: str, metadata: Dict[str, Any]):
        embedding = embedding_model.encode(text)
        self.vectors.append(embedding)
        self.metadata.append(metadata)
        
    def search(self, query: str, top_k: int = 3):
        if not self.vectors:
            return []
        
        query_embedding = embedding_model.encode(query)
        similarities = [np.dot(query_embedding, vec) / (np.linalg.norm(query_embedding) * np.linalg.norm(vec)) 
                        for vec in self.vectors]
        
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        results = [{"similarity": similarities[i], "metadata": self.metadata[i]} for i in top_indices]
        
        return results
    
    def clear(self):
        self.vectors = []
        self.metadata = []

vector_db = SimpleVectorDB()

def preprocess_story(story_text: str):
    """Split story into paragraphs and identify potential branch points"""
    paragraphs = [p.strip() for p in story_text.split('\n') if p.strip()]
    
    vector_db.clear()

    # Add paragraphs to vector DB
    for i, para in enumerate(paragraphs):
        vector_db.add(
            para, 
            {
                "id": str(uuid.uuid4()),
                "type": "paragraph",
                "position": i,
                "text": para
            }
        )
    
    # Generate branch points
    prompt = f"""
    I have a story text. Please identify 3-5 key decision points or moments where the story could branch into different directions.
    For each point, provide:
    1. A brief description of the branching point
    2. The paragraph number where this occurs
    
    Only respond in valid JSON format as follows:
    [
        {{
            "id": "unique_id",
            "description": "Brief description of the branch point",
            "paragraph_index": paragraph_number_where_this_occurs
        }},
        ...
    ]

    Strictly follow the JSON format. Do not add any additional text or explanations. No prefix or suffix of any kind.
    
    Here's the story:
    {story_text}
    """
    
    response = gemini_model.generate_content(prompt)
    # print(response.text)  # Debugging line to check the response
    try:
        branch_points = json.loads(response.text)
        return branch_points
    except json.JSONDecodeError:
        # Fallback if JSON parsing fails
        return []

def generate_alternatives(branch_point, story_text, character_info, genre):
    """Generate alternative storylines for a branch point"""
    
    # Get related context from vector DB
    related_paragraphs = vector_db.search(branch_point["description"], top_k=3)
    context = "\n".join([item["metadata"]["text"] for item in related_paragraphs])
    
    prompt = f"""
    Based on this story and the selected branch point, generate 3 alternative story paths.
    
    STORY CONTEXT:
    {context}
    
    BRANCH POINT:
    {branch_point["description"]}
    
    CHARACTER INFORMATION:
    {character_info}
    
    GENRE:
    {genre}
    
    For each alternative path:
    1. Create a title that captures the essence of this path
    2. Write a summary of what happens in this alternative (2-3 sentences)
    3. Generate a sample paragraph showing how the story would continue in this direction
    4. Explain how this maintains character consistency

    Strictly follow the JSON format. Do not add any additional text or explanations. Not even prefix or suffix.
    
    Respond in valid JSON format as follows:
    [
        {{
            "id": "unique_id",
            "title": "Path Title",
            "summary": "Summary of what happens in this path",
            "sample_text": "Sample paragraph of story continuation",
            "character_consistency": "How this maintains character consistency"
        }},
        ...
    ]
    """
    
    response = gemini_model.generate_content(prompt)
    # print("RESPONSE:")
    # print(response.text)  # Debugging line to check the response
    try:
        alternatives = json.loads(response.text)
        return alternatives
    except json.JSONDecodeError:
        return []

def create_branch_visualization(branches):
    """Create a visualization of the story branches"""
    if not branches:
        return None
    
    fig = go.Figure()
    
    # Add main trunk
    fig.add_trace(go.Scatter(
        x=[0, 0], 
        y=[0, 1], 
        mode='lines',
        line=dict(color='brown', width=10),
        name='Main Story'
    ))
    
    # Add branches
    colors = ['green', 'blue', 'purple', 'orange', 'red']
    for i, branch in enumerate(branches):
        angle = -45 + (i * 45)
        x_end = np.sin(np.radians(angle)) * 0.8
        y_end = 1 + np.cos(np.radians(angle)) * 0.8
        
        # Draw the branch line
        fig.add_trace(go.Scatter(
            x=[0, x_end], 
            y=[1, y_end], 
            mode='lines',
            line=dict(color=colors[i % len(colors)], width=5),
            showlegend=False
        ))
        
        # Add branch title at the end
        fig.add_trace(go.Scatter(
            x=[x_end], 
            y=[y_end], 
            mode='text',
            text=[branch['title']],
            textposition="middle center",
            showlegend=False
        ))
    
    fig.update_layout(
        title='Story Branching Visualization',
        showlegend=False,
        xaxis=dict(visible=False, range=[-1, 1]),
        yaxis=dict(visible=False, range=[0, 2]),
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='black',  # Optional, but looks clean
        paper_bgcolor='black'
    )
    
    return fig