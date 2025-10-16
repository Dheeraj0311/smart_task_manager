# Smart Task Manager - Flask Backend

A RESTful API for task management with JWT authentication, built with Flask and MySQL.

## Overview

Smart Task Manager is a backend-only, production-ready REST API for creating, organizing, and tracking personal or team tasks. It uses Flask with SQLAlchemy (MySQL) and JWT-based authentication to securely manage users and their tasks. The API is modular (blueprints), easy to extend, and designed to be a strong foundation for future AI features like smart prioritization and natural language task entry.

## Why use this project

- **Clean architecture**: Factory pattern, centralized extensions, blueprints, and utilities.
- **Security-first**: JWT auth, password hashing, and input validation.
- **Production friendly**: Environment-based config, error handling, and ENUM-backed fields.
- **Extensible**: Clear separation of concerns for adding features like tags, comments, reminders, or AI.
- **Tooling**: Postman collection and a simple test script are included for quick verification.

## Key points at a glance

- **Auth**: Register/Login with JWT tokens; secure password hashing.
- **Tasks**: CRUD with priority (Low/Medium/High), status (Pending/Completed), and due dates.
- **Analytics**: Completion rate, overdue counts, and priority breakdown.
- **Filters**: Query tasks by status, priority, and overdue.
- **No frontend**: Pure JSON APIs for Postman or frontend/mobile apps.

## Common use cases

- Building a React/Flutter/Android frontend on top of a stable API.
- Integrating with automation/chatbots that create tasks via JSON.
- Extending with AI to prioritize tasks or parse natural language inputs.

## Features

## Architecture

High-level layout of the backend:

- `app.py`: App factory (`create_app`) that loads config, initializes extensions, registers blueprints, and creates tables.
- `extensions.py`: Centralized instances of `SQLAlchemy` and `JWTManager` to avoid circular imports.
- `models/`: Database models (`User`, `Task`) with clear relationships and enums for `priority` and `status`.
- `routes/`: Modular blueprints (`auth.py`, `tasks.py`) exposing REST endpoints only (JSON in/out).
- `utils/`: Helper utilities (validation, datetime parsing) to keep routes thin.
- `config.py`: Environment-driven configuration; MySQL credentials are URL-encoded for safety.

Data flow:
1) Client → Auth endpoints → JWT issued.
2) Client sends `Authorization: Bearer <token>` → Task endpoints.
3) SQLAlchemy persists data to MySQL; errors returned as structured JSON.

## Troubleshooting

### MySQL connection errors (OperationalError, connection refused)
- Ensure MySQL is running and listening on `localhost:3306`.
- Verify `.env` has the correct creds:
  - `MYSQL_HOST=localhost`, `MYSQL_PORT=3306`, `MYSQL_USERNAME`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`.
- If your password contains special characters (`@`, `#`, `:`), it's handled via URL-encoding in `config.py`.
- Test port: `Test-NetConnection localhost -Port 3306` (PowerShell).

### Flask cannot find Flask/SQLAlchemy (ModuleNotFoundError)
- Use the project virtual environment:
  - Windows: `venv\Scripts\activate` then `python app.py`
  - Or run directly with venv Python: `venv\Scripts\python app.py`

### Port 5000 already in use
- Find the PID and kill it:
  - PowerShell: `netstat -ano | findstr :5000` then `taskkill /PID <PID> /F`.

### 401 Unauthorized on protected endpoints
- Include the header: `Authorization: Bearer <your_jwt_token>`.
- Regenerate token by logging in again if expired.

### JSON validation errors
- Check required fields and formats (e.g., ISO datetime like `2025-10-20T18:00:00`).


- 🔐 JWT-based authentication (register/login)
- 📝 Complete CRUD operations for tasks
- 📊 Task analytics and statistics
- 🎯 Priority levels (Low, Medium, High)
- ✅ Task status tracking (Pending, Completed)
- 📅 Due date management
- 🔍 Task filtering and search
- 🛡️ Input validation and error handling

## Quick Start

### Prerequisite
- Python 3.10+
- MySQL 5.7+ or MySQL 8.0+
- pip (Python package manager)

### Installation

1. **Clone or download the project**
   ```bash
   cd smart_task_manager
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MySQL database**
   - Create a MySQL database named `smart_task_manager`
   - Update database credentials in `.env` file

5. **Configure environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your database credentials
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/register` | Register new user | No |
| POST | `/api/login` | Login user | No |
| GET | `/api/profile` | Get user profile | Yes |

### Task Management

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/tasks` | Create new task | Yes |
| GET | `/api/tasks` | Get all user tasks | Yes |
| GET | `/api/tasks/<id>` | Get specific task | Yes |
| PUT | `/api/tasks/<id>` | Update task | Yes |
| DELETE | `/api/tasks/<id>` | Delete task | Yes |
| GET | `/api/tasks/stats` | Get task statistics | Yes |

### Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | API health status |

## Testing with Postman

### 1. Register a new user
```json
POST http://localhost:5000/api/register
Content-Type: application/json

{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
}
```

### 2. Login
```json
POST http://localhost:5000/api/login
Content-Type: application/json

{
    "username": "testuser",
    "password": "password123"
}
```

### 3. Create a task (use JWT token from login)
```json
POST http://localhost:5000/api/tasks
Content-Type: application/json
Authorization: Bearer YOUR_JWT_TOKEN

{
    "title": "Complete project documentation",
    "description": "Write comprehensive API documentation",
    "due_date": "2024-01-15T18:00:00",
    "priority": "High"
}
```

### 4. Get all tasks
```json
GET http://localhost:5000/api/tasks
Authorization: Bearer YOUR_JWT_TOKEN
```

### 5. Get task statistics
```json
GET http://localhost:5000/api/tasks/stats
Authorization: Bearer YOUR_JWT_TOKEN
```

## Database Schema

### Users Table
- `id` (Primary Key)
- `username` (Unique)
- `email` (Unique)
- `password_hash`
- `created_at`

### Tasks Table
- `id` (Primary Key)
- `title`
- `description`
- `due_date`
- `priority` (Low, Medium, High)
- `status` (Pending, Completed)
- `user_id` (Foreign Key)
- `created_at`
- `updated_at`

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment | `development` |
| `SECRET_KEY` | Flask secret key | Required |
| `JWT_SECRET_KEY` | JWT secret key | Required |
| `MYSQL_HOST` | MySQL host | `localhost` |
| `MYSQL_PORT` | MySQL port | `3306` |
| `MYSQL_USERNAME` | MySQL username | `root` |
| `MYSQL_PASSWORD` | MySQL password | Required |
| `MYSQL_DATABASE` | MySQL database name | `smart_task_manager` |

## Project Structure

```
smart_task_manager/
├── app.py                 # Main application file
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── models/              # Database models
│   ├── __init__.py
│   ├── user.py         # User model
│   └── task.py         # Task model
├── routes/              # API routes
│   ├── __init__.py
│   ├── auth.py         # Authentication routes
│   └── tasks.py        # Task management routes
└── utils/               # Utility functions
    ├── __init__.py
    └── helpers.py      # Helper functions
```

## Error Handling

The API returns consistent JSON error responses:

```json
{
    "error": "Error type",
    "message": "Detailed error message"
}
```

Common HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `404` - Not Found
- `409` - Conflict
- `500` - Internal Server Error

## Future Enhancements

This project is designed to be easily extensible for AI integration:

- 🤖 Natural language task creation
- 📈 Smart task prioritization
- 🔔 Intelligent reminders
- 📊 Advanced analytics
- 🏷️ Task categorization and tagging
- 👥 Team collaboration features

## License

This project is open source and available under the MIT License.


