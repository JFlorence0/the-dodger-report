#!/usr/bin/env python3
"""
Simple migration script to add game_result column to games table.
Run this after updating the models and schemas.
"""

import sqlite3
import os

def migrate():
    # Get the database path
    db_path = os.path.join(os.path.dirname(__file__), 'dodgers.db')
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return
    
    print(f"Migrating database: {db_path}")
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if column already exists
        cursor.execute("PRAGMA table_info(games)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'game_result' in columns:
            print("Column 'game_result' already exists. Skipping migration.")
            return
        
        # Add the new column
        cursor.execute("ALTER TABLE games ADD COLUMN game_result TEXT")
        print("Added 'game_result' column to games table.")
        
        # Commit the changes
        conn.commit()
        print("Migration completed successfully!")
        
    except Exception as e:
        print(f"Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
