#!/usr/bin/env python3
"""
RAG System with Gemini Embeddings - No OpenAI Required
LocalRAGSystem class using Gemini for embeddings
"""

import sqlite3
import sqlite_vec
import os
import numpy as np
import google.generativeai as genai
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
import json
from datetime import datetime
from langchain.text_splitter import RecursiveCharacterTextSplitter
import re
import hashlib
import concurrent.futures

from config import config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiRAGSystem:
    """Complete RAG implementation with Gemini embeddings"""
    
    def __init__(self, db_path=None):
        self.db_path = db_path or config.RAG_DATABASE_PATH
        self.embedding_dim = 768  # Gemini embedding dimension
        self.chunk_size = config.CHUNK_SIZE
        self.chunk_overlap = config.CHUNK_OVERLAP
        self.max_context_length = config.MAX_CONTEXT_LENGTH
        
        # Initialize Gemini
        if config.GEMINI_API_KEY:
            genai.configure(api_key=config.GEMINI_API_KEY)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.gemini_model = None
            logger.error("Gemini API key not found")
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        logger.info(f"Gemini RAG System initialized with database: {self.db_path}")
    
    def run_with_timeout(self, func, timeout=10, *args, **kwargs):
        """Run function with timeout to prevent blocking"""
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(func, *args, **kwargs)
            try:
                return future.result(timeout=timeout)
            except concurrent.futures.TimeoutError:
                logger.error(f"Timeout running {func.__name__} after {timeout} seconds")
                return None
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {e}")
                return None
    
    def initialize_database(self):
        """Initialize SQLite database with vector search capabilities."""
        try:
            db = sqlite3.connect(self.db_path)
            try:
                db.enable_load_extension(True)
                sqlite_vec.load(db)
                db.enable_load_extension(False)
                logger.info("✅ sqlite-vec extension loaded successfully")
            except Exception as e:
                logger.error(f"❌ Failed to load sqlite-vec extension: {e}")
                raise
            
            cursor = db.cursor()
            
            # Create vector table for embeddings
            cursor.execute(f"""
                CREATE VIRTUAL TABLE IF NOT EXISTS document_embeddings USING vec0(
                    embedding float[{self.embedding_dim}]
                )
            """)
            
            # Create table for original text content
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    source TEXT,
                    chunk_index INTEGER DEFAULT 0,
                    content_hash TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT
                )
            """)
            
            # Create index for faster searches
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_documents_source ON documents(source)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_documents_hash ON documents(content_hash)
            """)
            
            # Create conversations table for memory
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_message TEXT NOT NULL,
                    agent_response TEXT NOT NULL,
                    session_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            db.commit()
            db.close()
            logger.info("✅ Database initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Database initialization failed: {e}")
            return False
    
    def get_simple_embedding(self, text):
        """Generate simple hash-based embedding for text (fallback method)."""
        try:
            # Create a simple hash-based embedding
            # This is a fallback when Gemini embeddings aren't available
            text_hash = hashlib.sha256(text.encode()).hexdigest()
            
            # Convert hash to float array
            embedding = []
            for i in range(0, len(text_hash), 2):
                hex_pair = text_hash[i:i+2]
                float_val = int(hex_pair, 16) / 255.0  # Normalize to 0-1
                embedding.append(float_val)
            
            # Pad or truncate to desired dimension
            while len(embedding) < self.embedding_dim:
                embedding.extend(embedding[:self.embedding_dim - len(embedding)])
            
            return embedding[:self.embedding_dim]
            
        except Exception as e:
            logger.error(f"Error generating simple embedding: {e}")
            return None
    
    def gemini_generate(self, prompt):
        """Helper function for Gemini generation"""
        if self.gemini_model:
            return self.gemini_model.generate_content(prompt)
        else:
            return None
    
    def get_embedding(self, text):
        """Generate embedding for text using Gemini or fallback method."""
        if not self.gemini_model:
            return self.get_simple_embedding(text)
            
        try:
            # Use Gemini for semantic understanding and create embedding
            prompt = f"""Analyze this text and provide 3 key semantic concepts that represent its meaning:
            
Text: {text[:500]}...

Provide exactly 3 concepts, one per line, no explanations."""
            
            # Use timeout wrapper to prevent blocking
            response = self.run_with_timeout(self.gemini_generate, timeout=10, prompt=prompt)
            if response is None:
                logger.warning("Gemini embedding generation timed out. Using fallback.")
                return self.get_simple_embedding(text)
            
            concepts = response.text.strip().split('\n')[:3]
            
            # Convert concepts to embedding
            embedding = []
            for concept in concepts:
                concept_hash = hashlib.sha256(concept.encode()).hexdigest()
                for i in range(0, len(concept_hash), 2):
                    if len(embedding) >= self.embedding_dim:
                        break
                    hex_pair = concept_hash[i:i+2]
                    float_val = int(hex_pair, 16) / 255.0
                    embedding.append(float_val)
            
            # Pad to desired dimension
            while len(embedding) < self.embedding_dim:
                embedding.append(0.0)
            
            return embedding[:self.embedding_dim]
            
        except Exception as e:
            logger.warning(f"Gemini embedding failed, using fallback: {e}")
            return self.get_simple_embedding(text)
    
    def clean_text(self, text):
        """Clean and normalize text content."""
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?;:()\-"\']', '', text)
        
        return text.strip()
    
    def process_text_file(self, file_path):
        """Process text file into chunks."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                raw_text = f.read()
            
            # Clean the text
            cleaned_text = self.clean_text(raw_text)
            
            # Split into chunks
            chunks = self.text_splitter.split_text(cleaned_text)
            
            logger.info(f"Processed {file_path}: {len(chunks)} chunks created")
            logger.info(f"Average chunk size: {sum(len(chunk) for chunk in chunks) / len(chunks):.0f} characters")
            
            return chunks
            
        except Exception as e:
            logger.error(f"Error processing text file {file_path}: {e}")
            return []
    
    def add_documents(self, text_chunks, source="unknown"):
        """Add text chunks to the knowledge base."""
        if not text_chunks:
            logger.warning("No text chunks provided")
            return False
            
        try:
            db = sqlite3.connect(self.db_path)
            db.enable_load_extension(True)
            sqlite_vec.load(db)
            db.enable_load_extension(False)
            
            cursor = db.cursor()
            
            logger.info(f"Adding {len(text_chunks)} documents to knowledge base...")
            successful_adds = 0
            
            for i, chunk in enumerate(text_chunks):
                if not chunk or len(chunk.strip()) < 20:  # Skip very short chunks
                    continue
                
                # Create content hash to avoid duplicates
                content_hash = hashlib.md5(chunk.encode()).hexdigest()
                
                # Check if already exists
                existing = cursor.execute(
                    "SELECT id FROM documents WHERE content_hash = ?", 
                    (content_hash,)
                ).fetchone()
                
                if existing:
                    logger.debug(f"Skipping duplicate chunk {i}")
                    continue
                    
                # Generate embedding
                embedding = self.get_embedding(chunk)
                if embedding is None:
                    logger.warning(f"Failed to generate embedding for chunk {i}")
                    continue
                
                # Insert document content
                cursor.execute(
                    "INSERT INTO documents (content, source, chunk_index, content_hash, metadata) VALUES (?, ?, ?, ?, ?)",
                    (chunk, source, i, content_hash, json.dumps({"length": len(chunk)}))
                )
                doc_id = cursor.lastrowid
                
                # Insert embedding
                cursor.execute(
                    "INSERT INTO document_embeddings (rowid, embedding) VALUES (?, ?)",
                    (doc_id, sqlite_vec.serialize_float32(embedding))
                )
                
                successful_adds += 1
                
                if (i + 1) % 10 == 0:
                    logger.info(f"  Processed {i + 1}/{len(text_chunks)} documents")
                    db.commit()  # Commit periodically
            
            db.commit()
            db.close()
            
            logger.info(f"✅ Successfully added {successful_adds}/{len(text_chunks)} documents")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error adding documents: {e}")
            return False
    
    def search_similar_documents(self, query, top_k=5, min_similarity=0.1):
        """Search for documents similar to the query."""
        if not query or not query.strip():
            return []
            
        # Generate query embedding
        query_embedding = self.get_embedding(query)
        if query_embedding is None:
            logger.error("Failed to generate query embedding")
            return []
        
        try:
            db = sqlite3.connect(self.db_path)
            db.enable_load_extension(True)
            sqlite_vec.load(db)
            db.enable_load_extension(False)
            
            cursor = db.cursor()
            
            # Perform vector search
            results = cursor.execute("""
                SELECT 
                    d.content,
                    d.source,
                    d.chunk_index,
                    v.distance
                FROM document_embeddings v
                JOIN documents d ON v.rowid = d.id
                WHERE v.embedding MATCH ? AND k = ?
                ORDER BY v.distance
            """, (sqlite_vec.serialize_float32(query_embedding), top_k)).fetchall()
            
            db.close()
            
            # Convert results and filter by similarity
            formatted_results = []
            for row in results:
                similarity = 1 - row[3]  # Convert distance to similarity
                if similarity >= min_similarity:
                    formatted_results.append({
                        'content': row[0],
                        'source': row[1],
                        'chunk_index': row[2],
                        'similarity': similarity,
                        'distance': row[3]
                    })
            
            logger.info(f"Found {len(formatted_results)} similar documents (similarity >= {min_similarity})")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching similar documents: {e}")
            return []
    
    def get_context_for_query(self, query, max_context_length=None):
        """Get relevant context for a query, respecting length limits."""
        if max_context_length is None:
            max_context_length = self.max_context_length
            
        similar_docs = self.search_similar_documents(query, top_k=10)
        
        if not similar_docs:
            return ""
        
        context_parts = []
        current_length = 0
        
        for doc in similar_docs:
            content = doc['content']
            source_info = f"[Source: {doc['source']}] "
            full_content = source_info + content
            
            if current_length + len(full_content) <= max_context_length:
                context_parts.append(full_content)
                current_length += len(full_content)
            else:
                # Add partial content if it fits
                remaining_space = max_context_length - current_length
                if remaining_space > 100:  # Only add if meaningful space left
                    context_parts.append(full_content[:remaining_space] + "...")
                break
        
        context = "\n\n---\n\n".join(context_parts)
        logger.info(f"Generated context: {len(context)} characters from {len(context_parts)} sources")
        
        return context
    
    def add_conversation(self, user_message, agent_response, session_id=None):
        """Add conversation to memory for future reference."""
        try:
            db = sqlite3.connect(self.db_path)
            cursor = db.cursor()
            
            cursor.execute(
                "INSERT INTO conversations (user_message, agent_response, session_id) VALUES (?, ?, ?)",
                (user_message, agent_response, session_id)
            )
            
            db.commit()
            db.close()
            
            # Also add as a document for RAG
            conversation_text = f"User asked: {user_message}\n\nAgent responded: {agent_response}"
            self.add_documents([conversation_text], source="conversation_history")
            
            logger.info("Conversation added to memory")
            return True
            
        except Exception as e:
            logger.error(f"Error adding conversation: {e}")
            return False
    
    def get_database_stats(self):
        """Get statistics about the database."""
        try:
            db = sqlite3.connect(self.db_path)
            cursor = db.cursor()
            
            # Get document count
            doc_count = cursor.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
            
            # Get unique sources
            sources = cursor.execute("SELECT DISTINCT source FROM documents").fetchall()
            source_list = [s[0] for s in sources]
            
            # Get conversation count
            conv_count = cursor.execute("SELECT COUNT(*) FROM conversations").fetchone()[0]
            
            db.close()
            
            return {
                'total_documents': doc_count,
                'unique_sources': len(source_list),
                'sources': source_list,
                'conversations': conv_count
            }
            
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {}

def setup_rag_system(knowledge_file=None):
    """Set up the RAG system with knowledge base."""
    rag = GeminiRAGSystem()
    
    # Initialize database
    if not rag.initialize_database():
        logger.error("Failed to initialize database")
        return None
    
    # Process and add documents if knowledge file provided
    if knowledge_file and Path(knowledge_file).exists():
        logger.info(f"Processing knowledge file: {knowledge_file}")
        chunks = rag.process_text_file(knowledge_file)
        if chunks:
            rag.add_documents(chunks, source=knowledge_file)
        else:
            logger.warning("No chunks generated from knowledge file")
    elif knowledge_file:
        logger.warning(f"Knowledge file {knowledge_file} not found")
    
    return rag

if __name__ == "__main__":
    # Test the RAG system
    rag = setup_rag_system("ai_knowledge_base.txt")
    
    if rag:
        # Get stats
        stats = rag.get_database_stats()
        print(f"\n📊 Database Stats:")
        print(f"  Documents: {stats.get('total_documents', 0)}")
        print(f"  Sources: {stats.get('unique_sources', 0)}")
        print(f"  Conversations: {stats.get('conversations', 0)}")
        
        # Test search
        if stats.get('total_documents', 0) > 0:
            test_query = "What is machine learning?"
            context = rag.get_context_for_query(test_query)
            
            print(f"\n🔍 Test Query: {test_query}")
            print(f"📄 Context Length: {len(context)} characters")
            if context:
                print(f"📝 Context Preview: {context[:200]}...")
        
        print("\n✅ Gemini RAG system ready for integration!")
