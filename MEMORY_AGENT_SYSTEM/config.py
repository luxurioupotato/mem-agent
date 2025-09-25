#!/usr/bin/env python3
"""
Configuration Management - SSI-Enhanced Memory Agent
Centralized configuration with environment variable loading
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

class Config:
    """Centralized configuration management"""
    
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyDj-aTJt7riqX6MJSsW2Tu7uO8cjisEGqE')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    
    # Database Configuration
    RAG_DATABASE_PATH = os.getenv('RAG_DATABASE_PATH', 'agent_memory.db')
    KNOWLEDGE_BASE_PATH = os.getenv('KNOWLEDGE_BASE_PATH', 'knowledge_base.txt')
    
    # Streamlit Configuration
    STREAMLIT_PORT = int(os.getenv('STREAMLIT_PORT', 8501))
    
    # RAG Configuration
    EMBEDDING_MODEL = "text-embedding-3-small"
    EMBEDDING_DIMENSION = 1536
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    MAX_CONTEXT_LENGTH = 3000
    
    # LLM Configuration
    GEMINI_MODEL = "gemini-1.5-flash"
    MAX_NEW_TOKENS = 500
    TEMPERATURE = 0.7
    
    @classmethod
    def validate_environment(cls):
        """Validate all required environment variables"""
        validation = {}
        
        # Check API keys
        validation['GEMINI_API_KEY'] = bool(cls.GEMINI_API_KEY)
        validation['OPENAI_API_KEY'] = bool(cls.OPENAI_API_KEY)
        
        # Check paths
        validation['RAG_DATABASE_PATH'] = cls.RAG_DATABASE_PATH is not None
        validation['KNOWLEDGE_BASE_PATH'] = cls.KNOWLEDGE_BASE_PATH is not None
        
        return validation
    
    @classmethod
    def get_missing_env_vars(cls):
        """Get list of missing environment variables"""
        validation = cls.validate_environment()
        return [key for key, value in validation.items() if not value]
    
    @classmethod
    def is_valid(cls):
        """Check if configuration is valid"""
        missing = cls.get_missing_env_vars()
        # Only require Gemini API key as essential
        return 'GEMINI_API_KEY' not in missing

# Create default configuration instance
config = Config()
