#!/usr/bin/env python3
"""
Simple UI Starter - SSI-Enhanced Ultimate Memory Agent
"""

import os
import subprocess
import sys

def main():
    print("🚀 STARTING SSI-ENHANCED MEMORY AGENT UI")
    print("=" * 50)
    
    # Set API key
    os.environ['GEMINI_API_KEY'] = 'AIzaSyDj-aTJt7riqX6MJSsW2Tu7uO8cjisEGqE'
    
    # Change to correct directory
    os.chdir(r'E:\MEM_AGENT\MEMORY_AGENT_SYSTEM')
    
    print("✅ API Key set")
    print("✅ Directory changed")
    print("🚀 Starting Streamlit...")
    
    try:
        # Start Streamlit
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 
            'streamlit_chat_ui.py', 
            '--server.port', '8501',
            '--server.headless', 'true'
        ])
    except KeyboardInterrupt:
        print("\n🛑 UI stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()




