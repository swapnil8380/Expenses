from flask import Flask
from app.config import Config
from app.extensions import db, migrate
from app.auth import register_auth_routes
from app.expenses import register_expense_routes
from flask_jwt_extended import JWTManager
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    jwt = JWTManager()
    # Initialize extensions
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all() 

    # Register routes from separate files
    register_auth_routes(app)
    register_expense_routes(app)

    return app
