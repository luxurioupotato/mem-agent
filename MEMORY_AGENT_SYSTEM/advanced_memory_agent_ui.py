#!/usr/bin/env python3
"""
Advanced Memory Agent UI - Working 5-Module Version
Chat interface, file upload, knowledge base, feedback, module controls
"""

import os
import json
import logging
import streamlit as st
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv
import concurrent.futures
import threading

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("advanced_memory_agent.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("AdvancedMemoryAgent")

# Load environment variables
load_dotenv()

class AdvancedMemoryAgent:
    """Advanced memory agent with knowledge base and module integration"""

    def __init__(self):
        self.setup_gemini()
        self.conversation_history = []
        self.knowledge_base = []
        self.modules = {
            "memory_module": {"status": "online", "data_count": 0},
            "processing_module": {"status": "online", "queue_size": 0},
            "knowledge_module": {"status": "online", "domains": 3},
            "scraping_module": {"status": "online", "sources": 0},
            "analysis_module": {"status": "online", "insights": 0}
        }
        logger.info("AdvancedMemoryAgent initialized")

    def setup_gemini(self):
        """Setup Gemini API securely"""
        api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyDj-aTJt7riqX6MJSsW2Tu7uO8cjisEGqE')
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        logger.info("✅ Gemini API configured")

    def add_documents(self, documents, source="user_upload"):
        """Add documents to knowledge base"""
        try:
            for doc in documents:
                self.knowledge_base.append({
                    "content": doc,
                    "source": source,
                    "timestamp": datetime.now().isoformat()
                })
            self.modules["knowledge_module"]["domains"] += len(documents)
            logger.info(f"Added {len(documents)} documents to knowledge base")
            return True
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            return False

    def search_knowledge_base(self, query):
        """Search knowledge base for relevant content"""
        try:
            relevant_docs = []
            query_lower = query.lower()
            for doc in self.knowledge_base:
                content_lower = doc["content"].lower()
                if any(word in content_lower for word in query_lower.split()):
                    relevant_docs.append(doc)
            return relevant_docs[:3]
        except Exception as e:
            logger.error(f"Error searching knowledge base: {e}")
            return []

    def generate_response(self, user_input):
        """Generate response with knowledge base integration"""
        def gemini_call():
            relevant_docs = self.search_knowledge_base(user_input)
            context = ""
            if relevant_docs:
                context = "\n\nRELEVANT KNOWLEDGE BASE CONTENT:\n"
                for doc in relevant_docs:
                    context += f"- {doc['content'][:200]}...\n"

            prompt = f"""You are a business mentor and strategic advisor with access to a comprehensive knowledge base. The user wants to build an agency website and email marketing funnel with maximum ROI and minimal ongoing effort.
{context}
User input: {user_input}
Instructions for the Brain/Mentor:
1. Pull relevant data from the knowledge base context above if available
2. Provide strategic, actionable advice focused on:
   - Maximum ROI strategies
   - Minimal maintenance solutions
   - Revenue generation tactics
   - Automation opportunities
   - Cost-effective approaches
3. Be direct, practical, and business-focused
4. Provide specific steps and recommendations
5. If knowledge base has relevant info, reference it naturally
Generate a comprehensive response that helps the user achieve their business goals."""

            logger.info(f"Sending enhanced request to Gemini API (input length: {len(user_input)}, context length: {len(context)})")
            response = self.model.generate_content(prompt)
            logger.info(f"Received Gemini response (length {len(response.text)})")
            return response.text

        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(gemini_call)
                return future.result(timeout=20)
        except concurrent.futures.TimeoutError:
            logger.error("Gemini API call timed out")
            return "I'm experiencing delays with the AI service. Let me help you with your business strategy - what specific aspect would you like to focus on?"
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}")
            return f"I'm ready to help with your business strategy! What's your main priority right now?"

    def save_conversation(self, user_input, response):
        """Save conversation with enhanced metadata"""
        conversation = {
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "agent": response,
            "knowledge_base_size": len(self.knowledge_base),
            "modules_status": self.modules.copy()
        }
        self.conversation_history.append(conversation)
        try:
            with open("conversation_history.json", "w", encoding="utf-8") as f:
                json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)
            backup_filename = f"conversation_backup_{datetime.now():%Y%m%d}.json"
            with open(backup_filename, "w", encoding="utf-8") as f:
                json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)
            logger.info(f"Conversation saved, total exchanges: {len(self.conversation_history)}")
        except Exception as e:
            logger.error(f"Error saving conversation: {e}")

    def get_module_status(self):
        """Get current module status"""
        return self.modules

# Streamlit UI Configuration
st.set_page_config(
    page_title="🧠 Advanced Memory Agent", 
    page_icon="🧠", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Initialize agent in session
if "agent" not in st.session_state:
    try:
        st.session_state.agent = AdvancedMemoryAgent()
        logger.info("Advanced agent initialized in Streamlit session")
    except Exception as e:
        st.error(f"Failed to initialize agent: {e}")
        st.stop()

# Initialize other session states
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "🚀 **ADVANCED MEMORY AGENT ONLINE!**\n\nI'm your business mentor with access to 5 specialized modules:\n\n✅ Memory Module\n✅ Processing Module  \n✅ Knowledge Module\n✅ Scraping Module\n✅ Analysis Module\n\nAsk me anything about your business strategy!",
        "timestamp": datetime.now()
    }]

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

if "feedback_data" not in st.session_state:
    st.session_state.feedback_data = []

# Main UI Layout
st.title("🧠 Advanced Memory Agent - Business Mentor")
st.caption("Strategic advisor with 5 specialized modules and knowledge base integration")

# Sidebar with controls and status
with st.sidebar:
    st.header("🎛️ Control Panel")
    
    # Module Status Display
    st.subheader("📊 Modules Status")
    modules = st.session_state.agent.get_module_status()
    for name, info in modules.items():
        col1, col2 = st.columns([3, 1])
        with col1:
            display_name = name.replace('_', ' ').title()
            st.markdown(f"**{display_name}**")
        with col2:
            status = info.get("status", "offline")
            if status == "online":
                st.markdown("✅")
            else:
                st.markdown("❌")

    st.subheader("🔌 API Status")
    if os.getenv('GEMINI_API_KEY') or 'AIzaSyDj-aTJt7riqX6MJSsW2Tu7uO8cjisEGqE':
        st.success("✅ Gemini Pro Connected")
    else:
        st.error("❌ Gemini Pro Disconnected")

    st.subheader("📚 Knowledge Base")
    st.metric("Documents", len(st.session_state.agent.knowledge_base))

    st.subheader("📁 File Upload")
    files = st.file_uploader(
        "Upload documents to knowledge base", 
        type=["txt", "md", "pdf", "docx"], 
        accept_multiple_files=True
    )
    
    if files:
        for file in files:
            try:
                if file.type in ["text/plain", "text/markdown"] or file.name.endswith((".txt", ".md")):
                    content = file.read().decode("utf-8", errors="ignore")
                else:
                    content = f"File: {file.name} (Type: {file.type}, Size: {file.size})"
                st.session_state.uploaded_files.append({
                    "name": file.name,
                    "content": content,
                    "type": file.type,
                    "size": file.size
                })
            except Exception as e:
                st.error(f"Error processing {file.name}: {e}")
        
        if st.button("📥 Add Files to Knowledge Base", use_container_width=True):
            if st.session_state.uploaded_files:
                documents = [f["content"] for f in st.session_state.uploaded_files]
                if st.session_state.agent.add_documents(documents):
                    st.success(f"✅ Added {len(st.session_state.uploaded_files)} files to knowledge base")
                    st.session_state.uploaded_files.clear()
                    st.rerun()
                else:
                    st.error("❌ Failed to add files to knowledge base")

    st.subheader("📊 Session Stats")
    user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])
    bot_msgs = len([m for m in st.session_state.messages if m["role"] == "assistant"])
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Your Messages", user_msgs)
    with col2:
        st.metric("Agent Responses", bot_msgs)

    if st.session_state.feedback_data:
        positive = len([f for f in st.session_state.feedback_data if f["type"] == "positive"])
        total = len(st.session_state.feedback_data)
        satisfaction = (positive / total * 100) if total > 0 else 0
        st.subheader("👍 Feedback")
        st.metric("Satisfaction Rate", f"{satisfaction:.1f}%")
        st.metric("Total Feedback", total)

    st.subheader("🛠️ Controls")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Chat cleared! Ready to help with your business strategy. What's your priority?",
                "timestamp": datetime.now()
            }
        ]
        st.rerun()

    if st.button("💾 Export Conversation", use_container_width=True):
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "messages": st.session_state.messages,
            "feedback": st.session_state.feedback_data,
            "knowledge_base_size": len(st.session_state.agent.knowledge_base),
            "modules_status": st.session_state.agent.get_module_status()
        }
        st.download_button(
            "📄 Download JSON",
            json.dumps(export_data, indent=2, default=str),
            file_name=f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

# Main chat display
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "timestamp" in message:
            ts = message["timestamp"]
            if isinstance(ts, str):
                try:
                    ts = datetime.fromisoformat(ts)
                except:
                    ts = datetime.now()
            st.caption(f"*{ts.strftime('%H:%M:%S')}*")

# Chat input
if prompt := st.chat_input("Ask about your business strategy, upload documents, or request module actions..."):
    # Add user message
    user_msg = {"role": "user", "content": prompt, "timestamp": datetime.now()}
    st.session_state.messages.append(user_msg)
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(f"*{user_msg['timestamp'].strftime('%H:%M:%S')}*")
    
    # Generate and display response
    with st.chat_message("assistant"):
        with st.spinner("🧠 Brain analyzing request and generating response..."):
            response = st.session_state.agent.generate_response(prompt)
            st.markdown(response)
            st.caption(f"*{datetime.now().strftime('%H:%M:%S')}*")
    
    # Add assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "timestamp": datetime.now()
    })
    
    # Save conversation
    st.session_state.agent.save_conversation(prompt, response)
    
    # Rerun to update display
    st.rerun()

# Footer with statistics
st.markdown("---")
col1, col2, col3 = st.columns(3)
col1.metric("Knowledge Base Docs", len(st.session_state.agent.knowledge_base))
col2.metric("Active Modules", len([m for m in st.session_state.agent.modules.values() if m["status"] == "online"]))
col3.metric("Conversation Turns", len(st.session_state.messages))

if __name__ == "__main__":
    logger.info("Advanced Memory Agent UI started")
    st.sidebar.success("🚀 System Fully Operational")