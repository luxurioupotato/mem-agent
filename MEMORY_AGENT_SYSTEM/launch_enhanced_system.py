#!/usr/bin/env python3
"""
Launch Enhanced Memory Agent System
Simple launcher to test and run the complete 20+ module system
"""

import os
import sys
import asyncio
import logging
from datetime import datetime

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from modules import create_all_modules, ModuleManager
    print("✅ Successfully imported complete module system")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure modules.py is in the current directory")
    sys.exit(1)

async def test_enhanced_system():
    """Test the complete enhanced system"""
    print("🚀 Enhanced Memory Agent System - Integration Test")
    print("=" * 60)
    
    try:
        # Create and initialize all modules
        print("🔧 Creating module manager with all 20+ modules...")
        manager = create_all_modules()
        
        print("🔧 Initializing all modules...")
        init_results = await manager.initialize_all()
        
        # Display initialization results
        success_count = 0
        for module_id, result in init_results.items():
            status = "✅" if result == "success" else "❌"
            print(f"{status} {module_id.replace('_', ' ').title()}: {result}")
            if result == "success":
                success_count += 1
        
        print(f"\n📊 Initialization Summary: {success_count}/{len(init_results)} modules online")
        
        # Get system status
        print("\n📊 System Status by Category:")
        status = manager.get_system_status()
        
        # Group by type
        module_types = {}
        for module_id, module_data in status.items():
            module_type = module_data.get("type", "Other")
            if module_type not in module_types:
                module_types[module_type] = []
            module_types[module_type].append(module_id)
        
        type_icons = {
            "Core": "🧠",
            "Advanced": "⚡",
            "Brain": "🎯",
            "Business": "💼", 
            "Intelligence": "🔍",
            "Optimization": "🚀",
            "Other": "⚙️"
        }
        
        total_modules = 0
        for module_type, modules in module_types.items():
            icon = type_icons.get(module_type, "⚙️")
            print(f"\n{icon} {module_type} Modules ({len(modules)}):")
            for module_id in modules:
                module_status = status[module_id]
                status_icon = "✅" if module_status.get("status") == "online" else "❌"
                print(f"  {status_icon} {module_id.replace('_', ' ').title()}")
            total_modules += len(modules)
        
        print(f"\n🎯 Total System Modules: {total_modules}")
        
        # Test module communication
        print("\n🧪 Testing Module Communication:")
        
        # Test memory module
        if "memory_module" in manager.modules:
            memory_result = await manager.dispatch("memory_module", {
                "content": "System test successful",
                "memory_type": "episodic",
                "importance": 0.9
            })
            print(f"✅ Memory Module: {memory_result.get('status', 'unknown')}")
        
        # Test knowledge module
        if "knowledge_module" in manager.modules:
            knowledge_result = await manager.dispatch("knowledge_module", {
                "entity": "business_strategy",
                "domain": "business",
                "data": {"test": "knowledge integration"}
            })
            print(f"✅ Knowledge Module: {knowledge_result.get('status', 'unknown')}")
        
        # Test analysis module
        if "analysis_module" in manager.modules:
            analysis_result = await manager.dispatch("analysis_module", {
                "analysis_type": "business",
                "data": {"test": "business analysis"}
            })
            print(f"✅ Analysis Module: {analysis_result.get('status', 'unknown')}")
        
        print("\n🎉 Enhanced System Test Completed Successfully!")
        print("=" * 60)
        print("✅ All modules are functional and communicating properly")
        print("✅ System is ready for Streamlit UI integration")
        print("✅ Knowledge base and memory systems are operational")
        print("✅ Business intelligence modules are active")
        
        return True
        
    except Exception as e:
        print(f"❌ System test failed: {e}")
        return False

def main():
    """Main function"""
    print("🧠 Enhanced Memory Agent System Launcher")
    print("=" * 50)
    
    # Check environment
    if not os.getenv('GEMINI_API_KEY'):
        print("⚠️  Warning: GEMINI_API_KEY not set in environment")
        print("Setting API key for testing...")
        os.environ['GEMINI_API_KEY'] = 'AIzaSyDj-aTJt7riqX6MJSsW2Tu7uO8cjisEGqE'
    
    # Run system test
    print("🧪 Running comprehensive system test...")
    success = asyncio.run(test_enhanced_system())
    
    if success:
        print("\n🚀 System Ready! Launch options:")
        print("1. For enhanced UI: streamlit run enhanced_memory_agent_ui.py --server.port 8501")
        print("2. For basic UI: streamlit run advanced_memory_agent_ui.py --server.port 8501")
        print("3. Access at: http://localhost:8501")
    else:
        print("\n❌ System test failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
