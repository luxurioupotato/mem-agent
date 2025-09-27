#!/usr/bin/env python3
"""
MEM_AGENT Mentor Agent
LLM Mentor agent with GCP authentication, Supabase integration, and Secret Manager
"""

import os
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime
from google.cloud import secretmanager
from google import genai
from google.genai.types import HttpOptions, Tool, ToolCodeExecution, GenerateContentConfig
from supabase import create_client, Client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MEMAgentMentor:
    """MEM_AGENT Mentor Agent with GCP integration"""
    
    def __init__(self):
        """Initialize mentor agent with GCP authentication"""
        self.project_id = os.environ.get("GCP_PROJECT_ID")
        self.supabase_url = None
        self.supabase_key = None
        self.genai_client = None
        self.supabase_client = None
        self._authenticate_gcp()
        self._initialize_supabase()
        self._initialize_genai()
    
    def _authenticate_gcp(self):
        """Authenticate with GCP using service account from Secret Manager"""
        try:
            # Fetch service account key from Secret Manager
            sa_key = self._fetch_secret("GCP_SA_KEY")
            sa_info = json.loads(sa_key)
            
            # Set up authentication
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/tmp/gcp_sa_key.json"
            with open("/tmp/gcp_sa_key.json", "w") as f:
                json.dump(sa_info, f)
            
            logger.info("✅ GCP authentication successful")
        except Exception as e:
            logger.error(f"❌ GCP authentication failed: {e}")
            raise
    
    def _fetch_secret(self, secret_name: str) -> str:
        """Fetch secret from Google Secret Manager"""
        try:
            client = secretmanager.SecretManagerServiceClient()
            resource = f"projects/{self.project_id}/secrets/{secret_name}/versions/latest"
            return client.access_secret_version(name=resource).payload.data.decode("UTF-8")
        except Exception as e:
            logger.error(f"❌ Failed to fetch secret {secret_name}: {e}")
            raise
    
    def _initialize_supabase(self):
        """Initialize Supabase client"""
        try:
            self.supabase_url = self._fetch_secret("SUPABASE_URL")
            self.supabase_key = self._fetch_secret("SUPABASE_KEY")
            self.supabase_client = create_client(self.supabase_url, self.supabase_key)
            logger.info("✅ Supabase client initialized")
        except Exception as e:
            logger.error(f"❌ Supabase initialization failed: {e}")
            raise
    
    def _initialize_genai(self):
        """Initialize Gemini AI client"""
        try:
            # Configure Gemini with service account authentication
            self.genai_client = genai.Client(
                http_options=HttpOptions(api_version="v1")
            )
            logger.info("✅ Gemini AI client initialized")
        except Exception as e:
            logger.error(f"❌ Gemini AI initialization failed: {e}")
            raise
    
    def mentor_respond(self, prompt: str, user_id: Optional[str] = None) -> str:
        """
        Generate mentor response using Gemini AI and store in Supabase
        
        Args:
            prompt: User's question or request
            user_id: Optional user identifier for conversation tracking
            
        Returns:
            AI mentor response
        """
        try:
            # Configure Gemini with code execution capabilities
            code_execution_tool = Tool(code_execution=ToolCodeExecution())
            
            # Generate response using Gemini 1.5 Pro
            response = self.genai_client.models.generate_content(
                model="gemini-1.5-pro",
                contents=prompt,
                config=GenerateContentConfig(
                    tools=[code_execution_tool],
                    temperature=0.7,
                    max_output_tokens=2048
                )
            )
            
            answer = response.text
            
            # Store conversation in Supabase
            self._store_conversation(prompt, answer, user_id)
            
            logger.info("✅ Mentor response generated and stored")
            return answer
            
        except Exception as e:
            logger.error(f"❌ Mentor response generation failed: {e}")
            return "I apologize, but I'm experiencing technical difficulties. Please try again."
    
    def _store_conversation(self, prompt: str, response: str, user_id: Optional[str] = None):
        """Store conversation in Supabase"""
        try:
            conversation_data = {
                "prompt": prompt,
                "response": response,
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "created_at": datetime.now().isoformat()
            }
            
            self.supabase_client.table("mentor_memory").insert(conversation_data).execute()
            logger.info("✅ Conversation stored in Supabase")
            
        except Exception as e:
            logger.error(f"❌ Failed to store conversation: {e}")
    
    def get_conversation_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Retrieve conversation history for a user"""
        try:
            result = self.supabase_client.table("mentor_memory")\
                .select("*")\
                .eq("user_id", user_id)\
                .order("created_at", desc=True)\
                .limit(limit)\
                .execute()
            
            return result.data if result.data else []
            
        except Exception as e:
            logger.error(f"❌ Failed to retrieve conversation history: {e}")
            return []
    
    def analyze_business_metrics(self, metrics_data: Dict) -> str:
        """Analyze business metrics and provide strategic insights"""
        try:
            analysis_prompt = f"""
            Analyze the following business metrics and provide strategic insights:
            
            Metrics Data: {json.dumps(metrics_data, indent=2)}
            
            Please provide:
            1. Key performance indicators analysis
            2. Trends and patterns identification
            3. Strategic recommendations
            4. Revenue optimization opportunities
            5. Risk assessment and mitigation strategies
            
            Focus on actionable insights for achieving $10K-$20K monthly revenue target.
            """
            
            return self.mentor_respond(analysis_prompt)
            
        except Exception as e:
            logger.error(f"❌ Business metrics analysis failed: {e}")
            return "Unable to analyze business metrics at this time."

def main():
    """Main function for testing mentor agent"""
    mentor = MEMAgentMentor()
    
    print("MEM_AGENT Mentor Agent - Ready for consultation")
    print("Type 'exit' to quit")
    
    while True:
        user_input = input("\nAsk your mentor agent a question: ")
        if user_input.lower() == 'exit':
            break
        
        response = mentor.mentor_respond(user_input)
        print(f"\nMentor: {response}")

if __name__ == "__main__":
    main()
