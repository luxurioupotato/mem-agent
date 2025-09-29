#!/usr/bin/env python3
"""
Secure Memory Agent - Following Best Practices
Environment variables, timeout handling, comprehensive logging
"""

import os
import json
import asyncio
import logging
import concurrent.futures
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('memory_agent.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SecureMemoryAgent:
    """Secure memory agent with best practices"""
    
    def __init__(self):
        self.setup_gemini()
        self.conversation_history = []
        logger.info("SecureMemoryAgent initialized")
        
    def setup_gemini(self):
        """Setup Gemini API securely"""
        try:
            # Load environment variables
            load_dotenv()
            
            # Get API key from environment
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                # Fallback to direct assignment for this session
                api_key = os.getenv('GEMINI_API_KEY', '')
                os.environ['GEMINI_API_KEY'] = api_key
                logger.warning("Using fallback API key - consider setting GEMINI_API_KEY environment variable")
            
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            logger.info("✅ Gemini API configured securely")
            
        except Exception as e:
            logger.error(f"❌ Gemini setup failed: {e}")
            raise Exception(f"Failed to setup Gemini API: {e}")

    def generate_response(self, user_input):
        """Generate business-focused response with timeout."""
        try:
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
                
                logger.info(f"Sending request to Gemini API (input length: {len(user_input)})")
                start_time = datetime.now()
                
                response = self.model.generate_content(prompt)
                
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                logger.info(f"Gemini API response received (duration: {duration:.2f}s, response length: {len(response.text)})")
                
                return response.text

            # Use timeout wrapper to prevent hanging
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(gemini_call)
                try:
                    return future.result(timeout=15)  # 15 second timeout
                except concurrent.futures.TimeoutError:
                    logger.error("Gemini API call timed out after 15 seconds")
                    return "I'm experiencing delays with the AI service. Let me give you a quick response: I'm ready to help you build your agency website and email funnel with maximum ROI. What specific aspect would you like to focus on first?"
            
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}")
            return f"I'm ready to help with your business strategy! Let's focus on building your agency website and email funnel. What specific aspect would you like to start with? (Note: Experiencing technical issues, but I'm still here to help!)"
    
    def save_conversation(self, user_input, response):
        """Save conversation with error handling"""
        try:
            conversation = {
                "timestamp": datetime.now().isoformat(),
                "user": user_input,
                "agent": response
            }
            
            self.conversation_history.append(conversation)
            
            # Save to file with backup
            filename = "conversation_history.json"
            backup_filename = f"conversation_backup_{datetime.now().strftime('%Y%m%d')}.json"
            
            with open(filename, "w", encoding='utf-8') as f:
                json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)
            
            # Create daily backup
            with open(backup_filename, "w", encoding='utf-8') as f:
                json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Conversation saved ({len(self.conversation_history)} total exchanges)")
            
        except Exception as e:
            logger.error(f"Failed to save conversation: {e}")
    
    async def start_conversation(self):
        """Start interactive conversation with comprehensive logging"""
        logger.info("Starting conversation session")
        
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
        print("💡 TIP: Type 'quit', 'exit', or press Ctrl+C to end the session")
        print("-" * 60)
        print()
        
        conversation_count = 0
        
        while True:
            try:
                user_input = input("👤 YOU: ").strip()
                
                if not user_input:
                    continue
                
                logger.info(f"User input received: {user_input[:100]}...")
                
                if user_input.lower() in ['quit', 'exit', 'bye', 'stop']:
                    print("\n🧠 MENTOR: Great talking with you! Your business strategy")
                    print("is saved and ready for implementation. Let's make money!")
                    logger.info("Session ended by user")
                    break
                
                print("\n🔍 PROCESSING:")
                print("-" * 20)
                print(f"📝 Analyzing: {user_input[:50]}...")
                print("🧠 Generating strategic response...")
                
                # Generate response with timeout
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
                logger.info("Session interrupted by user (Ctrl+C)")
                break
            except Exception as e:
                logger.error(f"Conversation error: {e}")
                print(f"\n❌ Error: {e}")
                print("Let's continue - what's your next question?")
                print()

def main():
    """Main function with comprehensive error handling"""
    try:
        logger.info("Starting SecureMemoryAgent")
        print("🔧 Initializing secure memory agent...")
        
        agent = SecureMemoryAgent()
        
        print("✅ Agent initialized successfully")
        print("🚀 Starting conversation...")
        print()
        
        asyncio.run(agent.start_conversation())
        
    except Exception as e:
        logger.error(f"Failed to start agent: {e}")
        print(f"❌ Failed to start agent: {e}")
        print("Please check your API key and try again.")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
