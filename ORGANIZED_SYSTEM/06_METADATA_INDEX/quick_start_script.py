#!/usr/bin/env python3
"""
Quick Start Script for Modular AI Memory Agent System
This script automates the initial setup and configuration process.
"""

import os
import sys
import subprocess
import json
import shutil
from pathlib import Path

class MemoryAgentSetup:
    def __init__(self, base_path="E:/MEM_AGENT/MEMORY_AGENT_SYSTEM"):
        self.base_path = Path(base_path)
        self.organized_system_path = Path("E:/MEM_AGENT/ORGANIZED_SYSTEM")
        self.setup_log = []
        
    def log(self, message):
        """Log setup progress"""
        print(f"🔧 {message}")
        self.setup_log.append(message)
        
    def run_command(self, command, description=""):
        """Run a command and log the result"""
        try:
            self.log(f"Running: {command}")
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                self.log(f"✅ Success: {description}")
                return True
            else:
                self.log(f"❌ Error: {description} - {result.stderr}")
                return False
        except Exception as e:
            self.log(f"❌ Exception: {description} - {str(e)}")
            return False
    
    def create_directory_structure(self):
        """Create the main directory structure"""
        self.log("Creating directory structure...")
        
        directories = [
            "agents",
            "memory_bank/episodic",
            "memory_bank/semantic", 
            "memory_bank/working",
            "memory_bank/procedural",
            "memory_bank/templates",
            "memory_bank/schemas",
            "logs/agents",
            "logs/errors",
            "logs/performance",
            "logs/learning",
            "logs/audit",
            "config",
            "data/input",
            "data/output",
            "data/processed",
            "data/external",
            "data/temp",
            "backups",
            "tests/unit",
            "tests/integration",
            "tests/end_to_end"
        ]
        
        for directory in directories:
            dir_path = self.base_path / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            self.log(f"Created directory: {dir_path}")
    
    def copy_template_files(self):
        """Copy foundational template files"""
        self.log("Copying template files...")
        
        template_files = {
            "modular_memory_agent_architecture.json": "config/",
            "implementation_specifications.json": "config/",
            "foundational_schema.json": "memory_bank/schemas/",
            "migration_implementation_plan.json": "config/",
            "setup_evolution_guide.json": "config/",
            "example_workflows.json": "config/"
        }
        
        source_dir = self.organized_system_path / "06_METADATA_INDEX"
        
        for filename, dest_dir in template_files.items():
            source_file = source_dir / filename
            dest_file = self.base_path / dest_dir / filename
            
            if source_file.exists():
                shutil.copy2(source_file, dest_file)
                self.log(f"Copied: {filename} -> {dest_dir}")
            else:
                self.log(f"⚠️  Warning: {filename} not found in source")
    
    def create_agent_templates(self):
        """Create basic agent template files"""
        self.log("Creating agent templates...")
        
        agents = [
            "memory_manager",
            "ingestion_agent", 
            "categorization_agent",
            "search_agent",
            "context_assembly_agent",
            "analytics_agent",
            "reasoning_agent",
            "summarization_agent",
            "error_detection_agent",
            "learning_agent",
            "brain_module"
        ]
        
        for agent in agents:
            agent_file = self.base_path / "agents" / f"{agent}.py"
            
            template_content = f'''#!/usr/bin/env python3
"""
{agent.replace('_', ' ').title()} Agent
Part of the Modular AI Memory Agent System
"""

import asyncio
import logging
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

class {agent.replace('_', '').title()}Agent:
    """{agent.replace('_', ' ').title()} Agent Implementation"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(f"{{__name__}}.{{agent}}")
        self.agent_id = "{agent.upper()}-001"
        self.status = "initialized"
        
    async def initialize(self):
        """Initialize the agent"""
        self.logger.info(f"Initializing {{self.agent_id}}")
        self.status = "running"
        
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data through the agent"""
        self.logger.info(f"Processing data in {{self.agent_id}}")
        # TODO: Implement agent-specific processing logic
        return {{"status": "processed", "agent": self.agent_id}}
        
    async def health_check(self) -> Dict[str, Any]:
        """Check agent health"""
        return {{
            "agent_id": self.agent_id,
            "status": self.status,
            "timestamp": datetime.utcnow().isoformat(),
            "healthy": self.status == "running"
        }}

# Example usage
if __name__ == "__main__":
    agent = {agent.replace('_', '').title()}Agent({{}})
    asyncio.run(agent.initialize())
'''
            
            with open(agent_file, 'w') as f:
                f.write(template_content)
            
            self.log(f"Created agent template: {agent}.py")
    
    def create_config_files(self):
        """Create configuration files"""
        self.log("Creating configuration files...")
        
        # Main configuration
        main_config = {
            "system": {
                "name": "Modular AI Memory Agent System",
                "version": "1.0.0",
                "base_path": str(self.base_path)
            },
            "agents": {
                "memory_manager": {"port": 8001, "enabled": True},
                "ingestion_agent": {"port": 8002, "enabled": True},
                "categorization_agent": {"port": 8003, "enabled": True},
                "search_agent": {"port": 8004, "enabled": True},
                "context_assembly_agent": {"port": 8005, "enabled": True},
                "analytics_agent": {"port": 8006, "enabled": True},
                "reasoning_agent": {"port": 8007, "enabled": True},
                "summarization_agent": {"port": 8008, "enabled": True},
                "error_detection_agent": {"port": 8009, "enabled": True},
                "learning_agent": {"port": 8010, "enabled": True},
                "brain_module": {"port": 8011, "enabled": True}
            },
            "databases": {
                "redis": {"host": "localhost", "port": 6379, "db": 0},
                "neo4j": {"host": "localhost", "port": 7687, "user": "neo4j", "password": "password"},
                "influxdb": {"host": "localhost", "port": 8086, "database": "memory_agent"},
                "postgresql": {"host": "localhost", "port": 5432, "database": "memory_agent", "user": "postgres", "password": "password"}
            },
            "ai_services": {
                "openai": {"api_key": "${OPENAI_API_KEY}", "model": "gpt-4"},
                "anthropic": {"api_key": "${ANTHROPIC_API_KEY}", "model": "claude-3-sonnet"}
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "file": "logs/system.log"
            }
        }
        
        config_file = self.base_path / "config" / "system_config.json"
        with open(config_file, 'w') as f:
            json.dump(main_config, f, indent=2)
        
        self.log(f"Created system configuration: {config_file}")
    
    def create_requirements_file(self):
        """Create requirements.txt file"""
        self.log("Creating requirements.txt...")
        
        requirements = [
            "pandas>=2.0.0",
            "numpy>=1.24.0",
            "scikit-learn>=1.3.0",
            "fastapi>=0.100.0",
            "uvicorn>=0.23.0",
            "pydantic>=2.0.0",
            "redis>=4.6.0",
            "neo4j>=5.12.0",
            "influxdb-client>=1.36.0",
            "psycopg2-binary>=2.9.0",
            "sqlalchemy>=2.0.0",
            "celery>=5.3.0",
            "openai>=1.0.0",
            "anthropic>=0.7.0",
            "transformers>=4.33.0",
            "torch>=2.0.0",
            "elasticsearch>=8.8.0",
            "beautifulsoup4>=4.12.0",
            "requests>=2.31.0",
            "prometheus-client>=0.17.0",
            "mlflow>=2.5.0",
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "docker>=6.1.0",
            "kubernetes>=27.2.0",
            "browser-use>=0.1.0",
            "selenium>=4.15.0",
            "playwright>=1.37.0",
            "scrapy>=2.11.0"
        ]
        
        requirements_file = self.base_path / "requirements.txt"
        with open(requirements_file, 'w') as f:
            f.write('\n'.join(requirements))
        
        self.log(f"Created requirements.txt: {requirements_file}")
    
    def create_docker_compose(self):
        """Create Docker Compose configuration"""
        self.log("Creating Docker Compose configuration...")
        
        docker_compose = {
            "version": "3.8",
            "services": {
                "redis": {
                    "image": "redis:7-alpine",
                    "ports": ["6379:6379"],
                    "volumes": ["redis_data:/data"],
                    "command": "redis-server --appendonly yes"
                },
                "neo4j": {
                    "image": "neo4j:5.12",
                    "ports": ["7474:7474", "7687:7687"],
                    "environment": {
                        "NEO4J_AUTH": "neo4j/password",
                        "NEO4J_PLUGINS": "[\"apoc\"]"
                    },
                    "volumes": ["neo4j_data:/data", "neo4j_logs:/logs"]
                },
                "influxdb": {
                    "image": "influxdb:2.7",
                    "ports": ["8086:8086"],
                    "environment": {
                        "DOCKER_INFLUXDB_INIT_MODE": "setup",
                        "DOCKER_INFLUXDB_INIT_USERNAME": "admin",
                        "DOCKER_INFLUXDB_INIT_PASSWORD": "password",
                        "DOCKER_INFLUXDB_INIT_ORG": "memory_agent",
                        "DOCKER_INFLUXDB_INIT_BUCKET": "memory_agent"
                    },
                    "volumes": ["influxdb_data:/var/lib/influxdb2"]
                },
                "postgresql": {
                    "image": "postgres:15",
                    "ports": ["5432:5432"],
                    "environment": {
                        "POSTGRES_DB": "memory_agent",
                        "POSTGRES_USER": "postgres",
                        "POSTGRES_PASSWORD": "password"
                    },
                    "volumes": ["postgres_data:/var/lib/postgresql/data"]
                },
                "elasticsearch": {
                    "image": "elasticsearch:8.8.0",
                    "ports": ["9200:9200", "9300:9300"],
                    "environment": {
                        "discovery.type": "single-node",
                        "xpack.security.enabled": "false"
                    },
                    "volumes": ["elasticsearch_data:/usr/share/elasticsearch/data"]
                }
            },
            "volumes": {
                "redis_data": {},
                "neo4j_data": {},
                "neo4j_logs": {},
                "influxdb_data": {},
                "postgres_data": {},
                "elasticsearch_data": {}
            }
        }
        
        docker_compose_file = self.base_path / "docker-compose.yml"
        with open(docker_compose_file, 'w') as f:
            json.dump(docker_compose, f, indent=2)
        
        self.log(f"Created Docker Compose: {docker_compose_file}")
    
    def create_startup_script(self):
        """Create startup script"""
        self.log("Creating startup script...")
        
        startup_script = '''#!/usr/bin/env python3
"""
Memory Agent System Startup Script
"""

import asyncio
import logging
import json
from pathlib import Path
import sys

# Add the agents directory to the path
sys.path.append(str(Path(__file__).parent / "agents"))

from memory_manager import MemoryManagerAgent
from brain_module import BrainModuleAgent

async def main():
    """Main startup function"""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Load configuration
    config_path = Path(__file__).parent / "config" / "system_config.json"
    with open(config_path) as f:
        config = json.load(f)
    
    logger.info("Starting Memory Agent System...")
    
    # Initialize core agents
    memory_manager = MemoryManagerAgent(config)
    brain_module = BrainModuleAgent(config)
    
    # Start agents
    await memory_manager.initialize()
    await brain_module.initialize()
    
    logger.info("Memory Agent System started successfully!")
    
    # Keep running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down Memory Agent System...")

if __name__ == "__main__":
    asyncio.run(main())
'''
        
        startup_file = self.base_path / "start_system.py"
        with open(startup_file, 'w') as f:
            f.write(startup_script)
        
        self.log(f"Created startup script: {startup_file}")
    
    def create_readme(self):
        """Create README file"""
        self.log("Creating README...")
        
        readme_content = '''# Modular AI Memory Agent System

A comprehensive, self-updating, and research-optimized memory agent system for business applications.

## Quick Start

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Database Services:**
   ```bash
   docker-compose up -d
   ```

3. **Set Environment Variables:**
   ```bash
   export OPENAI_API_KEY=your_openai_key
   export ANTHROPIC_API_KEY=your_anthropic_key
   ```

4. **Start the System:**
   ```bash
   python start_system.py
   ```

## System Architecture

- **Memory Manager**: Central memory coordination
- **Ingestion Agent**: Data processing and validation
- **Categorization Agent**: Content classification
- **Search Agent**: Semantic and hybrid search
- **Context Assembly Agent**: Multi-source context synthesis
- **Analytics Agent**: Pattern detection and insights
- **Reasoning Agent**: Advanced logical reasoning
- **Summarization Agent**: Content summarization
- **Error Detection Agent**: Monitoring and recovery
- **Learning Agent**: Continuous adaptation
- **Brain Module**: Supervisory orchestration

## Features

- ✅ Modular, self-adapting architecture
- ✅ Multi-tier memory system
- ✅ Advanced error handling and recovery
- ✅ Continuous learning and optimization
- ✅ External research integration
- ✅ AI Studio integration
- ✅ Comprehensive monitoring and logging

## Documentation

See the `config/` directory for detailed configuration files and documentation.

## Support

For issues and questions, refer to the troubleshooting guide in the setup documentation.
'''
        
        readme_file = self.base_path / "README.md"
        with open(readme_file, 'w') as f:
            f.write(readme_content)
        
        self.log(f"Created README: {readme_file}")
    
    def run_setup(self):
        """Run the complete setup process"""
        self.log("🚀 Starting Modular AI Memory Agent System Setup...")
        
        try:
            # Create directory structure
            self.create_directory_structure()
            
            # Copy template files
            self.copy_template_files()
            
            # Create agent templates
            self.create_agent_templates()
            
            # Create configuration files
            self.create_config_files()
            
            # Create requirements file
            self.create_requirements_file()
            
            # Create Docker Compose
            self.create_docker_compose()
            
            # Create startup script
            self.create_startup_script()
            
            # Create README
            self.create_readme()
            
            self.log("🎉 Setup completed successfully!")
            self.log(f"System created at: {self.base_path}")
            self.log("Next steps:")
            self.log("1. Install dependencies: pip install -r requirements.txt")
            self.log("2. Start databases: docker-compose up -d")
            self.log("3. Set environment variables")
            self.log("4. Start system: python start_system.py")
            
        except Exception as e:
            self.log(f"❌ Setup failed: {str(e)}")
            return False
        
        return True

def main():
    """Main function"""
    print("🧠 Modular AI Memory Agent System - Quick Setup")
    print("=" * 50)
    
    setup = MemoryAgentSetup()
    success = setup.run_setup()
    
    if success:
        print("\n✅ Setup completed successfully!")
        print(f"📁 System created at: {setup.base_path}")
        print("\n📋 Next Steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Start databases: docker-compose up -d")
        print("3. Set environment variables for API keys")
        print("4. Start system: python start_system.py")
        print("\n📖 See README.md for detailed instructions")
    else:
        print("\n❌ Setup failed. Check the logs above for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()
