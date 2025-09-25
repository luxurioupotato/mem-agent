#!/usr/bin/env python3
"""
Simple Windows-Compatible Health Check
Basic health monitoring for the automation framework
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

def check_project_structure() -> Dict[str, bool]:
    """Check if required project files and directories exist"""
    project_root = Path.cwd()
    
    required_files = [
        'R1_Detailed_Task_Bundles.yaml',
        'Complete_Execution_Guide_Current_Stage.yaml',
        'Master_Prompt_Task_Bundle_Planning.yaml',
        '.cursor/rules/master.md',
        '.cursor/scripts/health-check.py',
        '.cursor/scripts/automation-runner.py'
    ]
    
    required_dirs = [
        '.cursor',
        '.cursor/rules',
        '.cursor/scripts',
        'docs',
        'tests'
    ]
    
    checks = {}
    
    print("📁 Checking project structure...")
    for file_path in required_files:
        full_path = project_root / file_path
        exists = full_path.exists()
        checks[f"file_{file_path}"] = exists
        status = "✅" if exists else "❌"
        print(f"  {status} {file_path}")
    
    for dir_path in required_dirs:
        full_path = project_root / dir_path
        exists = full_path.exists()
        checks[f"dir_{dir_path}"] = exists
        status = "✅" if exists else "❌"
        print(f"  {status} {dir_path}/")
    
    return checks

def check_python_environment() -> Dict[str, Any]:
    """Check Python environment and required packages"""
    checks = {}
    
    print("\n🐍 Checking Python environment...")
    
    # Check Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    checks['python_version'] = python_version
    print(f"  ✅ Python version: {python_version}")
    
    # Check required packages
    required_packages = ['requests', 'pathlib', 'json', 'subprocess']
    for package in required_packages:
        try:
            __import__(package)
            checks[f"package_{package}"] = True
            print(f"  ✅ Package: {package}")
        except ImportError:
            checks[f"package_{package}"] = False
            print(f"  ❌ Package: {package}")
    
    return checks

def check_environment_variables() -> Dict[str, bool]:
    """Check important environment variables"""
    checks = {}
    
    print("\n🔑 Checking environment variables...")
    
    env_vars = [
        'GEMINI_API_KEY',
        'OPENAI_API_KEY',
        'PATH'
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if var in ['GEMINI_API_KEY', 'OPENAI_API_KEY']:
            checks[var] = value is not None and len(value) > 10
            status = "✅" if checks[var] else "❌"
            display_value = f"{value[:10]}..." if value and len(value) > 10 else "Not set"
        else:
            checks[var] = value is not None
            status = "✅" if checks[var] else "❌"
            display_value = "Set" if value else "Not set"
        
        print(f"  {status} {var}: {display_value}")
    
    return checks

def check_automation_readiness() -> Dict[str, bool]:
    """Check if automation components are ready"""
    checks = {}
    
    print("\n🤖 Checking automation readiness...")
    
    # Check if main scripts exist and are readable
    automation_files = [
        '.cursor/scripts/automation-runner.py',
        '.cursor/scripts/gcp-deploy.sh',
        '.cursor/scripts/setup.ps1'
    ]
    
    for file_path in automation_files:
        full_path = Path(file_path)
        exists = full_path.exists()
        checks[f"automation_{file_path}"] = exists
        status = "✅" if exists else "❌"
        print(f"  {status} {file_path}")
    
    # Check if Gemini API key is available
    gemini_key = os.getenv('GEMINI_API_KEY')
    checks['gemini_api_ready'] = gemini_key is not None and len(gemini_key) > 20
    status = "✅" if checks['gemini_api_ready'] else "⚠️ "
    print(f"  {status} Gemini API key configured")
    
    return checks

def generate_health_report() -> Dict[str, Any]:
    """Generate comprehensive health report"""
    print("🏥 CURSOR AUTOMATION FRAMEWORK HEALTH CHECK")
    print("=" * 50)
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "platform": "Windows",
        "project_root": str(Path.cwd()),
        "checks": {}
    }
    
    # Run all checks
    report['checks']['project_structure'] = check_project_structure()
    report['checks']['python_environment'] = check_python_environment()
    report['checks']['environment_variables'] = check_environment_variables()
    report['checks']['automation_readiness'] = check_automation_readiness()
    
    # Calculate overall health
    total_checks = 0
    passed_checks = 0
    
    for category, checks in report['checks'].items():
        for check_name, result in checks.items():
            total_checks += 1
            if result is True:
                passed_checks += 1
    
    health_percentage = (passed_checks / total_checks) * 100 if total_checks > 0 else 0
    report['health_percentage'] = health_percentage
    report['overall_status'] = (
        "HEALTHY" if health_percentage >= 80 else
        "WARNING" if health_percentage >= 60 else
        "CRITICAL"
    )
    
    print(f"\n📊 HEALTH SUMMARY")
    print("=" * 30)
    print(f"Overall Status: {report['overall_status']}")
    print(f"Health Score: {health_percentage:.1f}% ({passed_checks}/{total_checks} checks passed)")
    
    return report

def save_health_report(report: Dict[str, Any]):
    """Save health report to file"""
    health_dir = Path('.cursor/health-checks')
    health_dir.mkdir(parents=True, exist_ok=True)
    
    report_file = health_dir / 'simple_health_report.json'
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Health report saved to: {report_file}")

def show_next_steps(report: Dict[str, Any]):
    """Show recommended next steps based on health check"""
    print(f"\n💡 RECOMMENDED NEXT STEPS")
    print("=" * 30)
    
    if report['overall_status'] == "CRITICAL":
        print("🚨 Critical issues detected:")
        print("  1. Install missing Python packages: pip install requests")
        print("  2. Set up Gemini API key: $env:GEMINI_API_KEY='your-key'")
        print("  3. Install Google Cloud SDK (optional for GCP features)")
    
    elif report['overall_status'] == "WARNING":
        print("⚠️  Some improvements needed:")
        print("  1. Set up API keys for full functionality")
        print("  2. Install Google Cloud SDK for GCP automation")
        print("  3. Run: python .cursor/scripts/automation-runner.py")
    
    else:
        print("🎉 System is healthy! Ready for automation:")
        print("  1. Set GEMINI_API_KEY: $env:GEMINI_API_KEY='your-key'")
        print("  2. Run automation: python .cursor/scripts/automation-runner.py")
        print("  3. Deploy GCP infrastructure: .cursor/scripts/setup.ps1 -RunAutomation")
    
    print(f"\n📖 For detailed instructions, see: MANUAL_SETUP_INSTRUCTIONS.md")

def main():
    """Main execution function"""
    try:
        # Generate health report
        report = generate_health_report()
        
        # Save report
        save_health_report(report)
        
        # Show next steps
        show_next_steps(report)
        
        # Exit with appropriate code
        if report['overall_status'] == "CRITICAL":
            sys.exit(1)
        else:
            sys.exit(0)
            
    except Exception as e:
        print(f"\n💥 Health check failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
