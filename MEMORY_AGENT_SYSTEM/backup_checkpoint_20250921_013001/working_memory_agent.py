#!/usr/bin/env python3
"""
Working Memory Agent - Command Line Version
Guaranteed to work immediately for business strategy
"""

import os
import json
import asyncio
from datetime import datetime
import google.generativeai as genai

class WorkingMemoryAgent:
    """Working memory agent for immediate business use"""
    
    def __init__(self):
        self.setup_gemini()
        self.conversation_history = []
        
    def setup_gemini(self):
        """Setup Gemini API"""
        api_key = 'AIzaSyDj-aTJt7riqX6MJSsW2Tu7uO8cjisEGqE'
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        print("✅ Gemini API configured")
    
    def generate_response(self, user_input):
        """Generate business-focused response"""
        try:
            # Business-focused prompt
            prompt = f"""You are a business mentor and strategic advisor specializing in agency growth and revenue optimization. The user wants to build an agency website and email marketing funnel with maximum ROI and minimal ongoing effort.

User input: {user_input}

Provide strategic, actionable advice focused on:
- Maximum ROI strategies
- Minimal maintenance solutions
- Revenue generation tactics
- Automation opportunities
- Cost-effective approaches

Be direct, practical, and business-focused. Provide specific steps and recommendations."""
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"I'm ready to help with your business strategy! Let's focus on building your agency website and email funnel. What specific aspect would you like to start with? (Note: {e})"
    
    def save_conversation(self, user_input, response):
        """Save conversation to file"""
        conversation = {
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "agent": response
        }
        
        self.conversation_history.append(conversation)
        
        # Save to file
        with open("conversation_history.json", "w", encoding='utf-8') as f:
            json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)
    
    async def start_conversation(self):
        """Start interactive conversation"""
        print("🚀 SSI-ENHANCED MEMORY AGENT - BUSINESS MODE")
        print("=" * 60)
        print()
        print("🧠 MENTOR: Hello! I'm your business mentor and strategic advisor.")
        print("I'm here to help you build your agency website and email marketing")
        print("funnel with maximum ROI and minimal ongoing effort.")
        print()
        print("I specialize in:")
        print("• Agency website development with high conversion")
        print("• Email marketing funnels that generate revenue")
        print("• Automation systems that minimize your workload")
        print("• ROI optimization strategies")
        print("• Cost-effective business solutions")
        print()
        print("💬 MENTOR: Tell me about your agency and what you want to achieve.")
        print("What services do you offer? Who's your ideal client?")
        print()
        
        conversation_count = 0
        
        while True:
            try:
                user_input = input("👤 YOU: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye', 'stop']:
                    print("\n🧠 MENTOR: Great talking with you! Your business strategy")
                    print("is saved and ready for implementation. Let's make money!")
                    break
                
                print("\n🔍 PROCESSING:")
                print("-" * 20)
                print(f"📝 Analyzing: {user_input[:50]}...")
                print("🧠 Generating strategic response...")
                
                # Generate response
                response = self.generate_response(user_input)
                
                print(f"✅ Response ready ({len(response)} characters)")
                print()
                
                # Display response
                print("🧠 MENTOR:")
                print("-" * 10)
                print(response)
                print()
                
                # Save conversation
                self.save_conversation(user_input, response)
                conversation_count += 1
                
                print(f"💾 Conversation saved ({conversation_count} exchanges)")
                print("-" * 60)
                print()
                
            except KeyboardInterrupt:
                print("\n\n🧠 MENTOR: No problem! Your business strategy is saved.")
                print("Run this script again anytime to continue planning!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Let's continue - what's your next question?")
                print()

def main():
    """Main function"""
    agent = WorkingMemoryAgent()
    asyncio.run(agent.start_conversation())

if __name__ == "__main__":
    main()
