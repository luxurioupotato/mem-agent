#!/usr/bin/env python3
"""
Streamlit UI - Complete chat interface following comprehensive guide specifications
Features: Chat history, streaming responses, feedback collection, export functionality
"""

import streamlit as st
import os
import json
import time
import logging
from datetime import datetime
import google.generativeai as genai
from streamlit_feedback import streamlit_feedback

# Import our components
from config import config
from rag_system_gemini import GeminiRAGSystem, setup_rag_system

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatInterface:
    """Complete Streamlit chat interface"""
    
    def __init__(self):
        self.setup_page_config()
        self.initialize_session_state()
        self.setup_gemini()
        
    def setup_page_config(self):
        """Configure Streamlit page settings."""
        st.set_page_config(
            page_title="🧠 Memory Agent",
            page_icon="🧠",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
    def setup_gemini(self):
        """Setup Gemini API."""
        if config.GEMINI_API_KEY:
            genai.configure(api_key=config.GEMINI_API_KEY)
            self.gemini_model = genai.GenerativeModel(config.GEMINI_MODEL)
        else:
            st.error("❌ GEMINI_API_KEY not found. Please set your API key.")
            st.stop()
        
    def initialize_session_state(self):
        """Initialize session state variables."""
        if "messages" not in st.session_state:
            st.session_state.messages = [{
                "role": "assistant", 
                "content": "Hello! I'm your memory-enhanced AI agent. I can help you with questions and remember our conversation for future reference. How can I assist you today?",
                "timestamp": datetime.now()
            }]
        
        if "rag_system" not in st.session_state:
            try:
                st.session_state.rag_system = GeminiRAGSystem()
                if st.session_state.rag_system.initialize_database():
                    stats = st.session_state.rag_system.get_database_stats()
                    if stats.get('total_documents', 0) == 0:
                        st.info("📚 No knowledge base found. System will work with conversation memory only.")
                else:
                    st.error("❌ Failed to initialize RAG database")
            except Exception as e:
                st.error(f"❌ Failed to initialize RAG system: {e}")
                
        if "conversation_id" not in st.session_state:
            st.session_state.conversation_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            
        if "feedback_data" not in st.session_state:
            st.session_state.feedback_data = []
    
    def render_header(self):
        """Render the application header."""
        st.title("🧠 Memory Agent")
        st.caption("Your intelligent assistant with persistent memory and knowledge base")
        
    def display_chat_history(self):
        """Display the conversation history."""
        for i, message in enumerate(st.session_state.messages):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Add timestamp
                if "timestamp" in message:
                    timestamp = message["timestamp"]
                    if isinstance(timestamp, str):
                        timestamp = datetime.fromisoformat(timestamp)
                    st.caption(f"*{timestamp.strftime('%H:%M:%S')}*")
                
                # Add feedback for assistant messages (skip the first welcome message)
                if message["role"] == "assistant" and i > 0:
                    self.collect_feedback(i)
    
    def get_agent_response(self, user_input):
        """Generate agent response using RAG + Gemini integration."""
        try:
            # Get relevant context from RAG system
            rag_system = st.session_state.rag_system
            context = rag_system.get_context_for_query(user_input, max_context_length=2000)
            
            # Construct enhanced prompt
            if context.strip():
                enhanced_prompt = f"""You are a helpful AI assistant with access to a comprehensive knowledge base. Use the provided context to answer the user's question accurately and comprehensively.

CONTEXT FROM KNOWLEDGE BASE:
{context}

USER QUESTION: {user_input}

Please provide a helpful response based on the context provided. If the context contains relevant information, use it to give a detailed answer. If the context doesn't contain relevant information, say so and provide what general help you can. Always be conversational and helpful.

IMPORTANT: Be natural and conversational. Don't mention "based on the context" unless specifically relevant. Just provide a helpful answer."""
            else:
                enhanced_prompt = f"""You are a helpful AI assistant. The user is asking: {user_input}

Please provide a helpful response. Note that no specific context was found in the knowledge base for this query, so provide the best general assistance you can."""
            
            # Get response from Gemini Pro
            response = self.gemini_model.generate_content(
                enhanced_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=config.TEMPERATURE,
                    max_output_tokens=config.MAX_NEW_TOKENS,
                )
            )
            
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"I encountered an error while processing your request. Please try again or rephrase your question."
    
    def save_conversation_to_memory(self, user_input, agent_response):
        """Save conversation to the agent's memory system."""
        try:
            rag_system = st.session_state.rag_system
            rag_system.add_conversation(
                user_input, 
                agent_response, 
                session_id=st.session_state.conversation_id
            )
            logger.info("Conversation saved to memory")
        except Exception as e:
            logger.error(f"Error saving conversation to memory: {e}")
    
    def collect_feedback(self, message_index):
        """Collect user feedback for responses."""
        feedback_key = f"feedback_{message_index}"
        
        if feedback_key not in st.session_state:
            feedback = streamlit_feedback(
                feedback_type="thumbs",
                optional_text_label="💭 How can I improve? (optional)",
                key=feedback_key,
            )
            
            if feedback:
                # Save feedback
                self.save_feedback(message_index, feedback)
                st.session_state[feedback_key] = feedback
                st.success("Thanks for your feedback! 🙏")
    
    def save_feedback(self, message_index, feedback):
        """Save feedback to file for future analysis."""
        try:
            feedback_data = {
                "timestamp": datetime.now().isoformat(),
                "user_message": st.session_state.messages[message_index-1]["content"] if message_index > 0 else "",
                "agent_response": st.session_state.messages[message_index]["content"],
                "feedback_score": feedback["score"],
                "feedback_text": feedback.get("text", ""),
                "session_id": st.session_state.conversation_id
            }
            
            # Add to session state
            st.session_state.feedback_data.append(feedback_data)
            
            # Append to feedback file
            feedback_file = "feedback_data.jsonl"
            with open(feedback_file, "a", encoding='utf-8') as f:
                f.write(json.dumps(feedback_data) + "\n")
                
            logger.info("Feedback saved successfully")
                
        except Exception as e:
            logger.error(f"Error saving feedback: {e}")
    
    def handle_user_input(self):
        """Handle new user input."""
        if prompt := st.chat_input("Ask me anything..."):
            # Add user message to history
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
            
            # Generate and display assistant response
            with st.chat_message("assistant"):
                with st.spinner("🔍 Searching knowledge base and thinking..."):
                    response = self.get_agent_response(prompt)
                
                # Stream the response for better UX
                response_placeholder = st.empty()
                displayed_text = ""
                
                for char in response:
                    displayed_text += char
                    response_placeholder.markdown(displayed_text + "▊")
                    time.sleep(0.01)  # Adjust speed as needed
                
                response_placeholder.markdown(displayed_text)
                st.caption(f"*{datetime.now().strftime('%H:%M:%S')}*")
                
                # Save conversation to memory
                self.save_conversation_to_memory(prompt, response)
            
            # Add assistant response to history
            assistant_message = {
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now()
            }
            st.session_state.messages.append(assistant_message)
            
            # Rerun to update the display
            st.rerun()
    
    def render_sidebar(self):
        """Render sidebar with system information and controls."""
        with st.sidebar:
            st.header("🎛️ System Status")
            
            # RAG System Status
            if "rag_system" in st.session_state:
                stats = st.session_state.rag_system.get_database_stats()
                st.success("✅ RAG System Active")
                st.metric("Documents", stats.get('total_documents', 0))
                st.metric("Sources", stats.get('unique_sources', 0))
                st.metric("Conversations", stats.get('conversations', 0))
            else:
                st.error("❌ RAG System Offline")
            
            # API Status
            st.header("🔌 API Status")
            if config.GEMINI_API_KEY:
                st.success("✅ Gemini Pro Connected")
            else:
                st.error("❌ Gemini Pro Disconnected")
            
            # Conversation Stats
            st.header("📊 Conversation Stats")
            user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])
            bot_msgs = len([m for m in st.session_state.messages if m["role"] == "assistant"])
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Your Messages", user_msgs)
            with col2:
                st.metric("My Responses", bot_msgs)
            
            # Feedback Stats
            if st.session_state.feedback_data:
                positive_feedback = len([f for f in st.session_state.feedback_data if f['feedback_score'] == 1])
                total_feedback = len(st.session_state.feedback_data)
                satisfaction_rate = (positive_feedback / total_feedback * 100) if total_feedback > 0 else 0
                
                st.header("👍 Feedback")
                st.metric("Satisfaction Rate", f"{satisfaction_rate:.1f}%")
                st.metric("Total Feedback", total_feedback)
            
            # Controls
            st.header("🛠️ Controls")
            
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.messages = [{
                    "role": "assistant",
                    "content": "Chat cleared! How can I help you?",
                    "timestamp": datetime.now()
                }]
                st.rerun()
            
            if st.button("💾 Export Chat", use_container_width=True):
                chat_data = {
                    "session_id": st.session_state.conversation_id,
                    "timestamp": datetime.now().isoformat(),
                    "messages": st.session_state.messages,
                    "feedback": st.session_state.feedback_data
                }
                
                st.download_button(
                    "📄 Download JSON",
                    data=json.dumps(chat_data, indent=2, default=str),
                    file_name=f"chat_export_{st.session_state.conversation_id}.json",
                    mime="application/json"
                )
            
            # Knowledge Base Management
            st.header("📚 Knowledge Base")
            
            # File upload for adding documents
            uploaded_file = st.file_uploader(
                "Upload document to knowledge base",
                type=['txt', 'md'],
                help="Upload text files to expand the knowledge base"
            )
            
            if uploaded_file is not None:
                if st.button("Add to Knowledge Base"):
                    try:
                        # Save uploaded file
                        content = uploaded_file.read().decode('utf-8')
                        filename = f"uploaded_{uploaded_file.name}"
                        
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        # Process and add to RAG
                        rag_system = st.session_state.rag_system
                        chunks = rag_system.process_text_file(filename)
                        
                        if chunks:
                            rag_system.add_documents(chunks, source=filename)
                            st.success(f"✅ Added {len(chunks)} chunks from {uploaded_file.name}")
                            st.rerun()
                        else:
                            st.error("❌ Failed to process file")
                            
                    except Exception as e:
                        st.error(f"❌ Error adding file: {e}")
    
    def run(self):
        """Main application loop."""
        self.render_header()
        self.render_sidebar()
        self.display_chat_history()
        self.handle_user_input()

def main():
    """Main function to run the Streamlit app"""
    app = ChatInterface()
    app.run()

if __name__ == "__main__":
    main()
