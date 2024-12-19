import os
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
import firebase_admin 
from firebase_admin import auth, credentials 

cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    from app import db
    from models import User
    if not request.is_json:
        return jsonify(message="Request must be JSON"), 415
    data = request.get_json()
    
    if "email" not in data or "password" not in data or "username" not in data:
        return jsonify(message="Email, username, and password are required."), 400  

    existing_user = db.session.query(User).filter_by(email=data["email"]).first()
    if existing_user:
        return jsonify(message="User already exists in Database. Please log in."), 400
    try:
        firebase_user = auth.get_user_by_email(data["email"])
        firebase_uid = firebase_user.uid
    except firebase_admin.exceptions.NotFoundError:
        
        try:
            firebase_user = auth.create_user(
                email=data["email"],
                password=data["password"]
            )
            firebase_uid = firebase_user.uid
        except firebase_admin.exceptions.FirebaseError as e:
            return jsonify(message=f"Firebase error: {str(e)}"), 400  

    hashed_password = generate_password_hash(data["password"])
    new_user = User(username=data["username"], 
                    password=hashed_password,
                    firebase_uid=firebase_uid,
                    email=data["email"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message="User registered successfully"), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    from models import User
    from app import db

    data = request.json
    if "token" in data:
        try:
            decoded_token = auth.verify_id_token(data["token"])
            firebase_uid = decoded_token["uid"]
            email = decoded_token["email"]

            user = User.query.filter_by(firebase_uid=firebase_uid).first()
            if not user:
                new_user = User(
                    username=email.split('@')[0],
                    firebase_uid=firebase_uid,
                    email=email,
                    password=None, 
                    role="user",
                )
                db.session.add(new_user)
                db.session.commit()
                user = new_user

            additional_claims = {"username": user.username, "role": user.role}
            access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)
            refresh_token = create_refresh_token(identity=str(user.id), additional_claims=additional_claims)

            return jsonify(
                access_token=access_token,
                refresh_token=refresh_token,
                username=user.username,
            ), 200

        except Exception as e:
            return jsonify(message="Invalid Firebase token", details=str(e)), 401
    
    if "email" in data and "password" in data:
        user = User.query.filter_by(email=data["email"]).first()
        if not user:
            return jsonify(message="User not found. Please register first."), 404        
        if user.firebase_uid and user.password is None:
            return jsonify(message="Please use Google Sign-In for this account."), 400

        try:
            firebase_user = auth.get_user_by_email(data["email"])
        except Exception as e:
            return jsonify(message="Firebase email not found.", details=str(e)), 404
        if check_password_hash(user.password, data["password"]):
            additional_claims = {"username": user.username, "role": user.role}
            access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)
            refresh_token = create_refresh_token(identity=str(user.id), additional_claims=additional_claims)

            return jsonify(
                access_token=access_token,
                refresh_token=refresh_token,
                username=user.username,
            ), 200

        return jsonify(message="Invalid credentials."), 401
    return jsonify(message="Invalid request format."), 400


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    current_user = get_jwt_identity()  
    additional_claims = {"username": get_jwt()["username"], "role": get_jwt()["role"]} 
    new_access_token = create_access_token(identity=current_user, additional_claims=additional_claims)  
    return jsonify(access_token=new_access_token), 200

@auth_bp.route('/check-user', methods=['POST'])
def check_user():
    from app import db
    from models import User
    
    try:
        data = request.json
        email = data.get('email')

        if not email:
            return jsonify({"error": "Email is required"}), 400
        user = db.session.query(User).filter_by(email=email).first()

        if user:
            return jsonify(is_registered=True), 200
        else:
            return jsonify(is_registered=False), 200
    except Exception as e:   
        return jsonify({"error": "Internal server error"}), 500 

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    from app import db
    from models import User

    if not request.is_json:
        return jsonify(message="Request must be JSON"), 415

    data = request.get_json()
    username = data.get("username")
    new_password = data.get("new_password")

    if not username or not new_password:
        return jsonify(message="Username and new password are required"), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify(message="User not found"), 404

    hashed_password = generate_password_hash(new_password)
    user.password = hashed_password
    db.session.commit()
    return jsonify(message="Password updated successfully"), 200


@auth_bp.route("/change-password", methods=["POST"])
@jwt_required()
def change_password():
    from app import db
    from models import User

    data = request.get_json()
    current_password = data.get("current_password")
    new_password = data.get("new_password")

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user or not check_password_hash(user.password, current_password):
        return jsonify(message="Current password is incorrect"), 401

    user.password = generate_password_hash(new_password)
    db.session.commit()
    return jsonify(message="Password updated successfully"), 200
   

@auth_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    from models import User
    users = User.query.all()
    user_data = [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            
        }
        for user in users
    ]
    return jsonify(users=user_data), 200


@auth_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    from app import db
    from models import User

    data = request.get_json()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    user.username = data.get("username", user.username)
    user.role = data.get("role", user.role)
    db.session.commit()
    return jsonify({"message": "User updated successfully"}), 200

@auth_bp.route('/users/delete/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    from app import db
    from models import User

    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200

@auth_bp.route("/update-username", methods=["POST"])
@jwt_required()
def update_username():
    from app import db
    from models import User
    """
    Endpoint to update the username of a user.
    """
    data = request.get_json()
    new_username = data.get("new_username")

    if not new_username or len(new_username.strip()) == 0:
        return jsonify(message="New username cannot be empty"), 400

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify(message="User not found"), 404
    existing_user = User.query.filter_by(username=new_username).first()
    if existing_user:
        return jsonify(message="Username already taken"), 409

    user.username = new_username
    db.session.commit()
    return jsonify(message="Username updated successfully"), 200