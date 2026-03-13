from flask import request, jsonify
    
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.rbac.constants import Permission
from app.rbac.decorators import permission_required
from app.services.wishlist_services import get_wishlist,add_to_wishlist, clear_wishlist, remove_from_wishlist,move_to_cart


@jwt_required()
@permission_required(Permission.VIEW_WISHLIST)
def get_wishlist_controller():
    user_id = get_jwt_identity()
    response, status = get_wishlist(user_id)
    return jsonify(response), status

   
@jwt_required()
@permission_required(Permission.ADD_TO_WISHLIST)
def add_wishlist_controller():
    user_id = get_jwt_identity()
    data = request.get_json()
    product_id = data.get("product_id")
    response, status = add_to_wishlist(user_id, product_id)
    return jsonify(response), status


@jwt_required()
@permission_required(Permission.REMOVE_FROM_WISHLIST)
def remove_wishlist_controller(product_id):
    user_id = get_jwt_identity()
    response, status = remove_from_wishlist(user_id, product_id)
    return jsonify(response), status

@jwt_required()
@permission_required(Permission.CLEAR_WISHLIST)
def clear_wishlist_controller():
    user_id = get_jwt_identity()
    response, status = clear_wishlist(user_id)
    return jsonify(response), status
    
@jwt_required()
@permission_required(Permission.ADD_TO_CART)
def move_to_cart_controller(product_id):
    user_id = get_jwt_identity()
    response, status = move_to_cart(user_id, product_id, quantity=1)
    return jsonify(response), status