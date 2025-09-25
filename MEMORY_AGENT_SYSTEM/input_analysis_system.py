#!/usr/bin/env python3
"""
SSI Input Analysis System
Analyzes user inputs for keywords, instructions, and requirements
"""

import re
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

class SSIInputAnalysisSystem:
    """SSI-compliant input analysis and requirement tracking"""
    
    def __init__(self):
        self.requirements_tracker = {}
        self.keyword_patterns = {
            'modules': ['module', 'agent', 'system', 'component', 'tool'],
            'functionality': ['function', 'feature', 'capability', 'ability'],
            'compliance': ['ssi', 'compliance', 'standard', 'requirement'],
            'testing': ['test', 'verify', 'check', 'validate'],
            'launch': ['launch', 'start', 'run', 'execute', 'deploy'],
            'error': ['error', 'bug', 'fix', 'debug', 'issue'],
            'loop': ['loop', 'repeat', 'cycle', 'infinite', 'timeout'],
            'scraping': ['scrape', 'extract', 'data', 'web', 'research'],
            'knowledge': ['knowledge', 'base', 'database', 'memory'],
            'token': ['token', 'efficiency', 'optimization', 'cost'],
            'industry': ['industry', 'leader', 'standard', 'benchmark'],
            'functionality': ['functionality', 'preserve', 'maintain', 'guarantee']
        }
        
    def analyze_input(self, user_input: str) -> Dict[str, Any]:
        """Analyze user input for keywords and requirements"""
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'input': user_input,
            'keywords_found': [],
            'modules_mentioned': [],
            'requirements': [],
            'instructions': [],
            'priority': 'normal',
            'action_required': False
        }
        
        # Convert to lowercase for analysis
        input_lower = user_input.lower()
        
        # Find keywords
        for category, keywords in self.keyword_patterns.items():
            for keyword in keywords:
                if keyword in input_lower:
                    analysis['keywords_found'].append({
                        'category': category,
                        'keyword': keyword,
                        'context': self._extract_context(user_input, keyword)
                    })
        
        # Extract specific requirements
        analysis['requirements'] = self._extract_requirements(user_input)
        
        # Extract instructions
        analysis['instructions'] = self._extract_instructions(user_input)
        
        # Determine priority
        analysis['priority'] = self._determine_priority(analysis)
        
        # Determine if action is required
        analysis['action_required'] = self._determine_action_required(analysis)
        
        return analysis
    
    def _extract_context(self, text: str, keyword: str) -> str:
        """Extract context around keyword"""
        pattern = f".{{0,50}}{re.escape(keyword)}.{{0,50}}"
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(0) if match else ""
    
    def _extract_requirements(self, text: str) -> List[str]:
        """Extract specific requirements from text"""
        requirements = []
        
        # Look for requirement patterns
        req_patterns = [
            r'must\s+([^.!?]+)',
            r'should\s+([^.!?]+)',
            r'need\s+([^.!?]+)',
            r'require\s+([^.!?]+)',
            r'ensure\s+([^.!?]+)',
            r'verify\s+([^.!?]+)',
            r'check\s+([^.!?]+)',
            r'validate\s+([^.!?]+)'
        ]
        
        for pattern in req_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            requirements.extend(matches)
        
        return requirements
    
    def _extract_instructions(self, text: str) -> List[str]:
        """Extract specific instructions from text"""
        instructions = []
        
        # Look for instruction patterns
        inst_patterns = [
            r'do\s+([^.!?]+)',
            r'implement\s+([^.!?]+)',
            r'create\s+([^.!?]+)',
            r'build\s+([^.!?]+)',
            r'develop\s+([^.!?]+)',
            r'design\s+([^.!?]+)',
            r'construct\s+([^.!?]+)',
            r'make\s+([^.!?]+)'
        ]
        
        for pattern in inst_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            instructions.extend(matches)
        
        return instructions
    
    def _determine_priority(self, analysis: Dict[str, Any]) -> str:
        """Determine priority based on analysis"""
        high_priority_keywords = ['error', 'bug', 'fix', 'critical', 'urgent', 'immediate']
        medium_priority_keywords = ['test', 'verify', 'check', 'validate']
        
        keywords = [kw['keyword'] for kw in analysis['keywords_found']]
        
        if any(kw in keywords for kw in high_priority_keywords):
            return 'high'
        elif any(kw in keywords for kw in medium_priority_keywords):
            return 'medium'
        else:
            return 'normal'
    
    def _determine_action_required(self, analysis: Dict[str, Any]) -> bool:
        """Determine if action is required based on analysis"""
        action_keywords = ['do', 'implement', 'create', 'build', 'develop', 'fix', 'test', 'verify']
        
        keywords = [kw['keyword'] for kw in analysis['keywords_found']]
        
        return any(kw in keywords for kw in action_keywords) or len(analysis['requirements']) > 0
    
    def track_requirement(self, requirement: str, status: str = 'pending') -> None:
        """Track requirement status"""
        self.requirements_tracker[requirement] = {
            'status': status,
            'timestamp': datetime.now().isoformat(),
            'updates': []
        }
    
    def update_requirement(self, requirement: str, status: str, note: str = '') -> None:
        """Update requirement status"""
        if requirement in self.requirements_tracker:
            self.requirements_tracker[requirement]['status'] = status
            self.requirements_tracker[requirement]['updates'].append({
                'status': status,
                'note': note,
                'timestamp': datetime.now().isoformat()
            })
    
    def get_requirements_status(self) -> Dict[str, Any]:
        """Get current requirements status"""
        return {
            'total_requirements': len(self.requirements_tracker),
            'pending': len([r for r in self.requirements_tracker.values() if r['status'] == 'pending']),
            'completed': len([r for r in self.requirements_tracker.values() if r['status'] == 'completed']),
            'failed': len([r for r in self.requirements_tracker.values() if r['status'] == 'failed']),
            'requirements': self.requirements_tracker
        }
    
    def generate_requirement_report(self) -> str:
        """Generate requirement compliance report"""
        status = self.get_requirements_status()
        
        report = f"""
📋 REQUIREMENT COMPLIANCE REPORT
================================
Total Requirements: {status['total_requirements']}
✅ Completed: {status['completed']}
⏳ Pending: {status['pending']}
❌ Failed: {status['failed']}

DETAILED STATUS:
"""
        
        for req, details in status['requirements'].items():
            status_icon = "✅" if details['status'] == 'completed' else "⏳" if details['status'] == 'pending' else "❌"
            report += f"{status_icon} {req}: {details['status']}\n"
        
        return report

# Global input analysis instance
input_analyzer = SSIInputAnalysisSystem()

def analyze_user_input(user_input: str) -> Dict[str, Any]:
    """Analyze user input for SSI compliance"""
    return input_analyzer.analyze_input(user_input)

# Test the input analysis system
if __name__ == "__main__":
    test_inputs = [
        "YOU WERE LOOPING FOR 2 OF YOUR TESTS",
        "I ASKED YOU TO JUSTIFY AND MAKE SURE ALL MY REQUESTS ARE MET",
        "SCRAPING MY INPUTS FOR EVERY KEYWORDS INSTRUCTIONS",
        "IMPLEMENTED APPROPRIATELY FOR FUNCTIONAL EXECUTION",
        "READY FOR LAUNCH AND HAS EVERYTHING I MENTIONED"
    ]
    
    for test_input in test_inputs:
        analysis = analyze_user_input(test_input)
        print(f"Input: {test_input}")
        print(f"Keywords: {[kw['keyword'] for kw in analysis['keywords_found']]}")
        print(f"Requirements: {analysis['requirements']}")
        print(f"Priority: {analysis['priority']}")
        print(f"Action Required: {analysis['action_required']}")
        print("---")
