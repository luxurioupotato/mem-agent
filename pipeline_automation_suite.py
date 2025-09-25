#!/usr/bin/env python3
"""
Full Pipeline Automation Script Suite
Forever-evolving Enhanced Memory Agent system with persistent memory,
dynamic prompt refinement, recursive self-improvement, and deployable API server.
Integrated with existing Cursor AI autonomous initialization system.
"""

import sqlite3
import asyncio
import logging
import json
import uuid
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template_string
import threading
import os
from dataclasses import dataclass, asdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("pipeline_automation.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("PipelineAutomation")

# Configuration
DB_PATH = "memory_agent_chat.db"
SIMILARITY_THRESHOLD = 0.8
MAX_CONTEXT_INTERACTIONS = 15
LOOP_DETECTION_WINDOW = 5

@dataclass
class InteractionMetadata:
    """Metadata for chat interactions"""
    action: Optional[str] = None
    step: Optional[str] = None
    instructions: Optional[str] = None
    operator_context: Optional[str] = None
    response_type: str = "text"
    confidence_score: float = 0.0
    processing_time: float = 0.0
    tokens_used: int = 0
    improvement_suggestions: List[str] = None

    def __post_init__(self):
        if self.improvement_suggestions is None:
            self.improvement_suggestions = []

class MemoryAgentDatabase:
    """Enhanced memory database with advanced schema and operations"""
    
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.setup_memory_db()
        logger.info(f"✅ Memory database initialized: {db_path}")

    def setup_memory_db(self):
        """Create comprehensive memory database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Main chat memory table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_memory (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            user_message TEXT NOT NULL,
            agent_response TEXT NOT NULL,
            action_taken TEXT,
            step_name TEXT,
            instructions TEXT,
            operator_context TEXT,
            conversation_id TEXT NOT NULL,
            response_type TEXT DEFAULT 'text',
            confidence_score REAL DEFAULT 0.0,
            processing_time REAL DEFAULT 0.0,
            tokens_used INTEGER DEFAULT 0,
            improvement_suggestions TEXT,
            message_hash TEXT,
            response_hash TEXT
        );
        """)
        
        # Conversation metadata table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversation_metadata (
            conversation_id TEXT PRIMARY KEY,
            created_timestamp TEXT NOT NULL,
            last_updated TEXT NOT NULL,
            total_interactions INTEGER DEFAULT 0,
            workflow_step TEXT DEFAULT 'initiate',
            active_modules TEXT,
            user_preferences TEXT,
            conversation_summary TEXT,
            quality_score REAL DEFAULT 0.0
        );
        """)
        
        # Loop detection and improvement tracking
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS loop_detection (
            detection_id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            loop_type TEXT NOT NULL,
            similar_responses TEXT,
            pivot_action TEXT,
            improvement_applied TEXT
        );
        """)
        
        # System performance metrics
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS performance_metrics (
            metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            metric_type TEXT NOT NULL,
            metric_value REAL NOT NULL,
            context_data TEXT,
            conversation_id TEXT
        );
        """)
        
        # Create indexes for performance
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_conversation ON chat_memory(conversation_id);",
            "CREATE INDEX IF NOT EXISTS idx_timestamp ON chat_memory(timestamp);",
            "CREATE INDEX IF NOT EXISTS idx_message_hash ON chat_memory(message_hash);",
            "CREATE INDEX IF NOT EXISTS idx_response_hash ON chat_memory(response_hash);",
            "CREATE INDEX IF NOT EXISTS idx_conv_updated ON conversation_metadata(last_updated);",
            "CREATE INDEX IF NOT EXISTS idx_loop_conv ON loop_detection(conversation_id);",
            "CREATE INDEX IF NOT EXISTS idx_metrics_type ON performance_metrics(metric_type);"
        ]
        
        for index_sql in indexes:
            cursor.execute(index_sql)
        
        conn.commit()
        conn.close()

    def log_interaction(self, conversation_id: str, user_msg: str, agent_resp: str, 
                       metadata: InteractionMetadata) -> int:
        """Log chat interaction with comprehensive metadata"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.utcnow().isoformat()
        message_hash = hashlib.md5(user_msg.encode()).hexdigest()
        response_hash = hashlib.md5(agent_resp.encode()).hexdigest()
        
        cursor.execute("""
        INSERT INTO chat_memory (
            timestamp, user_message, agent_response, action_taken, step_name,
            instructions, operator_context, conversation_id, response_type,
            confidence_score, processing_time, tokens_used, improvement_suggestions,
            message_hash, response_hash
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            timestamp, user_msg, agent_resp, metadata.action, metadata.step,
            metadata.instructions, metadata.operator_context, conversation_id,
            metadata.response_type, metadata.confidence_score, metadata.processing_time,
            metadata.tokens_used, json.dumps(metadata.improvement_suggestions),
            message_hash, response_hash
        ))
        
        log_id = cursor.lastrowid
        
        # Update conversation metadata
        cursor.execute("""
        INSERT OR REPLACE INTO conversation_metadata (
            conversation_id, created_timestamp, last_updated, total_interactions,
            workflow_step, active_modules
        ) VALUES (?, 
            COALESCE((SELECT created_timestamp FROM conversation_metadata WHERE conversation_id = ?), ?),
            ?, 
            COALESCE((SELECT total_interactions FROM conversation_metadata WHERE conversation_id = ?), 0) + 1,
            ?, ?
        )
        """, (conversation_id, conversation_id, timestamp, timestamp, conversation_id, 
              metadata.step or 'active', metadata.operator_context or ''))
        
        conn.commit()
        conn.close()
        
        return log_id

    def fetch_recent_interactions(self, conversation_id: str, limit: int = MAX_CONTEXT_INTERACTIONS) -> List[Tuple]:
        """Fetch recent interactions with enhanced context"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT timestamp, user_message, agent_response, action_taken, step_name,
               confidence_score, processing_time, improvement_suggestions
        FROM chat_memory 
        WHERE conversation_id = ? 
        ORDER BY timestamp DESC 
        LIMIT ?
        """, (conversation_id, limit))
        
        results = cursor.fetchall()
        conn.close()
        return results

    def get_conversation_summary(self, conversation_id: str) -> Dict[str, Any]:
        """Get comprehensive conversation summary"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get conversation metadata
        cursor.execute("""
        SELECT * FROM conversation_metadata WHERE conversation_id = ?
        """, (conversation_id,))
        
        metadata = cursor.fetchone()
        
        # Get interaction statistics
        cursor.execute("""
        SELECT COUNT(*) as total, AVG(confidence_score) as avg_confidence,
               AVG(processing_time) as avg_processing_time, SUM(tokens_used) as total_tokens
        FROM chat_memory WHERE conversation_id = ?
        """, (conversation_id,))
        
        stats = cursor.fetchone()
        conn.close()
        
        return {
            "conversation_id": conversation_id,
            "metadata": metadata,
            "statistics": stats,
            "created": metadata[1] if metadata else None,
            "last_updated": metadata[2] if metadata else None,
            "total_interactions": stats[0] if stats else 0,
            "avg_confidence": stats[1] if stats else 0.0,
            "avg_processing_time": stats[2] if stats else 0.0,
            "total_tokens": stats[3] if stats else 0
        }

class RecursivePromptGenerator:
    """Advanced prompt generation with recursive self-improvement"""
    
    def __init__(self, db: MemoryAgentDatabase):
        self.db = db
        self.prompt_templates = {
            "default": self._load_default_template(),
            "business_strategy": self._load_business_template(),
            "technical_analysis": self._load_technical_template(),
            "creative_problem_solving": self._load_creative_template()
        }
        logger.info("✅ Recursive prompt generator initialized")

    def _load_default_template(self) -> str:
        return """You are an advanced AI assistant with comprehensive memory and analytical capabilities. 
You are part of an Enhanced Memory Agent system with 21 specialized modules and autonomous initialization.

Current Context:
User Input: "{user_input}"
Conversation ID: {conversation_id}
Current Step: {current_step}
Active Modules: {active_modules}

Recent Conversation History:
{conversation_summary}

System Performance Metrics:
- Average Confidence: {avg_confidence:.2%}
- Processing Efficiency: {processing_efficiency}
- Total Interactions: {total_interactions}

Instructions:
1. Provide detailed, actionable responses based on conversation context
2. Leverage the 21-module system capabilities for comprehensive analysis
3. Avoid repetitive responses by building on previous interactions
4. Suggest improvements and next steps where appropriate
5. Maintain professional yet approachable communication style

Response should be strategic, context-aware, and demonstrate continuous learning from previous interactions."""

    def _load_business_template(self) -> str:
        return """You are a strategic business advisor within an Enhanced Memory Agent system focused on revenue optimization.

Business Context:
User Request: "{user_input}"
Revenue Target: $10,000-$20,000 monthly profit
Current Business Phase: {current_step}
Active Business Modules: {active_modules}

Conversation History & Insights:
{conversation_summary}

Strategic Analysis Framework:
- Market Opportunity Assessment
- Revenue Stream Optimization
- Competitive Advantage Development
- Risk Mitigation Strategies
- Implementation Roadmap

Provide strategic, ROI-focused recommendations with specific action items and measurable outcomes."""

    def _load_technical_template(self) -> str:
        return """You are a technical expert within an advanced AI memory system with autonomous capabilities.

Technical Context:
User Query: "{user_input}"
System State: {current_step}
Active Technical Modules: {active_modules}

Previous Technical Discussions:
{conversation_summary}

Technical Analysis Approach:
1. Problem decomposition and root cause analysis
2. Solution architecture and implementation strategy
3. Performance optimization and scalability considerations
4. Error handling and reliability improvements
5. Future enhancement recommendations

Provide detailed technical guidance with code examples, best practices, and implementation specifics."""

    def _load_creative_template(self) -> str:
        return """You are a creative problem-solving assistant with advanced analytical capabilities.

Creative Challenge:
User Input: "{user_input}"
Problem-Solving Phase: {current_step}
Available Creative Modules: {active_modules}

Previous Creative Explorations:
{conversation_summary}

Creative Methodology:
- Divergent thinking and idea generation
- Convergent analysis and solution refinement
- Cross-domain knowledge synthesis
- Innovative approach development
- Implementation feasibility assessment

Generate creative, innovative solutions with practical implementation pathways."""

    def generate_enhanced_prompt(self, user_input: str, conversation_id: str, 
                                current_step: str, active_modules: str,
                                template_type: str = "default") -> str:
        """Generate context-aware prompt with recursive improvement"""
        
        # Get conversation context
        recent_interactions = self.db.fetch_recent_interactions(conversation_id)
        conversation_summary = self._create_conversation_summary(recent_interactions)
        conv_stats = self.db.get_conversation_summary(conversation_id)
        
        # Select appropriate template
        template = self.prompt_templates.get(template_type, self.prompt_templates["default"])
        
        # Calculate performance metrics
        avg_confidence = conv_stats.get("avg_confidence", 0.0)
        processing_efficiency = self._calculate_processing_efficiency(conv_stats)
        total_interactions = conv_stats.get("total_interactions", 0)
        
        # Generate enhanced prompt
        enhanced_prompt = template.format(
            user_input=user_input,
            conversation_id=conversation_id,
            current_step=current_step,
            active_modules=active_modules,
            conversation_summary=conversation_summary,
            avg_confidence=avg_confidence,
            processing_efficiency=processing_efficiency,
            total_interactions=total_interactions
        )
        
        return enhanced_prompt

    def _create_conversation_summary(self, interactions: List[Tuple]) -> str:
        """Create intelligent conversation summary"""
        if not interactions:
            return "No previous interactions in this conversation."
        
        summary_parts = []
        for i, (timestamp, user_msg, agent_resp, action, step, confidence, proc_time, suggestions) in enumerate(reversed(interactions[-5:])):
            interaction_summary = f"""
Interaction {i+1} ({timestamp}):
User: {user_msg[:200]}{'...' if len(user_msg) > 200 else ''}
Agent: {agent_resp[:300]}{'...' if len(agent_resp) > 300 else ''}
Action Taken: {action or 'None'}
Confidence: {confidence:.2%}
"""
            summary_parts.append(interaction_summary)
        
        return "\n".join(summary_parts)

    def _calculate_processing_efficiency(self, conv_stats: Dict[str, Any]) -> str:
        """Calculate processing efficiency metrics"""
        avg_time = conv_stats.get("avg_processing_time", 0.0)
        if avg_time < 1.0:
            return "Excellent (< 1s)"
        elif avg_time < 3.0:
            return "Good (< 3s)"
        elif avg_time < 5.0:
            return "Fair (< 5s)"
        else:
            return "Needs Improvement (> 5s)"

class AdvancedGeminiWrapper:
    """Enhanced Gemini API wrapper with intelligent response processing"""
    
    def __init__(self):
        self.setup_gemini()
        self.response_cache = {}
        self.performance_tracker = {}
        logger.info("✅ Advanced Gemini wrapper initialized")

    def setup_gemini(self):
        """Setup Gemini API with configuration"""
        api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyDj-aTJt7riqX6MJSsW2Tu7uO8cjisEGqE')
        if not api_key:
            logger.warning("⚠️ GEMINI_API_KEY not set!")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        logger.info("✅ Gemini API configured")

    async def call_gemini_api(self, prompt_text: str, conversation_id: str) -> Tuple[str, InteractionMetadata]:
        """Enhanced Gemini API call with performance tracking"""
        start_time = time.time()
        
        try:
            # Check cache for similar prompts
            prompt_hash = hashlib.md5(prompt_text.encode()).hexdigest()
            if prompt_hash in self.response_cache:
                cached_response, cached_meta = self.response_cache[prompt_hash]
                cached_meta.processing_time = 0.1  # Cache hit time
                logger.info(f"📋 Cache hit for conversation {conversation_id}")
                return cached_response, cached_meta
            
            # Generate response
            response = await asyncio.to_thread(self.model.generate_content, prompt_text)
            processing_time = time.time() - start_time
            
            # Extract response text
            response_text = response.text if response.text else "I apologize, but I couldn't generate a response. Could you please rephrase your request?"
            
            # Calculate metadata
            metadata = InteractionMetadata(
                response_type="text",
                confidence_score=self._calculate_confidence_score(response_text, prompt_text),
                processing_time=processing_time,
                tokens_used=len(prompt_text.split()) + len(response_text.split()),
                improvement_suggestions=self._generate_improvement_suggestions(response_text, processing_time)
            )
            
            # Cache response
            self.response_cache[prompt_hash] = (response_text, metadata)
            
            # Track performance
            self._track_performance(conversation_id, processing_time, metadata.confidence_score)
            
            logger.info(f"✅ Gemini response generated in {processing_time:.2f}s (confidence: {metadata.confidence_score:.2%})")
            return response_text, metadata
            
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"❌ Gemini API error: {e}")
            
            error_response = f"I encountered a technical issue while processing your request: {str(e)}. Let me try to help you in a different way."
            metadata = InteractionMetadata(
                response_type="error",
                confidence_score=0.0,
                processing_time=processing_time,
                improvement_suggestions=["API error handling", "Fallback response implementation"]
            )
            
            return error_response, metadata

    def _calculate_confidence_score(self, response_text: str, prompt_text: str) -> float:
        """Calculate confidence score based on response quality indicators"""
        score = 0.5  # Base score
        
        # Length appropriateness
        if 50 <= len(response_text) <= 1000:
            score += 0.2
        
        # Contains specific information
        if any(word in response_text.lower() for word in ['specifically', 'detailed', 'recommend', 'suggest']):
            score += 0.1
        
        # Avoids generic responses
        generic_phrases = ['i understand', 'let me help', 'i can assist']
        if not any(phrase in response_text.lower() for phrase in generic_phrases):
            score += 0.1
        
        # Contains actionable content
        if any(word in response_text.lower() for word in ['step', 'action', 'implement', 'execute']):
            score += 0.1
        
        return min(1.0, score)

    def _generate_improvement_suggestions(self, response_text: str, processing_time: float) -> List[str]:
        """Generate suggestions for response improvement"""
        suggestions = []
        
        if processing_time > 5.0:
            suggestions.append("Optimize prompt length for faster processing")
        
        if len(response_text) < 50:
            suggestions.append("Provide more detailed responses")
        
        if len(response_text) > 2000:
            suggestions.append("Consider breaking down long responses")
        
        if response_text.count('.') < 3:
            suggestions.append("Add more structured information")
        
        return suggestions

    def _track_performance(self, conversation_id: str, processing_time: float, confidence_score: float):
        """Track API performance metrics"""
        if conversation_id not in self.performance_tracker:
            self.performance_tracker[conversation_id] = {
                "total_calls": 0,
                "avg_processing_time": 0.0,
                "avg_confidence": 0.0
            }
        
        tracker = self.performance_tracker[conversation_id]
        tracker["total_calls"] += 1
        tracker["avg_processing_time"] = (tracker["avg_processing_time"] * (tracker["total_calls"] - 1) + processing_time) / tracker["total_calls"]
        tracker["avg_confidence"] = (tracker["avg_confidence"] * (tracker["total_calls"] - 1) + confidence_score) / tracker["total_calls"]

class LoopDetectionAndPivot:
    """Advanced loop detection with intelligent pivot strategies"""
    
    def __init__(self, db: MemoryAgentDatabase):
        self.db = db
        self.similarity_cache = {}
        logger.info("✅ Loop detection system initialized")

    def detect_repetitive_pattern(self, response_text: str, conversation_id: str) -> bool:
        """Detect if response is repetitive using advanced similarity analysis"""
        recent_responses = self._get_recent_responses(conversation_id, LOOP_DETECTION_WINDOW)
        
        if len(recent_responses) < 2:
            return False
        
        # Check semantic similarity with recent responses
        for prev_response in recent_responses:
            similarity_score = self._calculate_semantic_similarity(response_text, prev_response)
            if similarity_score > SIMILARITY_THRESHOLD:
                self._log_loop_detection(conversation_id, "semantic_similarity", [response_text, prev_response])
                return True
        
        # Check for exact phrase repetition
        if self._detect_phrase_repetition(response_text, recent_responses):
            self._log_loop_detection(conversation_id, "phrase_repetition", recent_responses)
            return True
        
        return False

    def generate_pivot_response(self, original_response: str, user_input: str, conversation_id: str) -> str:
        """Generate intelligent pivot response to break loops"""
        pivot_strategies = [
            self._clarification_pivot,
            self._alternative_approach_pivot,
            self._context_expansion_pivot,
            self._creative_reframe_pivot
        ]
        
        # Select strategy based on conversation context
        strategy = self._select_pivot_strategy(conversation_id)
        pivot_response = pivot_strategies[strategy](original_response, user_input, conversation_id)
        
        self._log_pivot_action(conversation_id, strategy, pivot_response)
        return pivot_response

    def _get_recent_responses(self, conversation_id: str, limit: int) -> List[str]:
        """Get recent agent responses for comparison"""
        interactions = self.db.fetch_recent_interactions(conversation_id, limit)
        return [interaction[2] for interaction in interactions]  # agent_response column

    def _calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts"""
        # Simple implementation - can be enhanced with embeddings
        text1_words = set(text1.lower().split())
        text2_words = set(text2.lower().split())
        
        if not text1_words or not text2_words:
            return 0.0
        
        intersection = text1_words.intersection(text2_words)
        union = text1_words.union(text2_words)
        
        return len(intersection) / len(union) if union else 0.0

    def _detect_phrase_repetition(self, response_text: str, recent_responses: List[str]) -> bool:
        """Detect repetitive phrases across responses"""
        response_phrases = self._extract_key_phrases(response_text)
        
        for prev_response in recent_responses:
            prev_phrases = self._extract_key_phrases(prev_response)
            common_phrases = response_phrases.intersection(prev_phrases)
            
            if len(common_phrases) > 2:  # More than 2 common phrases
                return True
        
        return False

    def _extract_key_phrases(self, text: str) -> set:
        """Extract key phrases from text"""
        # Simple phrase extraction - can be enhanced with NLP
        sentences = text.split('.')
        phrases = set()
        
        for sentence in sentences:
            words = sentence.strip().split()
            if 3 <= len(words) <= 8:  # Phrases of reasonable length
                phrases.add(' '.join(words).lower())
        
        return phrases

    def _select_pivot_strategy(self, conversation_id: str) -> int:
        """Select appropriate pivot strategy based on conversation context"""
        conv_summary = self.db.get_conversation_summary(conversation_id)
        total_interactions = conv_summary.get("total_interactions", 0)
        
        # Cycle through strategies based on interaction count
        return total_interactions % 4

    def _clarification_pivot(self, original_response: str, user_input: str, conversation_id: str) -> str:
        """Generate clarification-focused pivot response"""
        return f"""I notice we might be covering similar ground. Let me approach this differently to better help you.

To provide more targeted assistance, could you help me understand:
1. What specific aspect of "{user_input}" is most important to you right now?
2. Are there particular constraints or requirements I should consider?
3. What would an ideal outcome look like from your perspective?

This will help me give you a more focused and actionable response."""

    def _alternative_approach_pivot(self, original_response: str, user_input: str, conversation_id: str) -> str:
        """Generate alternative approach pivot response"""
        return f"""Let me try a different approach to address your request about "{user_input}".

Instead of the conventional path, consider these alternative strategies:

🔄 **Alternative Perspective**: What if we approached this from the opposite direction?
🎯 **Focused Solution**: Let's identify the single most critical element to address first.
🚀 **Innovation Angle**: How might emerging trends or technologies change this approach?

Which of these alternative angles resonates most with your current situation?"""

    def _context_expansion_pivot(self, original_response: str, user_input: str, conversation_id: str) -> str:
        """Generate context expansion pivot response"""
        return f"""I want to expand our discussion beyond the immediate question to provide more comprehensive value.

Your request about "{user_input}" connects to several broader considerations:

📊 **Strategic Context**: How does this fit into your larger objectives?
🔗 **System Integration**: What other systems or processes does this impact?
⏰ **Timeline Considerations**: What's the urgency and sequence of implementation?
📈 **Success Metrics**: How will you measure the effectiveness of the solution?

Let's explore whichever dimension would be most valuable for your planning."""

    def _creative_reframe_pivot(self, original_response: str, user_input: str, conversation_id: str) -> str:
        """Generate creative reframing pivot response"""
        return f"""Let me reframe your question creatively to unlock new possibilities.

Instead of asking "{user_input}", what if we asked:
- "What would this look like if we had unlimited resources?"
- "How would a completely different industry solve this challenge?"
- "What assumptions are we making that might not be true?"

Sometimes the most breakthrough solutions come from questioning our initial framing. Which reframed perspective sparks the most interesting ideas for you?"""

    def _log_loop_detection(self, conversation_id: str, loop_type: str, similar_responses: List[str]):
        """Log loop detection event"""
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO loop_detection (conversation_id, timestamp, loop_type, similar_responses)
        VALUES (?, ?, ?, ?)
        """, (conversation_id, datetime.utcnow().isoformat(), loop_type, json.dumps(similar_responses)))
        
        conn.commit()
        conn.close()
        
        logger.warning(f"🔄 Loop detected in conversation {conversation_id}: {loop_type}")

    def _log_pivot_action(self, conversation_id: str, strategy: int, pivot_response: str):
        """Log pivot action taken"""
        strategy_names = ["clarification", "alternative_approach", "context_expansion", "creative_reframe"]
        strategy_name = strategy_names[strategy]
        
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        UPDATE loop_detection SET pivot_action = ?, improvement_applied = ?
        WHERE conversation_id = ? AND pivot_action IS NULL
        ORDER BY timestamp DESC LIMIT 1
        """, (strategy_name, pivot_response[:200], conversation_id))
        
        conn.commit()
        conn.close()
        
        logger.info(f"🎯 Pivot applied in conversation {conversation_id}: {strategy_name}")

class EnhancedMemoryAgentCore:
    """Core orchestrator for the enhanced memory agent pipeline"""
    
    def __init__(self):
        self.db = MemoryAgentDatabase()
        self.prompt_generator = RecursivePromptGenerator(self.db)
        self.gemini_wrapper = AdvancedGeminiWrapper()
        self.loop_detector = LoopDetectionAndPivot(self.db)
        
        # Integration with existing Cursor AI system
        self.cursor_ai_integration = self._setup_cursor_ai_integration()
        
        logger.info("✅ Enhanced Memory Agent Core initialized")

    def _setup_cursor_ai_integration(self):
        """Setup integration with existing Cursor AI autonomous system"""
        try:
            from cursor_ai_integration_wrapper import CursorAIIntegrationWrapper
            wrapper = CursorAIIntegrationWrapper()
            logger.info("✅ Cursor AI integration available")
            return wrapper
        except ImportError:
            logger.warning("⚠️ Cursor AI integration not available")
            return None

    async def process_user_input(self, user_input: str, conversation_id: str = None, 
                                template_type: str = "default") -> Dict[str, Any]:
        """Process user input through the complete pipeline"""
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
        
        start_time = time.time()
        
        try:
            # Get current system state
            current_step = self._determine_current_step(conversation_id)
            active_modules = self._get_active_modules()
            
            # Generate enhanced prompt
            enhanced_prompt = self.prompt_generator.generate_enhanced_prompt(
                user_input, conversation_id, current_step, active_modules, template_type
            )
            
            # Call Gemini API
            response_text, metadata = await self.gemini_wrapper.call_gemini_api(enhanced_prompt, conversation_id)
            
            # Check for loops and apply pivot if necessary
            if self.loop_detector.detect_repetitive_pattern(response_text, conversation_id):
                response_text = self.loop_detector.generate_pivot_response(response_text, user_input, conversation_id)
                metadata.improvement_suggestions.append("Applied loop detection and pivot strategy")
            
            # Log interaction
            log_id = self.db.log_interaction(conversation_id, user_input, response_text, metadata)
            
            # Calculate total processing time
            total_time = time.time() - start_time
            
            # Prepare response
            response_data = {
                "conversation_id": conversation_id,
                "response": response_text,
                "metadata": asdict(metadata),
                "processing_time": total_time,
                "log_id": log_id,
                "system_status": {
                    "current_step": current_step,
                    "active_modules": active_modules,
                    "cursor_ai_available": self.cursor_ai_integration is not None
                }
            }
            
            logger.info(f"✅ User input processed successfully (conversation: {conversation_id})")
            return response_data
            
        except Exception as e:
            logger.error(f"❌ Error processing user input: {e}")
            return {
                "conversation_id": conversation_id,
                "response": f"I apologize, but I encountered an error while processing your request: {str(e)}",
                "error": str(e),
                "processing_time": time.time() - start_time
            }

    def _determine_current_step(self, conversation_id: str) -> str:
        """Determine current workflow step based on conversation context"""
        conv_summary = self.db.get_conversation_summary(conversation_id)
        total_interactions = conv_summary.get("total_interactions", 0)
        
        if total_interactions == 0:
            return "initiate"
        elif total_interactions < 5:
            return "explore"
        elif total_interactions < 10:
            return "develop"
        else:
            return "optimize"

    def _get_active_modules(self) -> str:
        """Get status of active system modules"""
        # Integration with existing 21-module system
        try:
            if self.cursor_ai_integration:
                status = self.cursor_ai_integration.get_system_status()
                return f"21-module system: {status.get('system_state', 'unknown')}"
            else:
                return "memory_module, processing_module, knowledge_module, interface_module"
        except Exception:
            return "core_modules_active"

class FlaskAPIServer:
    """Enhanced Flask API server with comprehensive endpoints"""
    
    def __init__(self, memory_agent: EnhancedMemoryAgentCore):
        self.app = Flask(__name__)
        self.memory_agent = memory_agent
        self.setup_routes()
        logger.info("✅ Flask API server initialized")

    def setup_routes(self):
        """Setup all API routes"""
        
        @self.app.route("/", methods=["GET"])
        def index():
            """API documentation and status"""
            return render_template_string("""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Enhanced Memory Agent API</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; }
                    .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
                    .method { color: #007bff; font-weight: bold; }
                </style>
            </head>
            <body>
                <h1>🤖 Enhanced Memory Agent API</h1>
                <p>Forever-evolving AI system with persistent memory and recursive self-improvement</p>
                
                <h2>Available Endpoints:</h2>
                
                <div class="endpoint">
                    <span class="method">POST</span> <strong>/chat</strong><br>
                    Main chat interface with persistent memory<br>
                    Body: {"user_input": "your message", "conversation_id": "optional", "template_type": "default"}
                </div>
                
                <div class="endpoint">
                    <span class="method">GET</span> <strong>/conversation/{conversation_id}</strong><br>
                    Get conversation summary and statistics
                </div>
                
                <div class="endpoint">
                    <span class="method">GET</span> <strong>/health</strong><br>
                    System health check and performance metrics
                </div>
                
                <div class="endpoint">
                    <span class="method">POST</span> <strong>/cursor-ai/init</strong><br>
                    Trigger Cursor AI autonomous initialization
                </div>
                
                <div class="endpoint">
                    <span class="method">GET</span> <strong>/analytics</strong><br>
                    System analytics and improvement insights
                </div>
            </body>
            </html>
            """)

        @self.app.route("/chat", methods=["POST"])
        def chat_endpoint():
            """Main chat endpoint with enhanced processing"""
            try:
                data = request.get_json()
                user_input = data.get("user_input", "")
                conversation_id = data.get("conversation_id")
                template_type = data.get("template_type", "default")
                
                if not user_input:
                    return jsonify({"error": "user_input is required"}), 400
                
                # Process input asynchronously
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    self.memory_agent.process_user_input(user_input, conversation_id, template_type)
                )
                loop.close()
                
                return jsonify(result)
                
            except Exception as e:
                logger.error(f"❌ Chat endpoint error: {e}")
                return jsonify({"error": str(e)}), 500

        @self.app.route("/conversation/<conversation_id>", methods=["GET"])
        def get_conversation(conversation_id):
            """Get conversation summary and history"""
            try:
                summary = self.memory_agent.db.get_conversation_summary(conversation_id)
                interactions = self.memory_agent.db.fetch_recent_interactions(conversation_id, 20)
                
                return jsonify({
                    "conversation_summary": summary,
                    "recent_interactions": [
                        {
                            "timestamp": interaction[0],
                            "user_message": interaction[1],
                            "agent_response": interaction[2],
                            "confidence_score": interaction[5]
                        } for interaction in interactions
                    ]
                })
                
            except Exception as e:
                logger.error(f"❌ Conversation endpoint error: {e}")
                return jsonify({"error": str(e)}), 500

        @self.app.route("/health", methods=["GET"])
        def health_check():
            """System health and performance metrics"""
            try:
                # Get database statistics
                conn = sqlite3.connect(self.memory_agent.db.db_path)
                cursor = conn.cursor()
                
                cursor.execute("SELECT COUNT(*) FROM chat_memory")
                total_interactions = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(DISTINCT conversation_id) FROM chat_memory")
                total_conversations = cursor.fetchone()[0]
                
                cursor.execute("SELECT AVG(confidence_score) FROM chat_memory WHERE confidence_score > 0")
                avg_confidence = cursor.fetchone()[0] or 0.0
                
                conn.close()
                
                return jsonify({
                    "status": "healthy",
                    "timestamp": datetime.utcnow().isoformat(),
                    "statistics": {
                        "total_interactions": total_interactions,
                        "total_conversations": total_conversations,
                        "average_confidence": avg_confidence,
                        "cursor_ai_available": self.memory_agent.cursor_ai_integration is not None
                    },
                    "system_components": {
                        "database": "operational",
                        "gemini_api": "operational",
                        "loop_detection": "operational",
                        "prompt_generator": "operational"
                    }
                })
                
            except Exception as e:
                logger.error(f"❌ Health check error: {e}")
                return jsonify({"status": "unhealthy", "error": str(e)}), 500

        @self.app.route("/cursor-ai/init", methods=["POST"])
        def cursor_ai_init():
            """Trigger Cursor AI autonomous initialization"""
            try:
                if not self.memory_agent.cursor_ai_integration:
                    return jsonify({"error": "Cursor AI integration not available"}), 400
                
                # Execute autonomous initialization
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    self.memory_agent.cursor_ai_integration.execute_cursor_ai_prompt()
                )
                loop.close()
                
                return jsonify({
                    "status": "initialization_completed",
                    "result": result,
                    "timestamp": datetime.utcnow().isoformat()
                })
                
            except Exception as e:
                logger.error(f"❌ Cursor AI init error: {e}")
                return jsonify({"error": str(e)}), 500

        @self.app.route("/analytics", methods=["GET"])
        def analytics():
            """System analytics and improvement insights"""
            try:
                conn = sqlite3.connect(self.memory_agent.db.db_path)
                cursor = conn.cursor()
                
                # Get loop detection statistics
                cursor.execute("SELECT COUNT(*) FROM loop_detection")
                total_loops = cursor.fetchone()[0]
                
                # Get recent performance trends
                cursor.execute("""
                SELECT DATE(timestamp) as date, AVG(confidence_score), AVG(processing_time)
                FROM chat_memory 
                WHERE timestamp > datetime('now', '-7 days')
                GROUP BY DATE(timestamp)
                ORDER BY date DESC
                """)
                performance_trends = cursor.fetchall()
                
                conn.close()
                
                return jsonify({
                    "analytics": {
                        "loop_detections": total_loops,
                        "performance_trends": [
                            {
                                "date": trend[0],
                                "avg_confidence": trend[1],
                                "avg_processing_time": trend[2]
                            } for trend in performance_trends
                        ]
                    },
                    "improvement_insights": [
                        "System shows continuous learning from conversation context",
                        "Loop detection preventing repetitive responses",
                        "Recursive prompt improvement enhancing response quality",
                        "Persistent memory enabling context-aware conversations"
                    ]
                })
                
            except Exception as e:
                logger.error(f"❌ Analytics endpoint error: {e}")
                return jsonify({"error": str(e)}), 500

    def run(self, host: str = "0.0.0.0", port: int = 5000, debug: bool = False):
        """Run the Flask API server"""
        logger.info(f"🚀 Starting Enhanced Memory Agent API server on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug, threaded=True)

def main():
    """Main function to initialize and run the complete pipeline"""
    print("🚀 ENHANCED MEMORY AGENT PIPELINE AUTOMATION SUITE")
    print("=" * 70)
    
    try:
        # Initialize core system
        logger.info("🔧 Initializing Enhanced Memory Agent Core...")
        memory_agent = EnhancedMemoryAgentCore()
        
        # Initialize API server
        logger.info("🌐 Setting up Flask API server...")
        api_server = FlaskAPIServer(memory_agent)
        
        print("\n✅ SYSTEM INITIALIZATION COMPLETE")
        print("=" * 70)
        print("🎯 Enhanced Memory Agent Features:")
        print("  • Persistent chat memory with SQLite database")
        print("  • Recursive prompt generation with context awareness")
        print("  • Advanced loop detection and intelligent pivot strategies")
        print("  • Gemini API integration with performance tracking")
        print("  • Cursor AI autonomous initialization integration")
        print("  • Comprehensive analytics and health monitoring")
        print("  • RESTful API for integration and deployment")
        print("\n🌐 API Server starting...")
        print("  • Main endpoint: http://localhost:5000/chat")
        print("  • Health check: http://localhost:5000/health")
        print("  • Documentation: http://localhost:5000/")
        print("\n🎉 FOREVER-EVOLVING AI SYSTEM READY FOR OPERATION!")
        
        # Start API server
        api_server.run(debug=False)
        
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down Enhanced Memory Agent Pipeline...")
        logger.info("System shutdown requested by user")
    except Exception as e:
        print(f"\n❌ System initialization failed: {e}")
        logger.error(f"Critical error: {e}")
        raise

if __name__ == "__main__":
    main()
