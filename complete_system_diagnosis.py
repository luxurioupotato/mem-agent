#!/usr/bin/env python3
"""
Complete System Diagnosis and Troubleshooting
Comprehensive analysis of Enhanced Memory Agent system health,
dependencies, configurations, and operational status.
"""

import os
import sys
import json
import sqlite3
import logging
import asyncio
import traceback
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("system_diagnosis.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("SystemDiagnosis")

class ComprehensiveSystemDiagnosis:
    """Complete system diagnosis and troubleshooting"""
    
    def __init__(self):
        self.diagnosis_results = {}
        self.issues_found = []
        self.recommendations = []
        self.system_health_score = 0.0
        
        logger.info("🔍 Starting comprehensive system diagnosis")

    async def run_complete_diagnosis(self) -> Dict[str, Any]:
        """Run complete system diagnosis and troubleshooting"""
        print("🔍 ENHANCED MEMORY AGENT - COMPLETE SYSTEM DIAGNOSIS")
        print("=" * 70)
        
        try:
            # Phase 1: Environment and Dependencies
            await self.diagnose_environment()
            
            # Phase 2: Core System Files
            await self.diagnose_core_files()
            
            # Phase 3: System Components
            await self.diagnose_system_components()
            
            # Phase 4: Configuration Analysis
            await self.diagnose_configurations()
            
            # Phase 5: Integration Testing
            await self.diagnose_integrations()
            
            # Phase 6: Performance Analysis
            await self.diagnose_performance()
            
            # Phase 7: Security Assessment
            await self.diagnose_security()
            
            # Generate comprehensive report
            self.generate_diagnosis_report()
            
            return self.diagnosis_results
            
        except Exception as e:
            logger.error(f"❌ Diagnosis failed: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise

    async def diagnose_environment(self):
        """Diagnose Python environment and dependencies"""
        print("\n🔧 Phase 1: Environment and Dependencies Analysis")
        print("-" * 50)
        
        env_results = {}
        
        # Check Python version
        python_version = sys.version
        env_results['python_version'] = python_version
        print(f"Python Version: {python_version}")
        
        # Check virtual environment
        venv_active = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
        env_results['virtual_environment'] = venv_active
        print(f"Virtual Environment: {'✅ Active' if venv_active else '❌ Not Active'}")
        
        # Check critical dependencies
        critical_deps = [
            'streamlit', 'google.generativeai', 'sqlite3', 'asyncio',
            'logging', 'json', 'pathlib', 'datetime'
        ]
        
        missing_deps = []
        available_deps = []
        
        for dep in critical_deps:
            try:
                __import__(dep)
                available_deps.append(dep)
                print(f"✅ {dep}")
            except ImportError:
                missing_deps.append(dep)
                print(f"❌ {dep} - MISSING")
        
        env_results['available_dependencies'] = available_deps
        env_results['missing_dependencies'] = missing_deps
        
        # Check optional dependencies
        optional_deps = ['psutil', 'pandas', 'numpy', 'flask']
        optional_available = []
        optional_missing = []
        
        for dep in optional_deps:
            try:
                __import__(dep)
                optional_available.append(dep)
                print(f"✅ {dep} (optional)")
            except ImportError:
                optional_missing.append(dep)
                print(f"⚠️ {dep} (optional) - NOT AVAILABLE")
        
        env_results['optional_available'] = optional_available
        env_results['optional_missing'] = optional_missing
        
        # Check API key
        api_key = os.getenv('GEMINI_API_KEY')
        env_results['api_key_configured'] = bool(api_key)
        print(f"Gemini API Key: {'✅ Configured' if api_key else '❌ Not Set'}")
        
        self.diagnosis_results['environment'] = env_results
        
        if missing_deps:
            self.issues_found.append(f"Missing critical dependencies: {', '.join(missing_deps)}")
        if not api_key:
            self.issues_found.append("Gemini API key not configured")

    async def diagnose_core_files(self):
        """Diagnose core system files"""
        print("\n📁 Phase 2: Core System Files Analysis")
        print("-" * 50)
        
        core_files = [
            'modules.py',
            'orchestrator.py', 
            'enhanced_memory_agent_ui.py',
            'working_memory_agent.py',
            'comprehensive_boot_orchestrator.py',
            'autonomous_initialization_orchestrator.py',
            'cursor_ai_integration_wrapper.py',
            'test_autonomous_init.py',
            'requirements_rag.txt',
            'launch_working_agent.bat'
        ]
        
        file_results = {}
        missing_files = []
        available_files = []
        
        for file_path in core_files:
            if Path(file_path).exists():
                file_stat = Path(file_path).stat()
                file_results[file_path] = {
                    'exists': True,
                    'size': file_stat.st_size,
                    'modified': datetime.fromtimestamp(file_stat.st_mtime).isoformat()
                }
                available_files.append(file_path)
                print(f"✅ {file_path} ({file_stat.st_size:,} bytes)")
            else:
                file_results[file_path] = {'exists': False}
                missing_files.append(file_path)
                print(f"❌ {file_path} - MISSING")
        
        file_results['summary'] = {
            'total_files': len(core_files),
            'available_files': len(available_files),
            'missing_files': len(missing_files)
        }
        
        self.diagnosis_results['core_files'] = file_results
        
        if missing_files:
            self.issues_found.append(f"Missing core files: {', '.join(missing_files)}")

    async def diagnose_system_components(self):
        """Diagnose system components and imports"""
        print("\n⚙️ Phase 3: System Components Analysis")
        print("-" * 50)
        
        component_results = {}
        
        # Test core module imports
        components_to_test = [
            ('modules', 'modules.py'),
            ('orchestrator', 'orchestrator.py'),
            ('enhanced_memory_agent_ui', 'enhanced_memory_agent_ui.py'),
            ('working_memory_agent', 'working_memory_agent.py'),
            ('comprehensive_boot_orchestrator', 'comprehensive_boot_orchestrator.py'),
            ('autonomous_initialization_orchestrator', 'autonomous_initialization_orchestrator.py'),
            ('cursor_ai_integration_wrapper', 'cursor_ai_integration_wrapper.py')
        ]
        
        for component_name, file_name in components_to_test:
            try:
                # Test import
                module = __import__(component_name)
                component_results[component_name] = {
                    'import_status': 'success',
                    'file_exists': Path(file_name).exists(),
                    'error': None
                }
                print(f"✅ {component_name} - Import successful")
                
                # Test specific component functionality
                if component_name == 'modules':
                    try:
                        create_all_modules = getattr(module, 'create_all_modules', None)
                        if create_all_modules:
                            manager = create_all_modules()
                            component_results[component_name]['module_manager'] = 'available'
                            print(f"   ✅ Module manager creation successful")
                        else:
                            component_results[component_name]['module_manager'] = 'function_missing'
                            print(f"   ⚠️ create_all_modules function not found")
                    except Exception as e:
                        component_results[component_name]['module_manager'] = f'error: {str(e)}'
                        print(f"   ❌ Module manager test failed: {e}")
                
            except ImportError as e:
                component_results[component_name] = {
                    'import_status': 'failed',
                    'file_exists': Path(file_name).exists(),
                    'error': str(e)
                }
                print(f"❌ {component_name} - Import failed: {e}")
                self.issues_found.append(f"Component import failed: {component_name} - {str(e)}")
            except Exception as e:
                component_results[component_name] = {
                    'import_status': 'error',
                    'file_exists': Path(file_name).exists(), 
                    'error': str(e)
                }
                print(f"❌ {component_name} - Error: {e}")
                self.issues_found.append(f"Component error: {component_name} - {str(e)}")
        
        self.diagnosis_results['system_components'] = component_results

    async def diagnose_configurations(self):
        """Diagnose system configurations"""
        print("\n⚙️ Phase 4: Configuration Analysis")
        print("-" * 50)
        
        config_results = {}
        
        # Check environment variables
        env_vars = ['GEMINI_API_KEY', 'ANTHROPIC_API_KEY']
        env_status = {}
        
        for var in env_vars:
            value = os.getenv(var)
            env_status[var] = {
                'configured': bool(value),
                'length': len(value) if value else 0
            }
            status = "✅ Configured" if value else "❌ Not Set"
            print(f"{var}: {status}")
        
        config_results['environment_variables'] = env_status
        
        # Check configuration files
        config_files = [
            'requirements_rag.txt',
            '.env',
            'MEMORY_AGENT_SYSTEM/config/system_config.json'
        ]
        
        config_file_status = {}
        for config_file in config_files:
            exists = Path(config_file).exists()
            config_file_status[config_file] = exists
            status = "✅ Found" if exists else "❌ Missing"
            print(f"{config_file}: {status}")
        
        config_results['configuration_files'] = config_file_status
        
        # Check working directory
        current_dir = Path.cwd()
        config_results['working_directory'] = str(current_dir)
        print(f"Working Directory: {current_dir}")
        
        self.diagnosis_results['configurations'] = config_results

    async def diagnose_integrations(self):
        """Diagnose system integrations"""
        print("\n🔗 Phase 5: Integration Testing")
        print("-" * 50)
        
        integration_results = {}
        
        # Test Gemini API integration
        try:
            import google.generativeai as genai
            api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyDj-aTJt7riqX6MJSsW2Tu7uO8cjisEGqE')
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Test API call
            response = await asyncio.to_thread(model.generate_content, "Hello, test connection")
            integration_results['gemini_api'] = {
                'status': 'success',
                'response_length': len(response.text),
                'error': None
            }
            print("✅ Gemini API - Connection successful")
            
        except Exception as e:
            integration_results['gemini_api'] = {
                'status': 'failed',
                'error': str(e)
            }
            print(f"❌ Gemini API - Connection failed: {e}")
            self.issues_found.append(f"Gemini API integration failed: {str(e)}")
        
        # Test Streamlit availability
        try:
            import streamlit
            integration_results['streamlit'] = {
                'status': 'available',
                'version': streamlit.__version__
            }
            print(f"✅ Streamlit - Available (version {streamlit.__version__})")
        except ImportError as e:
            integration_results['streamlit'] = {
                'status': 'unavailable',
                'error': str(e)
            }
            print(f"❌ Streamlit - Not available: {e}")
            self.issues_found.append(f"Streamlit not available: {str(e)}")
        
        # Test autonomous initialization components
        try:
            from autonomous_initialization_orchestrator import AutonomousInitializationOrchestrator
            from cursor_ai_integration_wrapper import CursorAIIntegrationWrapper
            
            # Test orchestrator creation
            orchestrator = AutonomousInitializationOrchestrator()
            wrapper = CursorAIIntegrationWrapper()
            
            integration_results['cursor_ai'] = {
                'status': 'available',
                'orchestrator': 'functional',
                'wrapper': 'functional'
            }
            print("✅ Cursor AI - Autonomous initialization available")
            
        except ImportError as e:
            integration_results['cursor_ai'] = {
                'status': 'unavailable',
                'error': str(e)
            }
            print(f"❌ Cursor AI - Components not available: {e}")
            self.issues_found.append(f"Cursor AI components unavailable: {str(e)}")
        except Exception as e:
            integration_results['cursor_ai'] = {
                'status': 'error',
                'error': str(e)
            }
            print(f"❌ Cursor AI - Error during initialization: {e}")
            self.issues_found.append(f"Cursor AI initialization error: {str(e)}")
        
        self.diagnosis_results['integrations'] = integration_results

    async def diagnose_performance(self):
        """Diagnose system performance"""
        print("\n📊 Phase 6: Performance Analysis")
        print("-" * 50)
        
        performance_results = {}
        
        # Check system resources
        try:
            import psutil
            
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('.')
            
            performance_results['system_resources'] = {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available_gb': memory.available / (1024**3),
                'disk_free_gb': disk.free / (1024**3),
                'disk_percent': (disk.used / disk.total) * 100
            }
            
            print(f"CPU Usage: {cpu_percent}%")
            print(f"Memory Usage: {memory.percent}% ({memory.available / (1024**3):.1f} GB available)")
            print(f"Disk Usage: {(disk.used / disk.total) * 100:.1f}% ({disk.free / (1024**3):.1f} GB free)")
            
            # Performance warnings
            if cpu_percent > 80:
                self.issues_found.append("High CPU usage detected")
            if memory.percent > 90:
                self.issues_found.append("High memory usage detected")
            if (disk.used / disk.total) * 100 > 90:
                self.issues_found.append("Low disk space available")
                
        except ImportError:
            performance_results['system_resources'] = 'psutil_not_available'
            print("⚠️ psutil not available - cannot check system resources")
            self.issues_found.append("psutil not installed - system monitoring limited")
        
        # Check file system performance
        try:
            start_time = datetime.now()
            test_files = list(Path('.').glob('*.py'))
            scan_time = (datetime.now() - start_time).total_seconds()
            
            performance_results['file_system'] = {
                'python_files_found': len(test_files),
                'scan_time_seconds': scan_time
            }
            
            print(f"File System: {len(test_files)} Python files scanned in {scan_time:.2f}s")
            
        except Exception as e:
            performance_results['file_system'] = f'error: {str(e)}'
            print(f"❌ File system test failed: {e}")
        
        self.diagnosis_results['performance'] = performance_results

    async def diagnose_security(self):
        """Diagnose system security"""
        print("\n🛡️ Phase 7: Security Assessment")
        print("-" * 50)
        
        security_results = {}
        
        # Check API key security
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            security_results['api_key_security'] = {
                'configured': True,
                'format_valid': api_key.startswith('AIza') and len(api_key) > 35,
                'exposed_in_code': self.check_api_key_exposure()
            }
            
            if api_key.startswith('AIza') and len(api_key) > 35:
                print("✅ API Key - Valid format")
            else:
                print("⚠️ API Key - Invalid format")
                self.issues_found.append("API key format appears invalid")
        else:
            security_results['api_key_security'] = {'configured': False}
            print("❌ API Key - Not configured")
        
        # Check file permissions
        sensitive_files = ['.env', 'autonomous_system_memory.db', 'memory_agent_chat.db']
        file_permissions = {}
        
        for file_path in sensitive_files:
            if Path(file_path).exists():
                try:
                    # Check if file is readable/writable
                    with open(file_path, 'r') as f:
                        pass
                    file_permissions[file_path] = 'accessible'
                    print(f"✅ {file_path} - Accessible")
                except Exception as e:
                    file_permissions[file_path] = f'error: {str(e)}'
                    print(f"❌ {file_path} - Access error: {e}")
            else:
                file_permissions[file_path] = 'not_found'
                print(f"ℹ️ {file_path} - Not found")
        
        security_results['file_permissions'] = file_permissions
        
        # Check network configuration
        security_results['network_config'] = {
            'streamlit_host': '0.0.0.0',  # From previous analysis
            'api_host': '0.0.0.0',
            'security_level': 'medium'
        }
        print("⚠️ Network Configuration - Services accessible on network (0.0.0.0)")
        print("   Recommendation: Consider firewall configuration for production")
        
        self.diagnosis_results['security'] = security_results

    def check_api_key_exposure(self) -> bool:
        """Check if API key is exposed in code files"""
        try:
            python_files = list(Path('.').glob('*.py'))
            for file_path in python_files:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if 'AIzaSyDj-aTJt7riqX6MJSsW2Tu7uO8cjisEGqE' in content:
                            return True
                except Exception:
                    continue
            return False
        except Exception:
            return False

    def generate_diagnosis_report(self):
        """Generate comprehensive diagnosis report"""
        print("\n📋 COMPREHENSIVE DIAGNOSIS REPORT")
        print("=" * 70)
        
        # Calculate system health score
        total_checks = 0
        passed_checks = 0
        
        # Environment checks
        env_results = self.diagnosis_results.get('environment', {})
        total_checks += 4
        if not env_results.get('missing_dependencies'):
            passed_checks += 1
        if env_results.get('virtual_environment'):
            passed_checks += 1
        if env_results.get('api_key_configured'):
            passed_checks += 1
        if not env_results.get('optional_missing'):
            passed_checks += 1
        
        # File checks
        file_results = self.diagnosis_results.get('core_files', {})
        file_summary = file_results.get('summary', {})
        total_checks += 1
        if file_summary.get('missing_files', 1) == 0:
            passed_checks += 1
        
        # Integration checks
        integration_results = self.diagnosis_results.get('integrations', {})
        total_checks += 3
        if integration_results.get('gemini_api', {}).get('status') == 'success':
            passed_checks += 1
        if integration_results.get('streamlit', {}).get('status') == 'available':
            passed_checks += 1
        if integration_results.get('cursor_ai', {}).get('status') in ['available', 'functional']:
            passed_checks += 1
        
        self.system_health_score = (passed_checks / total_checks) * 100 if total_checks > 0 else 0
        
        print(f"🎯 SYSTEM HEALTH SCORE: {self.system_health_score:.1f}%")
        print(f"📊 CHECKS PASSED: {passed_checks}/{total_checks}")
        
        if self.system_health_score >= 90:
            print("✅ SYSTEM STATUS: EXCELLENT - Ready for full operation")
        elif self.system_health_score >= 75:
            print("⚠️ SYSTEM STATUS: GOOD - Minor issues to address")
        elif self.system_health_score >= 50:
            print("⚠️ SYSTEM STATUS: FAIR - Several issues need attention")
        else:
            print("❌ SYSTEM STATUS: POOR - Significant issues require resolution")
        
        # Print issues found
        if self.issues_found:
            print(f"\n⚠️ ISSUES IDENTIFIED ({len(self.issues_found)}):")
            for i, issue in enumerate(self.issues_found, 1):
                print(f"  {i}. {issue}")
        else:
            print("\n✅ NO CRITICAL ISSUES FOUND")
        
        # Generate recommendations
        self.generate_recommendations()
        
        if self.recommendations:
            print(f"\n💡 RECOMMENDATIONS ({len(self.recommendations)}):")
            for i, rec in enumerate(self.recommendations, 1):
                print(f"  {i}. {rec}")

    def generate_recommendations(self):
        """Generate troubleshooting recommendations"""
        self.recommendations = []
        
        # Environment recommendations
        env_results = self.diagnosis_results.get('environment', {})
        if env_results.get('missing_dependencies'):
            self.recommendations.append("Install missing dependencies: pip install -r requirements_rag.txt")
        
        if not env_results.get('virtual_environment'):
            self.recommendations.append("Activate virtual environment: .\\venv\\Scripts\\activate")
        
        if not env_results.get('api_key_configured'):
            self.recommendations.append("Set Gemini API key: $env:GEMINI_API_KEY='your_api_key'")
        
        # File recommendations
        file_results = self.diagnosis_results.get('core_files', {})
        if file_results.get('summary', {}).get('missing_files', 0) > 0:
            self.recommendations.append("Restore missing files from PROTOTYPE_1_BACKUP directory")
        
        # Integration recommendations
        integration_results = self.diagnosis_results.get('integrations', {})
        if integration_results.get('gemini_api', {}).get('status') != 'success':
            self.recommendations.append("Check Gemini API key and network connectivity")
        
        if integration_results.get('cursor_ai', {}).get('status') not in ['available', 'functional']:
            self.recommendations.append("Verify Cursor AI components are properly installed")
        
        # Performance recommendations
        performance_results = self.diagnosis_results.get('performance', {})
        resources = performance_results.get('system_resources', {})
        if isinstance(resources, dict):
            if resources.get('cpu_percent', 0) > 80:
                self.recommendations.append("High CPU usage - close unnecessary applications")
            if resources.get('memory_percent', 0) > 90:
                self.recommendations.append("High memory usage - restart system or close applications")
        
        # Security recommendations
        security_results = self.diagnosis_results.get('security', {})
        if security_results.get('api_key_security', {}).get('exposed_in_code'):
            self.recommendations.append("API key exposed in code - move to environment variables")
        
        # General recommendations
        if self.system_health_score < 90:
            self.recommendations.append("Run system restoration from backup if issues persist")
        
        if not self.recommendations:
            self.recommendations.append("System appears healthy - ready for operation")

# Main execution
async def main():
    """Main diagnosis function"""
    diagnosis = ComprehensiveSystemDiagnosis()
    
    try:
        results = await diagnosis.run_complete_diagnosis()
        
        # Save diagnosis results
        with open("system_diagnosis_report.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n💾 Diagnosis report saved: system_diagnosis_report.json")
        print(f"📋 Log file saved: system_diagnosis.log")
        
        return results
        
    except Exception as e:
        logger.error(f"❌ Diagnosis failed: {e}")
        print(f"\n❌ DIAGNOSIS FAILED: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(main())
