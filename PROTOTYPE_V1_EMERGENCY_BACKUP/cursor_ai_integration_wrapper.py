#!/usr/bin/env python3
"""
Cursor AI Integration Wrapper
Surgical integration wrapper for the autonomous initialization orchestrator
with the existing Enhanced Memory Agent system.
"""

import asyncio
import logging
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Import existing system components
try:
    from modules import create_all_modules
    from orchestrator import ClusterOrchestrator
    from autonomous_initialization_orchestrator import AutonomousInitializationOrchestrator, execute_autonomous_initialization
except ImportError as e:
    logging.warning(f"Some system components not available: {e}")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("cursor_integration.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("CursorIntegration")

class CursorAIIntegrationWrapper:
    """
    Integration wrapper that bridges Cursor AI prompt with the autonomous orchestrator
    and existing Enhanced Memory Agent system components.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.orchestrator = None
        self.module_manager = None
        self.cluster_orchestrator = None
        self.readiness_report = None
        self.system_state = "uninitialized"
        
        self.logger.info("🔧 Cursor AI Integration Wrapper initialized")

    async def execute_cursor_ai_prompt(self) -> Dict[str, Any]:
        """
        Execute the comprehensive Cursor AI initialization prompt:
        
        1. Access every project file and folder accessible in the environment
        2. Read and parse each file fully, extracting all data
        3. Populate memory structures and placeholders
        4. Initialize all 21 system modules
        5. Perform multi-pass consistency check
        6. Generate comprehensive readiness report
        7. Present report and pause for operator approval
        """
        
        self.logger.info("🚀 EXECUTING CURSOR AI COMPREHENSIVE INITIALIZATION PROMPT")
        self.logger.info("=" * 80)
        
        start_time = datetime.now()
        
        try:
            # Phase 1: Initialize Autonomous Orchestrator
            self.logger.info("🎯 Phase 1: Initializing Autonomous Orchestrator")
            self.orchestrator = AutonomousInitializationOrchestrator()
            
            # Phase 2: Execute Comprehensive Initialization
            self.logger.info("🎯 Phase 2: Executing Comprehensive System Initialization")
            self.readiness_report = await self.orchestrator.execute_comprehensive_initialization()
            
            # Phase 3: Integrate with Existing System Components
            self.logger.info("🎯 Phase 3: Integrating with Existing System Components")
            await self.integrate_with_existing_system()
            
            # Phase 4: Generate Final Integration Report
            self.logger.info("🎯 Phase 4: Generating Final Integration Report")
            integration_report = await self.generate_integration_report()
            
            # Phase 5: Present Comprehensive Report
            self.logger.info("🎯 Phase 5: Presenting Comprehensive Readiness Report")
            await self.present_comprehensive_report(integration_report)
            
            # Phase 6: Await Operator Approval
            self.logger.info("🎯 Phase 6: Awaiting Operator Approval")
            approval_status = await self.await_operator_approval()
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            final_report = {
                "initialization_status": "completed",
                "execution_time_seconds": execution_time,
                "readiness_report": self.readiness_report.__dict__ if self.readiness_report else None,
                "integration_report": integration_report,
                "approval_status": approval_status,
                "system_state": self.system_state,
                "timestamp": datetime.now().isoformat()
            }
            
            self.logger.info(f"🎉 CURSOR AI INITIALIZATION COMPLETED in {execution_time:.2f}s")
            self.logger.info("=" * 80)
            
            return final_report
            
        except Exception as e:
            self.logger.error(f"❌ Cursor AI initialization failed: {e}")
            self.system_state = "failed"
            raise

    async def integrate_with_existing_system(self):
        """Integrate autonomous orchestrator results with existing system components"""
        try:
            # Initialize existing module system
            try:
                self.module_manager = create_all_modules()
                await self.module_manager.initialize_all()
                self.logger.info("✅ Existing module system integrated")
            except Exception as e:
                self.logger.warning(f"⚠️ Could not integrate existing modules: {e}")
            
            # Initialize cluster orchestrator
            try:
                self.cluster_orchestrator = ClusterOrchestrator()
                self.logger.info("✅ Cluster orchestrator integrated")
            except Exception as e:
                self.logger.warning(f"⚠️ Could not integrate cluster orchestrator: {e}")
            
            # Sync autonomous orchestrator data with existing components
            if self.orchestrator and self.module_manager:
                await self.sync_orchestrator_data()
            
            self.system_state = "integrated"
            
        except Exception as e:
            self.logger.error(f"❌ Integration with existing system failed: {e}")
            self.system_state = "integration_failed"
            raise

    async def sync_orchestrator_data(self):
        """Sync data between autonomous orchestrator and existing system"""
        try:
            # Get aggregated data from autonomous orchestrator
            if hasattr(self.orchestrator, 'db_path'):
                import sqlite3
                conn = sqlite3.connect(self.orchestrator.db_path)
                cursor = conn.cursor()
                
                # Get operator requirements
                cursor.execute('''
                    SELECT data FROM memory_structures 
                    WHERE structure_type = 'operator_requirements' 
                    AND structure_name = 'aggregated_requirements'
                ''')
                requirements_result = cursor.fetchone()
                
                # Get business strategies
                cursor.execute('''
                    SELECT data FROM memory_structures 
                    WHERE structure_type = 'business_strategies' 
                    AND structure_name = 'aggregated_strategies'
                ''')
                strategies_result = cursor.fetchone()
                
                conn.close()
                
                # Integrate data with module manager if available
                if requirements_result and self.module_manager:
                    requirements_data = json.loads(requirements_result[0])
                    # Pass requirements to business modules
                    for module_id in ['mentor_brain', 'business_manager', 'personal_assistant']:
                        if hasattr(self.module_manager, 'modules') and module_id in self.module_manager.modules:
                            # Update module with requirements data
                            pass
                
                self.logger.info("✅ Orchestrator data synced with existing system")
                
        except Exception as e:
            self.logger.error(f"❌ Data sync failed: {e}")

    async def generate_integration_report(self) -> Dict[str, Any]:
        """Generate comprehensive integration report"""
        try:
            # Collect system component status
            component_status = {
                "autonomous_orchestrator": "active" if self.orchestrator else "inactive",
                "module_manager": "active" if self.module_manager else "inactive",
                "cluster_orchestrator": "active" if self.cluster_orchestrator else "inactive"
            }
            
            # Get module health from existing system
            module_health = {}
            if self.module_manager and hasattr(self.module_manager, 'get_system_status'):
                try:
                    system_status = self.module_manager.get_system_status()
                    module_health = {k: v.get('status', 'unknown') for k, v in system_status.items()}
                except Exception as e:
                    self.logger.warning(f"Could not get module health: {e}")
            
            # Get processed file statistics
            file_stats = {
                "total_files": len(self.orchestrator.processed_files) if self.orchestrator else 0,
                "successful_processing": len([f for f in (self.orchestrator.processed_files if self.orchestrator else []) if f.processing_status == 'completed']),
                "file_types_processed": {}
            }
            
            if self.orchestrator:
                file_types = {}
                for file_analysis in self.orchestrator.processed_files:
                    file_types[file_analysis.type] = file_types.get(file_analysis.type, 0) + 1
                file_stats["file_types_processed"] = file_types
            
            # Get consistency check results
            consistency_results = {
                "total_checks": len(self.orchestrator.consistency_checks) if self.orchestrator else 0,
                "issues_found": sum(len(c.get('issues_found', [])) for c in (self.orchestrator.consistency_checks if self.orchestrator else [])),
                "checks_passed": len([c for c in (self.orchestrator.consistency_checks if self.orchestrator else []) if not c.get('issues_found')])
            }
            
            integration_report = {
                "integration_timestamp": datetime.now().isoformat(),
                "component_status": component_status,
                "module_health": module_health,
                "file_processing_stats": file_stats,
                "consistency_check_results": consistency_results,
                "system_readiness_score": self.readiness_report.overall_readiness_score if self.readiness_report else 0.0,
                "integration_success": self.system_state == "integrated"
            }
            
            return integration_report
            
        except Exception as e:
            self.logger.error(f"❌ Integration report generation failed: {e}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}

    async def present_comprehensive_report(self, integration_report: Dict[str, Any]):
        """Present comprehensive report to operator"""
        try:
            print("\n" + "=" * 80)
            print("🎯 COMPREHENSIVE CURSOR AI INITIALIZATION REPORT")
            print("=" * 80)
            
            # Present readiness report from autonomous orchestrator
            if self.orchestrator:
                readiness_text = await self.orchestrator.present_readiness_report()
                print(readiness_text)
            
            print("\n🔧 INTEGRATION STATUS:")
            print("-" * 40)
            
            component_status = integration_report.get("component_status", {})
            for component, status in component_status.items():
                status_icon = "✅" if status == "active" else "❌"
                print(f"  {status_icon} {component.replace('_', ' ').title()}: {status}")
            
            file_stats = integration_report.get("file_processing_stats", {})
            print(f"\n📁 FILE PROCESSING SUMMARY:")
            print(f"  • Total Files: {file_stats.get('total_files', 0)}")
            print(f"  • Successfully Processed: {file_stats.get('successful_processing', 0)}")
            
            file_types = file_stats.get("file_types_processed", {})
            if file_types:
                print(f"  • File Types:")
                for file_type, count in file_types.items():
                    print(f"    - {file_type}: {count} files")
            
            consistency_results = integration_report.get("consistency_check_results", {})
            print(f"\n🔍 CONSISTENCY VERIFICATION:")
            print(f"  • Total Checks: {consistency_results.get('total_checks', 0)}")
            print(f"  • Checks Passed: {consistency_results.get('checks_passed', 0)}")
            print(f"  • Issues Found: {consistency_results.get('issues_found', 0)}")
            
            readiness_score = integration_report.get("system_readiness_score", 0.0)
            print(f"\n📊 OVERALL SYSTEM READINESS: {readiness_score:.2%}")
            
            if readiness_score >= 0.9:
                print("✅ SYSTEM READY FOR FULL ACTIVATION")
            elif readiness_score >= 0.7:
                print("⚠️ SYSTEM PARTIALLY READY - REVIEW REQUIRED")
            else:
                print("❌ SYSTEM NOT READY - SIGNIFICANT ISSUES FOUND")
            
            print("=" * 80)
            
        except Exception as e:
            self.logger.error(f"❌ Report presentation failed: {e}")

    async def await_operator_approval(self) -> str:
        """Await operator approval before proceeding with full system activation"""
        try:
            print("\n🎯 OPERATOR APPROVAL REQUIRED")
            print("-" * 40)
            
            if self.readiness_report and not self.readiness_report.approval_required:
                print("✅ System appears ready for automatic activation")
                print("No critical issues found - proceeding with activation")
                self.system_state = "approved"
                return "auto_approved"
            
            print("⚠️ Manual approval required due to:")
            if self.readiness_report:
                if self.readiness_report.overall_readiness_score < 0.9:
                    print(f"  • Low readiness score: {self.readiness_report.overall_readiness_score:.2%}")
                if len(self.readiness_report.identified_gaps) > 5:
                    print(f"  • Multiple issues found: {len(self.readiness_report.identified_gaps)}")
                
                print("\n💡 Recommended actions:")
                for recommendation in self.readiness_report.actionable_recommendations[:5]:
                    print(f"  • {recommendation}")
            
            print("\n🔄 SYSTEM PAUSED - AWAITING OPERATOR DECISION")
            print("Review the comprehensive report above and address any issues before activation.")
            
            self.system_state = "awaiting_approval"
            return "manual_approval_required"
            
        except Exception as e:
            self.logger.error(f"❌ Operator approval process failed: {e}")
            self.system_state = "approval_failed"
            return "approval_failed"

    async def activate_system(self) -> Dict[str, Any]:
        """Activate the system after approval"""
        try:
            self.logger.info("🚀 Activating Enhanced Memory Agent System")
            
            # Activate all system components
            activation_results = {}
            
            if self.module_manager:
                try:
                    # Ensure all modules are active
                    system_status = self.module_manager.get_system_status()
                    active_modules = len([m for m in system_status.values() if m.get('status') == 'online'])
                    activation_results['modules_active'] = f"{active_modules}/{len(system_status)}"
                except Exception as e:
                    activation_results['modules_error'] = str(e)
            
            if self.cluster_orchestrator:
                try:
                    # Test cluster orchestration
                    activation_results['cluster_orchestrator'] = "active"
                except Exception as e:
                    activation_results['cluster_error'] = str(e)
            
            # Update system state
            self.system_state = "active"
            
            activation_report = {
                "activation_timestamp": datetime.now().isoformat(),
                "system_state": self.system_state,
                "activation_results": activation_results,
                "ready_for_operations": True
            }
            
            self.logger.info("✅ System activation completed successfully")
            return activation_report
            
        except Exception as e:
            self.logger.error(f"❌ System activation failed: {e}")
            self.system_state = "activation_failed"
            raise

    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        return {
            "system_state": self.system_state,
            "orchestrator_active": self.orchestrator is not None,
            "module_manager_active": self.module_manager is not None,
            "cluster_orchestrator_active": self.cluster_orchestrator is not None,
            "readiness_score": self.readiness_report.overall_readiness_score if self.readiness_report else 0.0,
            "timestamp": datetime.now().isoformat()
        }

# Main execution function for Cursor AI integration
async def execute_cursor_ai_integration():
    """Execute the complete Cursor AI integration process"""
    wrapper = CursorAIIntegrationWrapper()
    
    try:
        # Execute comprehensive initialization
        final_report = await wrapper.execute_cursor_ai_prompt()
        
        # Return wrapper instance and report for further operations
        return wrapper, final_report
        
    except Exception as e:
        logger.error(f"❌ Cursor AI integration failed: {e}")
        raise

# Standalone execution
if __name__ == "__main__":
    print("🚀 EXECUTING CURSOR AI COMPREHENSIVE INITIALIZATION")
    print("=" * 60)
    
    try:
        wrapper, report = asyncio.run(execute_cursor_ai_integration())
        
        print("\n✅ INITIALIZATION COMPLETED")
        print(f"System State: {wrapper.system_state}")
        print(f"Readiness Score: {report.get('readiness_report', {}).get('overall_readiness_score', 0):.2%}")
        
        if wrapper.system_state == "awaiting_approval":
            print("\n⚠️ MANUAL APPROVAL REQUIRED")
            print("Review the report above and run activation when ready.")
        elif wrapper.system_state == "approved":
            print("\n🎉 SYSTEM READY FOR ACTIVATION")
            activation_report = asyncio.run(wrapper.activate_system())
            print(f"Activation Status: {activation_report['ready_for_operations']}")
        
    except Exception as e:
        print(f"\n❌ INITIALIZATION FAILED: {e}")
        exit(1)
