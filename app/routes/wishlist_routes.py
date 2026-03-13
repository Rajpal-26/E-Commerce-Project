from flask import Blueprint
from app.controllers.wishlist_controller import get_wishlist_controller, add_wishlist_controller, \
     remove_wishlist_controller, clear_wishlist_controller,move_to_cart_controller

wishlist_bp = Blueprint("wishlist",__name__)

wishlist_bp.route("/get", methods=["GET"])(get_wishlist_controller)
wishlist_bp.route("/add", methods=["POST"])(add_wishlist_controller)
wishlist_bp.route("/remove/<int:product_id>", methods =["DELETE"])(remove_wishlist_controller)
wishlist_bp.route("/clear", methods=["DELETE"])(clear_wishlist_controller)
wishlist_bp.route("/add-to-cart/<int:product_id>", methods=["POST"])(move_to_cart_controller)