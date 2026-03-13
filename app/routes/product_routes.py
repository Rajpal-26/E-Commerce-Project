from flask import Blueprint
from app.controllers.product_controller import (
    get_all_products_controller,
    get_single_product_controller,
    create_product_controller,
    update_product_controller,
    delete_product_controller,
    create_multiple_products_controller, upload_image, upload_image_file, bulk_sheet_upload_controller
)


product_bp = Blueprint("product_bp", __name__)


product_bp.route("/", methods=["GET"])(get_all_products_controller)
product_bp.route("/<int:product_id>", methods=["GET"])(get_single_product_controller)
product_bp.route("/", methods=["POST"])(create_product_controller)
product_bp.route("/<int:product_id>", methods=["PUT"])(update_product_controller)
product_bp.route("/<int:product_id>", methods=["DELETE"])(delete_product_controller)
product_bp.route("/bulk-create", methods=["POST"])(create_multiple_products_controller)
product_bp.route("/upload", methods=["POST"])(upload_image)
product_bp.route("/upload/<filename>", methods=["GET"])(upload_image_file)
product_bp.route("/bulk-sheet-upload", methods=["POST"])(bulk_sheet_upload_controller)



