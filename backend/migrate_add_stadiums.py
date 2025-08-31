import sqlite3
import os

def migrate():
    db_path = os.path.join(os.path.dirname(__file__), 'dodgers.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Create stadiums table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stadiums (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL UNIQUE,
                city VARCHAR(100) NOT NULL,
                state VARCHAR(50) NOT NULL,
                country VARCHAR(50) DEFAULT 'USA',
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                capacity INTEGER,
                surface_type VARCHAR(50),
                roof_type VARCHAR(50),
                primary_team VARCHAR(100),
                league VARCHAR(10) DEFAULT 'MLB',
                is_active BOOLEAN DEFAULT 1,
                opened_year INTEGER,
                created_at VARCHAR,
                updated_at VARCHAR
            )
        """)
        
        # Add stadium_id column to games table if it doesn't exist
        cursor.execute("PRAGMA table_info(games)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'stadium_id' not in columns:
            cursor.execute("ALTER TABLE games ADD COLUMN stadium_id INTEGER REFERENCES stadiums(id)")
            print("Added 'stadium_id' column to games table.")
        
        # Create index on stadium name for faster lookups
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_stadiums_name ON stadiums(name)")
        
        conn.commit()
        print("Migration completed successfully!")
        
    except Exception as e:
        print(f"Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
