from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.rbac.decorators import permission_required
from app.rbac.constants import Permission
from app.services.order_services import (
    order_place_service,
    select_payment_service,
    get_order_by_id_details_service,
    cancel_order_service,
    get_all_orders_service,
)


@jwt_required()
@permission_required(Permission.PLACE_ORDER)
def order_place_controller():
    user_id = get_jwt_identity()
    data = request.get_json()

    address_id = data.get("address_id")
    if not address_id:
        return jsonify({"error": "address_id is required"}), 400

    # params = {
    #     "user_id": request.args.get("user_id", type= int),
    #     "order": request.args.get("order", "desc"),
    #     "sort_by": request.args.get("created_at"),
    #     "page": request.args.get("page", 1, type=int),
    #     "limit": request.args.get("limit", 10, type=int)
    # }

    result, status = order_place_service(user_id=user_id, address_id=address_id)
    return jsonify(result), status

@jwt_required()
@permission_required(Permission.SELECT_PAYMENT)
def select_payment_controller():
    data = request.get_json()
    result, status = select_payment_service(data)
    return jsonify(result), status

@jwt_required()
@permission_required(Permission.TRACK_ORDERS)
def get_order_by_id_details_controller(order_id):
    user_id = get_jwt_identity()
    data, status = get_order_by_id_details_service(user_id, order_id)
    return jsonify(data), status

@jwt_required()
@permission_required(Permission.CANCEL_ORDERS)
def cancel_order_controller(order_id):
    user_id = get_jwt_identity()
    data, status = cancel_order_service(order_id,user_id)
    return jsonify(data),status

@jwt_required()
@permission_required(Permission.VIEW_ORDERS)
def get_all_orders_controller():
    user_id = get_jwt_identity()

    params = {
        "page": request.args.get("page", 1, type=int),
        "limit": request.args.get("limit", 10, type=int),
        "search": request.args.get("search"),
        "sort_by": request.args.get("sort_by", "created_at"),
        "order": request.args.get("order", "desc")

    }

    data, status = get_all_orders_service(user_id=user_id, **params)
    return jsonify(data), status

