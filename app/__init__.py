from datetime import timedelta
import os

from flask import Flask, g
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from config import Config
from app.extensions import cache, db, migrate, jwt, mail, redis_client
from app.models import *

from rate_limit.limiter import global_rate_limit
from flask import request



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Only use RedisCache if we successfully connected to Redis in extensions.py
    if hasattr(redis_client, 'ping'):
        app.config["CACHE_TYPE"] = "RedisCache"
    else:
        app.config["CACHE_TYPE"] = "SimpleCache"

    # let redis url come from Config.REDIS_URL or env
    app.config["CACHE_REDIS_URL"] = app.config.get("REDIS_URL")

    # initialize cache if available; fallback implementation is safe
    try:
        cache.init_app(app)
    except Exception:
        pass

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
  
    # Consolidated before_request hook for rate limiting, auth, and user loading.
    # This replaces the three separate hooks to ensure correct execution order and logic.
    @app.before_request
    def before_request_handler():
        # --- 1. Global Rate Limiter ---
        # Skip rate limiting for auth and gmail routes (OAuth flows shouldn't be limited).
        if request.path.startswith("/auth") or request.path.startswith("/gmail"):
            pass  # Continue to the next step
        else:
            rate_limit_result = global_rate_limit(window=60)
            if rate_limit_result:
                return rate_limit_result

        # --- 2. Auth and User Loading ---

        # Allow browser CORS preflight (OPTIONS) requests to pass through without checks.
        if request.method == "OPTIONS":
            return

        # Define endpoints that are publicly accessible without a token.
        public_endpoints = [
            "home",
            "gmail.gmail_login_controller",
            "gmail.gmail_callback_controller",
            "auth.user_signup_controller",
            "auth.seller_signup_controller",
            "auth.login_controller",
            "auth.forgot_password_controller",
            "auth.reset_password_controller",
            "static"  # Allows access to static files.
        ]

        # If no route is matched, request.endpoint is None.
        # Let Flask handle it as a 404, not an auth error.
        if request.endpoint is None:
            g.current_user = None
            return

        is_public = request.endpoint in public_endpoints

        # --- 3. Token Verification and User Loading ---
        try:
            # For public endpoints, token is optional. For others, it's required.
            verify_jwt_in_request(optional=is_public)

            user_id = get_jwt_identity()
            if user_id:
                from app.models.user import User
                g.current_user = User.query.get(int(user_id))
            else:
                g.current_user = None
        except Exception as e:
            # This block is hit if verify_jwt_in_request(optional=False) fails.
            # Set user to None and re-raise the exception, which contains the JSON error response.
            g.current_user = None
            if not is_public:
                raise e

    @app.route("/")
    def home():
        return "Server is running"

    from app import models

    from app.routes.product_routes import product_bp
    app.register_blueprint(product_bp, url_prefix="/api/products")

    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.routes.address_routes import address_bp
    app.register_blueprint(address_bp, url_prefix="/address")

    from app.routes.cart_routes import cart_bp
    app.register_blueprint(cart_bp, url_prefix="/api/cart")

    from app.routes.order_routes import order_bp
    app.register_blueprint(order_bp, url_prefix="/api/orders")
    
    from app.routes.wishlist_routes import wishlist_bp
    app.register_blueprint(wishlist_bp, url_prefix="/api/wishlist")
    
    from app.routes.review_routes import review_bp
    app.register_blueprint(review_bp, url_prefix="/reviews")
    
    from app.routes.gmail_routes import gmail_bp
    app.register_blueprint(gmail_bp, url_prefix="/gmail")

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # If uploads is at project root level
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER



    return app
