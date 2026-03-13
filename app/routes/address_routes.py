from flask import Blueprint

from app.controllers.address_controller import get_address_controller, create_address_controller, \
    update_address_controller, delete_address_controller, get_address_by_id_controller

address_bp = Blueprint("address", __name__)

address_bp.route("/", methods=["GET"])(get_address_controller)
address_bp.route("/<int:address_id>", methods=["GET"])(get_address_by_id_controller)
address_bp.route("/", methods=["POST"])(create_address_controller)
address_bp.route("/<int:address_id>", methods=["PUT"])(update_address_controller)
address_bp.route("/<int:address_id>", methods=["DELETE"])(delete_address_controller)
