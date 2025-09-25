#!/usr/bin/env python3
"""
Cursor Project Health Check Script
Comprehensive health monitoring for the digital agency automation project
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

class CursorProjectHealth:
    def __init__(self):
        self.project_root = Path.cwd()
        self.health_report = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "UNKNOWN",
            "checks": {},
            "recommendations": [],
            "critical_issues": [],
            "warnings": []
        }
    
    def check_cursor_setup(self) -> Dict[str, Any]:
        """Verify Cursor-specific configurations"""
        checks = {
            'rules_exist': (self.project_root / '.cursor' / 'rules').exists(),
            'docs_exist': (self.project_root / 'docs' / 'ai-instructions').exists(),
            'tests_configured': (self.project_root / 'tests').exists(),
            'cursor_settings': self.verify_cursor_settings(),
            'automation_scripts': (self.project_root / '.cursor' / 'scripts').exists()
        }
        
        self.health_report['checks']['cursor_setup'] = checks
        return checks
    
    def verify_cursor_settings(self) -> bool:
        """Check if essential Cursor settings are configured"""
        try:
            # Check for .cursorrules or new .cursor/rules/ structure
            rules_files = list((self.project_root / '.cursor' / 'rules').glob('*.md'))
            legacy_rules = (self.project_root / '.cursorrules').exists()
            return len(rules_files) > 0 or legacy_rules
        except Exception as e:
            self.health_report['warnings'].append(f"Error checking Cursor settings: {e}")
            return False
    
    def check_gcp_connectivity(self) -> Dict[str, Any]:
        """Verify GCP connectivity and configuration"""
        checks = {
            'gcloud_installed': self.check_command_exists('gcloud'),
            'gcp_authenticated': self.check_gcp_auth(),
            'project_configured': self.check_gcp_project(),
            'vm_accessible': self.check_vm_access()
        }
        
        self.health_report['checks']['gcp_connectivity'] = checks
        return checks
    
    def check_command_exists(self, command: str) -> bool:
        """Check if a command exists in PATH"""
        try:
            subprocess.run([command, '--version'], capture_output=True, timeout=10)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def check_gcp_auth(self) -> bool:
        """Check if GCP is authenticated"""
        try:
            result = subprocess.run(['gcloud', 'auth', 'list', '--filter=status:ACTIVE'], 
                                  capture_output=True, text=True, timeout=30)
            return '@gmail.com' in result.stdout or '@googlemail.com' in result.stdout
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def check_gcp_project(self) -> bool:
        """Check if GCP project is configured"""
        try:
            result = subprocess.run(['gcloud', 'config', 'get-value', 'project'], 
                                  capture_output=True, text=True, check=True)
            return 'hardy-canyon-470416-q9' in result.stdout
        except subprocess.CalledProcessError:
            return False
    
    def check_vm_access(self) -> bool:
        """Check if VM is accessible"""
        try:
            result = subprocess.run(['gcloud', 'compute', 'instances', 'describe', 
                                   'browser-use-server', '--zone=us-central1-a'], 
                                  capture_output=True, text=True, check=True)
            return 'RUNNING' in result.stdout
        except subprocess.CalledProcessError:
            return False
    
    def check_docker_environment(self) -> Dict[str, Any]:
        """Verify Docker environment on remote VM"""
        checks = {
            'docker_installed': False,
            'docker_running': False,
            'containers_healthy': False
        }
        
        try:
            # Check Docker installation
            result = subprocess.run(['gcloud', 'compute', 'ssh', 'browser-use-server', 
                                   '--zone=us-central1-a', '--command=docker --version'], 
                                  capture_output=True, text=True, timeout=30)
            checks['docker_installed'] = 'Docker version' in result.stdout
            
            # Check Docker service
            result = subprocess.run(['gcloud', 'compute', 'ssh', 'browser-use-server', 
                                   '--zone=us-central1-a', '--command=sudo systemctl is-active docker'], 
                                  capture_output=True, text=True, timeout=30)
            checks['docker_running'] = 'active' in result.stdout
            
            # Check container status
            result = subprocess.run(['gcloud', 'compute', 'ssh', 'browser-use-server', 
                                   '--zone=us-central1-a', '--command=cd ~/browser-automation && docker-compose ps'], 
                                  capture_output=True, text=True, timeout=30)
            checks['containers_healthy'] = 'Up (healthy)' in result.stdout
            
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
            self.health_report['warnings'].append(f"Docker check failed: {e}")
        
        self.health_report['checks']['docker_environment'] = checks
        return checks
    
    def check_web_services(self) -> Dict[str, Any]:
        """Verify web services accessibility"""
        checks = {
            'browser_use_ui': False,
            'vnc_viewer': False,
            'website': False
        }
        
        try:
            # Try using requests library (more cross-platform)
            import requests
            
            # Check Browser-use UI
            try:
                response = requests.get('http://34.28.159.240:7788/', timeout=10)
                checks['browser_use_ui'] = response.status_code == 200
            except requests.RequestException:
                checks['browser_use_ui'] = False
            
            # Check VNC Viewer
            try:
                response = requests.get('http://34.28.159.240:6080/', timeout=10)
                checks['vnc_viewer'] = response.status_code == 200
            except requests.RequestException:
                checks['vnc_viewer'] = False
                
        except ImportError:
            # Fallback to curl if requests not available
            try:
                result = subprocess.run(['curl', '-f', 'http://34.28.159.240:7788/', '--max-time', '10'], 
                                      capture_output=True, text=True, timeout=15)
                checks['browser_use_ui'] = result.returncode == 0
                
                result = subprocess.run(['curl', '-f', 'http://34.28.159.240:6080/', '--max-time', '10'], 
                                      capture_output=True, text=True, timeout=15)
                checks['vnc_viewer'] = result.returncode == 0
            except Exception as e:
                self.health_report['warnings'].append(f"Web service check failed: {e}")
        
        self.health_report['checks']['web_services'] = checks
        return checks
    
    def check_project_structure(self) -> Dict[str, Any]:
        """Verify project structure and files"""
        required_files = [
            'R1_Detailed_Task_Bundles.yaml',
            'Complete_Execution_Guide_Current_Stage.yaml',
            'Master_Prompt_Task_Bundle_Planning.yaml',
            '.cursor/rules/master.md',
            '.cursor/scripts/health-check.py'
        ]
        
        checks = {
            'required_files': {},
            'project_directories': {}
        }
        
        for file_path in required_files:
            full_path = self.project_root / file_path
            checks['required_files'][file_path] = full_path.exists()
        
        # Check project directories
        required_dirs = ['.cursor', 'docs', 'tests', '.github/workflows']
        for dir_path in required_dirs:
            full_path = self.project_root / dir_path
            checks['project_directories'][dir_path] = full_path.exists()
        
        self.health_report['checks']['project_structure'] = checks
        return checks
    
    def generate_recommendations(self) -> List[str]:
        """Generate automated fix suggestions based on findings"""
        recommendations = []
        
        # Check Cursor setup
        cursor_checks = self.health_report['checks'].get('cursor_setup', {})
        if not cursor_checks.get('rules_exist'):
            recommendations.append("Run: mkdir -p .cursor/rules && create essential rule files")
        
        if not cursor_checks.get('docs_exist'):
            recommendations.append("Run: mkdir -p docs/ai-instructions && create documentation")
        
        if not cursor_checks.get('tests_configured'):
            recommendations.append("Run: mkdir -p tests/{unit,integration,e2e} && set up test framework")
        
        # Check GCP connectivity
        gcp_checks = self.health_report['checks'].get('gcp_connectivity', {})
        if not gcp_checks.get('gcloud_installed'):
            recommendations.append("Install Google Cloud SDK: https://cloud.google.com/sdk/docs/install")
        
        if not gcp_checks.get('gcp_authenticated'):
            recommendations.append("Run: gcloud auth login")
        
        if not gcp_checks.get('project_configured'):
            recommendations.append("Run: gcloud config set project hardy-canyon-470416-q9")
        
        # Check Docker environment
        docker_checks = self.health_report['checks'].get('docker_environment', {})
        if not docker_checks.get('docker_installed'):
            recommendations.append("Install Docker on the VM: gcloud compute ssh browser-use-server --zone=us-central1-a --command='curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh'")
        
        if not docker_checks.get('docker_running'):
            recommendations.append("Start Docker service: gcloud compute ssh browser-use-server --zone=us-central1-a --command='sudo systemctl start docker && sudo systemctl enable docker'")
        
        # Check web services
        web_checks = self.health_report['checks'].get('web_services', {})
        if not web_checks.get('browser_use_ui'):
            recommendations.append("Deploy Browser-use application: gcloud compute ssh browser-use-server --zone=us-central1-a --command='cd ~/browser-automation && docker-compose up -d'")
        
        self.health_report['recommendations'] = recommendations
        return recommendations
    
    def run_comprehensive_checks(self) -> bool:
        """Execute comprehensive health checks"""
        print("🔍 Running comprehensive project health checks...")
        
        # Run all checks
        self.check_cursor_setup()
        self.check_gcp_connectivity()
        self.check_docker_environment()
        self.check_web_services()
        self.check_project_structure()
        
        # Generate recommendations
        self.generate_recommendations()
        
        # Determine overall status
        all_checks = self.health_report['checks']
        critical_failures = 0
        warnings = len(self.health_report['warnings'])
        
        for category, checks in all_checks.items():
            if isinstance(checks, dict):
                for check_name, result in checks.items():
                    if isinstance(result, bool) and not result:
                        if check_name in ['gcp_authenticated', 'vm_accessible', 'docker_running']:
                            critical_failures += 1
                        else:
                            warnings += 1
        
        if critical_failures == 0 and warnings == 0:
            self.health_report['overall_status'] = "HEALTHY"
        elif critical_failures == 0:
            self.health_report['overall_status'] = "WARNING"
        else:
            self.health_report['overall_status'] = "CRITICAL"
        
        return self.health_report['overall_status'] == "HEALTHY"
    
    def print_report(self):
        """Print formatted health report"""
        print("\n" + "="*60)
        print("🏥 CURSOR PROJECT HEALTH REPORT")
        print("="*60)
        print(f"Timestamp: {self.health_report['timestamp']}")
        print(f"Overall Status: {self.health_report['overall_status']}")
        print(f"Critical Issues: {len(self.health_report['critical_issues'])}")
        print(f"Warnings: {len(self.health_report['warnings'])}")
        
        print("\n📊 CHECK RESULTS:")
        for category, checks in self.health_report['checks'].items():
            print(f"\n{category.upper()}:")
            if isinstance(checks, dict):
                for check_name, result in checks.items():
                    status = "✅" if result else "❌"
                    print(f"  {status} {check_name}")
        
        if self.health_report['recommendations']:
            print("\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(self.health_report['recommendations'], 1):
                print(f"  {i}. {rec}")
        
        if self.health_report['warnings']:
            print("\n⚠️  WARNINGS:")
            for warning in self.health_report['warnings']:
                print(f"  - {warning}")
        
        print("\n" + "="*60)
    
    def save_report(self, filename: str = "health_report.json"):
        """Save health report to file"""
        report_path = self.project_root / '.cursor' / 'health-checks' / filename
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(self.health_report, f, indent=2)
        
        print(f"📄 Health report saved to: {report_path}")

def main():
    """Main execution function"""
    health_checker = CursorProjectHealth()
    
    try:
        is_healthy = health_checker.run_comprehensive_checks()
        health_checker.print_report()
        health_checker.save_report()
        
        if is_healthy:
            print("\n🎉 Project is healthy! Ready for development.")
            sys.exit(0)
        else:
            print("\n🚨 Project has issues that need attention.")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n💥 Health check failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
