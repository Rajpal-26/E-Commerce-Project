from app.extensions import db
from app.models.product_reviews import ProductReview
from datetime import datetime, timezone


def add_review_service(user_id, product_id, rating, review):
    existing_review = ProductReview.query.filter_by(
        user_id=user_id,
        product_id=product_id
    ).first()

    if existing_review:
        return {"error": "User already reviewed this product"}, 400

    if rating < 1 or rating > 5:
        return {"error": "Rating must be between 1 and 5"}, 400

    new_review = ProductReview(
        user_id=user_id,
        product_id=product_id,
        rating=rating,
        review=review
    )

    db.session.add(new_review)
    db.session.commit()

    return {"msg": "Review added successfully"}, 201


def get_reviews_service(review_id):
    reviews = ProductReview.query.filter_by(id=review_id).all()

    review_list = []
    
    if not reviews:
        return {"error": "No reviews found "}, 404

    for r in reviews:
        review_list.append({
            "id": r.id,
            "user_id": r.user_id,
            "rating": r.rating,
            "review": r.review,
            "created_at": r.created_at
        })

    return {"reviews": review_list}, 200


def update_review_service(user_id, review_id, rating=None, review=None):
    review_obj = ProductReview.query.filter_by(
        id=review_id,
        user_id=user_id
    ).first()

    if not review_obj:
        return {"error": "Review not found"}, 404

    if rating is not None:
        if rating < 1 or rating > 5:
            return {"error": "Rating must be between 1 and 5"}, 400
        review_obj.rating = rating

    if review is not None:
        review_obj.review = review

    review_obj.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)

    db.session.commit()

    return {"msg": "Review updated successfully"}, 200


def delete_review_service(user_id, review_id):
    review_obj = ProductReview.query.filter_by(
        id=review_id,
        user_id=user_id
    ).first()

    if not review_obj:
        return {"error": "Review not found"}, 404

    db.session.delete(review_obj)
    db.session.commit()

    return {"msg": "Review deleted successfully"}, 200