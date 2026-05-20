# URL Shortener

A modern, high-performance URL shortening service built with FastAPI, PostgreSQL, and SQLAlchemy. This service provides a simple API to create short links, redirect to original URLs, and track click statistics.

## Features

- **Short Link Creation**: Generate unique short codes for any URL
- **Redirection**: Fast and efficient redirects to target URLs
- **Click Tracking**: Track the number of clicks per short link
- **Statistics API**: Retrieve click counts for any short link
- **Authentication**: Protected API endpoints with HTTP Basic Auth
- **Logging**: Request logging with decorator pattern
- **Database Migrations**: Alembic for schema management
- **Docker Support**: Containerized deployment ready

## Tech Stack

- **Python 3.13+**
- **FastAPI**: Modern, fast web framework
- **PostgreSQL**: Relational database
- **SQLAlchemy 2.0**: Python SQL toolkit and ORM
- **Alembic**: Database migration tool
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server
- **uv**: Fast Python package installer

## Prerequisites

- Python 3.13 or higher
- PostgreSQL database
- uv package manager (recommended) or pip

## Installation

### Using uv (recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync
```

### Using pip

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with the following variable:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/url_shortener
```

Replace `username`, `password`, and `url_shortener` with your actual database credentials.

## Database Setup

Run database migrations to create the required tables:

```bash
make run_migrations
```

Or manually:

```bash
cd src
alembic upgrade head
```

## Running the Application

### Development Mode

```bash
make run
```

Or manually:

```bash
uvicorn main:app --reload --app-dir src
```

The API will be available at `http://localhost:8000`

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --app-dir src
```

## Docker Deployment

Build and run using Docker:

```bash
docker build -t url-shortener .
docker run -p 8000:8000 --env-file .env url-shortener
```

## API Documentation

The API documentation is available at `/docs` and requires authentication.

**Credentials:**
- Username: `admin`
- Password: `8L5JDjUuu63K`

## API Endpoints

### Public Endpoints

#### Redirect to Original URL
```
GET /{short_code}
```
Redirects to the original URL associated with the short code.

### Protected Endpoints (requires authentication)

#### Create Short Link
```
POST /shorten
Content-Type: application/json

{
  "target_url": "https://example.com/very-long-url"
}
```

Response:
```json
{
  "short_code": "abc123",
  "target_url": "https://example.com/very-long-url",
  "click_count": 0,
  "created_at": "2024-01-01T00:00:00"
}
```

#### Get Statistics
```
GET /stats/{short_code}
```

Response:
```json
{
  "click_count": 42
}
```

#### Health Check
```
GET /health
```

Response:
```json
{
  "msg": "API is running"
}
```

## Testing

Run the test suite:

```bash
make run_tests
```

Or manually:

```bash
pytest
```

## Project Structure

```
url-shortener/
├── src/
│   ├── alembic/           # Database migrations
│   ├── core/              # Core utilities (settings, logging, exceptions)
│   ├── db/                # Database configuration and unit of work
│   ├── dtos/              # Data transfer objects
│   ├── models/            # SQLAlchemy models
│   ├── services/          # Business logic handlers
│   ├── test/              # Tests
│   └── main.py            # FastAPI application entry point
├── .env                   # Environment variables (not in git)
├── Dockerfile             # Docker configuration
├── makefile               # Common commands
├── pyproject.toml         # Project dependencies
└── README.md              # This file
```

## Scalability Considerations

This project includes scalability considerations documented in [SCALABILITY.md](SCALABILITY.md), covering:

1. **Heavy logging per request**: Queue-based logging with background workers
2. **Multi-instance deployment**: Shared cache, message broker, and load balancing
3. **Heavy traffic/campaigns**: Cache-first lookups, async logging, rate limiting

## Development

### Available Make Commands

```bash
make run           # Start development server
make run_tests     # Run test suite
make run_migrations# Apply database migrations
```

### Code Style

The project uses Ruff for linting with isort configuration. Run:

```bash
ruff check src/
```

## License

This project is provided as-is for educational and commercial use.