"""
Task management routes for CRUD operations
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from models.task import Task, Priority, Status
from models.user import User
from extensions import db
from utils.helpers import parse_datetime

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    """
    Create a new task
    
    Expected JSON payload:
    {
        "title": "string",
        "description": "string (optional)",
        "due_date": "string (ISO format, optional)",
        "priority": "Low|Medium|High (optional, defaults to Medium)"
    }
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate required fields
        if 'title' not in data or not data['title'].strip():
            return jsonify({'error': 'Title is required'}), 400
        
        title = data['title'].strip()
        description = data.get('description', '').strip() if data.get('description') else None
        due_date = None
        priority = Priority.MEDIUM
        
        # Parse due_date if provided
        if 'due_date' in data and data['due_date']:
            due_date = parse_datetime(data['due_date'])
            if not due_date:
                return jsonify({'error': 'Invalid due_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400
        
        # Parse priority if provided
        if 'priority' in data and data['priority']:
            try:
                priority = Priority(data['priority'].title())
            except ValueError:
                return jsonify({'error': 'Invalid priority. Must be Low, Medium, or High'}), 400
        
        # Create new task
        task = Task(
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            user_id=user_id
        )
        
        db.session.add(task)
        db.session.commit()
        
        return jsonify({
            'message': 'Task created successfully',
            'task': task.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create task', 'details': str(e)}), 500

@tasks_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    """
    Get all tasks for the current user
    
    Query parameters:
    - status: Filter by status (Pending, Completed)
    - priority: Filter by priority (Low, Medium, High)
    - overdue: Filter overdue tasks (true/false)
    """
    try:
        user_id = get_jwt_identity()
        
        # Build query
        query = Task.query.filter_by(user_id=user_id)
        
        # Apply filters
        status_filter = request.args.get('status')
        if status_filter:
            try:
                status_enum = Status(status_filter.title())
                query = query.filter_by(status=status_enum)
            except ValueError:
                return jsonify({'error': 'Invalid status filter'}), 400
        
        priority_filter = request.args.get('priority')
        if priority_filter:
            try:
                priority_enum = Priority(priority_filter.title())
                query = query.filter_by(priority=priority_enum)
            except ValueError:
                return jsonify({'error': 'Invalid priority filter'}), 400
        
        overdue_filter = request.args.get('overdue')
        if overdue_filter and overdue_filter.lower() == 'true':
            query = query.filter(Task.due_date < datetime.utcnow(), Task.status == Status.PENDING)
        
        # Execute query and sort by created_at desc
        tasks = query.order_by(Task.created_at.desc()).all()
        
        return jsonify({
            'tasks': [task.to_dict() for task in tasks],
            'count': len(tasks)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get tasks', 'details': str(e)}), 500

@tasks_bp.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    """
    Get a specific task by ID
    """
    try:
        user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        return jsonify({
            'task': task.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get task', 'details': str(e)}), 500

@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    """
    Update a specific task
    
    Expected JSON payload (all fields optional):
    {
        "title": "string",
        "description": "string",
        "due_date": "string (ISO format)",
        "priority": "Low|Medium|High",
        "status": "Pending|Completed"
    }
    """
    try:
        user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Update fields if provided
        if 'title' in data and data['title']:
            task.title = data['title'].strip()
        
        if 'description' in data:
            task.description = data['description'].strip() if data['description'] else None
        
        if 'due_date' in data:
            if data['due_date']:
                due_date = parse_datetime(data['due_date'])
                if not due_date:
                    return jsonify({'error': 'Invalid due_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400
                task.due_date = due_date
            else:
                task.due_date = None
        
        if 'priority' in data and data['priority']:
            try:
                task.priority = Priority(data['priority'].title())
            except ValueError:
                return jsonify({'error': 'Invalid priority. Must be Low, Medium, or High'}), 400
        
        if 'status' in data and data['status']:
            try:
                task.status = Status(data['status'].title())
            except ValueError:
                return jsonify({'error': 'Invalid status. Must be Pending or Completed'}), 400
        
        # Update timestamp
        task.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Task updated successfully',
            'task': task.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update task', 'details': str(e)}), 500

@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """
    Delete a specific task
    """
    try:
        user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        db.session.delete(task)
        db.session.commit()
        
        return jsonify({
            'message': 'Task deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete task', 'details': str(e)}), 500

@tasks_bp.route('/tasks/stats', methods=['GET'])
@jwt_required()
def get_task_stats():
    """
    Get task statistics for the current user
    """
    try:
        user_id = get_jwt_identity()
        
        # Get all tasks for the user
        all_tasks = Task.query.filter_by(user_id=user_id).all()
        
        # Calculate statistics
        total_tasks = len(all_tasks)
        completed_tasks = len([t for t in all_tasks if t.status == Status.COMPLETED])
        pending_tasks = len([t for t in all_tasks if t.status == Status.PENDING])
        overdue_tasks = len([t for t in all_tasks if t.is_overdue()])
        
        # Priority breakdown
        priority_stats = {
            'low': len([t for t in all_tasks if t.priority == Priority.LOW]),
            'medium': len([t for t in all_tasks if t.priority == Priority.MEDIUM]),
            'high': len([t for t in all_tasks if t.priority == Priority.HIGH])
        }
        
        return jsonify({
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'overdue_tasks': overdue_tasks,
            'completion_rate': round((completed_tasks / total_tasks * 100), 2) if total_tasks > 0 else 0,
            'priority_breakdown': priority_stats
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get task statistics', 'details': str(e)}), 500


