#!/usr/bin/env python3
"""
Test script for the new roster sync functionality.
Run this to test the sync status and sync operations.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal
from app.services.player_service import PlayerService
from app.db.models import Player

def test_sync_functionality():
    """Test the sync functionality."""
    db = SessionLocal()
    try:
        player_service = PlayerService(db)
        
        print("=== Testing Roster Sync Functionality ===\n")
        
        # Test 1: Check sync status
        print("1. Checking sync status...")
        should_sync = player_service.should_sync_roster()
        print(f"   Should sync: {should_sync}")
        
        # Test 2: Get current player count
        player_count = db.query(Player).count()
        print(f"   Current players in DB: {player_count}")
        
        # Test 3: Check last updated time
        if player_count > 0:
            latest_player = db.query(Player).order_by(Player.last_updated.desc()).first()
            if latest_player and latest_player.last_updated:
                print(f"   Last updated: {latest_player.last_updated}")
            else:
                print("   No last_updated timestamp found")
        
        print("\n2. Testing ESPN data fetch (no DB changes)...")
        players_data = player_service.sync_roster_from_espn()
        print(f"   Players found on ESPN: {len(players_data)}")
        
        if players_data:
            print("   Sample player data:")
            for i, player in enumerate(players_data[:3]):  # Show first 3
                print(f"     {i+1}. {player['name']} - {player['positions']} - #{player['uniform_number']}")
        
        print("\n3. Sync status summary:")
        if should_sync:
            print("   ✅ Roster needs to be synced")
            print("   💡 Use POST /api/v1/roster-espn-sync to sync")
        else:
            print("   ✅ Roster is up to date")
            print("   💡 No sync needed for now")
            
    except Exception as e:
        print(f"Error during testing: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_sync_functionality()
