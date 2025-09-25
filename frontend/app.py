#!/usr/bin/env python3
"""
MEM_AGENT Frontend Application
Streamlit dashboard with mentor chat interface and GCP integration
"""

import streamlit as st
import os
import json
from datetime import datetime
from typing import Dict, List
from agents.mentor import MEMAgentMentor

# Configure Streamlit page
st.set_page_config(
    page_title="MEM_AGENT Mentor Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'mentor' not in st.session_state:
    st.session_state.mentor = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_id' not in st.session_state:
    st.session_state.user_id = f"user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

def initialize_mentor():
    """Initialize mentor agent"""
    try:
        if st.session_state.mentor is None:
            st.session_state.mentor = MEMAgentMentor()
        return True
    except Exception as e:
        st.error(f"Failed to initialize mentor agent: {e}")
        return False

def display_conversation_history():
    """Display conversation history"""
    if st.session_state.messages:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

def main():
    """Main application function"""
    st.title("🧠 MEM_AGENT Mentor Dashboard")
    st.markdown("**Your AI Business Mentor with Strategic Intelligence**")
    
    # Sidebar
    with st.sidebar:
        st.header("🎯 System Status")
        
        # Initialize mentor
        if st.button("🚀 Initialize Mentor Agent"):
            with st.spinner("Initializing mentor agent..."):
                if initialize_mentor():
                    st.success("✅ Mentor agent initialized successfully!")
                else:
                    st.error("❌ Failed to initialize mentor agent")
        
        # System information
        if st.session_state.mentor:
            st.success("✅ Mentor Agent Active")
            st.info("🤖 Gemini 1.5 Pro Connected")
            st.info("🗄️ Supabase Database Connected")
            st.info("🔐 GCP Secret Manager Active")
        else:
            st.warning("⚠️ Mentor Agent Not Initialized")
        
        # Quick actions
        st.header("⚡ Quick Actions")
        if st.button("📊 Business Analysis"):
            st.info("Upload business metrics for strategic analysis")
        
        if st.button("💡 Strategic Insights"):
            st.info("Get strategic recommendations for revenue optimization")
        
        if st.button("📈 Performance Review"):
            st.info("Review system performance and health metrics")
    
    # Main chat interface
    st.header("💬 Chat with Your AI Mentor")
    st.markdown("*Ask questions about business strategy, revenue optimization, or any topic you need guidance on*")
    
    # Display conversation history
    display_conversation_history()
    
    # Chat input
    if prompt := st.chat_input("Ask your mentor agent a question..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display response
        with st.chat_message("assistant"):
            with st.spinner("🧠 Mentor is thinking..."):
                if st.session_state.mentor:
                    response = st.session_state.mentor.mentor_respond(
                        prompt, 
                        st.session_state.user_id
                    )
                    st.markdown(response)
                    
                    # Add assistant message
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    st.error("Please initialize the mentor agent first")
    
    # Footer
    st.markdown("---")
    st.markdown("**🧠 MEM_AGENT Mentor Dashboard** - Strategic AI Business Intelligence")
    
    # System status
    if st.session_state.mentor:
        st.success("✅ System Operational - All services connected")
    else:
        st.warning("⚠️ System Initialization Required")

if __name__ == "__main__":
    main()
