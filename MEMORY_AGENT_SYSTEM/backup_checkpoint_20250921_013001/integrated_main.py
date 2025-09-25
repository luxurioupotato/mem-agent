#!/usr/bin/env python3
"""
Integrated Main Application - Complete RAG + Gemini Pro Integration
Main application that combines all components with Streamlit UI
"""

import streamlit as st
import os
import json
import logging
from datetime import datetime
import google.generativeai as genai
from streamlit_feedback import streamlit_feedback

# Import our components
from config import config
from rag_system import LocalRAGSystem, setup_rag_system
from web_scraper import WebScraper

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IntegratedMemoryAgent:
    """Complete integrated memory agent with RAG + Gemini Pro"""
    
    def __init__(self):
        self.setup_environment()
        self.initialize_components()
        
    def setup_environment(self):
        """Set up API keys and environment variables."""
        # Configure Gemini Pro
        if config.GEMINI_API_KEY:
            genai.configure(api_key=config.GEMINI_API_KEY)
            self.gemini_model = genai.GenerativeModel(config.GEMINI_MODEL)
            logger.info("✅ Gemini Pro configured")
        else:
            st.error("❌ GEMINI_API_KEY not found. Please set your API key.")
            st.stop()
    
    def initialize_components(self):
        """Initialize RAG system and other components."""
        if "rag_system" not in st.session_state:
            try:
                # Initialize RAG system
                st.session_state.rag_system = LocalRAGSystem()
                
                # Check if database exists, if not initialize
                if not st.session_state.rag_system.initialize_database():
                    st.error("❌ Failed to initialize RAG database")
                    st.stop()
                
                # Get database stats
                stats = st.session_state.rag_system.get_database_stats()
                if stats.get('total_documents', 0) == 0:
                    st.info("📚 No knowledge base found. The system will work with conversation memory only.")
                else:
                    st.success(f"✅ RAG system loaded with {stats['total_documents']} documents")
                
            except Exception as e:
                st.error(f"❌ Failed to initialize RAG system: {e}")
                logger.error(f"RAG initialization error: {e}")
        
        # Initialize session state
        if "messages" not in st.session_state:
            st.session_state.messages = [{
                "role": "assistant",
                "content": "Hello! I'm your memory-enhanced AI agent. I can access my knowledge base to provide informed answers and remember our conversation. How can I help you?",
                "timestamp": datetime.now()
            }]
        
        if "conversation_id" not in st.session_state:
            st.session_state.conversation_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if "feedback_data" not in st.session_state:
            st.session_state.feedback_data = []
    
    def generate_response(self, user_input):
        """Generate response using RAG + Gemini Pro integration."""
        try:
            # Step 1: Get relevant context from RAG system
            rag_system = st.session_state.rag_system
            context = rag_system.get_context_for_query(user_input, max_context_length=2000)
            
            # Step 2: Construct enhanced prompt
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
            
            # Step 3: Get response from Gemini Pro
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
                # Save feedback for training data
                self.save_feedback(message_index, feedback)
                st.session_state[feedback_key] = feedback
                st.success("Thanks for your feedback! 🙏")
    
    def save_feedback(self, message_index, feedback):
        """Save feedback to file for future fine-tuning."""
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
    
    def display_chat_interface(self):
        """Main chat interface."""
        st.title("🧠 Memory Agent")
        st.caption("Intelligent assistant with persistent memory and knowledge base")
        
        # Display conversation history
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
        
        # Handle new user input
        if prompt := st.chat_input("Ask me anything..."):
            # Add user message
            user_message = {
                "role": "user", 
                "content": prompt,
                "timestamp": datetime.now()
            }
            st.session_state.messages.append(user_message)
            
            with st.chat_message("user"):
                st.markdown(prompt)
                st.caption(f"*{datetime.now().strftime('%H:%M:%S')}*")
            
            # Generate and display response
            with st.chat_message("assistant"):
                with st.spinner("🔍 Searching knowledge base and thinking..."):
                    response = self.generate_response(prompt)
                
                st.markdown(response)
                st.caption(f"*{datetime.now().strftime('%H:%M:%S')}*")
                
                # Save conversation to memory
                self.save_conversation_to_memory(prompt, response)
            
            # Add assistant message
            assistant_message = {
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now()
            }
            st.session_state.messages.append(assistant_message)
            
            st.rerun()
    
    def display_sidebar_info(self):
        """Display system information and controls in sidebar."""
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
            
            if config.OPENAI_API_KEY:
                st.success("✅ OpenAI Connected")
            else:
                st.warning("⚠️ OpenAI Not Connected (Embeddings disabled)")
            
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
        """Run the complete integrated application."""
        st.set_page_config(
            page_title="Memory Agent",
            page_icon="🧠", 
            layout="wide"
        )
        
        self.display_sidebar_info()
        self.display_chat_interface()

def main():
    """Main function to run the application"""
    app = IntegratedMemoryAgent()
    app.run()

if __name__ == "__main__":
    main()
