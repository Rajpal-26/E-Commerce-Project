from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import request, jsonify
from app.services.review_services import (
    add_review_service,
    get_reviews_service,
    update_review_service,
    delete_review_service
)
from app.rbac.constants import Permission
from app.rbac.decorators import permission_required


@jwt_required()
@permission_required(Permission.ADD_REVIEW)
def add_review_controller(product_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    rating = data.get("rating")
    review = data.get("review")

    response, status = add_review_service(user_id, product_id, rating, review)
    return jsonify(response), status


@jwt_required()
@permission_required(Permission.VIEW_REVIEW)
def get_reviews_by_id_controller(review_id):
    response, status = get_reviews_service(review_id)
    return jsonify(response), status


@jwt_required()
@permission_required(Permission.UPDATE_REVIEW)
def update_review_controller(review_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    rating = data.get("rating")
    review = data.get("review")

    response, status = update_review_service(user_id, review_id, rating, review)
    return jsonify(response), status


@jwt_required()
@permission_required(Permission.DELETE_REVIEW)
def delete_review_controller(review_id):
    user_id = get_jwt_identity()

    response, status = delete_review_service(user_id, review_id)
    return jsonify(response), status