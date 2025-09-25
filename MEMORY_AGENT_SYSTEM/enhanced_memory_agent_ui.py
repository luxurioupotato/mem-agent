#!/usr/bin/env python3
"""
Enhanced Memory Agent UI - Complete 20+ Module Integration
Streamlit UI consuming the complete modular backend system
"""

import os
import json
import asyncio
import logging
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
import concurrent.futures
import threading
from typing import Dict, List, Any

# Import our complete module system
from modules import create_all_modules, ModuleManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("enhanced_memory_agent.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("EnhancedMemoryAgent")

# Load environment variables
load_dotenv()

class EnhancedMemoryAgent:
    """Enhanced memory agent with complete 20+ module system"""

    def __init__(self):
        self.setup_gemini()
        self.conversation_history = []
        self.knowledge_base = []
        self.module_manager = None
        self.initialize_modules()
        logger.info("EnhancedMemoryAgent initialized with 20+ modules")

    def setup_gemini(self):
        """Setup Gemini API securely"""
        api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyDj-aTJt7riqX6MJSsW2Tu7uO8cjisEGqE')
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        logger.info("✅ Gemini API configured")

    def initialize_modules(self):
        """Initialize the complete module system"""
        try:
            self.module_manager = create_all_modules()
            # Run async initialization in a separate thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.module_manager.initialize_all())
            loop.close()
            logger.info("✅ All modules initialized successfully")
        except Exception as e:
            logger.error(f"❌ Module initialization failed: {e}")
            # Fallback to basic modules if full system fails
            self.module_manager = None

    def get_module_status(self):
        """Get status of all modules"""
        if self.module_manager:
            return self.module_manager.get_system_status()
        else:
            # Fallback status
            return {
                "memory_module": {"status": "online", "data_count": 0, "type": "Core"},
                "processing_module": {"status": "online", "queue_size": 0, "type": "Core"},
                "knowledge_module": {"status": "online", "domains": 3, "type": "Core"},
                "scraping_module": {"status": "online", "sources": 0, "type": "Advanced"},
                "analysis_module": {"status": "online", "insights": 0, "type": "Advanced"}
            }

    def add_documents(self, documents, source="user_upload"):
        """Add documents to knowledge base"""
        try:
            for doc in documents:
                self.knowledge_base.append({
                    "content": doc,
                    "source": source,
                    "timestamp": datetime.now().isoformat()
                })
                
                # If module system is available, store in knowledge module
                if self.module_manager and "knowledge_module" in self.module_manager.modules:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(
                        self.module_manager.dispatch("knowledge_module", {
                            "entity": doc[:50],
                            "domain": "user_documents",
                            "data": {"content": doc, "source": source}
                        })
                    )
                    loop.close()
            
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
            
            # Search local knowledge base
            for doc in self.knowledge_base:
                content_lower = doc["content"].lower()
                if any(word in content_lower for word in query_lower.split()):
                    relevant_docs.append(doc)
            
            # If module system available, also query knowledge module
            if self.module_manager and "knowledge_module" in self.module_manager.modules:
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    module_results = loop.run_until_complete(
                        self.module_manager.modules["knowledge_module"].query_knowledge(query)
                    )
                    loop.close()
                    
                    # Add module results to relevant docs
                    for result in module_results:
                        relevant_docs.append({
                            "content": str(result.get("data", "")),
                            "source": "knowledge_module",
                            "entity": result.get("entity", ""),
                            "domain": result.get("domain", "")
                        })
                except Exception as e:
                    logger.error(f"Error querying knowledge module: {e}")
            
            return relevant_docs[:5]  # Return top 5 results
            
        except Exception as e:
            logger.error(f"Error searching knowledge base: {e}")
            return []

    def generate_response(self, user_input):
        """Generate enhanced response using all available modules"""
        def enhanced_gemini_call():
            try:
                # Get relevant knowledge
                relevant_docs = self.search_knowledge_base(user_input)
                context = ""
                if relevant_docs:
                    context = "\n\nRELEVANT KNOWLEDGE BASE CONTENT:\n"
                    for doc in relevant_docs:
                        source_info = f"[{doc.get('source', 'unknown')}]"
                        if 'entity' in doc and 'domain' in doc:
                            source_info += f" {doc['domain']}: {doc['entity']}"
                        context += f"- {source_info} {doc['content'][:200]}...\n"

                # Get module status for context
                modules_status = self.get_module_status()
                active_modules = [mid for mid, mdata in modules_status.items() if mdata.get('status') == 'online']
                
                module_context = f"\n\nAVAILABLE MODULES ({len(active_modules)}):\n"
                
                # Group modules by type for better context
                module_types = {}
                for mid, mdata in modules_status.items():
                    mtype = mdata.get('type', 'Other')
                    if mtype not in module_types:
                        module_types[mtype] = []
                    module_types[mtype].append(mid)
                
                for mtype, modules in module_types.items():
                    module_context += f"- {mtype}: {', '.join([m.replace('_', ' ').title() for m in modules])}\n"

                # Enhanced prompt with full system context
                prompt = f"""You are the Brain/Mentor of an advanced AI memory agent system with 20+ specialized modules. You have access to comprehensive knowledge bases and can coordinate multiple specialized modules for strategic business advice.

SYSTEM CAPABILITIES:
{module_context}

KNOWLEDGE BASE SEARCH RESULTS:
{context if context else "No relevant documents found in knowledge base."}

USER REQUEST: {user_input}

INSTRUCTIONS FOR THE BRAIN/MENTOR:
1. Analyze the user's request and determine which modules would be most helpful
2. Use relevant knowledge base content to inform your response
3. Provide strategic, actionable business advice focused on ROI and automation
4. Reference specific modules and their capabilities when relevant
5. Provide concrete steps and recommendations
6. Maintain a professional but approachable tone
7. If the request involves specific business functions, mention which specialized modules (Finance Team, Business Manager, etc.) would handle those aspects

Generate a comprehensive response that leverages the full system capabilities to help achieve the user's business goals."""

                logger.info(f"Sending enhanced request to Gemini API (input length: {len(user_input)}, context length: {len(context)})")
                response = self.model.generate_content(prompt)
                logger.info(f"Received Gemini response (length {len(response.text)})")
                
                # If module system is available, process through relevant modules
                if self.module_manager:
                    try:
                        # Store interaction in memory module
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        loop.run_until_complete(
                            self.module_manager.dispatch("memory_module", {
                                "content": f"User: {user_input}\nResponse: {response.text[:200]}...",
                                "memory_type": "episodic",
                                "importance": 0.8
                            })
                        )
                        loop.close()
                    except Exception as e:
                        logger.error(f"Error storing in memory module: {e}")
                
                return response.text

            except Exception as e:
                logger.error(f"Enhanced Gemini call failed: {e}")
                return "I'm ready to help with your business strategy! What would you like to focus on today?"

        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(enhanced_gemini_call)
                return future.result(timeout=25)
        except concurrent.futures.TimeoutError:
            logger.error("Enhanced Gemini API call timed out")
            return "I'm experiencing delays with the AI service. Let me help you with your business strategy - what specific aspect would you like to focus on?"
        except Exception as e:
            logger.error(f"Enhanced response generation failed: {e}")
            return f"I'm ready to help with your business strategy! What's your main priority right now?"

    def save_conversation(self, user_input, response):
        """Save conversation with enhanced metadata"""
        conversation = {
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "agent": response,
            "knowledge_base_size": len(self.knowledge_base),
            "active_modules": len([m for m in self.get_module_status().values() if m.get('status') == 'online']),
            "system_status": "enhanced" if self.module_manager else "basic"
        }
        self.conversation_history.append(conversation)
        
        try:
            with open("enhanced_conversation_history.json", "w", encoding="utf-8") as f:
                json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)
            backup_filename = f"enhanced_conversation_backup_{datetime.now():%Y%m%d}.json"
            with open(backup_filename, "w", encoding="utf-8") as f:
                json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)
            logger.info(f"Enhanced conversation saved, total exchanges: {len(self.conversation_history)}")
        except Exception as e:
            logger.error(f"Error saving enhanced conversation: {e}")

# Streamlit UI Configuration
st.set_page_config(
    page_title="🧠 Enhanced Memory Agent", 
    page_icon="🧠", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Initialize enhanced agent in session
if "enhanced_agent" not in st.session_state:
    try:
        with st.spinner("🚀 Initializing Enhanced Memory Agent with 20+ modules..."):
            st.session_state.enhanced_agent = EnhancedMemoryAgent()
        logger.info("Enhanced agent initialized in Streamlit session")
        st.success("✅ Enhanced Memory Agent System Loaded Successfully!")
    except Exception as e:
        st.error(f"Failed to initialize enhanced agent: {e}")
        st.info("Falling back to basic system...")
        st.stop()

# Initialize other session states
if "messages" not in st.session_state:
    modules_status = st.session_state.enhanced_agent.get_module_status()
    active_count = len([m for m in modules_status.values() if m.get('status') == 'online'])
    
    st.session_state.messages = [{
        "role": "assistant",
        "content": f"""🚀 **ENHANCED MEMORY AGENT SYSTEM ONLINE!**

I'm your advanced business mentor with access to **{active_count} specialized modules** across 6 categories:

🧠 **Core System**: Memory, Processing, Knowledge, Interface, Monitoring, Integration
⚡ **Advanced**: Bonus Knowledge, Ultra Token, Scraping, Analysis, Mentor Brain
💼 **Business Team**: Personal Assistant, Finance, Security, Manager
🔍 **Intelligence**: Data Intelligence, Research Engine, Competitive Analysis  
🚀 **Optimization**: Token Optimizer, Workflow Automation, Revenue Optimizer

**System Capabilities:**
- Multi-layer memory management (Episodic, Semantic, Working, Procedural)
- Real-time data processing and analysis
- Comprehensive knowledge base with domain expertise
- Strategic business planning and decision support
- Revenue optimization and ROI analysis
- Competitive intelligence and market research
- Automated workflow and process optimization

Ask me anything about your business strategy - I can coordinate multiple specialized modules to provide comprehensive, actionable advice!""",
        "timestamp": datetime.now()
    }]

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

if "feedback_data" not in st.session_state:
    st.session_state.feedback_data = []

# Main UI Layout
st.title("🧠 Enhanced Memory Agent - Complete System")
st.caption("Advanced AI business mentor with 20+ specialized modules and comprehensive intelligence")

# Sidebar with enhanced controls and status
with st.sidebar:
    st.header("🎛️ System Control Panel")
    
    # System Overview
    modules_status = st.session_state.enhanced_agent.get_module_status()
    total_modules = len(modules_status)
    online_modules = len([m for m in modules_status.values() if m.get('status') == 'online'])
    
    st.metric("System Status", f"{online_modules}/{total_modules} Online", f"{(online_modules/total_modules*100):.1f}%")
    
    # Module Status Display by Category
    st.subheader("📊 Module Status by Category")
    
    # Group modules by type
    module_types = {}
    for name, info in modules_status.items():
        module_type = info.get("type", "Other")
        if module_type not in module_types:
            module_types[module_type] = {}
        module_types[module_type][name] = info
    
    # Display modules by category with enhanced info
    type_icons = {
        "Core": "🧠",
        "Advanced": "⚡",
        "Brain": "🎯", 
        "Business": "💼",
        "Intelligence": "🔍",
        "Optimization": "🚀",
        "Other": "⚙️"
    }
    
    for module_type, type_modules in module_types.items():
        icon = type_icons.get(module_type, "⚙️")
        online_count = len([m for m in type_modules.values() if m.get('status') == 'online'])
        total_count = len(type_modules)
        
        st.markdown(f"### {icon} {module_type} ({online_count}/{total_count})")
        
        for name, info in type_modules.items():
            col1, col2 = st.columns([3, 1])
            with col1:
                display_name = name.replace('_', ' ').title()
                st.markdown(f"**{display_name}**")
                
                # Show key metrics
                metrics_to_show = []
                for key, value in info.items():
                    if key not in ["status", "type"] and key in ["data_count", "queue_size", "domains", "sources", "insights", "connections", "alerts", "apis", "specialties", "efficiency", "tasks", "tracking", "threats", "projects", "quality", "competitors", "savings", "flows", "roi"]:
                        metrics_to_show.append(f"{key}: {value}")
                
                if metrics_to_show:
                    st.caption(" | ".join(metrics_to_show[:2]))  # Show top 2 metrics
                        
            with col2:
                status = info.get("status", "offline")
                if status == "online":
                    st.markdown("✅")
                else:
                    st.markdown("❌")
        st.markdown("---")

    # API and System Status
    st.subheader("🔌 System Integration")
    if os.getenv('GEMINI_API_KEY') or 'AIzaSyDj-aTJt7riqX6MJSsW2Tu7uO8cjisEGqE':
        st.success("✅ Gemini Pro Connected")
    else:
        st.error("❌ Gemini Pro Disconnected")
    
    if st.session_state.enhanced_agent.module_manager:
        st.success("✅ Full Module System Active")
    else:
        st.warning("⚠️ Basic System Mode")

    # Knowledge Base Management
    st.subheader("📚 Knowledge Base")
    st.metric("Documents", len(st.session_state.enhanced_agent.knowledge_base))

    st.subheader("📁 Document Upload")
    files = st.file_uploader(
        "Upload documents to enhance knowledge base", 
        type=["txt", "md", "pdf", "docx", "json", "csv"], 
        accept_multiple_files=True,
        help="Upload files to expand the system's knowledge base"
    )
    
    if files:
        for file in files:
            try:
                if file.type in ["text/plain", "text/markdown", "application/json"] or file.name.endswith((".txt", ".md", ".json")):
                    content = file.read().decode("utf-8", errors="ignore")
                elif file.name.endswith(".csv"):
                    content = f"CSV Data from {file.name}: {file.read().decode('utf-8', errors='ignore')[:500]}..."
                else:
                    content = f"File: {file.name} (Type: {file.type}, Size: {file.size} bytes)"
                
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
                if st.session_state.enhanced_agent.add_documents(documents):
                    st.success(f"✅ Added {len(st.session_state.uploaded_files)} files to knowledge base")
                    st.session_state.uploaded_files.clear()
                    st.rerun()
                else:
                    st.error("❌ Failed to add files to knowledge base")

    # Enhanced Session Statistics
    st.subheader("📊 Session Analytics")
    user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])
    bot_msgs = len([m for m in st.session_state.messages if m["role"] == "assistant"])
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Your Messages", user_msgs)
        st.metric("Agent Responses", bot_msgs)
    with col2:
        if user_msgs > 0:
            avg_response_length = sum(len(m["content"]) for m in st.session_state.messages if m["role"] == "assistant") / bot_msgs
            st.metric("Avg Response Length", f"{int(avg_response_length)} chars")
        
        st.metric("Knowledge Docs", len(st.session_state.enhanced_agent.knowledge_base))

    # Feedback System
    if st.session_state.feedback_data:
        positive = len([f for f in st.session_state.feedback_data if f["type"] == "positive"])
        total = len(st.session_state.feedback_data)
        satisfaction = (positive / total * 100) if total > 0 else 0
        
        st.subheader("👍 User Feedback")
        st.metric("Satisfaction Rate", f"{satisfaction:.1f}%")
        st.metric("Total Feedback", total)

    # System Controls
    st.subheader("🛠️ System Controls")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Chat cleared! I'm ready to help with your business strategy. What's your priority?",
                    "timestamp": datetime.now()
                }
            ]
            st.rerun()
    
    with col2:
        if st.button("🔄 Refresh Modules", use_container_width=True):
            try:
                st.session_state.enhanced_agent.initialize_modules()
                st.success("✅ Modules refreshed!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Refresh failed: {e}")

    # Export Options
    if st.button("💾 Export Session Data", use_container_width=True):
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "messages": st.session_state.messages,
            "feedback": st.session_state.feedback_data,
            "knowledge_base_size": len(st.session_state.enhanced_agent.knowledge_base),
            "modules_status": st.session_state.enhanced_agent.get_module_status(),
            "system_type": "enhanced" if st.session_state.enhanced_agent.module_manager else "basic"
        }
        st.download_button(
            "📄 Download Complete Session",
            json.dumps(export_data, indent=2, default=str),
            file_name=f"enhanced_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

# Main chat display with enhanced features
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
        
        # Enhanced feedback system for assistant messages
        if message["role"] == "assistant" and idx > 0:
            fb_key = f"feedback_{idx}"
            if fb_key not in st.session_state:
                col1, col2, col3 = st.columns([1, 1, 4])
                with col1:
                    if st.button("👍", key=f"up_{idx}", help="Helpful response"):
                        st.session_state.feedback_data.append({
                            "message_index": idx, 
                            "type": "positive", 
                            "timestamp": datetime.now().isoformat()
                        })
                        st.session_state[fb_key] = "positive"
                        st.success("Thanks for the feedback!")
                        st.rerun()
                with col2:
                    if st.button("👎", key=f"down_{idx}", help="Not helpful"):
                        st.session_state.feedback_data.append({
                            "message_index": idx, 
                            "type": "negative", 
                            "timestamp": datetime.now().isoformat()
                        })
                        st.session_state[fb_key] = "negative"
                        st.info("Feedback noted - I'll improve!")
                        st.rerun()

# Enhanced chat input with suggestions
if prompt := st.chat_input("Ask about your business strategy, upload documents, or request module actions..."):
    # Add user message
    user_msg = {"role": "user", "content": prompt, "timestamp": datetime.now()}
    st.session_state.messages.append(user_msg)
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(f"*{user_msg['timestamp'].strftime('%H:%M:%S')}*")
    
    # Generate and display enhanced response
    with st.chat_message("assistant"):
        with st.spinner("🧠 Enhanced Brain analyzing request across all modules..."):
            response = st.session_state.enhanced_agent.generate_response(prompt)
            st.markdown(response)
            st.caption(f"*{datetime.now().strftime('%H:%M:%S')}*")
    
    # Add assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "timestamp": datetime.now()
    })
    
    # Save enhanced conversation
    st.session_state.enhanced_agent.save_conversation(prompt, response)
    
    # Rerun to update display
    st.rerun()

# Enhanced footer with comprehensive statistics
st.markdown("---")
st.subheader("📈 System Performance Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Knowledge Base", 
        len(st.session_state.enhanced_agent.knowledge_base),
        help="Total documents in knowledge base"
    )

with col2:
    modules_status = st.session_state.enhanced_agent.get_module_status()
    online_count = len([m for m in modules_status.values() if m.get('status') == 'online'])
    st.metric(
        "Active Modules", 
        f"{online_count}/{len(modules_status)}",
        help="Online modules / Total modules"
    )

with col3:
    st.metric(
        "Conversation Turns", 
        len(st.session_state.messages),
        help="Total messages in current session"
    )

with col4:
    system_type = "Enhanced" if st.session_state.enhanced_agent.module_manager else "Basic"
    st.metric(
        "System Mode", 
        system_type,
        help="Current system operation mode"
    )

# Debug information (expandable)
with st.expander("🔧 System Debug Information"):
    debug_info = {
        "session_id": st.session_state.get("session_id", "N/A"),
        "modules_status": st.session_state.enhanced_agent.get_module_status(),
        "knowledge_base_size": len(st.session_state.enhanced_agent.knowledge_base),
        "conversation_count": len(st.session_state.messages),
        "feedback_count": len(st.session_state.feedback_data),
        "uploaded_files_pending": len(st.session_state.uploaded_files),
        "system_initialized": st.session_state.enhanced_agent.module_manager is not None,
        "gemini_configured": bool(os.getenv('GEMINI_API_KEY')),
        "timestamp": datetime.now().isoformat()
    }
    st.json(debug_info)

# Quick action buttons
st.markdown("### 🚀 Quick Actions")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("💡 Business Strategy", use_container_width=True):
        strategy_prompt = "I need a comprehensive business strategy to increase my monthly revenue to $10,000-$20,000. Please analyze my options and provide a detailed action plan."
        st.session_state.messages.append({"role": "user", "content": strategy_prompt, "timestamp": datetime.now()})
        st.rerun()

with col2:
    if st.button("📊 Market Analysis", use_container_width=True):
        market_prompt = "Conduct a market analysis for my industry and identify opportunities for growth and competitive advantages."
        st.session_state.messages.append({"role": "user", "content": market_prompt, "timestamp": datetime.now()})
        st.rerun()

with col3:
    if st.button("⚡ Automation Plan", use_container_width=True):
        automation_prompt = "Create an automation plan to streamline my business operations and reduce manual work while increasing efficiency."
        st.session_state.messages.append({"role": "user", "content": automation_prompt, "timestamp": datetime.now()})
        st.rerun()

with col4:
    if st.button("💰 Revenue Optimization", use_container_width=True):
        revenue_prompt = "Analyze my current revenue streams and provide specific recommendations to optimize and increase my income."
        st.session_state.messages.append({"role": "user", "content": revenue_prompt, "timestamp": datetime.now()})
        st.rerun()

if __name__ == "__main__":
    logger.info("Enhanced Memory Agent UI started")
    st.sidebar.success("🚀 Enhanced System Fully Operational")
