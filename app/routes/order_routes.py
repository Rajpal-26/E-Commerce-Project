from flask import Blueprint

from app.controllers.order_controller import order_place_controller, select_payment_controller, \
     cancel_order_controller, get_order_by_id_details_controller, get_all_orders_controller

order_bp = Blueprint("order_bp", __name__)

order_bp.route("/order-place", methods =["POST"])(order_place_controller)
order_bp.route("/select-payment", methods =["POST"])(select_payment_controller)
order_bp.route("/<int:order_id>", methods =["GET"])(get_order_by_id_details_controller)
order_bp.route("/cancel/<int:order_id>", methods =["POST"])(cancel_order_controller)
order_bp.route("/get-orders", methods =["GET"])(get_all_orders_controller)