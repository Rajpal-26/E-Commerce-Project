from app.models import Wishlist
from app.extensions import db
from app.services.cart_services import add_cart_item_service
from app.models.product import Product

def get_wishlist(user_id):
    
    empty = Wishlist.query.filter_by(user_id=user_id).first() 
    
    if empty is None:
        return {"wishlist": []}, 200

    items = Wishlist.query.filter_by(user_id=user_id).all()

    result = []
    for item in items:
        result.append({
            "wishlist_id": item.id,
            "product_id": item.product_id,
            "product_name": item.product.name,
            "price": item.product.price
        })

    return {"wishlist": result}, 200

def add_to_wishlist(user_id, product_id):
    
    product = Product.query.get(product_id)
    
    if not product:
        return {"error": f"Product {product_id} not found"}, 404

    existing = Wishlist.query.filter_by(
        user_id=user_id,
        product_id=product_id
    ).first()

    if existing:
        return {"error": f"Product {product_id} already in wishlist"}, 400

    item = Wishlist(user_id=user_id, product_id=product_id)

    db.session.add(item)
    db.session.commit()

    return {"message": f"Added product {product_id} to wishlist"}, 201

def remove_from_wishlist(user_id, product_id):

    item = Wishlist.query.filter_by(
        user_id=user_id,
        product_id=product_id
    ).first()

    if not item:
        return {"error": "Item not found in wishlist"}, 404

    db.session.delete(item)
    db.session.commit()

    return {"message": f"Removed product {product_id} from wishlist"}, 200

def clear_wishlist(user_id):

    Wishlist.query.filter_by(user_id=user_id).delete()
    db.session.commit()

    return {"message": "Wishlist cleared"}, 200

def move_to_cart(user_id, product_id, quantity=1):

    wishlist_item = Wishlist.query.filter_by(
        user_id=user_id,
        product_id=product_id
    ).first()

    if not wishlist_item:
        return {"error": "Item not in wishlist"}, 404

    
    response, status = add_cart_item_service(user_id, product_id, quantity=1)

    if status != 200 and status != 201:
        return response, status

    
    db.session.delete(wishlist_item)
    db.session.commit()

    return {"message": f"Added Product {product_id} to cart successfully"}, 200
