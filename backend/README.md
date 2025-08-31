# Dodger Report API

A FastAPI-based API for the 2025 Los Angeles Dodgers season, showcasing data engineering and SQL skills.

## Features

- **Roster Management**: Full CRUD operations for Dodgers players
- **SQLite Database**: Lightweight database perfect for development and demos
- **RESTful API**: Clean, documented endpoints following REST principles
- **Modular Architecture**: Ready for future extensions (stats, schedule, historical data)
- **PostgreSQL Ready**: Easy migration path to production database

## Project Structure

```
backend/
├── app/
│   ├── api/           # API endpoints and routes
│   ├── db/            # Database models, schemas, and connection
│   ├── services/      # Business logic and database operations
│   ├── data/          # Seed data and data management
│   └── main.py        # FastAPI application entry point
├── requirements.txt    # Python dependencies
├── seed_db.py         # Database seeding script
└── README.md          # This file
```

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Seed the Database

```bash
python seed_db.py
```

This will create the SQLite database and populate it with sample Dodgers roster data.

### 3. Run the API

```bash
python -m app.main
```

The API will be available at `http://localhost:8000`

### 4. View API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Roster Management

- `GET /api/v1/roster` - Get all players
- `GET /api/v1/roster/{player_id}` - Get specific player
- `POST /api/v1/roster` - Add new player
- `PUT /api/v1/roster/{player_id}` - Update player
- `DELETE /api/v1/roster/{player_id}` - Delete player

### Query Parameters

- `position`: Filter by position (e.g., "P", "C", "1B", "2B", "3B", "SS", "LF", "CF", "RF")
- `status`: Filter by status (e.g., "Active", "Injured", "Suspended")

### Example Usage

```bash
# Get all players
curl http://localhost:8000/api/v1/roster

# Get only pitchers
curl http://localhost:8000/api/v1/roster?position=P

# Get only active players
curl http://localhost:8000/api/v1/roster?status=Active

# Get specific player
curl http://localhost:8000/api/v1/roster/1
```

## Database Schema

### Players Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| name | String | Player's full name |
| position | String | Fielding position |
| uniform_number | Integer | Jersey number |
| height | String | Height (e.g., "6'2\"") |
| weight | Integer | Weight in pounds |
| birth_date | Date | Date of birth |
| bats | String | Batting side (L/R/S) |
| throws | String | Throwing side (L/R) |
| team | String | Team name |
| status | String | Player status |
| created_at | String | Record creation timestamp |
| updated_at | String | Record update timestamp |

## Sample Data

The database comes pre-populated with 12 sample Dodgers players including:

- **Mookie Betts** (RF, #50)
- **Freddie Freeman** (1B, #5)
- **Shohei Ohtani** (DH, #17)
- **Will Smith** (C, #16)
- **Max Muncy** (3B, #13)
- **Gavin Lux** (2B, #9)
- **Miguel Rojas** (SS, #11)
- **James Outman** (CF, #33)
- **Teoscar Hernández** (LF, #37)
- **Tyler Glasnow** (P, #20)
- **Walker Buehler** (P, #21) - Injured
- **Evan Phillips** (P, #59)

## Future Extensions

This architecture is designed to easily accommodate:

- **Player Statistics**: Batting averages, ERA, home runs, etc.
- **Game Schedule**: Regular season and playoff games
- **Historical Data**: Past seasons and achievements
- **PostgreSQL Migration**: Production-ready database
- **Authentication**: User management and API keys
- **Caching**: Redis integration for performance
- **Analytics**: Advanced statistics and insights

## Development

### Adding New Models

1. Create model in `app/db/models.py`
2. Create schemas in `app/db/schemas.py`
3. Create service in `app/services/`
4. Create API endpoints in `app/api/`
5. Update `app/main.py` to include new router

### Database Migrations

For future PostgreSQL migration:

1. Update `SQLALCHEMY_DATABASE_URL` in `database.py`
2. Remove SQLite-specific `connect_args`
3. Use Alembic for schema migrations

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you're running from the `backend` directory
2. **Database Lock**: Delete `dodgers.db` file if SQLite is locked
3. **Port Already in Use**: Change port in `main.py` or kill existing process

### Reset Database

```bash
rm dodgers.db
python seed_db.py
```

## License

This project is for demonstration purposes.
