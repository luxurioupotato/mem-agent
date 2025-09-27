"""
MEM_AGENT Memory Management System
Advanced memory and knowledge management for the AI mentor
"""

import json
import sqlite3
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import hashlib
import pickle
import os
from pathlib import Path

@dataclass
class MemoryEntry:
    """Data structure for memory entries"""
    id: str
    content: str
    memory_type: str  # 'conversation', 'insight', 'fact', 'preference', 'goal'
    importance: int  # 1-10 scale
    tags: List[str]
    source: str
    created_at: datetime
    last_accessed: datetime
    access_count: int = 0
    metadata: Dict[str, Any] = None

@dataclass
class KnowledgeGraph:
    """Data structure for knowledge graph connections"""
    source_id: str
    target_id: str
    relationship_type: str
    strength: float  # 0-1
    created_at: datetime

class MEMAgentMemoryManager:
    """Advanced memory management system for MEM_AGENT"""
    
    def __init__(self, db_path: str = "mem_agent_memory.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self.memory_cache = {}
        self.knowledge_graph = {}
        self._init_database()
    
    def _init_database(self):
        """Initialize the memory database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create memory entries table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_entries (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                memory_type TEXT NOT NULL,
                importance INTEGER NOT NULL,
                tags TEXT,
                source TEXT,
                created_at TIMESTAMP,
                last_accessed TIMESTAMP,
                access_count INTEGER DEFAULT 0,
                metadata TEXT
            )
        ''')
        
        # Create knowledge graph table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS knowledge_graph (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id TEXT NOT NULL,
                target_id TEXT NOT NULL,
                relationship_type TEXT NOT NULL,
                strength REAL NOT NULL,
                created_at TIMESTAMP,
                FOREIGN KEY (source_id) REFERENCES memory_entries (id),
                FOREIGN KEY (target_id) REFERENCES memory_entries (id)
            )
        ''')
        
        # Create indexes for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_memory_type ON memory_entries (memory_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_importance ON memory_entries (importance)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_tags ON memory_entries (tags)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_created_at ON memory_entries (created_at)')
        
        conn.commit()
        conn.close()
    
    def store_memory(self, content: str, memory_type: str, importance: int = 5,
                    tags: List[str] = None, source: str = "user", 
                    metadata: Dict[str, Any] = None) -> str:
        """Store a new memory entry"""
        memory_id = self._generate_memory_id(content, memory_type)
        
        memory_entry = MemoryEntry(
            id=memory_id,
            content=content,
            memory_type=memory_type,
            importance=importance,
            tags=tags or [],
            source=source,
            created_at=datetime.now(),
            last_accessed=datetime.now(),
            access_count=0,
            metadata=metadata or {}
        )
        
        # Store in database
        self._store_memory_in_db(memory_entry)
        
        # Add to cache
        self.memory_cache[memory_id] = memory_entry
        
        self.logger.info(f"Stored memory: {memory_id}")
        return memory_id
    
    def retrieve_memory(self, memory_id: str) -> Optional[MemoryEntry]:
        """Retrieve a specific memory entry"""
        # Check cache first
        if memory_id in self.memory_cache:
            memory = self.memory_cache[memory_id]
            self._update_access_info(memory_id)
            return memory
        
        # Load from database
        memory = self._load_memory_from_db(memory_id)
        if memory:
            self.memory_cache[memory_id] = memory
            self._update_access_info(memory_id)
        
        return memory
    
    def search_memories(self, query: str, memory_type: str = None, 
                       tags: List[str] = None, limit: int = 10) -> List[MemoryEntry]:
        """Search for memories based on query and filters"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Build query
        where_conditions = []
        params = []
        
        if query:
            where_conditions.append("content LIKE ?")
            params.append(f"%{query}%")
        
        if memory_type:
            where_conditions.append("memory_type = ?")
            params.append(memory_type)
        
        if tags:
            for tag in tags:
                where_conditions.append("tags LIKE ?")
                params.append(f"%{tag}%")
        
        where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"
        
        query_sql = f'''
            SELECT * FROM memory_entries 
            WHERE {where_clause}
            ORDER BY importance DESC, last_accessed DESC
            LIMIT ?
        '''
        params.append(limit)
        
        cursor.execute(query_sql, params)
        rows = cursor.fetchall()
        
        memories = []
        for row in rows:
            memory = self._row_to_memory_entry(row)
            memories.append(memory)
            # Add to cache
            self.memory_cache[memory.id] = memory
        
        conn.close()
        return memories
    
    def get_conversation_history(self, user_id: str, limit: int = 50) -> List[MemoryEntry]:
        """Get conversation history for a specific user"""
        return self.search_memories(
            query="",
            memory_type="conversation",
            limit=limit
        )
    
    def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get user preferences from memory"""
        preferences = self.search_memories(
            query="",
            memory_type="preference",
            tags=[f"user:{user_id}"]
        )
        
        prefs = {}
        for memory in preferences:
            if memory.metadata:
                prefs.update(memory.metadata)
        
        return prefs
    
    def get_business_insights(self, category: str = None) -> List[MemoryEntry]:
        """Get business insights from memory"""
        tags = ["business", "insight"]
        if category:
            tags.append(f"category:{category}")
        
        return self.search_memories(
            query="",
            memory_type="insight",
            tags=tags,
            limit=20
        )
    
    def create_knowledge_connection(self, source_id: str, target_id: str, 
                                  relationship_type: str, strength: float = 0.5):
        """Create a connection between two memory entries"""
        connection = KnowledgeGraph(
            source_id=source_id,
            target_id=target_id,
            relationship_type=relationship_type,
            strength=strength,
            created_at=datetime.now()
        )
        
        # Store in database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO knowledge_graph 
            (source_id, target_id, relationship_type, strength, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            source_id, target_id, relationship_type, strength,
            connection.created_at.isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        # Add to knowledge graph cache
        if source_id not in self.knowledge_graph:
            self.knowledge_graph[source_id] = []
        self.knowledge_graph[source_id].append(connection)
    
    def get_related_memories(self, memory_id: str, relationship_type: str = None) -> List[MemoryEntry]:
        """Get memories related to a specific memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
            SELECT me.* FROM memory_entries me
            JOIN knowledge_graph kg ON me.id = kg.target_id
            WHERE kg.source_id = ?
        '''
        params = [memory_id]
        
        if relationship_type:
            query += " AND kg.relationship_type = ?"
            params.append(relationship_type)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        related_memories = []
        for row in rows:
            memory = self._row_to_memory_entry(row)
            related_memories.append(memory)
            self.memory_cache[memory.id] = memory
        
        conn.close()
        return related_memories
    
    def update_memory_importance(self, memory_id: str, new_importance: int):
        """Update the importance of a memory entry"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE memory_entries 
            SET importance = ? 
            WHERE id = ?
        ''', (new_importance, memory_id))
        
        conn.commit()
        conn.close()
        
        # Update cache
        if memory_id in self.memory_cache:
            self.memory_cache[memory_id].importance = new_importance
    
    def delete_memory(self, memory_id: str):
        """Delete a memory entry"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Delete from knowledge graph
        cursor.execute('DELETE FROM knowledge_graph WHERE source_id = ? OR target_id = ?', 
                      (memory_id, memory_id))
        
        # Delete memory entry
        cursor.execute('DELETE FROM memory_entries WHERE id = ?', (memory_id,))
        
        conn.commit()
        conn.close()
        
        # Remove from cache
        self.memory_cache.pop(memory_id, None)
    
    def cleanup_old_memories(self, days_old: int = 30, min_importance: int = 3):
        """Clean up old, low-importance memories"""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Find memories to delete
        cursor.execute('''
            SELECT id FROM memory_entries 
            WHERE created_at < ? AND importance < ?
        ''', (cutoff_date.isoformat(), min_importance))
        
        memory_ids = [row[0] for row in cursor.fetchall()]
        
        # Delete memories
        for memory_id in memory_ids:
            self.delete_memory(memory_id)
        
        conn.close()
        
        self.logger.info(f"Cleaned up {len(memory_ids)} old memories")
        return len(memory_ids)
    
    def get_memory_statistics(self) -> Dict[str, Any]:
        """Get statistics about stored memories"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total memories
        cursor.execute('SELECT COUNT(*) FROM memory_entries')
        total_memories = cursor.fetchone()[0]
        
        # Memories by type
        cursor.execute('''
            SELECT memory_type, COUNT(*) 
            FROM memory_entries 
            GROUP BY memory_type
        ''')
        memories_by_type = dict(cursor.fetchall())
        
        # Average importance
        cursor.execute('SELECT AVG(importance) FROM memory_entries')
        avg_importance = cursor.fetchone()[0] or 0
        
        # Most accessed memories
        cursor.execute('''
            SELECT content, access_count 
            FROM memory_entries 
            ORDER BY access_count DESC 
            LIMIT 5
        ''')
        most_accessed = cursor.fetchall()
        
        # Knowledge graph connections
        cursor.execute('SELECT COUNT(*) FROM knowledge_graph')
        total_connections = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_memories': total_memories,
            'memories_by_type': memories_by_type,
            'average_importance': round(avg_importance, 2),
            'most_accessed': most_accessed,
            'total_connections': total_connections,
            'cache_size': len(self.memory_cache)
        }
    
    def export_memories(self, filepath: str, memory_type: str = None):
        """Export memories to a JSON file"""
        memories = self.search_memories("", memory_type=memory_type, limit=10000)
        
        export_data = []
        for memory in memories:
            export_data.append({
                'id': memory.id,
                'content': memory.content,
                'memory_type': memory.memory_type,
                'importance': memory.importance,
                'tags': memory.tags,
                'source': memory.source,
                'created_at': memory.created_at.isoformat(),
                'last_accessed': memory.last_accessed.isoformat(),
                'access_count': memory.access_count,
                'metadata': memory.metadata
            })
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Exported {len(export_data)} memories to {filepath}")
    
    def import_memories(self, filepath: str):
        """Import memories from a JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            import_data = json.load(f)
        
        imported_count = 0
        for memory_data in import_data:
            try:
                memory_entry = MemoryEntry(
                    id=memory_data['id'],
                    content=memory_data['content'],
                    memory_type=memory_data['memory_type'],
                    importance=memory_data['importance'],
                    tags=memory_data['tags'],
                    source=memory_data['source'],
                    created_at=datetime.fromisoformat(memory_data['created_at']),
                    last_accessed=datetime.fromisoformat(memory_data['last_accessed']),
                    access_count=memory_data['access_count'],
                    metadata=memory_data.get('metadata', {})
                )
                
                self._store_memory_in_db(memory_entry)
                self.memory_cache[memory_entry.id] = memory_entry
                imported_count += 1
                
            except Exception as e:
                self.logger.error(f"Error importing memory: {str(e)}")
        
        self.logger.info(f"Imported {imported_count} memories from {filepath}")
        return imported_count
    
    def _generate_memory_id(self, content: str, memory_type: str) -> str:
        """Generate a unique memory ID"""
        hash_input = f"{content}_{memory_type}_{datetime.now().isoformat()}"
        return hashlib.md5(hash_input.encode()).hexdigest()
    
    def _store_memory_in_db(self, memory: MemoryEntry):
        """Store memory entry in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO memory_entries 
            (id, content, memory_type, importance, tags, source, 
             created_at, last_accessed, access_count, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            memory.id, memory.content, memory.memory_type, memory.importance,
            json.dumps(memory.tags), memory.source, memory.created_at.isoformat(),
            memory.last_accessed.isoformat(), memory.access_count,
            json.dumps(memory.metadata)
        ))
        
        conn.commit()
        conn.close()
    
    def _load_memory_from_db(self, memory_id: str) -> Optional[MemoryEntry]:
        """Load memory entry from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM memory_entries WHERE id = ?', (memory_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return self._row_to_memory_entry(row)
        return None
    
    def _row_to_memory_entry(self, row: Tuple) -> MemoryEntry:
        """Convert database row to MemoryEntry object"""
        return MemoryEntry(
            id=row[0],
            content=row[1],
            memory_type=row[2],
            importance=row[3],
            tags=json.loads(row[4]) if row[4] else [],
            source=row[5],
            created_at=datetime.fromisoformat(row[6]),
            last_accessed=datetime.fromisoformat(row[7]),
            access_count=row[8],
            metadata=json.loads(row[9]) if row[9] else {}
        )
    
    def _update_access_info(self, memory_id: str):
        """Update access information for a memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE memory_entries 
            SET last_accessed = ?, access_count = access_count + 1
            WHERE id = ?
        ''', (datetime.now().isoformat(), memory_id))
        
        conn.commit()
        conn.close()
        
        # Update cache
        if memory_id in self.memory_cache:
            self.memory_cache[memory_id].last_accessed = datetime.now()
            self.memory_cache[memory_id].access_count += 1

# Example usage
if __name__ == "__main__":
    # Initialize memory manager
    memory_manager = MEMAgentMemoryManager()
    
    # Store some sample memories
    memory_manager.store_memory(
        content="User prefers detailed explanations with examples",
        memory_type="preference",
        importance=8,
        tags=["user:123", "communication"],
        source="conversation"
    )
    
    memory_manager.store_memory(
        content="Business goal: Achieve $15K monthly profit",
        memory_type="goal",
        importance=10,
        tags=["business", "revenue"],
        source="user_input"
    )
    
    # Search memories
    results = memory_manager.search_memories("business", memory_type="goal")
    print(f"Found {len(results)} business-related memories")
    
    # Get statistics
    stats = memory_manager.get_memory_statistics()
    print(f"Memory statistics: {stats}")
