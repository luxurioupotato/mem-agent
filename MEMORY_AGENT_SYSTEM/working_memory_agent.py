#!/usr/bin/env python3
"""
Working Memory Agent - Command Line Version (Sanitized)
- Functional, lossless of valid instructions
- Uses environment variable GEMINI_API_KEY (no hardcoded secrets)
"""

import os
import json
import asyncio
from datetime import datetime
import google.generativeai as genai


class WorkingMemoryAgent:
    """Working memory agent for immediate business use"""

    def __init__(self) -> None:
        self._configure_gemini_from_env()
        self.conversation_history = []

    def _configure_gemini_from_env(self) -> None:
        """Configure Gemini using the GEMINI_API_KEY environment variable."""
        api_key = os.getenv("GEMINI_API_KEY", "")
        if not api_key:
            # Configure with empty key; upstream library will raise on use
            # This avoids embedding secrets in code while remaining functional
            pass
        genai.configure(api_key=api_key)
        model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-pro")
        self.model = genai.GenerativeModel(model_name)

    def generate_response(self, user_input: str) -> str:
        """Generate business-focused response."""
        try:
            prompt = (
                "You are a business mentor and strategic advisor specializing in agency "
                "growth and revenue optimization. The user wants to build an agency website "
                "and email marketing funnel with maximum ROI and minimal ongoing effort.\n\n"
                f"User input: {user_input}\n\n"
                "Provide strategic, actionable advice focused on:\n"
                "- Maximum ROI strategies\n"
                "- Minimal maintenance solutions\n"
                "- Revenue generation tactics\n"
                "- Automation opportunities\n"
                "- Cost-effective approaches\n\n"
                "Be direct, practical, and business-focused. Provide specific steps and recommendations."
            )
            response = self.model.generate_content(prompt)
            return getattr(response, "text", "") or "(No response text returned)"
        except Exception as e:
            return (
                "I'm ready to help with your business strategy! Let's focus on building your "
                f"agency website and email funnel. What specific aspect would you like to start with? (Note: {e})"
            )

    def save_conversation(self, user_input: str, response: str) -> None:
        """Persist conversation locally in JSON format."""
        conversation = {
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "agent": response,
        }
        self.conversation_history.append(conversation)
        with open("conversation_history.json", "w", encoding="utf-8") as f:
            json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)

    async def start_conversation(self) -> None:
        """Interactive CLI session."""
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

                if user_input.lower() in ["quit", "exit", "bye", "stop"]:
                    print("\n🧠 MENTOR: Great talking with you! Your business strategy")
                    print("is saved and ready for implementation. Let's make money!")
                    break

                print("\n🔍 PROCESSING:")
                print("-" * 20)
                print(f"📝 Analyzing: {user_input[:50]}...")
                print("🧠 Generating strategic response...")

                response = self.generate_response(user_input)
                print(f"✅ Response ready ({len(response)} characters)")
                print()
                print("🧠 MENTOR:")
                print("-" * 10)
                print(response)
                print()

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


def main() -> None:
    agent = WorkingMemoryAgent()
    asyncio.run(agent.start_conversation())


if __name__ == "__main__":
    main()


