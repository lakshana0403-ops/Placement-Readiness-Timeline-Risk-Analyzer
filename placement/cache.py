import sqlite3
import hashlib
import os

DB_PATH = "feedback_cache.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ai_feedback (
            hash_key TEXT PRIMARY KEY,
            feedback_text TEXT
        )
    ''')
    conn.commit()
    conn.close()

def _generate_hash(resume_text, job_desc):
    # Create a unique fingerprint from both texts
    combined_text = (resume_text.strip().lower() + "|" + job_desc.strip().lower()).encode('utf-8')
    return hashlib.sha256(combined_text).hexdigest()

def get_cached_feedback(resume_text, job_desc):
    init_db()
    hash_key = _generate_hash(resume_text, job_desc)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT feedback_text FROM ai_feedback WHERE hash_key = ?', (hash_key,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return result[0]
    return None

def save_feedback(resume_text, job_desc, feedback_text):
    init_db()
    hash_key = _generate_hash(resume_text, job_desc)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Use REPLACE to overwrite if somehow it already exists
    cursor.execute('INSERT OR REPLACE INTO ai_feedback (hash_key, feedback_text) VALUES (?, ?)', 
                   (hash_key, feedback_text))
    conn.commit()
    conn.close()
