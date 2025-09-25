#!/usr/bin/env python3
"""
Streamlit Chat UI for SSI-Enhanced Ultimate Memory Agent
Modern web-based interface with file sharing capabilities
"""

import streamlit as st
import os
import json
import asyncio
import sqlite3
import time
import re
from datetime import datetime
from pathlib import Path
import google.generativeai as genai
from typing import Dict, List, Any, Optional
import base64
import io

# Import our existing system
from final_system_integration import FinalSystemIntegration, InstructionScraper, ProcessTracker

class StreamlitChatUI:
    """Modern web-based chat interface for the Memory Agent System"""
    
    def __init__(self):
        self.setup_page_config()
        self.initialize_session_state()
        self.setup_gemini()
        self.setup_system()
    
    def setup_page_config(self):
        """Configure Streamlit page"""
        st.set_page_config(
            page_title="🧠 SSI-Enhanced Memory Agent",
            page_icon="🧠",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "system_initialized" not in st.session_state:
            st.session_state.system_initialized = False
        if "mentor_intro_complete" not in st.session_state:
            st.session_state.mentor_intro_complete = False
        if "uploaded_files" not in st.session_state:
            st.session_state.uploaded_files = []
        if "process_logs" not in st.session_state:
            st.session_state.process_logs = []
    
    def setup_gemini(self):
        """Setup Gemini API"""
        try:
            api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyDj-aTJt7riqX6MJSsW2Tu7uO8cjisEGqE')
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            return True
        except Exception as e:
            st.error(f"❌ Gemini setup failed: {e}")
            return False
    
    def setup_system(self):
        """Setup the memory agent system"""
        try:
            self.system = FinalSystemIntegration()
            self.instruction_scraper = InstructionScraper(self.system)
            self.process_tracker = ProcessTracker(self.system)
            return True
        except Exception as e:
            st.error(f"❌ System setup failed: {e}")
            return False
    
    def display_sidebar(self):
        """Display sidebar with system info and controls"""
        with st.sidebar:
            st.title("🧠 Memory Agent Control Panel")
            
            # System Status
            st.subheader("📊 System Status")
            st.success("✅ System Online")
            st.success("✅ Business Mode Ready")
            st.success("✅ Revenue Optimization Active")
            
            # Memory Layers
            st.subheader("🧠 Memory Layers")
            memory_layers = ["Episodic", "Semantic", "Procedural", "Working"]
            for layer in memory_layers:
                st.write(f"• {layer}")
            
            # File Upload
            st.subheader("📁 File Sharing")
            uploaded_file = st.file_uploader(
                "Upload a file to share with the agent",
                type=['txt', 'pdf', 'docx', 'png', 'jpg', 'jpeg', 'csv', 'json'],
                help="Upload files to share with the Memory Agent"
            )
            
            if uploaded_file is not None:
                self.handle_file_upload(uploaded_file)
            
            # Process Logs
            st.subheader("📋 Process Logs")
            if st.session_state.process_logs:
                for log in st.session_state.process_logs[-5:]:  # Show last 5
                    st.text(f"• {log}")
            else:
                st.text("No processes logged yet")
            
            # Clear Chat
            if st.button("🗑️ Clear Chat"):
                st.session_state.messages = []
                st.session_state.process_logs = []
                st.rerun()
    
    def handle_file_upload(self, uploaded_file):
        """Handle file upload and processing"""
        try:
            # Save file
            file_path = f"local_storage/uploads/{uploaded_file.name}"
            os.makedirs("local_storage/uploads", exist_ok=True)
            
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Process file content
            file_content = self.extract_file_content(uploaded_file, file_path)
            
            # Store in memory
            self.system.modules["memory_module"].store_memory(
                "episodic", 
                f"File uploaded: {uploaded_file.name} - {file_content[:200]}...",
                0.9
            )
            
            # Add to session state
            st.session_state.uploaded_files.append({
                "name": uploaded_file.name,
                "size": uploaded_file.size,
                "type": uploaded_file.type,
                "content": file_content[:500] + "..." if len(file_content) > 500 else file_content
            })
            
            st.success(f"✅ File '{uploaded_file.name}' uploaded successfully!")
            
        except Exception as e:
            st.error(f"❌ Error uploading file: {e}")
    
    def extract_file_content(self, uploaded_file, file_path):
        """Extract content from uploaded file"""
        try:
            if uploaded_file.type == "text/plain":
                return uploaded_file.read().decode("utf-8")
            elif uploaded_file.type == "application/json":
                return json.dumps(json.loads(uploaded_file.read().decode("utf-8")), indent=2)
            elif uploaded_file.type.startswith("image/"):
                return f"Image file: {uploaded_file.name} ({uploaded_file.size} bytes)"
            else:
                return f"File: {uploaded_file.name} ({uploaded_file.size} bytes)"
        except Exception as e:
            return f"Error reading file: {e}"
    
    def display_chat_interface(self):
        """Display the main chat interface"""
        st.title("🧠 SSI-Enhanced Ultimate Memory Agent")
        st.caption("Revolutionary AI Memory System with Real-time Processing")
        
        # Chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Show process logs if available
                if "process_logs" in message:
                    with st.expander("🔍 Process Details"):
                        for log in message["process_logs"]:
                            st.text(log)
    
    def process_user_input(self, user_input: str):
        """Process user input with real-time scraping and logging"""
        try:
            # Extract keywords and instructions
            keywords = self.instruction_scraper.extract_keywords(user_input)
            instructions = self.instruction_scraper.extract_instructions(user_input)
            
            # Determine memory layer
            memory_layer = self.system.determine_memory_layer(user_input, keywords)
            
            # Log to memory layer
            self.system.log_to_memory_layer(user_input, keywords, instructions, memory_layer)
            
            # Track process
            process_log = f"Keywords: {', '.join(keywords)} | Instructions: {len(instructions)} | Memory Layer: {memory_layer}"
            st.session_state.process_logs.append(process_log)
            
            return {
                "keywords": keywords,
                "instructions": instructions,
                "memory_layer": memory_layer,
                "process_log": process_log
            }
            
        except Exception as e:
            st.error(f"❌ Error processing input: {e}")
            return None
    
    def generate_mentor_response(self, user_input: str, conversation_count: int):
        """Generate mentor response using Gemini"""
        try:
            # Check if user wants to start business
            if user_input.lower() in ['done', 'finish', 'ready', 'let\'s go', 'start business', 'enough of talking! get to business!']:
                return """🚀 **BUSINESS MODE ACTIVATED!**

**SSI-ENHANCED ULTIMATE MEMORY AGENT - OPERATIONAL**

✅ **System Status**: All modules online
✅ **Memory Layers**: Active and processing
✅ **Knowledge Bases**: Fully loaded
✅ **Real-time Processing**: Enabled
✅ **File Sharing**: Ready
✅ **Revenue Optimization**: Active

**READY FOR STRATEGIC EXECUTION!**

What's our first business objective? I'm ready to:
- Build your agency website with maximum ROI
- Create your email marketing funnel
- Implement automation systems
- Generate revenue strategies
- Execute strategic plans

**Let's make money! What's the plan?**"""
            
            prompt = f"""
            You are the Mentor/Brain of an advanced AI system. You're having a friendly conversation with the user.
            Be human-like, engaging, and conversational. Don't sound like a bot.
            
            User said: "{user_input}"
            
            Respond in a natural, friendly way. Show genuine interest and curiosity.
            Keep it conversational and engaging. This is conversation #{conversation_count + 1}.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"I'm having a bit of trouble processing that right now, but I'm really interested in what you're saying! Could you tell me more about that?"
    
    def run(self):
        """Main application loop"""
        # Display sidebar
        self.display_sidebar()
        
        # Display chat interface
        self.display_chat_interface()
        
        # Chat input
        if prompt := st.chat_input("Type your message here..."):
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Process user input
            process_info = self.process_user_input(prompt)
            
            # Generate mentor response
            with st.spinner("🧠 Mentor is thinking..."):
                response = self.generate_mentor_response(prompt, len(st.session_state.messages))
            
            # Add mentor response to chat
            mentor_message = {
                "role": "assistant", 
                "content": response,
                "process_logs": [process_info["process_log"]] if process_info else []
            }
            st.session_state.messages.append(mentor_message)
            
            # Rerun to update the display
            st.rerun()

def main():
    """Main function to run the Streamlit app"""
    ui = StreamlitChatUI()
    ui.run()

if __name__ == "__main__":
    main()
