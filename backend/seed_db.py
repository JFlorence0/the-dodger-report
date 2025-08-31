#!/usr/bin/env python3
"""
Script to seed the database with sample Dodgers roster data.
Run this script to populate the database with initial player data.
"""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.data.seed_data import seed_database

if __name__ == "__main__":
    print("Seeding Dodgers roster database...")
    seed_database()
    print("Database seeding completed!")
