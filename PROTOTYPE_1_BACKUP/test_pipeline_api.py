#!/usr/bin/env python3
"""
Test Client for Enhanced Memory Agent Pipeline Automation API
Demonstrates the forever-evolving AI system with persistent memory and recursive self-improvement
"""

import requests
import json
import time
import uuid
from datetime import datetime

API_BASE_URL = "http://localhost:5000"

class PipelineAPITestClient:
    """Test client for the Enhanced Memory Agent Pipeline API"""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.conversation_id = str(uuid.uuid4())
        print(f"🧪 Test client initialized with conversation ID: {self.conversation_id}")

    def test_health_check(self):
        """Test the health check endpoint"""
        print("\n🔍 Testing health check endpoint...")
        try:
            response = requests.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                print("✅ Health check passed!")
                print(f"   Status: {data['status']}")
                print(f"   Total interactions: {data['statistics']['total_interactions']}")
                print(f"   Total conversations: {data['statistics']['total_conversations']}")
                print(f"   Average confidence: {data['statistics']['average_confidence']:.2%}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False

    def test_chat_interaction(self, user_input: str, template_type: str = "default"):
        """Test a chat interaction"""
        print(f"\n💬 Testing chat interaction...")
        print(f"   User: {user_input}")
        
        try:
            payload = {
                "user_input": user_input,
                "conversation_id": self.conversation_id,
                "template_type": template_type
            }
            
            start_time = time.time()
            response = requests.post(f"{self.base_url}/chat", json=payload)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Chat interaction successful!")
                print(f"   Agent: {data['response'][:200]}{'...' if len(data['response']) > 200 else ''}")
                print(f"   Processing time: {response_time:.2f}s")
                print(f"   Confidence: {data['metadata']['confidence_score']:.2%}")
                print(f"   Tokens used: {data['metadata']['tokens_used']}")
                
                if data['metadata']['improvement_suggestions']:
                    print(f"   Suggestions: {', '.join(data['metadata']['improvement_suggestions'])}")
                
                return data
            else:
                print(f"❌ Chat interaction failed: {response.status_code}")
                print(f"   Error: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Chat interaction error: {e}")
            return None

    def test_conversation_summary(self):
        """Test conversation summary retrieval"""
        print(f"\n📊 Testing conversation summary...")
        try:
            response = requests.get(f"{self.base_url}/conversation/{self.conversation_id}")
            if response.status_code == 200:
                data = response.json()
                print("✅ Conversation summary retrieved!")
                
                summary = data['conversation_summary']
                print(f"   Total interactions: {summary['total_interactions']}")
                print(f"   Average confidence: {summary['avg_confidence']:.2%}")
                print(f"   Average processing time: {summary['avg_processing_time']:.2f}s")
                
                interactions = data['recent_interactions']
                print(f"   Recent interactions: {len(interactions)}")
                
                return data
            else:
                print(f"❌ Conversation summary failed: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Conversation summary error: {e}")
            return None

    def test_analytics(self):
        """Test analytics endpoint"""
        print(f"\n📈 Testing analytics endpoint...")
        try:
            response = requests.get(f"{self.base_url}/analytics")
            if response.status_code == 200:
                data = response.json()
                print("✅ Analytics retrieved!")
                
                analytics = data['analytics']
                print(f"   Loop detections: {analytics['loop_detections']}")
                print(f"   Performance trends: {len(analytics['performance_trends'])} days")
                
                insights = data['improvement_insights']
                print("   Improvement insights:")
                for insight in insights:
                    print(f"     • {insight}")
                
                return data
            else:
                print(f"❌ Analytics failed: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Analytics error: {e}")
            return None

    def test_cursor_ai_integration(self):
        """Test Cursor AI autonomous initialization"""
        print(f"\n🤖 Testing Cursor AI integration...")
        try:
            response = requests.post(f"{self.base_url}/cursor-ai/init")
            if response.status_code == 200:
                data = response.json()
                print("✅ Cursor AI initialization successful!")
                print(f"   Status: {data['status']}")
                return data
            else:
                print(f"⚠️ Cursor AI integration: {response.status_code}")
                print(f"   Note: This may fail if Cursor AI components are not available")
                return None
        except Exception as e:
            print(f"⚠️ Cursor AI integration error: {e}")
            return None

    def test_loop_detection(self):
        """Test loop detection by sending repetitive messages"""
        print(f"\n🔄 Testing loop detection...")
        
        # Send the same message multiple times to trigger loop detection
        repetitive_message = "Can you help me with my business strategy?"
        
        responses = []
        for i in range(3):
            print(f"   Sending repetitive message #{i+1}...")
            response = self.test_chat_interaction(repetitive_message)
            if response:
                responses.append(response['response'])
                time.sleep(1)  # Brief delay between requests
        
        # Check if responses are different (indicating loop detection worked)
        if len(set(responses)) > 1:
            print("✅ Loop detection working - responses varied!")
        else:
            print("⚠️ Loop detection may not have triggered")
        
        return responses

    def run_comprehensive_test(self):
        """Run comprehensive test suite"""
        print("🚀 ENHANCED MEMORY AGENT PIPELINE API TEST SUITE")
        print("=" * 70)
        
        test_results = {}
        
        # Test 1: Health check
        test_results['health_check'] = self.test_health_check()
        
        # Test 2: Basic chat interactions
        test_interactions = [
            ("Hello! I'm testing the enhanced memory agent system.", "default"),
            ("What are the key features of this system?", "default"),
            ("How can this help me achieve $15,000 monthly revenue?", "business_strategy"),
            ("What technical capabilities does this system have?", "technical_analysis"),
            ("Give me a creative solution for customer acquisition.", "creative_problem_solving")
        ]
        
        chat_results = []
        for user_input, template_type in test_interactions:
            result = self.test_chat_interaction(user_input, template_type)
            chat_results.append(result is not None)
            time.sleep(2)  # Brief delay between interactions
        
        test_results['chat_interactions'] = all(chat_results)
        
        # Test 3: Conversation summary
        test_results['conversation_summary'] = self.test_conversation_summary() is not None
        
        # Test 4: Analytics
        test_results['analytics'] = self.test_analytics() is not None
        
        # Test 5: Loop detection
        loop_responses = self.test_loop_detection()
        test_results['loop_detection'] = len(set(loop_responses)) > 1 if loop_responses else False
        
        # Test 6: Cursor AI integration (optional)
        test_results['cursor_ai'] = self.test_cursor_ai_integration() is not None
        
        # Print test summary
        print("\n" + "=" * 70)
        print("🎯 TEST RESULTS SUMMARY")
        print("=" * 70)
        
        for test_name, result in test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name.replace('_', ' ').title()}: {status}")
        
        passed_tests = sum(test_results.values())
        total_tests = len(test_results)
        
        print(f"\nOverall: {passed_tests}/{total_tests} tests passed ({passed_tests/total_tests:.1%})")
        
        if passed_tests == total_tests:
            print("🎉 ALL TESTS PASSED! The Enhanced Memory Agent Pipeline is fully operational!")
        elif passed_tests >= total_tests * 0.8:
            print("✅ Most tests passed! System is operational with minor issues.")
        else:
            print("⚠️ Several tests failed. Check the API server and dependencies.")
        
        return test_results

def main():
    """Main test function"""
    print("🧪 Enhanced Memory Agent Pipeline API Test Client")
    print("Make sure the API server is running on http://localhost:5000")
    print("")
    
    # Wait for user confirmation
    input("Press Enter when the API server is ready...")
    
    # Run tests
    client = PipelineAPITestClient()
    results = client.run_comprehensive_test()
    
    print("\n📋 Test completed. Check the results above.")
    print("💡 Tip: Check the API server logs for detailed processing information.")

if __name__ == "__main__":
    main()
