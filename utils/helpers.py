"""
Helper utility functions for the Smart Task Manager
"""

import re
from datetime import datetime
from typing import Optional

def validate_email(email: str) -> bool:
    """
    Validate email format using regex
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if email is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password: str) -> bool:
    """
    Validate password strength
    
    Args:
        password (str): Password to validate
        
    Returns:
        bool: True if password meets requirements, False otherwise
    """
    return len(password) >= 6

def parse_datetime(date_string: str) -> Optional[datetime]:
    """
    Parse datetime string in various formats
    
    Args:
        date_string (str): Date string to parse
        
    Returns:
        Optional[datetime]: Parsed datetime object or None if parsing fails
    """
    if not date_string:
        return None
    
    # List of common datetime formats to try
    formats = [
        '%Y-%m-%dT%H:%M:%S',      # ISO format: 2023-12-25T14:30:00
        '%Y-%m-%dT%H:%M:%S.%f',   # ISO format with microseconds
        '%Y-%m-%dT%H:%M:%SZ',     # ISO format with Z suffix
        '%Y-%m-%d %H:%M:%S',      # Standard format: 2023-12-25 14:30:00
        '%Y-%m-%d',               # Date only: 2023-12-25
        '%m/%d/%Y',               # US format: 12/25/2023
        '%d/%m/%Y',               # EU format: 25/12/2023
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_string.strip(), fmt)
        except ValueError:
            continue
    
    return None

def format_datetime(dt: datetime) -> str:
    """
    Format datetime object to ISO string
    
    Args:
        dt (datetime): Datetime object to format
        
    Returns:
        str: Formatted datetime string
    """
    return dt.isoformat()

def sanitize_string(text: str) -> str:
    """
    Sanitize string input by removing extra whitespace
    
    Args:
        text (str): Text to sanitize
        
    Returns:
        str: Sanitized text
    """
    if not text:
        return ""
    return text.strip()

def validate_priority(priority: str) -> bool:
    """
    Validate priority value
    
    Args:
        priority (str): Priority to validate
        
    Returns:
        bool: True if priority is valid, False otherwise
    """
    valid_priorities = ['low', 'medium', 'high']
    return priority.lower() in valid_priorities

def validate_status(status: str) -> bool:
    """
    Validate status value
    
    Args:
        status (str): Status to validate
        
    Returns:
        bool: True if status is valid, False otherwise
    """
    valid_statuses = ['pending', 'completed']
    return status.lower() in valid_statuses

def calculate_completion_rate(completed: int, total: int) -> float:
    """
    Calculate completion rate percentage
    
    Args:
        completed (int): Number of completed tasks
        total (int): Total number of tasks
        
    Returns:
        float: Completion rate as percentage
    """
    if total == 0:
        return 0.0
    return round((completed / total) * 100, 2)


