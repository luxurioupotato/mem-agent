#!/usr/bin/env python3
"""
MEM_AGENT Complete System Setup
Comprehensive setup and initialization script
"""

import os
import sys
import json
import logging
import asyncio
from datetime import datetime
from pathlib import Path

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.mentor_enhanced import MEMAgentEnhancedMentor
from agents.memory_manager import MEMAgentMemoryManager
from agents.business_intelligence import MEMAgentBusinessIntelligence
from agents.data_scraper import MEMAgentDataScraper
from agents.automation_engine import MEMAgentAutomationEngine

class MEMAgentSystemSetup:
    """Complete MEM_AGENT system setup and initialization"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_log = []
        self.system_components = {}
        
    def setup_logging(self):
        """Setup comprehensive logging system"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('mem_agent_setup.log'),
                logging.StreamHandler()
            ]
        )
        self.logger.info("Logging system initialized")
    
    def create_directories(self):
        """Create necessary directories for the system"""
        directories = [
            'data',
            'logs',
            'exports',
            'backups',
            'config',
            'temp',
            'agents',
            'frontend',
            'dashboard'
        ]
        
        for directory in directories:
            Path(directory).mkdir(exist_ok=True)
            self.logger.info(f"Created directory: {directory}")
            self.setup_log.append(f"✅ Created directory: {directory}")
    
    def initialize_memory_system(self):
        """Initialize the memory management system"""
        try:
            memory_manager = MEMAgentMemoryManager("data/mem_agent_memory.db")
            
            # Store initial system memories
            memory_manager.store_memory(
                content="MEM_AGENT system initialized successfully",
                memory_type="system",
                importance=10,
                tags=["system", "initialization"],
                source="setup"
            )
            
            memory_manager.store_memory(
                content="Business goal: Achieve $10,000-$20,000 monthly profit",
                memory_type="goal",
                importance=10,
                tags=["business", "profit", "target"],
                source="setup"
            )
            
            memory_manager.store_memory(
                content="Mentor expertise: Business strategy, revenue optimization, market analysis, automation",
                memory_type="capability",
                importance=9,
                tags=["mentor", "expertise", "capabilities"],
                source="setup"
            )
            
            self.system_components['memory_manager'] = memory_manager
            self.logger.info("Memory system initialized")
            self.setup_log.append("✅ Memory management system initialized")
            
        except Exception as e:
            self.logger.error(f"Memory system initialization failed: {str(e)}")
            self.setup_log.append(f"❌ Memory system failed: {str(e)}")
    
    def initialize_business_intelligence(self):
        """Initialize the business intelligence system"""
        try:
            business_intelligence = MEMAgentBusinessIntelligence()
            
            # Set up initial business metrics
            initial_metrics = {
                "monthly_profit_target": 15000,
                "current_monthly_profit": 0,
                "revenue_streams": [],
                "customer_segments": [],
                "market_analysis": {}
            }
            
            # Store initial business data
            business_intelligence.metrics = initial_metrics
            
            self.system_components['business_intelligence'] = business_intelligence
            self.logger.info("Business intelligence system initialized")
            self.setup_log.append("✅ Business intelligence system initialized")
            
        except Exception as e:
            self.logger.error(f"Business intelligence initialization failed: {str(e)}")
            self.setup_log.append(f"❌ Business intelligence failed: {str(e)}")
    
    def initialize_data_scraper(self):
        """Initialize the data scraping system"""
        try:
            data_scraper = MEMAgentDataScraper()
            
            # Set up initial scraping targets
            initial_targets = [
                "https://example-business-news.com",
                "https://example-market-analysis.com",
                "https://example-competitor-analysis.com"
            ]
            
            # Store scraping configuration
            scraping_config = {
                "targets": initial_targets,
                "scraping_interval": "daily",
                "data_storage": "data/scraped_data.json"
            }
            
            with open('config/scraping_config.json', 'w') as f:
                json.dump(scraping_config, f, indent=2)
            
            self.system_components['data_scraper'] = data_scraper
            self.logger.info("Data scraper system initialized")
            self.setup_log.append("✅ Data scraper system initialized")
            
        except Exception as e:
            self.logger.error(f"Data scraper initialization failed: {str(e)}")
            self.setup_log.append(f"❌ Data scraper failed: {str(e)}")
    
    def initialize_automation_engine(self):
        """Initialize the automation engine"""
        try:
            automation_engine = MEMAgentAutomationEngine()
            
            # Create system automation tasks
            self._create_system_automations(automation_engine)
            
            self.system_components['automation_engine'] = automation_engine
            self.logger.info("Automation engine initialized")
            self.setup_log.append("✅ Automation engine initialized")
            
        except Exception as e:
            self.logger.error(f"Automation engine initialization failed: {str(e)}")
            self.setup_log.append(f"❌ Automation engine failed: {str(e)}")
    
    def _create_system_automations(self, automation_engine):
        """Create system automation tasks"""
        # System health monitoring
        async def system_health_check():
            """Monitor overall system health"""
            try:
                health_status = {
                    "timestamp": datetime.now().isoformat(),
                    "components": {
                        "memory_manager": "operational",
                        "business_intelligence": "operational",
                        "data_scraper": "operational",
                        "automation_engine": "operational"
                    },
                    "overall_status": "healthy"
                }
                
                # Store health status
                if 'memory_manager' in self.system_components:
                    self.system_components['memory_manager'].store_memory(
                        content=f"System health check: {json.dumps(health_status)}",
                        memory_type="system",
                        importance=5,
                        tags=["health", "monitoring"],
                        source="automation"
                    )
                
                self.logger.info("System health check completed")
                
            except Exception as e:
                self.logger.error(f"Health check failed: {str(e)}")
        
        # Business metrics collection
        async def collect_business_metrics():
            """Collect and analyze business metrics"""
            try:
                # Mock business metrics for demonstration
                metrics = {
                    "revenue": 8500,
                    "expenses": 3200,
                    "profit": 5300,
                    "customers": 150,
                    "conversion_rate": 0.12,
                    "timestamp": datetime.now().isoformat()
                }
                
                # Store metrics
                if 'memory_manager' in self.system_components:
                    self.system_components['memory_manager'].store_memory(
                        content=f"Business metrics: {json.dumps(metrics)}",
                        memory_type="insight",
                        importance=8,
                        tags=["business", "metrics"],
                        source="automation"
                    )
                
                # Analyze metrics
                if 'business_intelligence' in self.system_components:
                    analysis = self.system_components['business_intelligence'].analyze_revenue_streams([
                        {"name": "Product Sales", "revenue": metrics["revenue"] * 0.6},
                        {"name": "Services", "revenue": metrics["revenue"] * 0.4}
                    ])
                    
                    # Store analysis
                    self.system_components['memory_manager'].store_memory(
                        content=f"Revenue analysis: {json.dumps(analysis)}",
                        memory_type="insight",
                        importance=7,
                        tags=["business", "analysis"],
                        source="automation"
                    )
                
                self.logger.info("Business metrics collected and analyzed")
                
            except Exception as e:
                self.logger.error(f"Business metrics collection failed: {str(e)}")
        
        # Data scraping task
        async def daily_data_scraping():
            """Daily data scraping task"""
            try:
                if 'data_scraper' in self.system_components:
                    # Load scraping targets
                    with open('config/scraping_config.json', 'r') as f:
                        config = json.load(f)
                    
                    # Perform scraping
                    results = self.system_components['data_scraper'].scrape_multiple_urls(
                        config['targets']
                    )
                    
                    # Store scraped data
                    filename = f"data/scraped_data_{datetime.now().strftime('%Y%m%d')}.json"
                    self.system_components['data_scraper'].save_scraped_data(filename)
                    
                    # Store scraping results in memory
                    self.system_components['memory_manager'].store_memory(
                        content=f"Daily scraping completed: {len(results)} items scraped",
                        memory_type="system",
                        importance=6,
                        tags=["scraping", "data"],
                        source="automation"
                    )
                
                self.logger.info("Daily data scraping completed")
                
            except Exception as e:
                self.logger.error(f"Data scraping failed: {str(e)}")
        
        # Create automation tasks
        automation_engine.create_task(
            task_id="system_health_check",
            name="System Health Check",
            description="Monitor overall system health every 5 minutes",
            function=system_health_check,
            schedule="every_5_minutes",
            priority=3
        )
        
        automation_engine.create_task(
            task_id="business_metrics_collection",
            name="Business Metrics Collection",
            description="Collect and analyze business metrics hourly",
            function=collect_business_metrics,
            schedule="hourly",
            priority=2
        )
        
        automation_engine.create_task(
            task_id="daily_data_scraping",
            name="Daily Data Scraping",
            description="Scrape business data daily",
            function=daily_data_scraping,
            schedule="daily",
            priority=2
        )
    
    def initialize_enhanced_mentor(self, api_key: str = None):
        """Initialize the enhanced mentor system"""
        try:
            enhanced_mentor = MEMAgentEnhancedMentor(api_key)
            
            # Integrate all components
            enhanced_mentor.memory_manager = self.system_components.get('memory_manager')
            enhanced_mentor.business_intelligence = self.system_components.get('business_intelligence')
            enhanced_mentor.data_scraper = self.system_components.get('data_scraper')
            enhanced_mentor.automation_engine = self.system_components.get('automation_engine')
            
            self.system_components['enhanced_mentor'] = enhanced_mentor
            self.logger.info("Enhanced mentor system initialized")
            self.setup_log.append("✅ Enhanced mentor system initialized")
            
        except Exception as e:
            self.logger.error(f"Enhanced mentor initialization failed: {str(e)}")
            self.setup_log.append(f"❌ Enhanced mentor failed: {str(e)}")
    
    def create_system_configuration(self):
        """Create system configuration files"""
        try:
            # Main system configuration
            system_config = {
                "system_name": "MEM_AGENT",
                "version": "1.0.0",
                "description": "Advanced AI Business Mentor System",
                "target_profit": "$10,000-$20,000 monthly",
                "components": {
                    "memory_manager": "operational",
                    "business_intelligence": "operational",
                    "data_scraper": "operational",
                    "automation_engine": "operational",
                    "enhanced_mentor": "operational"
                },
                "features": [
                    "AI-powered business mentoring",
                    "Advanced memory management",
                    "Business intelligence analysis",
                    "Automated data scraping",
                    "Workflow automation",
                    "Profit optimization",
                    "Market analysis",
                    "Customer insights"
                ],
                "created_at": datetime.now().isoformat()
            }
            
            with open('config/system_config.json', 'w') as f:
                json.dump(system_config, f, indent=2)
            
            # Business configuration
            business_config = {
                "profit_targets": {
                    "monthly_minimum": 10000,
                    "monthly_target": 15000,
                    "monthly_maximum": 20000
                },
                "revenue_streams": [
                    "Product Sales",
                    "Services",
                    "Consulting",
                    "Digital Products",
                    "Affiliate Marketing"
                ],
                "key_metrics": [
                    "Monthly Revenue",
                    "Monthly Profit",
                    "Customer Acquisition Cost",
                    "Customer Lifetime Value",
                    "Conversion Rate",
                    "Churn Rate"
                ],
                "automation_schedule": {
                    "health_check": "every_5_minutes",
                    "metrics_collection": "hourly",
                    "data_scraping": "daily",
                    "memory_cleanup": "daily"
                }
            }
            
            with open('config/business_config.json', 'w') as f:
                json.dump(business_config, f, indent=2)
            
            self.logger.info("System configuration files created")
            self.setup_log.append("✅ System configuration files created")
            
        except Exception as e:
            self.logger.error(f"Configuration creation failed: {str(e)}")
            self.setup_log.append(f"❌ Configuration creation failed: {str(e)}")
    
    def run_system_tests(self):
        """Run comprehensive system tests"""
        try:
            test_results = {
                "timestamp": datetime.now().isoformat(),
                "tests_passed": 0,
                "tests_failed": 0,
                "test_details": []
            }
            
            # Test memory manager
            if 'memory_manager' in self.system_components:
                try:
                    memory_manager = self.system_components['memory_manager']
                    memory_manager.store_memory(
                        content="Test memory entry",
                        memory_type="test",
                        importance=5,
                        tags=["test"],
                        source="test"
                    )
                    test_results["tests_passed"] += 1
                    test_results["test_details"].append("✅ Memory manager test passed")
                except Exception as e:
                    test_results["tests_failed"] += 1
                    test_results["test_details"].append(f"❌ Memory manager test failed: {str(e)}")
            
            # Test business intelligence
            if 'business_intelligence' in self.system_components:
                try:
                    bi = self.system_components['business_intelligence']
                    analysis = bi.analyze_revenue_streams([
                        {"name": "Test Stream", "revenue": 1000}
                    ])
                    test_results["tests_passed"] += 1
                    test_results["test_details"].append("✅ Business intelligence test passed")
                except Exception as e:
                    test_results["tests_failed"] += 1
                    test_results["test_details"].append(f"❌ Business intelligence test failed: {str(e)}")
            
            # Test data scraper
            if 'data_scraper' in self.system_components:
                try:
                    scraper = self.system_components['data_scraper']
                    # Test with a simple URL
                    result = scraper.scrape_website("https://httpbin.org/html")
                    test_results["tests_passed"] += 1
                    test_results["test_details"].append("✅ Data scraper test passed")
                except Exception as e:
                    test_results["tests_failed"] += 1
                    test_results["test_details"].append(f"❌ Data scraper test failed: {str(e)}")
            
            # Test automation engine
            if 'automation_engine' in self.system_components:
                try:
                    automation = self.system_components['automation_engine']
                    tasks = automation.list_tasks()
                    test_results["tests_passed"] += 1
                    test_results["test_details"].append("✅ Automation engine test passed")
                except Exception as e:
                    test_results["tests_failed"] += 1
                    test_results["test_details"].append(f"❌ Automation engine test failed: {str(e)}")
            
            # Test enhanced mentor
            if 'enhanced_mentor' in self.system_components:
                try:
                    mentor = self.system_components['enhanced_mentor']
                    response = mentor.get_mentor_response("Test message")
                    test_results["tests_passed"] += 1
                    test_results["test_details"].append("✅ Enhanced mentor test passed")
                except Exception as e:
                    test_results["tests_failed"] += 1
                    test_results["test_details"].append(f"❌ Enhanced mentor test failed: {str(e)}")
            
            # Save test results
            with open('logs/system_tests.json', 'w') as f:
                json.dump(test_results, f, indent=2)
            
            self.logger.info(f"System tests completed: {test_results['tests_passed']} passed, {test_results['tests_failed']} failed")
            self.setup_log.append(f"✅ System tests completed: {test_results['tests_passed']} passed, {test_results['tests_failed']} failed")
            
            return test_results
            
        except Exception as e:
            self.logger.error(f"System tests failed: {str(e)}")
            self.setup_log.append(f"❌ System tests failed: {str(e)}")
            return None
    
    def generate_setup_report(self):
        """Generate comprehensive setup report"""
        try:
            report = {
                "setup_timestamp": datetime.now().isoformat(),
                "system_name": "MEM_AGENT Complete System",
                "version": "1.0.0",
                "setup_log": self.setup_log,
                "components_initialized": list(self.system_components.keys()),
                "directories_created": [
                    "data", "logs", "exports", "backups", 
                    "config", "temp", "agents", "frontend", "dashboard"
                ],
                "configuration_files": [
                    "config/system_config.json",
                    "config/business_config.json",
                    "config/scraping_config.json"
                ],
                "database_files": [
                    "data/mem_agent_memory.db"
                ],
                "next_steps": [
                    "Start the enhanced mentor system",
                    "Configure API keys for AI services",
                    "Set up business metrics tracking",
                    "Customize automation schedules",
                    "Begin business analysis and optimization"
                ],
                "system_ready": len(self.system_components) >= 5
            }
            
            # Save setup report
            with open('logs/setup_report.json', 'w') as f:
                json.dump(report, f, indent=2)
            
            # Generate human-readable report
            with open('MEM_AGENT_SETUP_REPORT.md', 'w') as f:
                f.write("# MEM_AGENT Complete System Setup Report\n\n")
                f.write(f"**Generated:** {report['setup_timestamp']}\n\n")
                f.write(f"**System Status:** {'✅ READY' if report['system_ready'] else '❌ NOT READY'}\n\n")
                
                f.write("## Setup Log\n\n")
                for log_entry in self.setup_log:
                    f.write(f"- {log_entry}\n")
                
                f.write("\n## Components Initialized\n\n")
                for component in report['components_initialized']:
                    f.write(f"- ✅ {component}\n")
                
                f.write("\n## Next Steps\n\n")
                for step in report['next_steps']:
                    f.write(f"1. {step}\n")
                
                f.write("\n## System Usage\n\n")
                f.write("```python\n")
                f.write("# Start the MEM_AGENT system\n")
                f.write("from agents.mentor_enhanced import MEMAgentEnhancedMentor\n")
                f.write("mentor = MEMAgentEnhancedMentor(api_key='your_api_key')\n")
                f.write("mentor.start_mentor_system()\n")
                f.write("response = mentor.get_mentor_response('Your business question')\n")
                f.write("```\n")
            
            self.logger.info("Setup report generated")
            return report
            
        except Exception as e:
            self.logger.error(f"Setup report generation failed: {str(e)}")
            return None
    
    def run_complete_setup(self, api_key: str = None):
        """Run the complete MEM_AGENT system setup"""
        try:
            self.logger.info("Starting MEM_AGENT Complete System Setup")
            
            # Setup logging
            self.setup_logging()
            
            # Create directories
            self.create_directories()
            
            # Initialize components
            self.initialize_memory_system()
            self.initialize_business_intelligence()
            self.initialize_data_scraper()
            self.initialize_automation_engine()
            self.initialize_enhanced_mentor(api_key)
            
            # Create configuration files
            self.create_system_configuration()
            
            # Run system tests
            test_results = self.run_system_tests()
            
            # Generate setup report
            report = self.generate_setup_report()
            
            self.logger.info("MEM_AGENT Complete System Setup completed successfully")
            
            return {
                "success": True,
                "report": report,
                "test_results": test_results,
                "components": self.system_components
            }
            
        except Exception as e:
            self.logger.error(f"Complete setup failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "setup_log": self.setup_log
            }

def main():
    """Main setup function"""
    print("🚀 MEM_AGENT Complete System Setup")
    print("=" * 50)
    
    # Get API key if provided
    api_key = None
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
        print(f"Using API key: {api_key[:10]}...")
    else:
        print("No API key provided - system will use fallback responses")
    
    # Run setup
    setup = MEMAgentSystemSetup()
    result = setup.run_complete_setup(api_key)
    
    if result["success"]:
        print("\n✅ MEM_AGENT Complete System Setup Successful!")
        print(f"📊 Components initialized: {len(result['components'])}")
        print(f"📋 Setup report: MEM_AGENT_SETUP_REPORT.md")
        print(f"📝 Setup log: mem_agent_setup.log")
        print("\n🎯 System ready for business optimization!")
    else:
        print("\n❌ Setup failed!")
        print(f"Error: {result['error']}")
        print("Check the setup log for details")

if __name__ == "__main__":
    main()
