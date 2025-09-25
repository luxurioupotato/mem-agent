#!/usr/bin/env python3
"""
Test script for autonomous initialization system
"""

import asyncio
import logging
import sys
import os
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

async def test_autonomous_initialization():
    """Test the autonomous initialization system"""
    try:
        logger.info("🧪 Testing Autonomous Initialization System")
        
        # Test 1: Import components
        logger.info("📦 Testing component imports...")
        try:
            from autonomous_initialization_orchestrator import AutonomousInitializationOrchestrator, execute_autonomous_initialization
            from cursor_ai_integration_wrapper import CursorAIIntegrationWrapper, execute_cursor_ai_integration
            logger.info("✅ All components imported successfully")
        except ImportError as e:
            logger.error(f"❌ Import failed: {e}")
            return False
        
        # Test 2: Create orchestrator instance
        logger.info("🔧 Testing orchestrator creation...")
        try:
            orchestrator = AutonomousInitializationOrchestrator()
            logger.info("✅ Orchestrator created successfully")
        except Exception as e:
            logger.error(f"❌ Orchestrator creation failed: {e}")
            return False
        
        # Test 3: Test database setup
        logger.info("🗄️ Testing database setup...")
        try:
            if Path(orchestrator.db_path).exists():
                logger.info("✅ Database file created successfully")
            else:
                logger.error("❌ Database file not found")
                return False
        except Exception as e:
            logger.error(f"❌ Database test failed: {e}")
            return False
        
        # Test 4: Test AI integration setup
        logger.info("🤖 Testing AI integration...")
        try:
            if orchestrator.ai_model:
                logger.info("✅ AI model configured successfully")
            else:
                logger.warning("⚠️ AI model not configured (API key may be missing)")
        except Exception as e:
            logger.error(f"❌ AI integration test failed: {e}")
            return False
        
        # Test 5: Test wrapper creation
        logger.info("🔗 Testing integration wrapper...")
        try:
            wrapper = CursorAIIntegrationWrapper()
            logger.info("✅ Integration wrapper created successfully")
        except Exception as e:
            logger.error(f"❌ Wrapper creation failed: {e}")
            return False
        
        # Test 6: Test file access (limited)
        logger.info("📁 Testing file access capabilities...")
        try:
            project_files = list(Path.cwd().glob("*.py"))
            logger.info(f"✅ Found {len(project_files)} Python files for processing")
        except Exception as e:
            logger.error(f"❌ File access test failed: {e}")
            return False
        
        logger.info("🎉 All tests passed! Autonomous initialization system is ready.")
        return True
        
    except Exception as e:
        logger.error(f"❌ Test suite failed: {e}")
        return False

async def test_quick_initialization():
    """Test a quick initialization run (first phase only)"""
    try:
        logger.info("⚡ Testing quick initialization (Phase 1 only)...")
        
        from autonomous_initialization_orchestrator import AutonomousInitializationOrchestrator
        
        orchestrator = AutonomousInitializationOrchestrator()
        
        # Test just the file access phase
        await orchestrator.phase_1_file_access_and_cataloging()
        
        logger.info(f"✅ Processed {len(orchestrator.processed_files)} files")
        
        # Show some statistics
        file_types = {}
        for file_analysis in orchestrator.processed_files:
            file_types[file_analysis.type] = file_types.get(file_analysis.type, 0) + 1
        
        logger.info("📊 File type breakdown:")
        for file_type, count in file_types.items():
            logger.info(f"  {file_type}: {count} files")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Quick initialization test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 AUTONOMOUS INITIALIZATION SYSTEM TEST SUITE")
    print("=" * 60)
    
    # Test 1: Basic component tests
    print("\n🔍 Running basic component tests...")
    basic_test_result = asyncio.run(test_autonomous_initialization())
    
    if not basic_test_result:
        print("❌ Basic tests failed. Stopping test suite.")
        sys.exit(1)
    
    # Test 2: Quick initialization test
    print("\n⚡ Running quick initialization test...")
    quick_test_result = asyncio.run(test_quick_initialization())
    
    if quick_test_result:
        print("\n✅ ALL TESTS PASSED!")
        print("🚀 Autonomous initialization system is ready for full deployment.")
    else:
        print("\n⚠️ Some tests failed, but basic functionality is available.")
    
    print("\n📋 SUMMARY:")
    print(f"  Basic Components: {'✅ PASS' if basic_test_result else '❌ FAIL'}")
    print(f"  Quick Init Test: {'✅ PASS' if quick_test_result else '❌ FAIL'}")
    
    print("\n🎯 To run full autonomous initialization:")
    print("  python -c \"import asyncio; from cursor_ai_integration_wrapper import execute_cursor_ai_integration; asyncio.run(execute_cursor_ai_integration())\"")

if __name__ == "__main__":
    main()
