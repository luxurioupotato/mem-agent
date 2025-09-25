#!/usr/bin/env python3
"""
Memory Agent App - Fixed Streamlit version with timeout handling
Professional chat interface with non-blocking initialization
"""

import streamlit as st
import os
import json
import time
import logging
from datetime import datetime
import google.generativeai as genai
import concurrent.futures
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set page config first
st.set_page_config(
    page_title="🧠 Memory Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Disable hot reload for stability
if hasattr(st, '_config'):
    try:
        st._config.set_option('server.runOnSave', False)
    except:
        pass

class MemoryAgentApp:
    """Memory Agent with timeout handling and non-blocking initialization"""
    
    def __init__(self):
        self.setup_environment()
        self.initialize_session_state()
        
    def setup_environment(self):
        """Setup environment with timeout protection"""
        logger.info("Setting up environment...")
        
        # Set API key
        api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyDj-aTJt7riqX6MJSsW2Tu7uO8cjisEGqE')
        os.environ['GEMINI_API_KEY'] = api_key
        
        try:
            genai.configure(api_key=api_key)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
            logger.info("✅ Gemini API configured")
        except Exception as e:
            logger.error(f"❌ Gemini setup failed: {e}")
            st.error(f"❌ Gemini setup failed: {e}")
            st.stop()
    
    def initialize_session_state(self):
        """Initialize session state with safe defaults"""
        logger.info("Initializing session state...")
        
        if "messages" not in st.session_state:
            st.session_state.messages = [{
                "role": "assistant",
                "content": "Hello! I'm your Memory Agent. I'm ready to help you with your agency website and email marketing funnel. Let's focus on maximum ROI with minimal effort. What's your first priority?",
                "timestamp": datetime.now()
            }]
        
        if "conversation_id" not in st.session_state:
            st.session_state.conversation_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if "system_ready" not in st.session_state:
            st.session_state.system_ready = True
        
        if "business_mode" not in st.session_state:
            st.session_state.business_mode = True
    
    def generate_response_with_timeout(self, user_input, timeout=15):
        """Generate response with timeout protection"""
        try:
            def generate_response():
                # Business-focused prompt
                prompt = f"""You are a business mentor and strategic advisor specializing in agency growth and revenue optimization. The user wants to build an agency website and email marketing funnel with maximum ROI and minimal ongoing effort.

User input: {user_input}

Provide strategic, actionable advice focused on:
- Maximum ROI strategies
- Minimal maintenance solutions
- Revenue generation tactics
- Automation opportunities
- Cost-effective approaches

Be direct, practical, and business-focused. Avoid fluff."""
                
                response = self.gemini_model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.7,
                        max_output_tokens=500,
                    )
                )
                return response.text
            
            # Run with timeout
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(generate_response)
                try:
                    return future.result(timeout=timeout)
                except concurrent.futures.TimeoutError:
                    logger.error(f"Response generation timed out after {timeout} seconds")
                    return "I'm experiencing some delays. Let me give you a quick response: I'm ready to help you build your agency website and email funnel with maximum ROI. What specific aspect would you like to focus on first?"
                
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"I encountered an issue, but I'm still here to help! Let's focus on your agency goals. What's your main priority right now?"
    
    def display_header(self):
        """Display application header"""
        st.title("🧠 Memory Agent - Business Mentor")
        st.caption("Strategic advisor for agency growth and revenue optimization")
    
    def display_sidebar(self):
        """Display sidebar with system status"""
        with st.sidebar:
            st.header("🎛️ System Status")
            
            if st.session_state.system_ready:
                st.success("✅ System Online")
                st.success("✅ Business Mode Active")
                st.success("✅ Revenue Optimization Ready")
            else:
                st.warning("⚠️ System Initializing...")
            
            st.header("📊 Session Stats")
            user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])
            bot_msgs = len([m for m in st.session_state.messages if m["role"] == "assistant"])
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Your Messages", user_msgs)
            with col2:
                st.metric("My Responses", bot_msgs)
            
            st.header("🛠️ Controls")
            
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.messages = [{
                    "role": "assistant",
                    "content": "Chat cleared! Let's focus on building your revenue-generating agency. What's your priority?",
                    "timestamp": datetime.now()
                }]
                st.rerun()
            
            if st.button("💾 Export Chat", use_container_width=True):
                chat_data = {
                    "session_id": st.session_state.conversation_id,
                    "timestamp": datetime.now().isoformat(),
                    "messages": st.session_state.messages
                }
                
                st.download_button(
                    "📄 Download JSON",
                    data=json.dumps(chat_data, indent=2, default=str),
                    file_name=f"business_strategy_{st.session_state.conversation_id}.json",
                    mime="application/json"
                )
            
            # Business Focus
            st.header("🎯 Business Focus")
            st.write("• Agency Website Development")
            st.write("• Email Marketing Funnel")
            st.write("• Revenue Optimization")
            st.write("• Automation Strategies")
            st.write("• ROI Maximization")
    
    def display_chat_history(self):
        """Display conversation history"""
        for i, message in enumerate(st.session_state.messages):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Add timestamp
                if "timestamp" in message:
                    timestamp = message["timestamp"]
                    if isinstance(timestamp, str):
                        timestamp = datetime.fromisoformat(timestamp)
                    st.caption(f"*{timestamp.strftime('%H:%M:%S')}*")
    
    def handle_user_input(self):
        """Handle new user input with timeout protection"""
        if prompt := st.chat_input("Tell me about your agency goals..."):
            # Add user message
            user_message = {
                "role": "user",
                "content": prompt,
                "timestamp": datetime.now()
            }
            st.session_state.messages.append(user_message)
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
                st.caption(f"*{datetime.now().strftime('%H:%M:%S')}*")
            
            # Generate response with timeout protection
            with st.chat_message("assistant"):
                with st.spinner("🧠 Analyzing your business strategy..."):
                    response = self.generate_response_with_timeout(prompt)
                
                # Stream response
                response_placeholder = st.empty()
                displayed_text = ""
                
                for char in response:
                    displayed_text += char
                    response_placeholder.markdown(displayed_text + "▊")
                    time.sleep(0.01)
                
                response_placeholder.markdown(displayed_text)
                st.caption(f"*{datetime.now().strftime('%H:%M:%S')}*")
            
            # Add assistant response
            assistant_message = {
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now()
            }
            st.session_state.messages.append(assistant_message)
            
            st.rerun()
    
    def run(self):
        """Main application loop"""
        logger.info("Starting Memory Agent App")
        
        self.display_header()
        self.display_sidebar()
        self.display_chat_history()
        self.handle_user_input()

def main():
    """Main function with error handling"""
    try:
        logger.info("Memory Agent App starting...")
        app = MemoryAgentApp()
        app.run()
    except Exception as e:
        logger.error(f"App error: {e}")
        st.error(f"System error: {e}")
        st.info("Please refresh the page to restart the application.")

if __name__ == "__main__":
    main()
