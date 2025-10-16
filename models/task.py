"""
Task model for task management
"""

from datetime import datetime
from enum import Enum
from extensions import db

class Priority(Enum):
    """Task priority levels"""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class Status(Enum):
    """Task status levels"""
    PENDING = "Pending"
    COMPLETED = "Completed"

class Task(db.Model):
    """Task model for task management"""
    
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    priority = db.Column(db.Enum(Priority), default=Priority.MEDIUM, nullable=False)
    status = db.Column(db.Enum(Status), default=Status.PENDING, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __init__(self, title, user_id, description=None, due_date=None, priority=Priority.MEDIUM, status=Status.PENDING):
        """Initialize a new task"""
        self.title = title
        self.user_id = user_id
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.status = status
    
    def to_dict(self):
        """Convert task object to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'priority': self.priority.value if self.priority else None,
            'status': self.status.value if self.status else None,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def is_overdue(self):
        """Check if the task is overdue"""
        if self.due_date and self.status == Status.PENDING:
            return datetime.utcnow() > self.due_date
        return False
    
    def __repr__(self):
        return f'<Task {self.title}>'


