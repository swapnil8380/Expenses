from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.models import User
from app.extensions import db
import uuid 

def register_auth_routes(app):

    @app.route('/register', methods=['POST'])
    def register():
        data = request.json
        username= data.get('username')
        password= data.get('password')
        email=  data.get('email')
        mobile_no = data.get('mobile_no')

        if not username or not password or not email or not  mobile_no:
            return jsonify({"error": "Please provied complete user details"}), 400
                        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({"error": "User already exists"}), 400
        if User.query.filter_by(mobile_number=data['mobile_no']).first():
            return jsonify({"error": "mobile_no already exists"}), 400
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"error": "email already exists"}), 400

        hashed_password = generate_password_hash(data['password'])
        id = str(uuid.uuid4())
        user = User(username=data['username'], password_hash=hashed_password, id=id, email=data['email'] , mobile_number=data['mobile_no'] )
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201

    @app.route('/login', methods=['POST'])
    def login():
        try:
            data = request.json
            user = User.query.filter_by(username=data['username']).first()
            if not user or not check_password_hash(user.password_hash, data['password']):
                return jsonify({"error": "Invalid credentials"}), 401

            token = create_access_token(identity=user.id)
            return jsonify({"access_token": token}), 200
        except Exception as e:
        # Log the error and return a message to the client
            app.logger.error(f"Error during login: {str(e)}")
            return jsonify({"error": "Internal Server Error", "details": str(e)}), 500