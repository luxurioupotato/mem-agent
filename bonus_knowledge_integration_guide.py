
# Integration with existing orchestrator.py
# Add to ClusterOrchestrator class:

from enhanced_bonus_knowledge_system import BonusKnowledgeSystem, SpecializedBusinessTeam

def __init__(self):
    # ... existing initialization ...
    self.bonus_knowledge = BonusKnowledgeSystem()
    self.business_team = SpecializedBusinessTeam()
    
def enhance_module_processing(self, module_name, base_prompt):
    # Enhance with bonus knowledge
    enhanced_prompt = self.bonus_knowledge.enhance_module_prompt(module_name, base_prompt)
    
    # Further enhance with business team specialization if applicable
    if module_name in self.business_team.team_specializations:
        enhanced_prompt = self.business_team.get_enhanced_team_prompt(module_name, enhanced_prompt)
    
    return enhanced_prompt
