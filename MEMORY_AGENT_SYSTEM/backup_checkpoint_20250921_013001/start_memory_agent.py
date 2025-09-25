#!/usr/bin/env python3
"""
Start Memory Agent - Simple startup script
"""

import os
import subprocess
import sys
import time

def main():
    print("🚀 STARTING SSI-ENHANCED MEMORY AGENT")
    print("=" * 50)
    
    # Set API key
    os.environ['GEMINI_API_KEY'] = 'AIzaSyDj-aTJt7riqX6MJSsW2Tu7uO8cjisEGqE'
    print("✅ API Key configured")
    
    # Change to correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"✅ Working directory: {script_dir}")
    
    # Start Streamlit
    print("🚀 Starting web interface...")
    print("🌐 Opening at: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop")
    print()
    
    try:
        # Start Streamlit with integrated_main.py
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 
            'integrated_main.py',
            '--server.address', 'localhost',
            '--server.port', '8501',
            '--server.headless', 'false'
        ])
    except KeyboardInterrupt:
        print("\n🛑 Memory Agent stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Trying alternative method...")
        
        # Alternative method
        try:
            subprocess.run([
                sys.executable, '-m', 'streamlit', 'run', 
                'streamlit_ui.py'
            ])
        except Exception as e2:
            print(f"❌ Alternative method failed: {e2}")

if __name__ == "__main__":
    main()
