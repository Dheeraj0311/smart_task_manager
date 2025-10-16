#!/bin/bash

echo "Starting Smart Task Manager Flask Backend..."
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo
    echo "Please edit .env file with your MySQL database credentials before running the app."
    echo
    read -p "Press Enter to continue..."
    exit 1
fi

# Start the Flask application
echo "Starting Flask application..."
echo "API will be available at: http://localhost:5000"
echo
python app.py


