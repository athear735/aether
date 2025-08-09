"""
AETHER Web Interface - Streamlit App
© 2024 AlgoRythm Tech - Built by Sri Aasrith Souri Kompella
"""

import streamlit as st
import requests
import json
import uuid
from datetime import datetime
import time
from typing import Dict, Any, Optional
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Page configuration
st.set_page_config(
    page_title="AETHER - AlgoRythm Tech",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .user-message {
        background-color: #e3f2fd;
        margin-left: 20%;
    }
    
    .assistant-message {
        background-color: #f3e5f5;
        margin-right: 20%;
    }
    
    .sidebar-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        border-top: 1px solid #ddd;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
# Try multiple sources for API URL
try:
    # First try Streamlit secrets
    API_BASE_URL = st.secrets["API_URL"]
except (KeyError, FileNotFoundError):
    # Then try environment variable
    API_BASE_URL = os.environ.get("API_URL", "http://localhost:8000")

# Show warning if using localhost in production
if "localhost" in API_BASE_URL and os.environ.get("STREAMLIT_RUNTIME_ENV") == "cloud":
    st.warning("⚠️ Using localhost API in cloud deployment. Please configure API_URL in Streamlit secrets.")

# Session State Initialization
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_id" not in st.session_state:
    st.session_state.user_id = f"user_{uuid.uuid4().hex[:8]}"

if "customization" not in st.session_state:
    st.session_state.customization = {
        "personality": "balanced",
        "response_style": "comprehensive",
        "expertise_areas": [],
        "language_preference": "accessible"
    }

# Helper Functions
def call_api(endpoint: str, method: str = "GET", data: Optional[Dict] = None) -> Dict[str, Any]:
    """Make API call to AETHER backend"""
    url = f"{API_BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return {}
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to AETHER API. Please ensure the backend is running.")
        return {}
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return {}

def display_message(role: str, content: str, timestamp: Optional[str] = None):
    """Display a chat message"""
    if role == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(content)
            if timestamp:
                st.caption(f"Sent at {timestamp}")
    else:
        with st.chat_message("assistant", avatar="🧠"):
            st.markdown(content)
            if timestamp:
                st.caption(f"AETHER responded at {timestamp}")

# Main Header
st.markdown("""
<div class="main-header">
    <h1>🧠 AETHER</h1>
    <h3>Advanced Engine for Thought, Heuristic Emotion and Reasoning</h3>
    <p>Built with ❤️ by AlgoRythm Tech </p>
    <p><em>The first AI built by teens, for everyone!</em></p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <h2>⚙️ AETHER Control Panel</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # User Info
    st.markdown("### 👤 User Profile")
    st.info(f"User ID: {st.session_state.user_id}")
    st.info(f"Session: {st.session_state.session_id[:8]}...")
    
    # Customization Section
    st.markdown("### 🎨 Customize AETHER")
    
    with st.expander("Personality Settings", expanded=True):
        personality = st.select_slider(
            "Personality Type",
            options=["Professional", "Balanced", "Friendly", "Creative", "Technical"],
            value="Balanced",
            help="How would you like AETHER to interact with you?"
        )
        
        response_style = st.selectbox(
            "Response Style",
            ["Concise", "Comprehensive", "Detailed", "Simple"],
            help="How detailed should AETHER's responses be?"
        )
        
        language_pref = st.selectbox(
            "Language Preference",
            ["Accessible", "Technical", "Academic", "Casual"],
            help="What language style do you prefer?"
        )
    
    with st.expander("Expertise Areas"):
        expertise = st.multiselect(
            "Select Areas of Focus",
            ["Coding", "AI/ML", "Science", "Math", "Writing", 
             "Business", "Philosophy", "Arts", "Technology", "Education"],
            help="AETHER will tailor responses to these areas"
        )
    
    with st.expander("Advanced Settings"):
        custom_instructions = st.text_area(
            "Custom Instructions",
            placeholder="Tell AETHER how you'd like it to behave...",
            help="Provide specific instructions for AETHER"
        )
        
        temperature = st.slider(
            "Creativity Level",
            0.1, 1.0, 0.7, 0.1,
            help="Higher = more creative, Lower = more focused"
        )
    
    # Apply Customization Button
    if st.button("🔧 Apply Customization", type="primary", use_container_width=True):
        customization_data = {
            "user_id": st.session_state.user_id,
            "personality": personality.lower(),
            "response_style": response_style.lower(),
            "expertise_areas": expertise,
            "language_preference": language_pref.lower(),
            "custom_instructions": custom_instructions
        }
        
        result = call_api("/customize", "POST", customization_data)
        if result.get("status") == "success":
            st.success("✅ AETHER customized successfully!")
            st.session_state.customization = customization_data
        else:
            st.error("Failed to apply customization")
    
    # Actions
    st.markdown("### 🎯 Actions")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 New Session", use_container_width=True):
            st.session_state.session_id = str(uuid.uuid4())
            st.session_state.messages = []
            st.rerun()
    
    with col2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            call_api(f"/session/{st.session_state.session_id}", "DELETE")
            st.rerun()
    
    # Stats
    st.markdown("### 📊 AETHER Stats")
    stats = call_api("/stats")
    if stats:
        st.metric("Total Sessions", stats.get("total_sessions", 0))
        st.metric("Active Users", stats.get("total_users", 0))
        st.metric("Messages Processed", stats.get("total_messages", 0))
    
    # Info
    st.markdown("### ℹ️ About AETHER")
    info = call_api("/info")
    if info:
        with st.expander("System Information"):
            st.json(info)

# Main Chat Interface
main_container = st.container()

with main_container:
    # Welcome message if no messages
    if not st.session_state.messages:
        st.markdown("""
        <div style='text-align: center; padding: 2rem;'>
            <h2>Welcome to AETHER! 🎉</h2>
            <p>I'm your Advanced Engine for Thought, Heuristic Emotion and Reasoning.</p>
            <p>Created by <strong>AlgoRythm Tech</strong> under the leadership of <strong>Sri Aasrith Souri Kompella</strong>.</p>
            <p>Ask me anything or customize my behavior using the sidebar!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.messages:
        display_message(
            message["role"],
            message["content"],
            message.get("timestamp")
        )
    
    # Chat input
    if prompt := st.chat_input("💭 Ask AETHER anything..."):
        # Add user message
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "timestamp": timestamp
        })
        
        # Display user message
        display_message("user", prompt, timestamp)
        
        # Show thinking indicator
        with st.chat_message("assistant", avatar="🧠"):
            with st.spinner("AETHER is thinking..."):
                # Call API
                response_data = call_api("/chat", "POST", {
                    "message": prompt,
                    "session_id": st.session_state.session_id,
                    "user_id": st.session_state.user_id,
                    "stream": False
                })
                
                if response_data:
                    response_text = response_data.get("response", "I'm having trouble processing that request.")
                    confidence = response_data.get("confidence", 0)
                    
                    # Display response
                    st.markdown(response_text)
                    
                    # Show confidence meter
                    if confidence > 0:
                        st.progress(confidence, text=f"Confidence: {confidence*100:.1f}%")
                    
                    # Show metadata in expander
                    if "metadata" in response_data:
                        with st.expander("Response Details"):
                            st.json(response_data["metadata"])
                    
                    # Add to messages
                    response_timestamp = datetime.now().strftime("%H:%M:%S")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response_text,
                        "timestamp": response_timestamp,
                        "confidence": confidence
                    })
                else:
                    fallback_response = """I'm AETHER, created by AlgoRythm Tech. 
                    I'm currently unable to connect to my main processing system, 
                    but I'm still here to help! Please ensure the backend API is running."""
                    
                    st.markdown(fallback_response)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": fallback_response,
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })

# Features Section
with st.expander("✨ AETHER Features", expanded=False):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🧠 Advanced Reasoning**
        - Multi-layer thought processing
        - Complex problem solving
        - Logical deduction
        """)
    
    with col2:
        st.markdown("""
        **❤️ Emotional Intelligence**
        - Context understanding
        - Empathetic responses
        - Mood detection
        """)
    
    with col3:
        st.markdown("""
        **🎯 Customization**
        - Personalized interactions
        - Adaptive learning
        - User preferences
        """)

# Feedback Section
with st.expander("📝 Provide Feedback", expanded=False):
    col1, col2 = st.columns([3, 1])
    
    with col1:
        feedback_text = st.text_area("Share your experience with AETHER")
    
    with col2:
        rating = st.slider("Rate AETHER", 1, 5, 5)
        
        if st.button("Submit Feedback"):
            if st.session_state.messages:
                result = call_api("/feedback", "POST", {
                    "session_id": st.session_state.session_id,
                    "rating": rating,
                    "feedback": feedback_text
                })
                if result.get("status") == "success":
                    st.success("Thank you for your feedback!")
            else:
                st.warning("Please interact with AETHER before providing feedback.")

# Footer
st.markdown("""
<div class="footer">
    <p><strong>AETHER</strong> - Advanced Engine for Thought, Heuristic Emotion and Reasoning</p>
    <p>© 2024 AlgoRythm Tech | CEO: Sri Aasrith Souri Kompella</p>
    <p>The world's first fully teen-built AI startup 🚀</p>
    <p><em>"AI should adapt to you, not the other way around."</em></p>
</div>
""", unsafe_allow_html=True)
