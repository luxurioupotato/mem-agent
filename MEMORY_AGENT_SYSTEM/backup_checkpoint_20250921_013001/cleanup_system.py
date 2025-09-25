#!/usr/bin/env python3
"""
System Cleanup - Remove junk files and ensure functionality
"""

import os
import shutil
from pathlib import Path

def cleanup_system():
    """Clean up system and remove junk files"""
    print("🧹 SYSTEM CLEANUP INITIATED")
    print("=" * 40)
    
    # Define essential files
    essential_files = [
        "final_system_integration.py",
        "ssi_enhanced_system_fixed.py", 
        "ssi_compliance_system.py",
        "loop_prevention_system_fixed.py",
        "input_analysis_system.py",
        "mentor_brain_boot_protocol.py",
        "test_system.py",
        "BEGINNER_GUIDE.md",
        "DETAILED_MEMORY_AGENT_COMPARISON.md",
        "COMPLETE_COMPARISON_JUSTIFICATIONS.md",
        "FINAL_LAUNCH_AUDIT.md",
        "TEST_RESULTS_REPORT.md",
        "COMPREHENSIVE_CHAT_THREAD_ANALYSIS.md",
        "FINAL_EXTRACTION_VERIFICATION.md",
        "JUSTIFIED_LAUNCH_APPROVAL.md",
        "REQUIREMENTS_VS_EXECUTION_AUDIT.md",
        "SSI_COMMANDS_REFERENCE.md",
        "SSI_IMPLEMENTATION_SUMMARY.md",
        "STRICT_SYSTEM_INSTRUCTION_SSI.md",
        "CRITICAL_ISSUE_VERIFICATION.md",
        "COMPLETE_VERIFICATION_REPORT.md"
    ]
    
    # Get all files in directory
    current_dir = Path(".")
    all_files = list(current_dir.glob("*.py")) + list(current_dir.glob("*.md")) + list(current_dir.glob("*.json"))
    
    # Find junk files
    junk_files = []
    for file in all_files:
        if file.name not in essential_files and not file.name.startswith("."):
            junk_files.append(file)
    
    # Remove junk files
    removed_count = 0
    for file in junk_files:
        try:
            if file.is_file():
                file.unlink()
                print(f"🗑️  Removed: {file.name}")
                removed_count += 1
        except Exception as e:
            print(f"❌ Failed to remove {file.name}: {e}")
    
    # Clean up directories
    junk_dirs = ["__pycache__", ".pytest_cache", "logs", "temp"]
    for dir_name in junk_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            try:
                shutil.rmtree(dir_path)
                print(f"🗑️  Removed directory: {dir_name}")
            except Exception as e:
                print(f"❌ Failed to remove directory {dir_name}: {e}")
    
    print(f"\n✅ CLEANUP COMPLETE: {removed_count} files removed")
    print("🎯 SYSTEM OPTIMIZED FOR FUNCTIONALITY")

if __name__ == "__main__":
    cleanup_system()
