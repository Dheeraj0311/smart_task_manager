"""
Test script for Smart Task Manager API
Run this script to verify the setup works correctly
"""

import requests
import json
from datetime import datetime, timedelta

# API base URL
BASE_URL = "http://localhost:5000/api"

def test_api():
    """Test the API endpoints"""
    print("🚀 Testing Smart Task Manager API...")
    print("=" * 50)
    
    # Test data
    test_user = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    }
    
    test_task = {
        "title": "Test Task",
        "description": "This is a test task",
        "due_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "priority": "High"
    }
    
    try:
        # 1. Test health endpoint
        print("1. Testing health endpoint...")
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return
        
        # 2. Test user registration
        print("\n2. Testing user registration...")
        response = requests.post(f"{BASE_URL}/register", json=test_user)
        if response.status_code == 201:
            print("✅ User registration successful")
            access_token = response.json()["access_token"]
        else:
            print(f"❌ User registration failed: {response.status_code}")
            print(f"Response: {response.text}")
            return
        
        # 3. Test user login
        print("\n3. Testing user login...")
        login_data = {
            "username": test_user["username"],
            "password": test_user["password"]
        }
        response = requests.post(f"{BASE_URL}/login", json=login_data)
        if response.status_code == 200:
            print("✅ User login successful")
            access_token = response.json()["access_token"]
        else:
            print(f"❌ User login failed: {response.status_code}")
            return
        
        # Set up headers for authenticated requests
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # 4. Test task creation
        print("\n4. Testing task creation...")
        response = requests.post(f"{BASE_URL}/tasks", json=test_task, headers=headers)
        if response.status_code == 201:
            print("✅ Task creation successful")
            task_id = response.json()["task"]["id"]
        else:
            print(f"❌ Task creation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return
        
        # 5. Test get all tasks
        print("\n5. Testing get all tasks...")
        response = requests.get(f"{BASE_URL}/tasks", headers=headers)
        if response.status_code == 200:
            tasks = response.json()["tasks"]
            print(f"✅ Retrieved {len(tasks)} tasks")
        else:
            print(f"❌ Get tasks failed: {response.status_code}")
            return
        
        # 6. Test get specific task
        print("\n6. Testing get specific task...")
        response = requests.get(f"{BASE_URL}/tasks/{task_id}", headers=headers)
        if response.status_code == 200:
            print("✅ Get specific task successful")
        else:
            print(f"❌ Get specific task failed: {response.status_code}")
            return
        
        # 7. Test task update
        print("\n7. Testing task update...")
        update_data = {
            "title": "Updated Test Task",
            "status": "Completed"
        }
        response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=update_data, headers=headers)
        if response.status_code == 200:
            print("✅ Task update successful")
        else:
            print(f"❌ Task update failed: {response.status_code}")
            return
        
        # 8. Test task statistics
        print("\n8. Testing task statistics...")
        response = requests.get(f"{BASE_URL}/tasks/stats", headers=headers)
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Task statistics retrieved: {stats['total_tasks']} total tasks")
        else:
            print(f"❌ Task statistics failed: {response.status_code}")
            return
        
        # 9. Test task deletion
        print("\n9. Testing task deletion...")
        response = requests.delete(f"{BASE_URL}/tasks/{task_id}", headers=headers)
        if response.status_code == 200:
            print("✅ Task deletion successful")
        else:
            print(f"❌ Task deletion failed: {response.status_code}")
            return
        
        print("\n" + "=" * 50)
        print("🎉 All tests passed! API is working correctly.")
        print("\nYou can now test the API using Postman with the following endpoints:")
        print(f"- Register: POST {BASE_URL}/register")
        print(f"- Login: POST {BASE_URL}/login")
        print(f"- Tasks: GET/POST/PUT/DELETE {BASE_URL}/tasks")
        print(f"- Stats: GET {BASE_URL}/tasks/stats")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure the Flask app is running on localhost:5000")
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")

if __name__ == "__main__":
    test_api()


