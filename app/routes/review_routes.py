from flask import Blueprint
from app.controllers.reviews_controller import add_review_controller, get_reviews_by_id_controller, update_review_controller, delete_review_controller

review_bp = Blueprint("review", __name__)

review_bp.route("/add/<int:product_id>", methods=["POST"])(add_review_controller)
review_bp.route("/view/<int:review_id>", methods=["GET"])(get_reviews_by_id_controller)
review_bp.route("/update/<int:review_id>", methods=["PUT"])(update_review_controller)
review_bp.route("/delete/<int:review_id>", methods=["DELETE"])(delete_review_controller)