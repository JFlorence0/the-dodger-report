# Configuration Guide

This guide explains how to configure the Dodger Report API using environment variables.

## Quick Setup

### Option 1: Interactive Setup (Recommended)
```bash
cd backend
python setup_env.py
```

### Option 2: Manual Setup
1. Copy `env.example` to `.env`
2. Fill in your values
3. Restart the backend

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `WEATHER_API_KEY` | Your WeatherAPI.com API key | `abc123def456` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Environment mode | `development` |
| `DATABASE_URL` | Database connection string | `sqlite:///./dodgers.db` |
| `SECRET_KEY` | Security key for JWT/sessions | Auto-generated |
| `ESPN_BASE_URL` | ESPN API base URL | ESPN default |
| `DODGERS_TEAM_ID` | ESPN team ID for Dodgers | `19` |
| `BACKEND_CORS_ORIGINS` | Allowed CORS origins | Localhost only |

## Getting Your Weather API Key

1. **Visit [WeatherAPI.com](https://www.weatherapi.com/)**
2. **Sign up for a free account**
3. **Get your API key** (1M calls/month free)
4. **Add it to your `.env` file**

## Environment Modes

### Development
- Debug mode enabled
- Local SQLite database
- Detailed logging
- CORS allows localhost

### Production
- Debug mode disabled
- Production database (set via `DATABASE_URL`)
- Minimal logging
- CORS restricted to production domains

## File Structure

```
backend/
├── .env                    # Your environment variables (create this)
├── env.example            # Template file
├── setup_env.py           # Interactive setup script
├── app/
│   ├── core/
│   │   └── config.py      # Configuration management
│   ├── services/          # Business logic
│   └── api/              # API endpoints
```

## Validation

The configuration system automatically validates your settings on startup:

- ✅ **Weather API**: Checks if key is provided
- ✅ **Security**: Warns about default secret keys
- ✅ **Database**: Validates connection strings
- ✅ **Environment**: Sets appropriate defaults

## Troubleshooting

### Weather API Not Working
- Check `WEATHER_API_KEY` is set in `.env`
- Verify the API key is valid
- Check API usage limits

### Configuration Not Loading
- Ensure `.env` file is in the `backend/` directory
- Check file permissions
- Restart the backend server

### CORS Issues
- Verify `BACKEND_CORS_ORIGINS` includes your frontend URL
- Check the frontend is running on the expected port

## Security Notes

- **Never commit `.env` files** to version control
- **Use strong secret keys** in production
- **Restrict CORS origins** in production
- **Rotate API keys** regularly

## Example .env File

```bash
# Environment
ENVIRONMENT=development

# Weather API
WEATHER_API_KEY=your_actual_api_key_here

# Database
DATABASE_URL=sqlite:///./dodgers.db

# Security
SECRET_KEY=your-super-secret-key-here

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```
