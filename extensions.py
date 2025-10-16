from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Centralized extensions to avoid circular imports
db = SQLAlchemy()
jwt = JWTManager()


