# Database Structure

This directory contains the database models and schemas organized in a modular structure for better maintainability.

## Directory Structure

```
db/
├── __init__.py
├── database.py          # Database connection and session
├── models/              # SQLAlchemy models
│   ├── __init__.py     # Exports all models
│   ├── players.py      # Player and PlayerPosition models
│   └── teams.py        # Team model (example)
└── schemas/             # Pydantic schemas
    ├── __init__.py     # Exports all schemas
    └── players.py      # Player and PlayerPosition schemas
```

## Adding New Models

1. **Create a new model file** in `models/` directory:
   ```python
   # models/games.py
   from sqlalchemy import Column, Integer, String
   from ..database import Base
   
   class Game(Base):
       __tablename__ = "games"
       # ... model definition
   ```

2. **Update `models/__init__.py`**:
   ```python
   from .players import Player, PlayerPosition
   from .teams import Team
   from .games import Game  # Add this line
   
   __all__ = ["Player", "PlayerPosition", "Team", "Game"]
   ```

3. **Create corresponding schemas** in `schemas/` directory:
   ```python
   # schemas/games.py
   from pydantic import BaseModel
   
   class GameBase(BaseModel):
       # ... schema definition
   ```

4. **Update `schemas/__init__.py`**:
   ```python
   from .players import PlayerBase, PlayerCreate, Player, PlayerUpdate
   from .games import GameBase, GameCreate, Game, GameUpdate  # Add this line
   
   __all__ = [
       "PlayerBase", "PlayerCreate", "Player", "PlayerUpdate",
       "GameBase", "GameCreate", "Game", "GameUpdate"  # Add this line
   ]
   ```

## Benefits of This Structure

- **Modularity**: Each model type has its own file
- **Maintainability**: Easier to find and modify specific models
- **Scalability**: Can add many models without cluttering single files
- **Team Development**: Multiple developers can work on different models
- **Testing**: Easier to test individual model files
- **Import Clarity**: Clear imports from specific modules

## Current Models

- **Player**: Core player information (name, uniform number, team, etc.)
- **PlayerPosition**: Multiple positions per player with primary flag
- **Team**: Team information (example model)

## Roster Sync Functionality

The system now includes intelligent roster syncing from ESPN:

### Sync Logic
- **24-Hour Rule**: Roster only syncs if more than 24 hours have passed since last update
- **Smart Detection**: Automatically detects if sync is needed
- **Data Preservation**: Prevents unnecessary overwrites of recent data

### API Endpoints
- `GET /api/v1/roster-sync-status` - Check if sync is needed
- `POST /api/v1/roster-espn-sync` - Sync roster from ESPN (respects 24-hour rule)

### Sync Process
1. **Check Status**: Verifies last update time
2. **Fetch Data**: Gets current roster from ESPN
3. **Clear & Replace**: Removes old data, adds fresh data
4. **Timestamp**: Updates `last_updated` field for all players

### Benefits
- **Efficiency**: No unnecessary API calls to ESPN
- **Data Freshness**: Ensures roster is reasonably current
- **Rate Limiting**: Respects external API limits
- **Audit Trail**: Tracks when data was last updated

## Database Constraints

- **Unique Constraint**: `team + uniform_number` must be unique
- **Foreign Keys**: PlayerPosition references Player
- **Cascade**: Deleting a player deletes their positions
