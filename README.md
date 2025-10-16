# Smart Task Manager - Flask Backend

A RESTful API for task management with JWT authentication, built with Flask and MySQL.

## Features

- 🔐 JWT-based authentication (register/login)
- 📝 Complete CRUD operations for tasks
- 📊 Task analytics and statistics
- 🎯 Priority levels (Low, Medium, High)
- ✅ Task status tracking (Pending, Completed)
- 📅 Due date management
- 🔍 Task filtering and search
- 🛡️ Input validation and error handling

## Quick Start

### Prerequisites

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


