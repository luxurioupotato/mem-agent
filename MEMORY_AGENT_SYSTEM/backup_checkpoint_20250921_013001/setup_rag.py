#!/usr/bin/env python3
"""
Setup RAG - Automated Setup Script
One-click setup script with dependency checking and system initialization
"""

import subprocess
import sys
import os
import logging
from pathlib import Path
import importlib.util

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RAGSetup:
    """Automated RAG system setup"""
    
    def __init__(self):
        self.required_packages = [
            'streamlit>=1.28.0',
            'sqlite-vec>=0.1.6',
            'openai>=1.3.0',
            'google-generativeai>=0.3.0',
            'langchain>=0.1.0',
            'langchain-text-splitters>=0.0.1',
            'beautifulsoup4>=4.12.0',
            'requests>=2.31.0',
            'python-dotenv>=1.0.0',
            'streamlit-feedback>=0.1.0',
            'pandas>=2.0.0',
            'numpy>=1.24.0'
        ]
        
        self.required_modules = [
            'streamlit',
            'sqlite_vec',
            'openai',
            'google.generativeai',
            'langchain',
            'bs4',
            'requests',
            'dotenv',
            'pandas',
            'numpy'
        ]
    
    def check_python_version(self):
        """Check if Python version is compatible."""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            logger.error("❌ Python 3.8+ is required")
            return False
        
        logger.info(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    
    def check_dependencies(self):
        """Check if all required dependencies are installed."""
        missing_packages = []
        
        logger.info("🔍 Checking dependencies...")
        
        for module_name in self.required_modules:
            try:
                if '.' in module_name:
                    # Handle nested imports like google.generativeai
                    main_module = module_name.split('.')[0]
                    importlib.import_module(main_module)
                else:
                    importlib.import_module(module_name)
                logger.info(f"  ✅ {module_name}")
            except ImportError:
                logger.warning(f"  ❌ {module_name} not found")
                missing_packages.append(module_name)
        
        return missing_packages
    
    def install_dependencies(self):
        """Install required dependencies."""
        logger.info("📦 Installing dependencies...")
        
        try:
            # Install from requirements file
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', '-r', 'requirements_rag.txt'
            ])
            logger.info("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to install dependencies: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected error during installation: {e}")
            return False
    
    def create_env_template(self):
        """Create .env template file."""
        env_template_content = """# API Keys for Memory Agent
OPENAI_API_KEY=your_openai_key_here
GEMINI_API_KEY=AIzaSyDj-aTJt7riqX6MJSsW2Tu7uO8cjisEGqE
ANTHROPIC_API_KEY=your_anthropic_key_here

# Database Configuration
RAG_DATABASE_PATH=agent_memory.db
KNOWLEDGE_BASE_PATH=knowledge_base.txt

# Streamlit Configuration
STREAMLIT_PORT=8501
"""
        
        env_template_path = Path('.env.template')
        
        try:
            with open(env_template_path, 'w') as f:
                f.write(env_template_content)
            logger.info("✅ Created .env.template file")
            
            # Create actual .env file if it doesn't exist
            env_path = Path('.env')
            if not env_path.exists():
                with open(env_path, 'w') as f:
                    f.write(env_template_content)
                logger.info("✅ Created .env file")
            
            return True
        except Exception as e:
            logger.error(f"❌ Failed to create environment files: {e}")
            return False
    
    def initialize_rag_database(self):
        """Initialize the RAG database."""
        logger.info("🗄️ Initializing RAG database...")
        
        try:
            from rag_system import LocalRAGSystem
            
            rag = LocalRAGSystem()
            if rag.initialize_database():
                logger.info("✅ RAG database initialized")
                return True
            else:
                logger.error("❌ Failed to initialize RAG database")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error initializing RAG database: {e}")
            return False
    
    def setup_sample_knowledge_base(self):
        """Set up sample knowledge base."""
        logger.info("📚 Setting up sample knowledge base...")
        
        knowledge_file = Path("ai_knowledge_base.txt")
        
        if knowledge_file.exists():
            logger.info("✅ Knowledge base already exists")
            return True
        
        try:
            from web_scraper import WebScraper
            
            # Sample URLs for AI knowledge
            urls = [
                "https://en.wikipedia.org/wiki/Artificial_intelligence",
                "https://en.wikipedia.org/wiki/Machine_learning",
                "https://en.wikipedia.org/wiki/Natural_language_processing"
            ]
            
            scraper = WebScraper()
            knowledge_file_path = scraper.scrape_multiple_sources(urls, "ai_knowledge_base")
            
            if Path(knowledge_file_path).exists():
                logger.info(f"✅ Sample knowledge base created: {knowledge_file_path}")
                
                # Add to RAG system
                from rag_system import setup_rag_system
                rag = setup_rag_system(knowledge_file_path)
                
                if rag:
                    stats = rag.get_database_stats()
                    logger.info(f"✅ Added {stats.get('total_documents', 0)} documents to RAG system")
                
                return True
            else:
                logger.warning("⚠️ Knowledge base creation failed, but continuing...")
                return True
                
        except Exception as e:
            logger.error(f"❌ Error setting up knowledge base: {e}")
            return True  # Continue even if this fails
    
    def verify_api_connections(self):
        """Verify API connections."""
        logger.info("🔌 Verifying API connections...")
        
        from config import config
        
        # Check Gemini API
        if config.GEMINI_API_KEY:
            try:
                import google.generativeai as genai
                genai.configure(api_key=config.GEMINI_API_KEY)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Test with a simple prompt
                response = model.generate_content("Say 'API test successful'")
                if response.text:
                    logger.info("✅ Gemini API connection verified")
                else:
                    logger.warning("⚠️ Gemini API response empty")
            except Exception as e:
                logger.warning(f"⚠️ Gemini API verification failed: {e}")
        else:
            logger.warning("⚠️ Gemini API key not set")
        
        # Check OpenAI API
        if config.OPENAI_API_KEY:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=config.OPENAI_API_KEY)
                
                # Test embeddings
                response = client.embeddings.create(
                    model="text-embedding-3-small",
                    input="test"
                )
                if response.data:
                    logger.info("✅ OpenAI API connection verified")
                else:
                    logger.warning("⚠️ OpenAI API response empty")
            except Exception as e:
                logger.warning(f"⚠️ OpenAI API verification failed: {e}")
        else:
            logger.warning("⚠️ OpenAI API key not set (embeddings will not work)")
        
        return True
    
    def run_setup(self):
        """Run complete setup process."""
        logger.info("🚀 Starting RAG System Setup")
        logger.info("=" * 50)
        
        # Step 1: Check Python version
        if not self.check_python_version():
            return False
        
        # Step 2: Check and install dependencies
        missing = self.check_dependencies()
        if missing:
            logger.info(f"Missing packages: {missing}")
            if not self.install_dependencies():
                return False
            
            # Recheck after installation
            missing_after = self.check_dependencies()
            if missing_after:
                logger.error(f"Still missing packages after installation: {missing_after}")
                return False
        
        # Step 3: Create environment files
        if not self.create_env_template():
            return False
        
        # Step 4: Initialize RAG database
        if not self.initialize_rag_database():
            return False
        
        # Step 5: Setup sample knowledge base
        if not self.setup_sample_knowledge_base():
            logger.warning("⚠️ Knowledge base setup failed, but continuing...")
        
        # Step 6: Verify API connections
        if not self.verify_api_connections():
            logger.warning("⚠️ API verification had issues, but continuing...")
        
        logger.info("🎉 RAG System Setup Complete!")
        logger.info("=" * 50)
        logger.info("Next steps:")
        logger.info("1. Edit .env file with your API keys")
        logger.info("2. Run: streamlit run integrated_main.py")
        logger.info("3. Access your Memory Agent at http://localhost:8501")
        
        return True

def main():
    """Main setup function."""
    setup = RAGSetup()
    
    try:
        success = setup.run_setup()
        if success:
            print("\n✅ Setup completed successfully!")
            print("Run 'streamlit run integrated_main.py' to start the application.")
        else:
            print("\n❌ Setup failed. Please check the logs above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
