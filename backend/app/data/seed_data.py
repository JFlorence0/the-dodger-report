from datetime import date
from ..db.database import SessionLocal, engine
from ..db.models import Player, Base

# Sample Dodgers roster data for 2025 season
SAMPLE_PLAYERS = [
    {
        "name": "Mookie Betts",
        "position": "RF",
        "jersey_number": 50,
        "height": "5'9\"",
        "weight": 180,
        "birth_date": date(1992, 10, 7),
        "bats": "R",
        "throws": "R",
        "team": "Los Angeles Dodgers",
        "status": "Active"
    },
    {
        "name": "Freddie Freeman",
        "position": "1B",
        "jersey_number": 5,
        "height": "6'5\"",
        "weight": 220,
        "birth_date": date(1989, 9, 12),
        "bats": "L",
        "throws": "R",
        "team": "Los Angeles Dodgers",
        "status": "Active"
    },
    {
        "name": "Shohei Ohtani",
        "position": "DH",
        "jersey_number": 17,
        "height": "6'4\"",
        "weight": 210,
        "birth_date": date(1994, 7, 5),
        "bats": "L",
        "throws": "R",
        "team": "Los Angeles Dodgers",
        "status": "Active"
    },
    {
        "name": "Will Smith",
        "position": "C",
        "jersey_number": 16,
        "height": "5'10\"",
        "weight": 180,
        "birth_date": date(1995, 3, 28),
        "bats": "R",
        "throws": "R",
        "team": "Los Angeles Dodgers",
        "status": "Active"
    },
    {
        "name": "Max Muncy",
        "position": "3B",
        "jersey_number": 13,
        "height": "6'0\"",
        "weight": 215,
        "birth_date": date(1990, 8, 25),
        "bats": "L",
        "throws": "R",
        "team": "Los Angeles Dodgers",
        "status": "Active"
    },
    {
        "name": "Gavin Lux",
        "position": "2B",
        "jersey_number": 9,
        "height": "6'2\"",
        "weight": 190,
        "birth_date": date(1997, 11, 23),
        "bats": "L",
        "throws": "R",
        "team": "Los Angeles Dodgers",
        "status": "Active"
    },
    {
        "name": "Miguel Rojas",
        "position": "SS",
        "jersey_number": 11,
        "height": "6'1\"",
        "weight": 190,
        "birth_date": date(1989, 2, 24),
        "bats": "R",
        "throws": "R",
        "team": "Los Angeles Dodgers",
        "status": "Active"
    },
    {
        "name": "James Outman",
        "position": "CF",
        "jersey_number": 33,
        "height": "6'3\"",
        "weight": 215,
        "birth_date": date(1997, 5, 14),
        "bats": "L",
        "throws": "R",
        "team": "Los Angeles Dodgers",
        "status": "Active"
    },
    {
        "name": "Teoscar Hernández",
        "position": "LF",
        "jersey_number": 37,
        "height": "6'2\"",
        "weight": 225,
        "birth_date": date(1992, 10, 15),
        "bats": "R",
        "throws": "R",
        "team": "Los Angeles Dodgers",
        "status": "Active"
    },
    {
        "name": "Tyler Glasnow",
        "position": "P",
        "jersey_number": 20,
        "height": "6'8\"",
        "weight": 225,
        "birth_date": date(1993, 8, 23),
        "bats": "L",
        "throws": "R",
        "team": "Los Angeles Dodgers",
        "status": "Active"
    },
    {
        "name": "Walker Buehler",
        "position": "P",
        "jersey_number": 21,
        "height": "6'2\"",
        "weight": 185,
        "birth_date": date(1994, 7, 28),
        "bats": "R",
        "throws": "R",
        "team": "Los Angeles Dodgers",
        "status": "Injured"
    },
    {
        "name": "Evan Phillips",
        "position": "P",
        "jersey_number": 59,
        "height": "6'0\"",
        "weight": 200,
        "birth_date": date(1994, 9, 6),
        "bats": "R",
        "throws": "R",
        "team": "Los Angeles Dodgers",
        "status": "Active"
    }
]

def seed_database():
    """
    Seed the database with sample Dodgers roster data.
    """
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_players = db.query(Player).count()
        if existing_players > 0:
            print(f"Database already contains {existing_players} players. Skipping seed.")
            return
        
        # Add sample players
        for player_data in SAMPLE_PLAYERS:
            player = Player(**player_data)
            db.add(player)
        
        # Commit the changes
        db.commit()
        print(f"Successfully seeded database with {len(SAMPLE_PLAYERS)} players!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
