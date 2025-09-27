#!/usr/bin/env python3
"""
MEM_AGENT Dashboard for Streamlit Cloud
Streamlit Cloud deployment with backend API integration
"""

import streamlit as st
import requests
import json
import os
from datetime import datetime
from typing import Dict, List

# Configure Streamlit page
st.set_page_config(
    page_title="MEM_AGENT Cloud Dashboard",
    page_icon="☁️",
    layout="wide"
)

# Configuration
API_BASE_URL = os.environ.get("API_BASE_URL", "http://your-gcp-vm-ip:8000")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

def make_api_request(endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
    """Make API request to backend services"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        else:
            return {"error": "Unsupported method"}
        
        return response.json() if response.status_code == 200 else {"error": "API request failed"}
    
    except Exception as e:
        return {"error": f"API request failed: {e}"}

def main():
    """Main dashboard function"""
    st.title("☁️ MEM_AGENT Cloud Dashboard")
    st.markdown("**Cloud-based AI Business Intelligence Platform**")
    
    # Sidebar
    with st.sidebar:
        st.header("🌐 System Status")
        
        # Check API connectivity
        if st.button("🏥 Check System Health"):
            with st.spinner("Checking system health..."):
                health_status = make_api_request("/health")
                if "error" not in health_status:
                    st.success("✅ All systems operational")
                else:
                    st.error("❌ System connectivity issues")
        
        # Quick stats
        st.header("📊 Quick Stats")
        stats = make_api_request("/stats")
        if "error" not in stats:
            st.metric("Active Users", stats.get("active_users", 0))
            st.metric("Total Conversations", stats.get("total_conversations", 0))
            st.metric("System Uptime", stats.get("uptime", "Unknown"))
    
    # Main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("💬 Mentor Chat")
        
        # Chat interface
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        
        # Display messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask your mentor..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    # Send to mentor API
                    response = make_api_request("/mentor/chat", "POST", {"prompt": prompt})
                    
                    if "error" not in response:
                        st.markdown(response.get("response", "No response received"))
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": response.get("response", "")
                        })
                    else:
                        st.error("Failed to get mentor response")
    
    with col2:
        st.header("📊 Business Analytics")
        
        # Business metrics
        metrics = make_api_request("/business/metrics")
        if "error" not in metrics:
            st.json(metrics)
        else:
            st.error("Unable to load business metrics")
        
        # System performance
        st.header("⚡ System Performance")
        performance = make_api_request("/system/performance")
        if "error" not in performance:
            st.json(performance)
        else:
            st.error("Unable to load performance data")

if __name__ == "__main__":
    main()
