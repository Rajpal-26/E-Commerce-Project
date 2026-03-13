from flask import  Blueprint

from app.controllers.cart_controller import get_cart_items_controller, add_cart_items_controller, \
    update_cart_items_controller, remove_cart_items_controller, clear_cart_controller

cart_bp = Blueprint("cart",__name__)

cart_bp.route("/", methods=["GET"])(get_cart_items_controller)
cart_bp.route("/add", methods=["POST"])(add_cart_items_controller)
cart_bp.route("/update/<int:item_id>", methods=["PUT"])(update_cart_items_controller)
cart_bp.route("/remove/<int:item_id>", methods =["DELETE"])(remove_cart_items_controller)
cart_bp.route("/delete", methods=["DELETE"])(clear_cart_controller)