#!/usr/bin/env python3
"""
Simple Memory Agent UI - Guaranteed to work
Basic but functional chat interface
"""

import streamlit as st
import os
import json
from datetime import datetime
import google.generativeai as genai

# Set page config
st.set_page_config(
    page_title="🧠 Memory Agent",
    page_icon="🧠",
    layout="wide"
)

# Setup API
@st.cache_resource
def setup_gemini():
    """Setup Gemini API"""
    api_key = 'AIzaSyDj-aTJt7riqX6MJSsW2Tu7uO8cjisEGqE'
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

# Initialize
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "🚀 **MEMORY AGENT ONLINE - BUSINESS MODE ACTIVATED!**\n\nI'm your strategic business mentor focused on:\n- Building your agency website with maximum ROI\n- Creating profitable email marketing funnels\n- Implementing automation systems\n- Generating revenue strategies\n- Minimizing maintenance costs\n\n**Ready to build your $10K-20K/month business!** What's our first move?",
        "timestamp": datetime.now()
    }]

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = datetime.now().strftime("%Y%m%d_%H%M%S")

# Get model
model = setup_gemini()

# Header
st.title("🧠 Memory Agent - Business Mentor")
st.caption("Strategic advisor for agency growth and revenue optimization")

# Sidebar
with st.sidebar:
    st.header("🎛️ System Status")
    st.success("✅ System Online")
    st.success("✅ Business Mode Active")
    st.success("✅ Revenue Optimization Ready")
    
    st.header("📊 Session Stats")
    user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])
    bot_msgs = len([m for m in st.session_state.messages if m["role"] == "assistant"])
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Your Messages", user_msgs)
    with col2:
        st.metric("My Responses", bot_msgs)
    
    st.header("🎯 Business Focus")
    st.write("• Agency Website Development")
    st.write("• Email Marketing Funnel")
    st.write("• Revenue Optimization")
    st.write("• Automation Strategies")
    st.write("• ROI Maximization")
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = [{
            "role": "assistant",
            "content": "Chat cleared! Ready to focus on your business goals. What's our priority?",
            "timestamp": datetime.now()
        }]
        st.rerun()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "timestamp" in message:
            timestamp = message["timestamp"]
            if isinstance(timestamp, str):
                timestamp = datetime.fromisoformat(timestamp)
            st.caption(f"*{timestamp.strftime('%H:%M:%S')}*")

# Handle user input
if prompt := st.chat_input("Tell me about your agency goals..."):
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": datetime.now()
    })
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(f"*{datetime.now().strftime('%H:%M:%S')}*")
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("🧠 Developing your business strategy..."):
            try:
                # Business-focused prompt
                business_prompt = f"""You are a business mentor and strategic advisor specializing in agency growth and revenue optimization. The user wants to build an agency website and email marketing funnel with maximum ROI and minimal ongoing effort.

User input: {prompt}

Provide strategic, actionable advice focused on:
- Maximum ROI strategies
- Minimal maintenance solutions
- Revenue generation tactics
- Automation opportunities
- Cost-effective approaches

Be direct, practical, and business-focused. Provide specific steps and recommendations."""
                
                response = model.generate_content(business_prompt)
                response_text = response.text
                
            except Exception as e:
                response_text = f"I'm ready to help with your business strategy! Let's focus on building your agency website and email funnel. What specific aspect would you like to start with? (Error: {e})"
        
        st.markdown(response_text)
        st.caption(f"*{datetime.now().strftime('%H:%M:%S')}*")
    
    # Add assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text,
        "timestamp": datetime.now()
    })
    
    st.rerun()
