from flask import Blueprint
from app.controllers.auth_controller import user_signup_controller,seller_signup_controller, login_controller, get_all_users_controller,get_user_by_id_controller,profile_controller, assign_role_to_user_controller,refresh_token_controller,logout_controller,forgot_password_controller,reset_password_controller



auth_bp = Blueprint("auth", __name__)

auth_bp.route("/signup/user", methods=["POST"])(user_signup_controller)
auth_bp.route("/signup/seller", methods=["POST"])(seller_signup_controller)
auth_bp.route("/login", methods=["POST"])(login_controller)
auth_bp.route("/users", methods=["GET"])(get_all_users_controller)
auth_bp.route("/users/<int:user_id>", methods=["GET"])(get_user_by_id_controller)
auth_bp.route("/profile", methods=["GET"])(profile_controller)
auth_bp.route("/assign-role", methods=["POST"])(assign_role_to_user_controller)
auth_bp.route("/refresh", methods=["POST"])(refresh_token_controller)
auth_bp.route("/logout", methods=["POST"])(logout_controller)
auth_bp.route("/forgot-password", methods=["POST"])(forgot_password_controller)
auth_bp.route("/reset-password", methods=["POST"])(reset_password_controller)