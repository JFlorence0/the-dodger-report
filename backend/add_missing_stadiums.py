import sqlite3
import os

def add_missing_stadiums():
    db_path = os.path.join(os.path.dirname(__file__), 'dodgers.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    missing_stadiums = [
        {
            "name": "Angel Stadium",
            "city": "Anaheim",
            "state": "CA",
            "latitude": 33.8003,
            "longitude": -117.8827,
            "primary_team": "Los Angeles Angels",
            "capacity": 45517,
            "surface_type": "Grass",
            "roof_type": "Open",
            "opened_year": 1966
        },
        {
            "name": "George M. Steinbrenner Field",
            "city": "Tampa",
            "state": "FL",
            "latitude": 27.9806,
            "longitude": -82.5036,
            "primary_team": "New York Yankees",
            "capacity": 11000,
            "surface_type": "Grass",
            "roof_type": "Open",
            "opened_year": 1996
        }
    ]
    
    try:
        for stadium_data in missing_stadiums:
            # Check if stadium already exists
            cursor.execute("SELECT id FROM stadiums WHERE name = ?", (stadium_data["name"],))
            existing = cursor.fetchone()
            
            if not existing:
                cursor.execute("""
                    INSERT INTO stadiums (name, city, state, country, latitude, longitude, 
                                        capacity, surface_type, roof_type, primary_team, 
                                        league, is_active, opened_year)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    stadium_data["name"], stadium_data["city"], stadium_data["state"], "USA",
                    stadium_data["latitude"], stadium_data["longitude"], stadium_data["capacity"],
                    stadium_data["surface_type"], stadium_data["roof_type"], stadium_data["primary_team"],
                    "MLB", True, stadium_data["opened_year"]
                ))
                print(f"Added stadium: {stadium_data['name']}")
            else:
                print(f"Stadium already exists: {stadium_data['name']}")
        
        conn.commit()
        print("Missing stadiums added successfully!")
        
    except Exception as e:
        print(f"Error adding stadiums: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    add_missing_stadiums()
