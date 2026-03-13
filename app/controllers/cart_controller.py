from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.rbac.decorators import permission_required
from app.rbac.constants import Permission
from app.services.cart_services import get_cart_item_service,update_cart_item_service,remove_cart_item_service,add_cart_item_service,clear_cart_service

@jwt_required()
@permission_required(Permission.VIEW_CART)
def get_cart_items_controller():
    try:
        user_id = get_jwt_identity()
        data = get_cart_item_service(user_id)
        return jsonify(data), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        })


@jwt_required()
@permission_required(Permission.ADD_TO_CART)
def add_cart_items_controller():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        product_id = data.get("product_id")
        quantity = data.get("quantity", 1)

        if not product_id:
            return jsonify({"error": "product_id is required"}), 400

        response, status = add_cart_item_service(user_id, product_id, quantity)

        return jsonify(response), status

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@jwt_required()
@permission_required(Permission.UPDATE_CART)
def update_cart_items_controller(item_id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        response, status = update_cart_item_service(user_id, data, item_id)
        return jsonify(response), status

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@jwt_required()
@permission_required(Permission.REMOVE_FROM_CART)
def remove_cart_items_controller(item_id):
    try:
        user_id = get_jwt_identity()
        response, status = remove_cart_item_service(user_id, item_id)
        return jsonify(response), status

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@jwt_required()
@permission_required(Permission.CLEAR_CART)
def clear_cart_controller():
    try:
        user_id = get_jwt_identity()
        response, status = clear_cart_service(user_id)
        return jsonify(response), status

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500