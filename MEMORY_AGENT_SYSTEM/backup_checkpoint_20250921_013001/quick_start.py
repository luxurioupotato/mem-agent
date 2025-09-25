#!/usr/bin/env python3
"""
Quick Start - SSI-Enhanced Ultimate Memory Agent
Command line version that works immediately
"""

import os
import asyncio
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set API key
os.environ['GEMINI_API_KEY'] = 'AIzaSyDj-aTJt7riqX6MJSsW2Tu7uO8cjisEGqE'

async def main():
    print("🚀 SSI-ENHANCED ULTIMATE MEMORY AGENT")
    print("=" * 50)
    print("✅ API Key set")
    print("✅ System initializing...")
    
    try:
        from final_system_integration import FinalSystemIntegration
        
        print("✅ System loaded successfully")
        print("🚀 Starting Memory Agent...")
        print()
        
        # Start the system
        system = FinalSystemIntegration()
        await system.start_system()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check your Python installation and dependencies")

if __name__ == "__main__":
    asyncio.run(main())




