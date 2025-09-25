#!/usr/bin/env python3
"""
All-in-One Memory Agent UI
Complete Streamlit implementation with threading and timeout handling
"""

import os
import json
import asyncio
import logging
import concurrent.futures
from datetime import datetime
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import threading

# Setup logging for debugging and audit
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("memory_agent.log", encoding="utf-8"), logging.StreamHandler()]
)
logger = logging.getLogger("MemoryAgent")

# Load environment variables from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY must be set in .env or environment variables!")

genai.configure(api_key=GEMINI_API_KEY)


class SecureMemoryAgent:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.conversation_history = []
        logger.info("SecureMemoryAgent initialized with Gemini API")

    def generate_response(self, user_input):
        def gemini_call():
            prompt = f"""You are a business mentor and strategic advisor specializing in agency growth and revenue optimization. The user wants to build an agency website and email marketing funnel with maximum ROI and minimal ongoing effort.
User input: {user_input}
Provide strategic, actionable advice focused on:
- Maximum ROI strategies
- Minimal maintenance solutions
- Revenue generation tactics
- Automation opportunities
- Cost-effective approaches
Be direct, practical, and business-focused. Provide specific steps and recommendations."""
            logger.info(f"Sending request to Gemini API; input length={len(user_input)}")
            start = datetime.now()
            response = self.model.generate_content(prompt)
            duration = (datetime.now() - start).total_seconds()
            logger.info(f"Received Gemini response in {duration:.2f}s, length={len(response.text)}")
            return response.text

        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(gemini_call)
                return future.result(timeout=15)
        except concurrent.futures.TimeoutError:
            logger.error("Gemini API call timed out")
            return "Sorry, the AI service is taking too long to respond. Please try again."
        except Exception as e:
            logger.error(f"Gemini API call error: {e}")
            return f"Technical issue occurred: {e}"

    def save_conversation(self, user_input, response):
        conversation = {
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "agent": response,
        }
        self.conversation_history.append(conversation)
        try:
            with open("conversation_history.json", "w", encoding="utf-8") as f:
                json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)

            backup_filename = f"conversation_backup_{datetime.now():%Y%m%d}.json"
            with open(backup_filename, "w", encoding="utf-8") as bf:
                json.dump(self.conversation_history, bf, indent=2, ensure_ascii=False)

            logger.info(f"Conversation saved, total exchanges: {len(self.conversation_history)}")
        except Exception as e:
            logger.error(f"Error saving conversation: {e}")


# Streamlit UI combined with backend
def main():
    st.set_page_config("🧠 Business Memory Agent", layout="wide")
    st.title("🧠 SSI-Enhanced Business Memory Agent")
    st.markdown(
        "Ask your AI business mentor about agency growth, ROI strategies, "
        "automation, and email marketing funnels."
    )

    # Initialize agent
    if "agent" not in st.session_state:
        try:
            st.session_state.agent = SecureMemoryAgent()
            logger.info("Agent initialized in Streamlit session")
        except Exception as e:
            st.error(f"Failed to initialize agent: {e}")
            st.stop()

    # Initialize messages
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "🚀 **BUSINESS MODE ACTIVATED!**\n\nHello! I'm your business mentor and strategic advisor. I'm ready to help you build your agency website and email marketing funnel with maximum ROI and minimal effort.\n\n**Let's focus on making money!** What's your first priority?",
            }
        ]

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
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Chat cleared! Ready to focus on your business goals. What's our priority?",
                }
            ]
            st.rerun()
        
        if st.button("💾 Export Chat", use_container_width=True):
            chat_data = {
                "timestamp": datetime.now().isoformat(),
                "messages": st.session_state.messages
            }
            
            st.download_button(
                "📄 Download JSON",
                data=json.dumps(chat_data, indent=2, default=str),
                file_name=f"business_strategy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

    # Display chat messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Get user input
    if prompt := st.chat_input("Type your business question here..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate AI response with threading to avoid blocking Streamlit
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            
            with st.spinner("🧠 Developing your business strategy..."):
                def generate_and_display():
                    try:
                        response = st.session_state.agent.generate_response(prompt)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        st.session_state.agent.save_conversation(prompt, response)
                        return response
                    except Exception as e:
                        logger.error(f"Error in generate_and_display: {e}")
                        return f"I'm ready to help with your business strategy! What specific aspect of your agency would you like to focus on?"
                
                # Use threading to prevent blocking
                response_container = {"response": None}
                
                def thread_target():
                    response_container["response"] = generate_and_display()
                
                thread = threading.Thread(target=thread_target)
                thread.start()
                thread.join(timeout=20)  # 20 second timeout
                
                if thread.is_alive():
                    logger.warning("Response generation timed out")
                    response_container["response"] = "I'm experiencing delays. Let me help you with your business strategy - what's your main goal right now?"
                
                response = response_container["response"]
                response_placeholder.markdown(response)
        
        st.rerun()


if __name__ == "__main__":
    main()
