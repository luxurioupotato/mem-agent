#!/usr/bin/env python3
"""
Quick Launch - One-click startup for Memory Agent
Launch script with automatic setup and verification
"""

import subprocess
import sys
import os
import logging
from pathlib import Path
import time

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class QuickLauncher:
    """One-click startup for Memory Agent"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.required_files = [
            'config.py',
            'rag_system.py',
            'web_scraper.py',
            'integrated_main.py',
            'requirements_rag.txt'
        ]
    
    def check_project_structure(self):
        """Check if all required files exist."""
        logger.info("🔍 Checking project structure...")
        
        missing_files = []
        for file_name in self.required_files:
            file_path = self.project_root / file_name
            if not file_path.exists():
                missing_files.append(file_name)
        
        if missing_files:
            logger.error(f"❌ Missing required files: {missing_files}")
            return False
        
        logger.info("✅ All required files present")
        return True
    
    def check_environment_setup(self):
        """Check if environment is properly set up."""
        logger.info("🔧 Checking environment setup...")
        
        # Check for .env file
        env_file = self.project_root / '.env'
        env_template = self.project_root / 'env_template.txt'
        
        if not env_file.exists():
            if env_template.exists():
                logger.info("📝 Creating .env file from template...")
                try:
                    # Copy template to .env
                    with open(env_template, 'r') as template:
                        content = template.read()
                    
                    with open(env_file, 'w') as env:
                        env.write(content)
                    
                    logger.info("✅ .env file created")
                except Exception as e:
                    logger.error(f"❌ Failed to create .env file: {e}")
                    return False
            else:
                logger.warning("⚠️ No .env file or template found")
        
        return True
    
    def check_dependencies(self):
        """Check if dependencies are installed."""
        logger.info("📦 Checking dependencies...")
        
        required_modules = [
            'streamlit',
            'google.generativeai',
            'requests',
            'bs4',
            'langchain'
        ]
        
        missing_modules = []
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                missing_modules.append(module)
        
        if missing_modules:
            logger.info(f"Installing missing modules: {missing_modules}")
            return self.install_dependencies()
        
        logger.info("✅ All dependencies available")
        return True
    
    def install_dependencies(self):
        """Install dependencies from requirements file."""
        try:
            logger.info("📦 Installing dependencies...")
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', '-r', 'requirements_rag.txt'
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            logger.info("✅ Dependencies installed")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to install dependencies: {e}")
            return False
    
    def initialize_system(self):
        """Initialize the system if needed."""
        logger.info("🚀 Initializing system...")
        
        try:
            # Check if setup is needed
            db_file = self.project_root / 'agent_memory.db'
            
            if not db_file.exists():
                logger.info("🔧 Running initial setup...")
                
                # Import and run setup
                sys.path.insert(0, str(self.project_root))
                from setup_rag import RAGSetup
                
                setup = RAGSetup()
                if not setup.run_setup():
                    logger.error("❌ Setup failed")
                    return False
            
            logger.info("✅ System initialized")
            return True
            
        except Exception as e:
            logger.error(f"❌ System initialization failed: {e}")
            return False
    
    def launch_application(self):
        """Launch the Streamlit application."""
        logger.info("🚀 Launching Memory Agent...")
        
        try:
            # Change to project directory
            os.chdir(self.project_root)
            
            # Launch Streamlit
            cmd = [
                sys.executable, '-m', 'streamlit', 'run', 
                'integrated_main.py',
                '--server.address', 'localhost',
                '--server.port', '8501',
                '--server.headless', 'false'
            ]
            
            logger.info("🌐 Opening Memory Agent at http://localhost:8501")
            logger.info("Press Ctrl+C to stop the application")
            
            # Run Streamlit
            subprocess.run(cmd)
            
        except KeyboardInterrupt:
            logger.info("\n👋 Memory Agent stopped by user")
        except Exception as e:
            logger.error(f"❌ Error launching application: {e}")
    
    def run(self):
        """Run the complete launch sequence."""
        logger.info("🧠 Memory Agent - Quick Launch")
        logger.info("=" * 40)
        
        # Step 1: Check project structure
        if not self.check_project_structure():
            logger.error("❌ Project structure check failed")
            return False
        
        # Step 2: Check environment setup
        if not self.check_environment_setup():
            logger.error("❌ Environment setup failed")
            return False
        
        # Step 3: Check dependencies
        if not self.check_dependencies():
            logger.error("❌ Dependency check failed")
            return False
        
        # Step 4: Initialize system
        if not self.initialize_system():
            logger.error("❌ System initialization failed")
            return False
        
        # Step 5: Launch application
        self.launch_application()
        
        return True

def main():
    """Main launch function."""
    launcher = QuickLauncher()
    
    try:
        success = launcher.run()
        if not success:
            logger.error("❌ Launch failed")
            input("Press Enter to exit...")
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("\n🛑 Launch interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
