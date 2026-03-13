
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.rbac.decorators import permission_required
from app.rbac.constants import Permission
from app.services.address_services import (
    create_address,
    get_address,
    get_address_by_id,
    update_address,
    delete_address
)

address_bp = Blueprint("address", __name__)


@jwt_required()
@permission_required(Permission.CREATE_ADDRESS)
def create_address_controller():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        address = create_address(data, user_id)

        return jsonify({
            "message": "Address created successfully",
            "id": address.id
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e)
        }),500

@jwt_required()
@permission_required(Permission.VIEW_ADDRESS)
def get_address_controller():
    try:
        user_id = get_jwt_identity()
        address = get_address(user_id)

        return jsonify([
            {
                "id": a.id,
                "house_number": a.house_number,
                "street_name": a.street_name,
                "city": a.city,
                "state": a.state,
                "pincode": a.pincode
            } for a in address
        ])
    except Exception as e:
        return jsonify({
            "error": str(e)
        }),500


@jwt_required()
@permission_required(Permission.VIEW_ADDRESS)
def get_address_by_id_controller(address_id):
    try:
        user_id = get_jwt_identity()
        address = get_address_by_id(address_id, user_id)

        if not address:
            return jsonify({"error": f"Address id {address_id} not found in database"}), 404

        return jsonify({
            "id": address.id,
            "house_number": address.house_number,
            "street_name": address.street_name,
            "city": address.city,
            "state": address.state,
            "pincode": address.pincode
        })
    except Exception as e:
        return jsonify({
            "error": str(e)
        }),500


@jwt_required()
@permission_required(Permission.UPDATE_ADDRESS)
def update_address_controller(address_id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        address = get_address_by_id(address_id, user_id)
        if not address:
            return jsonify({"error": f"Address id {address_id} not found in database"}), 404

        update_address(address, data)
        return jsonify({"message": f"Address id {address_id} updated successfully"})

    except Exception as e:
        return jsonify({
            "error": str(e)
        }),500

@jwt_required()
@permission_required(Permission.DELETE_ADDRESS)
def delete_address_controller(address_id):
    try:
        user_id = get_jwt_identity()

        response, status = delete_address(address_id, user_id)

        return jsonify(response), status

    except Exception as e:
        return jsonify({
            "error": str(e)
        }),500
