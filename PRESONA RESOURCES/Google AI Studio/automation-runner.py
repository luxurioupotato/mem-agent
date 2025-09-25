#!/usr/bin/env python3
"""
Automation Runner Script
Executes easy tasks automatically while providing instructions for complex ones
Uses Gemini 2.5 Pro API for code generation
"""

import os
import json
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import requests

class AutomationRunner:
    def __init__(self):
        self.project_root = Path.cwd()
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.gemini_api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent"
        self.execution_log = []
        
    def call_gemini_api(self, prompt: str, max_tokens: int = 1000) -> str:
        """Call Gemini 2.5 Pro API for code generation"""
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        
        headers = {
            "Content-Type": "application/json",
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": 0.1
            }
        }
        
        try:
            response = requests.post(
                f"{self.gemini_api_url}?key={self.gemini_api_key}",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            raise Exception(f"Gemini API call failed: {e}")
    
    def log_execution(self, task: str, status: str, details: str = ""):
        """Log task execution"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "status": status,
            "details": details
        }
        self.execution_log.append(log_entry)
        print(f"[{status.upper()}] {task}: {details}")
    
    def execute_gcp_command(self, command: str, description: str) -> bool:
        """Execute GCP command and log result"""
        try:
            self.log_execution(description, "STARTING")
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=300, encoding='utf-8', errors='ignore')
            
            if result.returncode == 0:
                self.log_execution(description, "SUCCESS", result.stdout[:200])
                return True
            else:
                self.log_execution(description, "FAILED", result.stderr[:200])
                return False
        except subprocess.TimeoutExpired:
            self.log_execution(description, "TIMEOUT", "Command timed out after 5 minutes")
            return False
        except Exception as e:
            self.log_execution(description, "ERROR", str(e))
            return False
    
    def verify_gcp_infrastructure(self) -> bool:
        """Verify GCP VM infrastructure (AUTOMATED)"""
        print("🔧 Verifying GCP Infrastructure...")
        
        commands = [
            ("gcloud config get-value project", "Check GCP project"),
            ("gcloud auth list --filter=status:ACTIVE --format=\"value(account)\"", "Check GCP authentication"),
            ("gcloud compute instances describe browser-use-server --zone=us-central1-a --format=\"value(name,status)\"", "Check VM status"),
            ("gcloud compute instances describe browser-use-server --zone=us-central1-a --format=\"value(networkInterfaces[0].accessConfigs[0].natIP)\"", "Check external IP")
        ]
        
        all_success = True
        for command, description in commands:
            if not self.execute_gcp_command(command, description):
                all_success = False
        
        return all_success
    
    def verify_docker_environment(self) -> bool:
        """Verify Docker environment on VM (AUTOMATED)"""
        print("🐳 Verifying Docker Environment...")
        
        commands = [
            ("gcloud compute ssh browser-use-server --zone=us-central1-a --command=\"docker --version\"", "Check Docker installation"),
            ("gcloud compute ssh browser-use-server --zone=us-central1-a --command=\"docker-compose --version\"", "Check Docker Compose"),
            ("gcloud compute ssh browser-use-server --zone=us-central1-a --command=\"sudo systemctl is-active docker\"", "Check Docker service"),
            ("gcloud compute ssh browser-use-server --zone=us-central1-a --command=\"docker info\"", "Check Docker daemon")
        ]
        
        all_success = True
        for command, description in commands:
            if not self.execute_gcp_command(command, description):
                all_success = False
        
        return all_success
    
    def deploy_browser_automation(self) -> bool:
        """Deploy Browser-use automation (AUTOMATED)"""
        print("🚀 Deploying Browser-use Automation...")
        
        # Create project directory
        create_dir_cmd = "gcloud compute ssh browser-use-server --zone=us-central1-a --command=\"mkdir -p ~/browser-automation\""
        if not self.execute_gcp_command(create_dir_cmd, "Create project directory"):
            return False
        
        # Generate Docker Compose file using Gemini
        docker_compose_prompt = """
        Create a docker-compose.yml file for Browser-use AI agent with the following requirements:
        - Use browseruse/browser-use:latest image
        - Expose port 7788 for web UI
        - Include VNC viewer on port 6080
        - Add Nginx reverse proxy on ports 80 and 443
        - Include environment variables for OPENAI_API_KEY
        - Add health checks for all services
        - Use proper networking and volume mounts
        """
        
        try:
            docker_compose_content = self.call_gemini_api(docker_compose_prompt, 2000)
            
            # Save Docker Compose file to VM
            save_compose_cmd = f"""gcloud compute ssh browser-use-server --zone=us-central1-a --command='cat > ~/browser-automation/docker-compose.yml << "EOF"
{docker_compose_content}
EOF'"""
            
            if not self.execute_gcp_command(save_compose_cmd, "Save Docker Compose file"):
                return False
                
        except Exception as e:
            self.log_execution("Generate Docker Compose", "ERROR", str(e))
            return False
        
        # Generate environment file
        env_content = """OPENAI_API_KEY=your-api-key-here
GEMINI_API_KEY=your-gemini-key-here
VNC_PASSWORD=youvncpassword
"""
        
        save_env_cmd = f"""gcloud compute ssh browser-use-server --zone=us-central1-a --command='cat > ~/browser-automation/.env << "EOF"
{env_content}
EOF'"""
        
        if not self.execute_gcp_command(save_env_cmd, "Save environment file"):
            return False
        
        # Start services
        start_services_cmd = "gcloud compute ssh browser-use-server --zone=us-central1-a --command='cd ~/browser-automation && docker-compose up -d'"
        if not self.execute_gcp_command(start_services_cmd, "Start Browser-use services"):
            return False
        
        return True
    
    def configure_firewall_rules(self) -> bool:
        """Configure GCP firewall rules (AUTOMATED)"""
        print("🔥 Configuring Firewall Rules...")
        
        firewall_commands = [
            ("gcloud compute firewall-rules create allow-7788 --allow tcp:7788 --source-ranges 0.0.0.0/0 --target-tags http-server", "Allow port 7788"),
            ("gcloud compute firewall-rules create allow-6080 --allow tcp:6080 --source-ranges 0.0.0.0/0 --target-tags http-server", "Allow port 6080"),
            ("gcloud compute instances add-tags browser-use-server --zone=us-central1-a --tags=http-server,https-server", "Add network tags to VM")
        ]
        
        all_success = True
        for command, description in firewall_commands:
            if not self.execute_gcp_command(command, description):
                all_success = False
        
        return all_success
    
    def test_web_services(self) -> bool:
        """Test web services accessibility (AUTOMATED)"""
        print("🌐 Testing Web Services...")
        
        test_commands = [
            ("curl -f http://34.28.159.240:7788/ --max-time 30", "Test Browser-use UI"),
            ("curl -f http://34.28.159.240:6080/ --max-time 30", "Test VNC Viewer")
        ]
        
        all_success = True
        for command, description in test_commands:
            if not self.execute_gcp_command(command, description):
                all_success = False
        
        return all_success
    
    def generate_website_template(self) -> str:
        """Generate website template using Gemini (AUTOMATED)"""
        print("🎨 Generating Website Template...")
        
        website_prompt = """
        Create a professional HTML website template for a digital agency specializing in AI automation. Include:
        - Modern, responsive design
        - Hero section with compelling headline
        - Services section (Browser Automation, Marketing Automation, AI Chatbots)
        - About section
        - Contact form
        - Professional styling with CSS
        - Mobile-friendly layout
        - Call-to-action buttons
        - SEO-friendly structure
        """
        
        try:
            website_content = self.call_gemini_api(website_prompt, 3000)
            return website_content
        except Exception as e:
            self.log_execution("Generate Website Template", "ERROR", str(e))
            return ""
    
    def generate_mautic_config(self) -> str:
        """Generate Mautic configuration using Gemini (AUTOMATED)"""
        print("📧 Generating Mautic Configuration...")
        
        mautic_prompt = """
        Create a comprehensive Mautic CRM configuration for a digital agency. Include:
        - Database setup commands
        - Nginx configuration for Mautic
        - PHP configuration requirements
        - Security settings
        - Email configuration
        - Lead capture form setup
        - Campaign automation rules
        - Integration with website forms
        """
        
        try:
            mautic_config = self.call_gemini_api(mautic_prompt, 2500)
            return mautic_config
        except Exception as e:
            self.log_execution("Generate Mautic Config", "ERROR", str(e))
            return ""
    
    def generate_chatbot_code(self) -> str:
        """Generate chatbot code using Gemini (AUTOMATED)"""
        print("🤖 Generating Chatbot Code...")
        
        chatbot_prompt = """
        Create a complete AI chatbot system for a digital agency using PHP and MySQL. Include:
        - Database schema for conversations and personas
        - API endpoint for chat interactions
        - Frontend interface with modern design
        - Integration with AI API (Gemini)
        - Persona management system
        - Conversation history
        - Lead qualification logic
        - Error handling and validation
        """
        
        try:
            chatbot_code = self.call_gemini_api(chatbot_prompt, 4000)
            return chatbot_code
        except Exception as e:
            self.log_execution("Generate Chatbot Code", "ERROR", str(e))
            return ""
    
    def run_automated_tasks(self) -> Dict[str, bool]:
        """Run all automated tasks"""
        print("🚀 Starting Automated Task Execution...")
        print("="*60)
        
        results = {
            "gcp_infrastructure": self.verify_gcp_infrastructure(),
            "docker_environment": self.verify_docker_environment(),
            "browser_automation": self.deploy_browser_automation(),
            "firewall_rules": self.configure_firewall_rules(),
            "web_services": self.test_web_services()
        }
        
        return results
    
    def generate_manual_instructions(self) -> str:
        """Generate manual setup instructions for complex tasks"""
        print("📋 Generating Manual Setup Instructions...")
        
        manual_tasks = """
        # MANUAL SETUP INSTRUCTIONS FOR COMPLEX TASKS
        
        ## Phase 2: Website Deployment & Mautic Funnel
        
        ### 1. Domain Configuration (MANUAL)
        - Register domain name with a reputable registrar
        - Configure DNS A record to point to VM external IP (34.28.159.240)
        - Set up CNAME records for www and subdomains
        - Wait for DNS propagation (24-48 hours)
        
        ### 2. SSL Certificate Setup (MANUAL)
        - Install Certbot: `sudo apt-get install certbot python3-certbot-nginx`
        - Obtain SSL certificate: `sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com`
        - Configure auto-renewal: `sudo crontab -e` (add: 0 12 * * * /usr/bin/certbot renew --quiet`)
        
        ### 3. Mautic Installation (MANUAL)
        - Access Mautic installation: http://34.28.159.240/mautic/
        - Follow installation wizard
        - Configure database connection (mautic/mautic_password)
        - Set up admin user account
        - Configure email settings for campaigns
        
        ### 4. Content Creation (MANUAL)
        - Write compelling website copy
        - Create lead capture forms
        - Design email marketing sequences
        - Set up analytics tracking (Google Analytics, Facebook Pixel)
        
        ## Phase 3: Chatbot Persona Development
        
        ### 1. Persona Definition (MANUAL)
        - Define chatbot personality and tone
        - Create conversation flow diagrams
        - Write sample dialogues
        - Set up escalation procedures
        
        ### 2. Integration Testing (MANUAL)
        - Test chatbot responses
        - Verify lead qualification logic
        - Test integration with Mautic
        - Configure monitoring and alerts
        
        ## Phase 4: Tool Integration & Data Pipelines
        
        ### 1. Tool Selection (MANUAL)
        - Choose web scraping tools
        - Select data processing platforms
        - Configure API integrations
        - Set up monitoring dashboards
        
        ### 2. Business Logic (MANUAL)
        - Define data processing rules
        - Create content generation templates
        - Set up social media schedules
        - Configure SEO optimization
        
        ## Phase 5: Full Agency Automation
        
        ### 1. Process Design (MANUAL)
        - Map client onboarding workflow
        - Create service delivery templates
        - Design revenue tracking system
        - Plan scaling infrastructure
        
        ### 2. Quality Assurance (MANUAL)
        - Test all automation workflows
        - Verify data accuracy
        - Check system performance
        - Document procedures
        """
        
        return manual_tasks
    
    def save_execution_log(self):
        """Save execution log to file"""
        log_path = self.project_root / '.cursor' / 'logs' / 'execution_log.json'
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_path, 'w') as f:
            json.dump(self.execution_log, f, indent=2)
        
        print(f"📄 Execution log saved to: {log_path}")
    
    def print_summary(self, results: Dict[str, bool]):
        """Print execution summary"""
        print("\n" + "="*60)
        print("📊 AUTOMATION EXECUTION SUMMARY")
        print("="*60)
        
        total_tasks = len(results)
        successful_tasks = sum(1 for success in results.values() if success)
        
        print(f"Total Tasks: {total_tasks}")
        print(f"Successful: {successful_tasks}")
        print(f"Failed: {total_tasks - successful_tasks}")
        print(f"Success Rate: {(successful_tasks/total_tasks)*100:.1f}%")
        
        print("\n📋 TASK RESULTS:")
        for task, success in results.items():
            status = "✅" if success else "❌"
            print(f"  {status} {task.replace('_', ' ').title()}")
        
        if successful_tasks == total_tasks:
            print("\n🎉 All automated tasks completed successfully!")
        else:
            print(f"\n⚠️  {total_tasks - successful_tasks} tasks failed. Check logs for details.")
        
        print("\n📖 MANUAL TASKS REQUIRED:")
        print("See generated manual instructions for complex tasks that require human intervention.")

def main():
    """Main execution function"""
    if not os.getenv('GEMINI_API_KEY'):
        print("❌ Error: GEMINI_API_KEY environment variable not set")
        print("Please set your Gemini API key: export GEMINI_API_KEY='your-api-key'")
        sys.exit(1)
    
    runner = AutomationRunner()
    
    try:
        # Run automated tasks
        results = runner.run_automated_tasks()
        
        # Generate manual instructions
        manual_instructions = runner.generate_manual_instructions()
        
        # Save manual instructions
        manual_path = runner.project_root / 'MANUAL_SETUP_INSTRUCTIONS.md'
        with open(manual_path, 'w') as f:
            f.write(manual_instructions)
        
        # Save execution log
        runner.save_execution_log()
        
        # Print summary
        runner.print_summary(results)
        
        print(f"\n📄 Manual instructions saved to: {manual_path}")
        
    except Exception as e:
        print(f"\n💥 Automation failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
