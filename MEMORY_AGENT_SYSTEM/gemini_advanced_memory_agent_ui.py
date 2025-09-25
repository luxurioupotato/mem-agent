#!/usr/bin/env python3
"""
Gemini Advanced Memory Agent UI - Complete Implementation
Full integrated Streamlit UI with modules, file uploads, feedback, knowledge base
"""

import os
import json
import logging
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
import concurrent.futures
import threading

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is required in the .env file")

genai.configure(api_key=GEMINI_API_KEY)

class MemoryAgent:
    """Advanced Memory Agent with Gemini integration"""
    
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.knowledge_base = []
        self.modules = {
            "memory_module": {"status": "online", "data_count": 0},
            "processing_module": {"status": "online", "queue_size": 0},
            "knowledge_module": {"status": "online", "domains": 3},
            "scraping_module": {"status": "online", "sources": 0},
            "analysis_module": {"status": "online", "insights": 0},
        }
        self.conversation_history = []
        self.upload_queue = []
        logger.info("MemoryAgent initialized with Gemini API")

    def add_documents(self, docs, source):
        """Add documents to knowledge base"""
        for doc in docs:
            self.knowledge_base.append({
                "content": doc,
                "source": source,
                "timestamp": datetime.now().isoformat()
            })
        self.modules["knowledge_module"]["domains"] += len(docs)
        logger.info(f"Added {len(docs)} documents to knowledge base")

    def search_knowledge(self, query):
        """Search knowledge base for relevant content"""
        lowercase = query.lower()
        return [
            d for d in self.knowledge_base 
            if any(word in d["content"].lower() for word in lowercase.split())
        ][:3]

    def generate_response(self, user_input):
        """Generate response with knowledge base and module integration"""
        def call():
            # Search knowledge base for context
            context_docs = self.search_knowledge(user_input)
            context_str = "\n".join(
                f"- {doc['content'][:200]}..." for doc in context_docs
            ) if context_docs else "No relevant documents found."

            # Build modules status
            modules_status = "\n".join(
                f"{k}: {v['status']}" for k, v in self.modules.items()
            )

            # Enhanced prompt for the Brain
            prompt = f"""You are a strategic business mentor and the Brain of an advanced memory agent system with access to multiple modules and a knowledge base.

AVAILABLE MODULES STATUS:
{modules_status}

KNOWLEDGE BASE SEARCH RESULTS:
{context_str}

USER REQUEST: {user_input}

INSTRUCTIONS FOR THE BRAIN:
1. Analyze the user's request and determine which modules to consult
2. Use any relevant knowledge base content to inform your response
3. Provide strategic business advice focused on ROI and automation
4. Reference specific modules or knowledge when relevant
5. Be direct, practical, and business-focused
6. Provide actionable steps and recommendations

As the Brain, you can instruct modules to:
- Process data (processing_module)
- Store/retrieve memories (memory_module)
- Analyze information (analysis_module)
- Scrape web data (scraping_module)
- Manage knowledge (knowledge_module)

Generate a comprehensive response that leverages your full system capabilities."""

            logger.info(f"Requesting Gemini API with prompt length {len(prompt)}")
            response = self.model.generate_content(prompt)
            logger.info("Gemini API responded successfully")
            return response.text

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(call)
            try:
                return future.result(timeout=20)
            except concurrent.futures.TimeoutError:
                logger.warning("Gemini API timeout")
                return "I'm taking too long to respond. Let me help you with your business strategy - what's your main priority?"

    def save_conversation(self, user_text, agent_text):
        """Save conversation with metadata"""
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_text,
            "agent": agent_text,
            "knowledge_base_size": len(self.knowledge_base),
            "modules_status": self.modules.copy()
        })
        
        # Save main file
        with open("conversation_history.json", "w", encoding="utf-8") as f:
            json.dump(self.conversation_history, f, indent=2)
        
        # Save backup
        backup = f"conversation_backup_{datetime.now():%Y%m%d}.json"
        with open(backup, "w", encoding="utf-8") as f:
            json.dump(self.conversation_history, f, indent=2)
        
        logger.info(f"Saved conversation. Total exchanges: {len(self.conversation_history)}")

# Streamlit Configuration
st.set_page_config(
    page_title="🧠 Gemini Memory Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "agent" not in st.session_state:
    st.session_state.agent = MemoryAgent()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "🚀 **GEMINI MEMORY AGENT ONLINE!**\n\nI'm your strategic business mentor with access to:\n• Knowledge base and document processing\n• Multiple specialized modules\n• Memory and conversation history\n• File upload and analysis capabilities\n\n**Ready to help you build your $10K-20K+ revenue business!** What's your first priority?",
        }
    ]

if "uploaded_docs" not in st.session_state:
    st.session_state.uploaded_docs = []

if "feedback" not in st.session_state:
    st.session_state.feedback = []

# Sidebar Controls
with st.sidebar:
    st.header("🎛️ Control Panel")
    
    # Module Status Display
    st.subheader("📊 Modules Status")
    for mod_name, mod_info in st.session_state.agent.modules.items():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{mod_name.replace('_', ' ').title()}**")
        with col2:
            status = mod_info.get("status", "offline")
            status_icon = "✅" if status == "online" else "❌"
            st.write(status_icon)
    
    # File Upload
    st.subheader("📁 Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload files to knowledge base",
        type=["txt", "md", "pdf", "docx"],
        accept_multiple_files=True,
        help="Upload documents to expand the agent's knowledge"
    )
    
    if uploaded_files:
        for file in uploaded_files:
            try:
                if file.type.startswith("text") or file.name.endswith(('.txt', '.md')):
                    content = file.read().decode("utf-8", errors="ignore")
                else:
                    content = f"File: {file.name} (Type: {file.type}, Size: {file.size} bytes)"
                
                st.session_state.uploaded_docs.append(content)
            except Exception as e:
                st.error(f"Error reading {file.name}: {e}")
        
        st.success(f"{len(uploaded_files)} files ready to add to knowledge base")
    
    if st.button("📥 Add to Knowledge Base", use_container_width=True):
        if st.session_state.uploaded_docs:
            st.session_state.agent.add_documents(st.session_state.uploaded_docs, source="user_upload")
            st.session_state.uploaded_docs = []
            st.success("Documents added to knowledge base!")
            st.rerun()
        else:
            st.warning("No documents to add")
    
    # Statistics
    st.subheader("📊 Statistics")
    user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])
    agent_msgs = len([m for m in st.session_state.messages if m["role"] == "assistant"])
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Your Messages", user_msgs)
    with col2:
        st.metric("Agent Responses", agent_msgs)
    
    # Feedback Statistics
    if st.session_state.feedback:
        positive = len([f for f in st.session_state.feedback if f == "positive"])
        total = len(st.session_state.feedback)
        satisfaction = (positive / total * 100) if total > 0 else 0
        
        st.subheader("👍 Feedback")
        st.metric("Satisfaction Rate", f"{satisfaction:.1f}%")
        st.metric("Total Feedback", total)
    
    # Controls
    st.subheader("🛠️ Controls")
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Chat cleared! Ready to help with your business strategy. What's your priority?",
            }
        ]
        st.rerun()
    
    if st.button("💾 Export Conversation", use_container_width=True):
        chat_data = {
            "timestamp": datetime.now().isoformat(),
            "messages": st.session_state.messages,
            "feedback": st.session_state.feedback,
            "knowledge_base_size": len(st.session_state.agent.knowledge_base),
            "modules_status": st.session_state.agent.modules
        }
        
        st.download_button(
            "📄 Download JSON",
            data=json.dumps(chat_data, indent=2, default=str),
            file_name=f"gemini_conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

# Main Chat Interface
st.title("🧠 Gemini Memory Agent - Business Advisor")
st.caption("Strategic business mentor with knowledge base, modules, and file processing")

# Display chat messages
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
        # Add feedback for assistant messages (skip welcome message)
        if msg["role"] == "assistant" and i > 0:
            feedback_key = f"feedback_{i}"
            
            if feedback_key not in st.session_state:
                col1, col2, col3 = st.columns([1, 1, 8])
                
                with col1:
                    if st.button("👍", key=f"pos_{i}"):
                        st.session_state.feedback.append("positive")
                        st.session_state[feedback_key] = "positive"
                        st.success("Thanks!")
                        st.rerun()
                
                with col2:
                    if st.button("👎", key=f"neg_{i}"):
                        st.session_state.feedback.append("negative")
                        st.session_state[feedback_key] = "negative"
                        st.info("Noted!")
                        st.rerun()

# Chat Input
if prompt := st.chat_input("Ask about business strategy, upload docs, or request module actions..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response with threading
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        with st.spinner("🧠 Brain consulting modules and knowledge base..."):
            def generate_response_threaded():
                try:
                    response = st.session_state.agent.generate_response(prompt)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.session_state.agent.save_conversation(prompt, response)
                    return response
                except Exception as e:
                    logger.error(f"Error generating response: {e}")
                    return "I'm ready to help with your business strategy! What specific aspect would you like to focus on?"
            
            # Use threading to prevent blocking
            response_container = {"response": None}
            
            def thread_target():
                response_container["response"] = generate_response_threaded()
            
            thread = threading.Thread(target=thread_target)
            thread.start()
            thread.join(timeout=25)  # 25 second timeout
            
            if thread.is_alive():
                logger.warning("Response generation timed out")
                response_container["response"] = "I'm experiencing delays. Let me help you with your business strategy - what's your main goal?"
            
            response = response_container["response"]
            response_placeholder.markdown(response)
    
    st.rerun()

# Footer with system metrics
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Knowledge Base", len(st.session_state.agent.knowledge_base))

with col2:
    active_modules = len([m for m in st.session_state.agent.modules.values() if m["status"] == "online"])
    st.metric("Active Modules", f"{active_modules}/5")

with col3:
    st.metric("Conversations", len(st.session_state.messages) // 2)

# Debug Information (expandable)
with st.expander("🔧 System Debug Info"):
    st.json({
        "modules_status": st.session_state.agent.modules,
        "knowledge_base_size": len(st.session_state.agent.knowledge_base),
        "conversation_count": len(st.session_state.messages),
        "feedback_count": len(st.session_state.feedback),
        "api_key_configured": bool(GEMINI_API_KEY)
    })

if __name__ == "__main__":
    logger.info("Gemini Advanced Memory Agent UI started")
    st.sidebar.success("🚀 System Fully Operational")
