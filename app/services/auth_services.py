import re
from flask import jsonify
from flask_jwt_extended import get_jwt
import redis

from app.extensions import db
from app.logger import logger
from app.models.user import User
from app.models.roles import Role
from app.services.email_services import send_email
import random
from werkzeug.security import generate_password_hash
from app.models.user import User
from app.extensions import redis_client, db



def register_user(name, email, password, confirm_password, role_name="user"):
    try:
        # Validate required fields
        if not name or not email or not password or not confirm_password:
            return None, "All fields are required"

        if not isinstance(name, str):
            return None, "Name must be a string"

        # Email validation
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, email):
            return None, "Invalid email format. Example: user@gmail.com"

        # Password validation
        if len(password) <= 6:
            return None, "Password must be greater than 6 characters"

        if password != confirm_password:
            return None, "Passwords do not match"

        # Check existing email
        if User.query.filter_by(email=email).first():
            return None, "Email already exists"

        # Create user
        user = User(name=name, email=email)
        user.set_password(password)

        # Assign role
        target_role = "seller" if role_name and role_name.lower() == "seller" else "user"

        role = Role.query.filter_by(name=target_role).first()

        if not role:
            return None, f"Role '{target_role}' not found in database"

        user.roles.append(role)

        db.session.add(user)
        db.session.commit()
        
        send_email(
        email,
        "Welcome to Our Store",
        f"Hello {name}, your account has been successfully created."
    )

        logger.info("User registered successfully")

        return user, None

    except Exception as e:
        return None, str(e)


def login_user(email, password):
    try:
        if not email or not password:
            return None, "All fields are required"

        user = User.query.filter_by(email=email).first()

        if not user:
            logger.warning("User not found")
            return None, "User not found"

        if not user.check_password(password):
            logger.warning(f"Invalid password for user {user.email}")
            return None, "Invalid password"
        
        send_email(
            user.email,
            "Login Alert",
            f"Hello {user.name}, you just logged into your account."
            )

        logger.info("User logged in successfully")

        return user, None

    except Exception as e:
        return None, str(e)


def forgot_password_service(email):

    user = User.query.filter_by(email=email).first()

    if not user:
        return None, "User not found"

    otp = str(random.randint(100000, 999999))

    key = f"reset_otp:{email}"

    redis_client.delete(key)
    redis_client.setex(key, 300, otp)

    return otp, None


def reset_password_service(email, otp, new_password):

    key = f"reset_otp:{email}"

    stored_otp = redis_client.get(key)
    
    if stored_otp:
        stored_otp = stored_otp.decode()

    if not stored_otp:
        return None, "OTP expired or invalid"

    if stored_otp != otp:
        return None, "Invalid OTP"

    user = User.query.filter_by(email=email).first()

    if not user:
        return None, "User not found"

    user.set_password(new_password)
    
    db.session.commit()

    redis_client.delete(key)

    return True, None
    
