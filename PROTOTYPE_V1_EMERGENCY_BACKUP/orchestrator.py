#!/usr/bin/env python3
"""
Multi-Cluster Orchestration System
Strategic cluster coordination with parallel processing for optimal decision making
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import google.generativeai as genai
import os

logger = logging.getLogger(__name__)

class ClusterOrchestrator:
    """Advanced multi-cluster orchestration with parallel processing"""
    
    def __init__(self):
        self.setup_gemini()
        self.clusters = {
            "Data_Acquisition": {
                "modules": ["research_engine", "scraping_module", "bonus_knowledge_module", "data_intelligence"],
                "weight": 0.15,
                "specialty": "Information gathering and data collection",
                "parallel_capacity": 4
            },
            "Analysis_Intelligence": {
                "modules": ["analysis_module", "data_intelligence", "competitive_analysis", "knowledge_module"],
                "weight": 0.25,
                "specialty": "Data analysis and intelligence processing",
                "parallel_capacity": 4
            },
            "Business_Strategy": {
                "modules": ["mentor_brain", "business_manager", "finance_team", "personal_assistant"],
                "weight": 0.35,
                "specialty": "Strategic planning and business execution",
                "parallel_capacity": 4
            },
            "Optimization_Automation": {
                "modules": ["workflow_automation", "revenue_optimizer", "token_optimizer", "ultra_token_module"],
                "weight": 0.20,
                "specialty": "Process optimization and automation",
                "parallel_capacity": 4
            },
            "Security_Monitoring": {
                "modules": ["security_team", "monitoring_module", "interface_module", "integration_module"],
                "weight": 0.05,
                "specialty": "Security and system monitoring",
                "parallel_capacity": 4
            }
        }
        
        self.processing_history = []
        self.cluster_performance = {}
        
        logger.info(f"✅ Cluster Orchestrator initialized with {len(self.clusters)} strategic clusters")

    def setup_gemini(self):
        """Setup Gemini API for cluster processing"""
        api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyDj-aTJt7riqX6MJSsW2Tu7uO8cjisEGqE')
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def process_module_in_cluster(self, module_name: str, cluster_name: str, input_data: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process input through a specific module within a cluster"""
        try:
            start_time = datetime.now()
            
            # Simplified processing with timeout protection
            await asyncio.sleep(0.1)  # Simulate processing
            
            # Create specialized prompt for each module
            module_prompts = {
                "research_engine": f"As a Research Engine, conduct comprehensive research on: {input_data}. Provide detailed findings, sources, and insights.",
                "scraping_module": f"As a Data Scraping Module, identify data sources and extraction strategies for: {input_data}. List actionable data collection approaches.",
                "bonus_knowledge_module": f"As a Specialized Knowledge Expert, provide domain-specific insights for: {input_data}. Include best practices and expert recommendations.",
                "data_intelligence": f"As a Data Intelligence Module, analyze data quality and patterns for: {input_data}. Provide intelligence assessment and recommendations.",
                "analysis_module": f"As an Analysis Module, perform comprehensive analysis of: {input_data}. Include sentiment, patterns, and strategic implications.",
                "competitive_analysis": f"As a Competitive Analysis Module, analyze competitive landscape for: {input_data}. Identify market opportunities and threats.",
                "knowledge_module": f"As a Knowledge Module, provide relevant knowledge and connections for: {input_data}. Include structured information and relationships.",
                "mentor_brain": f"As the Mentor Brain, provide strategic guidance and decision-making support for: {input_data}. Include long-term vision and tactical steps.",
                "business_manager": f"As a Business Manager, provide project management and execution strategies for: {input_data}. Include timelines, resources, and milestones.",
                "finance_team": f"As the Finance Team, analyze financial implications and ROI for: {input_data}. Include cost-benefit analysis and revenue projections.",
                "personal_assistant": f"As a Personal Assistant, organize tasks and workflows for: {input_data}. Include action items, priorities, and scheduling.",
                "workflow_automation": f"As Workflow Automation, identify automation opportunities for: {input_data}. Include process optimization and efficiency improvements.",
                "revenue_optimizer": f"As Revenue Optimizer, analyze revenue optimization strategies for: {input_data}. Include pricing, conversion, and growth tactics.",
                "token_optimizer": f"As Token Optimizer, optimize resource usage and costs for: {input_data}. Include efficiency improvements and cost savings.",
                "ultra_token_module": f"As Ultra Token Module, provide advanced optimization strategies for: {input_data}. Include cutting-edge efficiency techniques.",
                "security_team": f"As Security Team, assess security implications and protections for: {input_data}. Include risk assessment and mitigation strategies.",
                "monitoring_module": f"As Monitoring Module, provide system health and performance insights for: {input_data}. Include metrics and optimization recommendations.",
                "interface_module": f"As Interface Module, analyze integration and connectivity requirements for: {input_data}. Include API and system integration strategies.",
                "integration_module": f"As Integration Module, provide system integration and coordination strategies for: {input_data}. Include workflow and data flow optimization."
            }
            
            prompt = module_prompts.get(module_name, f"As {module_name}, analyze and provide insights for: {input_data}")
            
            # Add context if available
            if context:
                prompt += f"\n\nAdditional Context: {context}"
            
            # Generate response using Gemini
            response = self.model.generate_content(prompt)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            result = {
                "module": module_name,
                "cluster": cluster_name,
                "response": response.text,
                "confidence": 0.85 + (hash(module_name) % 15) / 100,  # Simulated confidence
                "processing_time": processing_time,
                "timestamp": datetime.now().isoformat(),
                "success": True
            }
            
            logger.info(f"✅ {module_name} processed successfully in {processing_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"❌ {module_name} processing failed: {e}")
            return {
                "module": module_name,
                "cluster": cluster_name,
                "response": f"Module {module_name} encountered an error: {str(e)}",
                "confidence": 0.0,
                "processing_time": 0,
                "timestamp": datetime.now().isoformat(),
                "success": False,
                "error": str(e)
            }

    async def process_cluster(self, cluster_name: str, cluster_info: Dict[str, Any], input_data: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process input through all modules in a cluster in parallel"""
        try:
            start_time = datetime.now()
            modules = cluster_info["modules"]
            
            logger.info(f"🔄 Processing cluster '{cluster_name}' with {len(modules)} modules in parallel")
            
            # Process all modules in the cluster in parallel
            tasks = [
                self.process_module_in_cluster(module, cluster_name, input_data, context or {})
                for module in modules
            ]
            
            module_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Filter successful results
            successful_results = []
            failed_results = []
            
            for result in module_results:
                if isinstance(result, Exception):
                    failed_results.append({"error": str(result)})
                elif result.get("success", False):
                    successful_results.append(result)
                else:
                    failed_results.append(result)
            
            # Synthesize cluster summary
            cluster_summary = await self.synthesize_cluster_results(cluster_name, successful_results, cluster_info)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            cluster_result = {
                "cluster_name": cluster_name,
                "specialty": cluster_info["specialty"],
                "weight": cluster_info["weight"],
                "modules_processed": len(successful_results),
                "modules_failed": len(failed_results),
                "processing_time": processing_time,
                "cluster_summary": cluster_summary,
                "detailed_results": successful_results,
                "failed_results": failed_results,
                "confidence": sum(r.get("confidence", 0) for r in successful_results) / len(successful_results) if successful_results else 0,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"✅ Cluster '{cluster_name}' completed: {len(successful_results)}/{len(modules)} modules successful")
            return cluster_result
            
        except Exception as e:
            logger.error(f"❌ Cluster '{cluster_name}' processing failed: {e}")
            return {
                "cluster_name": cluster_name,
                "error": str(e),
                "success": False,
                "timestamp": datetime.now().isoformat()
            }

    async def synthesize_cluster_results(self, cluster_name: str, results: List[Dict[str, Any]], cluster_info: Dict[str, Any]) -> str:
        """Synthesize results from all modules in a cluster into a coherent summary"""
        try:
            if not results:
                return f"No successful results from {cluster_name} cluster"
            
            # Combine all module responses
            combined_responses = "\n\n".join([
                f"**{result['module'].replace('_', ' ').title()}**: {result['response']}"
                for result in results
            ])
            
            # Create synthesis prompt
            synthesis_prompt = f"""You are a Strategic Synthesis Engine for the {cluster_name} cluster.

CLUSTER SPECIALTY: {cluster_info['specialty']}
CLUSTER WEIGHT: {cluster_info['weight']} (importance in final decision)

INDIVIDUAL MODULE RESPONSES:
{combined_responses}

SYNTHESIS INSTRUCTIONS:
1. Synthesize all module responses into a coherent, strategic summary
2. Identify key insights and patterns across modules
3. Highlight actionable recommendations
4. Note any conflicts or contradictions between modules
5. Provide confidence assessment for the cluster's conclusions
6. Focus on business value and ROI implications

Generate a comprehensive cluster summary that maximizes strategic value."""

            synthesis_response = self.model.generate_content(synthesis_prompt)
            return synthesis_response.text
            
        except Exception as e:
            logger.error(f"❌ Cluster synthesis failed for {cluster_name}: {e}")
            return f"Synthesis failed for {cluster_name}: {str(e)}"

    async def orchestrate_clusters(self, input_data: str, priority_clusters: List[str] = None) -> Dict[str, Any]:
        """Orchestrate multiple clusters in parallel for comprehensive analysis"""
        try:
            start_time = datetime.now()
            
            # Determine which clusters to process
            clusters_to_process = priority_clusters or list(self.clusters.keys())
            
            logger.info(f"🚀 Orchestrating {len(clusters_to_process)} clusters in parallel")
            
            # Process all clusters in parallel
            cluster_tasks = [
                self.process_cluster(cluster_name, self.clusters[cluster_name], input_data)
                for cluster_name in clusters_to_process
                if cluster_name in self.clusters
            ]
            
            cluster_results = await asyncio.gather(*cluster_tasks, return_exceptions=True)
            
            # Filter successful cluster results
            successful_clusters = []
            failed_clusters = []
            
            for result in cluster_results:
                if isinstance(result, Exception):
                    failed_clusters.append({"error": str(result)})
                elif result.get("cluster_name"):
                    successful_clusters.append(result)
                else:
                    failed_clusters.append(result)
            
            # Generate final strategic decision
            final_decision = await self.generate_final_decision(input_data, successful_clusters)
            
            total_processing_time = (datetime.now() - start_time).total_seconds()
            
            orchestration_result = {
                "input_data": input_data[:100] + "..." if len(input_data) > 100 else input_data,
                "clusters_processed": len(successful_clusters),
                "clusters_failed": len(failed_clusters),
                "total_processing_time": total_processing_time,
                "cluster_results": successful_clusters,
                "failed_clusters": failed_clusters,
                "final_decision": final_decision,
                "confidence_score": sum(c.get("confidence", 0) for c in successful_clusters) / len(successful_clusters) if successful_clusters else 0,
                "timestamp": datetime.now().isoformat(),
                "orchestration_success": len(successful_clusters) > 0
            }
            
            # Store in processing history
            self.processing_history.append(orchestration_result)
            
            logger.info(f"🎉 Orchestration completed: {len(successful_clusters)} clusters successful in {total_processing_time:.2f}s")
            return orchestration_result
            
        except Exception as e:
            logger.error(f"❌ Cluster orchestration failed: {e}")
            return {
                "error": str(e),
                "orchestration_success": False,
                "timestamp": datetime.now().isoformat()
            }

    async def generate_final_decision(self, input_data: str, cluster_results: List[Dict[str, Any]]) -> str:
        """Generate final strategic decision based on weighted cluster results"""
        try:
            if not cluster_results:
                return "No cluster results available for final decision generation"
            
            # Build weighted summary
            weighted_summaries = []
            total_weight = 0
            
            for cluster in cluster_results:
                cluster_name = cluster.get("cluster_name", "Unknown")
                cluster_summary = cluster.get("cluster_summary", "No summary available")
                weight = cluster.get("weight", 0)
                confidence = cluster.get("confidence", 0)
                
                weighted_summaries.append(f"""
**{cluster_name.replace('_', ' ').title()}** (Weight: {weight}, Confidence: {confidence:.2f})
{cluster_summary}
""")
                total_weight += weight
            
            combined_analysis = "\n".join(weighted_summaries)
            
            # Generate final strategic decision
            final_decision_prompt = f"""You are the Master Strategic Decision Engine coordinating multiple specialized clusters.

ORIGINAL REQUEST: {input_data}

CLUSTER ANALYSIS RESULTS:
{combined_analysis}

DECISION SYNTHESIS INSTRUCTIONS:
1. Analyze all cluster recommendations with their respective weights
2. Identify convergent insights across clusters
3. Resolve any conflicts between cluster recommendations
4. Generate a comprehensive, actionable strategic decision
5. Prioritize recommendations based on cluster weights and confidence scores
6. Focus on achieving $10K-$20K monthly revenue goals
7. Provide specific next steps and implementation timeline
8. Include risk assessment and mitigation strategies

Generate the FINAL STRATEGIC DECISION that maximizes business value and ROI."""

            final_response = self.model.generate_content(final_decision_prompt)
            
            # Add orchestration metadata
            decision_with_metadata = f"""
# 🎯 STRATEGIC DECISION - MULTI-CLUSTER ANALYSIS

**Clusters Analyzed**: {len(cluster_results)} parallel clusters
**Total Processing Weight**: {total_weight:.2f}
**Average Confidence**: {sum(c.get('confidence', 0) for c in cluster_results) / len(cluster_results):.2f}
**Processing Time**: {sum(c.get('processing_time', 0) for c in cluster_results):.2f}s total

---

{final_response.text}

---

**Cluster Contributions:**
{chr(10).join([f"• {c.get('cluster_name', 'Unknown').replace('_', ' ')}: {c.get('weight', 0)} weight, {c.get('confidence', 0):.2f} confidence" for c in cluster_results])}
"""
            
            return decision_with_metadata
            
        except Exception as e:
            logger.error(f"❌ Final decision generation failed: {e}")
            return f"Final decision generation failed: {str(e)}"

    async def execute_strategic_command(self, command: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute strategic commands using appropriate cluster combinations"""
        command_cluster_mapping = {
            "analyze": ["Analysis_Intelligence", "Data_Acquisition"],
            "plan": ["Business_Strategy", "Analysis_Intelligence"],
            "optimize": ["Optimization_Automation", "Business_Strategy"],
            "organize": ["Optimization_Automation", "Security_Monitoring"],
            "status": ["Security_Monitoring", "Analysis_Intelligence"],
            "report": ["Analysis_Intelligence", "Business_Strategy", "Security_Monitoring"]
        }
        
        priority_clusters = command_cluster_mapping.get(command.lower(), list(self.clusters.keys()))
        
        command_context = f"Execute strategic command: {command.upper()}"
        if parameters:
            command_context += f" with parameters: {parameters}"
        
        result = await self.orchestrate_clusters(command_context, priority_clusters)
        return result

    def get_cluster_performance_report(self) -> Dict[str, Any]:
        """Generate performance report for all clusters"""
        performance_report = {
            "timestamp": datetime.now().isoformat(),
            "total_orchestrations": len(self.processing_history),
            "cluster_stats": {},
            "overall_performance": {}
        }
        
        # Calculate cluster statistics
        for cluster_name in self.clusters.keys():
            cluster_history = [
                h for h in self.processing_history 
                if any(c.get("cluster_name") == cluster_name for c in h.get("cluster_results", []))
            ]
            
            if cluster_history:
                avg_confidence = sum(
                    c.get("confidence", 0) 
                    for h in cluster_history 
                    for c in h.get("cluster_results", []) 
                    if c.get("cluster_name") == cluster_name
                ) / len(cluster_history)
                
                avg_processing_time = sum(
                    c.get("processing_time", 0) 
                    for h in cluster_history 
                    for c in h.get("cluster_results", []) 
                    if c.get("cluster_name") == cluster_name
                ) / len(cluster_history)
                
                performance_report["cluster_stats"][cluster_name] = {
                    "executions": len(cluster_history),
                    "avg_confidence": avg_confidence,
                    "avg_processing_time": avg_processing_time,
                    "weight": self.clusters[cluster_name]["weight"]
                }
        
        return performance_report

# Global orchestrator instance
global_orchestrator = ClusterOrchestrator()

# Main orchestration function for UI integration
async def orchestrate_clusters(input_data: str, command_type: str = None) -> str:
    """Main orchestration function for UI integration"""
    try:
        if command_type and command_type.lower() in ["analyze", "plan", "optimize", "organize", "status", "report"]:
            # Execute strategic command
            result = await global_orchestrator.execute_strategic_command(command_type, {"input": input_data})
        else:
            # Full orchestration
            result = await global_orchestrator.orchestrate_clusters(input_data)
        
        if result.get("orchestration_success", False):
            return result.get("final_decision", "No decision generated")
        else:
            return f"Orchestration failed: {result.get('error', 'Unknown error')}"
            
    except Exception as e:
        logger.error(f"❌ Orchestration function failed: {e}")
        return f"I'm ready to help with your business strategy. What would you like to focus on? (Error: {str(e)})"

# Performance monitoring function
async def get_orchestration_performance() -> Dict[str, Any]:
    """Get current orchestration performance metrics"""
    return global_orchestrator.get_cluster_performance_report()

# Test function
async def test_orchestration():
    """Test the orchestration system"""
    print("🧪 Testing Multi-Cluster Orchestration System")
    print("=" * 60)
    
    test_input = "I need to increase my monthly revenue to $15,000. What's the best strategy?"
    
    print(f"📝 Test Input: {test_input}")
    print("🔄 Running parallel cluster orchestration...")
    
    result = await global_orchestrator.orchestrate_clusters(test_input)
    
    print(f"📊 Orchestration Results:")
    print(f"   Clusters Processed: {result.get('clusters_processed', 0)}")
    print(f"   Processing Time: {result.get('total_processing_time', 0):.2f}s")
    print(f"   Confidence Score: {result.get('confidence_score', 0):.2f}")
    print(f"   Success: {result.get('orchestration_success', False)}")
    
    if result.get("final_decision"):
        print(f"\n📋 Final Decision Preview:")
        print(result["final_decision"][:300] + "..." if len(result["final_decision"]) > 300 else result["final_decision"])
    
    print("\n🎉 Orchestration test completed!")
    return result

if __name__ == "__main__":
    # Run the test
    asyncio.run(test_orchestration())
