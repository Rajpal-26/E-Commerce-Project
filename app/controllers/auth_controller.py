from flask import jsonify, request
from app.extensions import redis_client
from flask_jwt_extended import create_access_token,create_refresh_token, get_jwt, jwt_required, get_jwt_identity

from app.logger import logger
from app.rbac.decorators import permission_required
from app.rbac.constants import Permission
from app.models.user import User
from app.services.auth_services import register_user, login_user
from rate_limit.limiter import ip_based_rate_limit
from app.services.auth_services import (
    forgot_password_service,
    reset_password_service
)
from app.services.email_services import send_email


def user_signup_controller():
    """Public endpoint - no authentication required"""
    try:
        data = request.get_json()

        user, error = register_user(
            data.get("name"),
            data.get("email"),
            data.get("password"),
            data.get("confirm_password"),
            role_name="user"
        )

        if error:
            logger.warning("Failed to signup")
            return jsonify({"error": error}), 400

        logger.info(f"Signup Successfully for user {user.email}")
        return jsonify({
            "message": "User registered successfully",
            "user_id": user.id
        }), 201


    except Exception as e:
        logger.error("Signup error", exc_info=True)
        return jsonify({
            "error": "Failed to Signup",
            "details": str(e)
        }), 500
        
def seller_signup_controller():
    """Public endpoint - no authentication required"""
    try:
        data = request.get_json()

        user, error = register_user(
            data.get("name"),
            data.get("email"),
            data.get("password"),
            data.get("confirm_password"),
            role_name="seller"
        )

        if error:
            logger.warning("Failed to signup")
            return jsonify({"error": error}), 400

        logger.info(f"Signup Successfully for seller {user.email}")
        return jsonify({
            "message": "Seller registered successfully",
            "user_id": user.id
        }), 201

    except Exception as e:
        logger.error("Signup error", exc_info=True)
        return jsonify({
            "error": "Failed to Signup",
            "details": str(e)
        }), 500
        
@ip_based_rate_limit(limit=5, window=60)  # Limit to 5 login attempts per IP per minute
def login_controller():
    
    try:
        data = request.get_json()

        user, error = login_user(
            data.get("email"),
            data.get("password")
        )


        if error:
             return jsonify({"error": error}), 401
         
        additional_claims = {
            "role": user.roles[0].name
        }

        

        access_token = create_access_token(
        identity=(user.id),
        additional_claims= additional_claims)
        
        refresh_token = create_refresh_token(
        identity=(user.id), 
        additional_claims=additional_claims)
        
        # Get user's roles
        user_roles = [role.name for role in user.roles]

        return jsonify({
            "message": f"Welcome {user.name}, you have successfully logged in to your dashboard",
            "access_token": access_token,
            "refresh_token": refresh_token,
            f"{user.roles[0].name}": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "roles": user_roles
            }
        }), 200

    except Exception as e:
        logger.error("Login error", exc_info= True)
        return jsonify({
            "error": "Failed to Login",
            "details": str(e)
        }), 500

@jwt_required()
@permission_required(Permission.MANAGE_USERS)
def get_all_users_controller():
    try:
        users = User.query.all()

        users_list = []
        for user in users:
            users_list.append({
                "id": user.id,
                "name": user.name,
                "email": user.email
            })
            logger.info(f"Get all products for user {user.email}")

        return jsonify({
            "total": len(users_list),
            "users": users_list
        }), 200
    except Exception as e:
        return  jsonify({
            "error": "Failed to get all User",
            "details": str(e)
        }), 500

@jwt_required()
@permission_required(Permission.MANAGE_USERS)
def get_user_by_id_controller(user_id):
    try:
        user = User.query.get(user_id)

        logger.info("Get user by id")
        if not user:
            logger.warning("Failed to get user : User not found")
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email
        }), 200

    except Exception as e:
        logger.error("get user error by id ", exc_info=True)
        return jsonify({
            "error": "failed to get user by id",
            "details": str(e)
        }), 500

@jwt_required()
def profile_controller():
    try:
        user_id = get_jwt_identity()

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "message": f"Authenticated user id: {user_id}",
            "name": user.name,
            "email": user.email
        }), 200

    except Exception as e:
        return jsonify({
            "error": "failed to get profile",
            "details": str(e)
        }), 500


@jwt_required()
@permission_required(Permission.MANAGE_USERS)
def assign_role_to_user_controller():
    
    try:
        from app.models.roles import Role
        from app.extensions import db
        logger.info("Assign role endpoint hit - Public access")
        
        data = request.get_json()
        user_id = data.get("user_id")
        role_name = data.get("role")
        
        if not user_id or not role_name:
            return jsonify({"error": "user_id and role are required"}), 400
        
        user = User.query.get(user_id)
        role = Role.query.filter_by(name=role_name).first()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        if not role:
            return jsonify({"error": "Role not found"}), 404
        
        # Add role if not already assigned
        if role not in user.roles:
            user.roles.append(role)
            db.session.commit()
        
        logger.info(f"Assigned {role_name} role to user {user.email}")
        
        return jsonify({
            "message": f"Assigned {role_name} role to user {user.name}",
            "user_id": user.id,
            "user_email": user.email,
            "roles": [r.name for r in user.roles]
        }), 200
    
    except Exception as e:
        logger.error(f"Failed to assign role: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500
    
    
@jwt_required(refresh=True)
def refresh_token_controller():
    identity = get_jwt_identity()
    claims = get_jwt()

    new_access_token = create_access_token(
        identity=identity,
        additional_claims={
            "role": claims["role"]
        }
    )

    new_refresh_token = create_refresh_token(
        identity=identity,
        additional_claims={
            "role": claims["role"]
        }
    )

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token
    }

@jwt_required()
def logout_controller():
    try:
        jti = get_jwt()["jti"]
        
        redis_client.setex(jti, 3600, "revoked")
        logger.info(f"User logged out, token revoked with jti: {jti}")
        return jsonify({"msg": "Successfully logged out"}), 200
    
    except Exception as e:
        logger.error("Logout error", exc_info=True)
        return jsonify({
            "error": "Logout failed",
            "details": str(e)
        }), 500
        
  
def forgot_password_controller():

    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email required"}), 400

    otp, error = forgot_password_service(email)

    if error:
        return jsonify({"error": error}), 400

    send_email(
        to=email,
        subject="Password Reset OTP",
        body=f"Your OTP is {otp}. It expires in 5 minutes."
    )

    return jsonify({
        "message": "OTP sent successfully"
    }), 200



def reset_password_controller():

    data = request.get_json()

    email = data.get("email")
    otp = data.get("otp")
    new_password = data.get("new_password")

    if not email or not otp or not new_password:
        return jsonify({"error": "Email, OTP and password required"}), 400

    success, error = reset_password_service(email, otp, new_password)

    if error:
        return jsonify({"error": error}), 400

    return jsonify({
        "message": "Password reset successful"
    }), 200