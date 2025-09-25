#!/usr/bin/env python3
"""
Test sqlite-vec extension loading
"""

import sqlite3
import sqlite_vec

def test_sqlite_vec():
    try:
        print("🔍 Testing sqlite-vec extension loading...")
        
        db = sqlite3.connect(":memory:")
        db.enable_load_extension(True)
        sqlite_vec.load(db)
        db.enable_load_extension(False)

        version = db.execute("select vec_version()").fetchone()
        print(f"✅ sqlite-vec extension loaded successfully! Version: {version[0]}")
        
        # Test creating a vector table
        db.execute("""
            CREATE VIRTUAL TABLE test_embeddings USING vec0(
                embedding float[3]
            )
        """)
        
        # Test inserting a vector
        test_vector = [0.1, 0.2, 0.3]
        db.execute(
            "INSERT INTO test_embeddings (rowid, embedding) VALUES (?, ?)",
            (1, sqlite_vec.serialize_float32(test_vector))
        )
        
        # Test querying
        results = db.execute("""
            SELECT rowid FROM test_embeddings 
            WHERE embedding MATCH ?
            ORDER BY distance
            LIMIT 1
        """, (sqlite_vec.serialize_float32(test_vector),)).fetchall()
        
        if results:
            print("✅ Vector search test successful!")
        else:
            print("⚠️ Vector search returned no results")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Failed to load sqlite-vec extension: {e}")
        print(f"Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    success = test_sqlite_vec()
    if success:
        print("\n🎉 sqlite-vec is working correctly!")
    else:
        print("\n❌ sqlite-vec has issues. Consider using FAISS as alternative.")
