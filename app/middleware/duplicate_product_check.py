from flask import request, jsonify
from app.models.product import Product

def check_duplicate_model_number():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Invalid or missing JSON data"
            }), 400

        name = data.get("name")
        model_number = data.get("model_number")

        if not name or not model_number:
            return jsonify({
                "error": "name and model_number are required"
            }), 400

        if Product.query.filter_by(name=name, model_number=model_number).first():
            return jsonify({
                "error": "Product with this name and model number already exists"
            }), 409

        if Product.query.filter_by(name=name).first():
            return jsonify({
                "error": "Product with this name already exists"
            }), 409

        if Product.query.filter_by(model_number=model_number).first():
            return jsonify({
                "error": "Product with this model number already exists"
            }), 409

        return None  # No duplicate found → allow request to continue

    except Exception as e:
        return jsonify({
            "error": "Failed to validate product duplication",
            "details": str(e)
        }), 500