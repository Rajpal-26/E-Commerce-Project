import os
import uuid

from flask import request, jsonify, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity

import app
from app.logger import logger
from app.rbac.decorators import permission_required
from app.rbac.constants import Permission
from app.services.product_services import (
    get_all_products,
    get_product_by_id,
    create_product,
    update_product,
    delete_product,
    create_multiple_products, bulk_sheet_upload_service
)
from rename_image_to_hex_id import UPLOAD_FOLDER


@jwt_required()
@permission_required(Permission.VIEW_PRODUCT)
def get_all_products_controller():
    user_id = get_jwt_identity()
    params = {
            "search": request.args.get("search"),
            "min_price": request.args.get("min_price", type=float),
            "max_price": request.args.get("max_price", type=float),
            "sort_by": request.args.get("sort_by", "id"),
            "order": request.args.get("order", "asc"),
            "page": request.args.get("page", 1, type=int),
            "limit": request.args.get("limit", 10, type=int)
    }

    result = get_all_products(**params,user_id=user_id)

    return jsonify(result), 200

@jwt_required()
@permission_required(Permission.VIEW_PRODUCT)
def get_single_product_controller(product_id):

    user_id = get_jwt_identity()
    response, status = get_product_by_id(product_id, user_id)

    return jsonify(response), status

@jwt_required()
@permission_required(Permission.CREATE_PRODUCT)
def create_product_controller():

    user_id = get_jwt_identity()
    data = request.get_json()
    response, status = create_product(data, user_id)

    return jsonify(response), status

@jwt_required()
@permission_required(Permission.UPDATE_PRODUCT)
def update_product_controller(product_id):

    user_id = get_jwt_identity()
    data = request.get_json()
    response, status = update_product(product_id, data, user_id)

    return jsonify(response), status

@jwt_required()
@permission_required(Permission.DELETE_PRODUCT)
def delete_product_controller(product_id):

    user_id = get_jwt_identity()
    response, status = delete_product(product_id, user_id)

    return jsonify(response), status

@jwt_required()
@permission_required(Permission.CREATE_PRODUCT)
def create_multiple_products_controller():

    user_id = get_jwt_identity()
    data = request.get_json()
    response, status = create_multiple_products(data, user_id)

    return jsonify(response), status

@jwt_required()
@permission_required(Permission.CREATE_PRODUCT)
def bulk_sheet_upload_controller():
    user_id = get_jwt_identity()
    file = request.files.get("file")

    if not file:
        return {"error": "Excel file required"},400

    return bulk_sheet_upload_service(file = file,user_id=user_id)

@jwt_required()
@permission_required(Permission.CREATE_PRODUCT)
def upload_image():
    try:
        file = request.files["file"]
        filename = f"{uuid.uuid4().hex}.jpg"
        file.save(os.path.join(UPLOAD_FOLDER, filename))


        return jsonify({
            "image_id": filename,
            "url": f"/api/products/upload/{filename}"
        })
    except Exception as e:
        return jsonify({
            "error": str(e)
        })

@jwt_required()
@permission_required(Permission.VIEW_PRODUCT)
def upload_image_file(filename):
    try:
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    except Exception as e:
        return jsonify({
            "error": str(e)
        })

