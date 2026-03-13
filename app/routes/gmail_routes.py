from flask import Blueprint
from app.controllers.gmail_controller import gmail_login_controller, gmail_callback_controller

gmail_bp = Blueprint("gmail", __name__)

gmail_bp.route("/login",methods=["GET"])(gmail_login_controller)
gmail_bp.route("/callback",methods=["GET"])(gmail_callback_controller)