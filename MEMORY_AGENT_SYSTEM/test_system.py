#!/usr/bin/env python3
"""
Comprehensive System Test
"""

import time
import sys

def test_imports():
    """Test all system imports"""
    print("🔍 Testing system imports...")
    
    try:
        import ssi_enhanced_system_fixed
        print("✅ SSI Enhanced System Fixed - Import PASSED")
    except Exception as e:
        print(f"❌ SSI Enhanced System Fixed - Import FAILED: {e}")
        return False
    
    try:
        from loop_prevention_system_fixed import ssi_safe_execute
        print("✅ Loop Prevention System - Import PASSED")
    except Exception as e:
        print(f"❌ Loop Prevention System - Import FAILED: {e}")
        return False
    
    try:
        from input_analysis_system import analyze_user_input
        print("✅ Input Analysis System - Import PASSED")
    except Exception as e:
        print(f"❌ Input Analysis System - Import FAILED: {e}")
        return False
    
    try:
        from ssi_compliance_system import SSIComplianceSystem
        print("✅ SSI Compliance System - Import PASSED")
    except Exception as e:
        print(f"❌ SSI Compliance System - Import FAILED: {e}")
        return False
    
    try:
        import google.generativeai as genai
        print("✅ Gemini API - Import PASSED")
    except Exception as e:
        print(f"❌ Gemini API - Import FAILED: {e}")
        return False
    
    return True

def test_loop_prevention():
    """Test loop prevention system"""
    print("\n🔍 Testing loop prevention system...")
    
    try:
        from loop_prevention_system_fixed import ssi_safe_execute
        
        def test_function():
            return 'Test successful'
        
        result, error = ssi_safe_execute(test_function, 'test_function')
        
        if error:
            print(f"❌ Loop Prevention - Execution FAILED: {error}")
            return False
        else:
            print(f"✅ Loop Prevention - Execution PASSED: {result}")
            return True
            
    except Exception as e:
        print(f"❌ Loop Prevention - Test FAILED: {e}")
        return False

def test_input_analysis():
    """Test input analysis system"""
    print("\n🔍 Testing input analysis system...")
    
    try:
        from input_analysis_system import analyze_user_input
        
        test_input = "YOU WERE LOOPING FOR 2 OF YOUR TESTS"
        analysis = analyze_user_input(test_input)
        
        if 'keywords_found' in analysis:
            print(f"✅ Input Analysis - Test PASSED: {len(analysis['keywords_found'])} keywords found")
            return True
        else:
            print("❌ Input Analysis - Test FAILED: No keywords found")
            return False
            
    except Exception as e:
        print(f"❌ Input Analysis - Test FAILED: {e}")
        return False

def test_gemini_api():
    """Test Gemini API connection"""
    print("\n🔍 Testing Gemini API connection...")
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv('GEMINI_API_KEY', ''))
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = model.generate_content("Test message")
        
        if response.text:
            print(f"✅ Gemini API - Connection PASSED: {response.text[:50]}...")
            return True
        else:
            print("❌ Gemini API - Connection FAILED: No response")
            return False
            
    except Exception as e:
        print(f"❌ Gemini API - Connection FAILED: {e}")
        return False

def test_ssi_compliance():
    """Test SSI compliance system"""
    print("\n🔍 Testing SSI compliance system...")
    
    try:
        from ssi_compliance_system import SSIComplianceSystem
        
        ssi_system = SSIComplianceSystem()
        
        if ssi_system:
            print("✅ SSI Compliance System - Initialization PASSED")
            return True
        else:
            print("❌ SSI Compliance System - Initialization FAILED")
            return False
            
    except Exception as e:
        print(f"❌ SSI Compliance System - Test FAILED: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 SSI-ENHANCED ULTIMATE MEMORY AGENT SYSTEM - COMPREHENSIVE TEST")
    print("=" * 70)
    
    tests = [
        test_imports,
        test_loop_prevention,
        test_input_analysis,
        test_gemini_api,
        test_ssi_compliance
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 70)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ ALL TESTS PASSED - SYSTEM READY FOR PRODUCTION")
        return True
    else:
        print("❌ SOME TESTS FAILED - SYSTEM NEEDS ATTENTION")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
