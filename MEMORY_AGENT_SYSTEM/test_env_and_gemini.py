#!/usr/bin/env python3
"""
Minimal reproducible test script for environment loading and Gemini connectivity
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

def main():
    print("🔍 Testing Environment and Gemini API")
    print("=" * 40)
    
    # Load environment variables from .env
    load_dotenv()
    print("✅ load_dotenv() called")
    
    # Print to confirm loading
    api_key = os.getenv("GEMINI_API_KEY")
    print(f"✅ GEMINI_API_KEY loaded: {api_key is not None}")
    
    if not api_key:
        print("❌ Error: GEMINI_API_KEY is not set in .env or environment variables.")
        return False
    
    print(f"🔑 API Key (first 20 chars): {api_key[:20]}...")
    
    # Configure Gemini API
    try:
        genai.configure(api_key=api_key)
        print("✅ Gemini API configured successfully")
    except Exception as e:
        print(f"❌ Failed to configure Gemini API: {e}")
        return False
    
    # Test Gemini call with a simple prompt
    try:
        print("🧠 Testing Gemini API call...")
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Say hello")
        print(f"✅ Gemini API response: {response.text}")
        print("🎉 ALL TESTS PASSED!")
        return True
    except Exception as e:
        print(f"❌ Failed to get response from Gemini API: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎯 READY TO RUN SECURE MEMORY AGENT!")
    else:
        print("\n❌ PLEASE FIX ISSUES ABOVE BEFORE PROCEEDING")
    
    input("Press Enter to continue...")
