from flask import jsonify

from app.extensions import db
from app.models.product import Product
from app.models.cart import Cart
from app.models.cartItems import CartItem



# def add_cart_item_service(user_id,product_id,data,quantity=1):
#     try:
#         product_id = data.get("product_id")
#         quantity = data.get("quantity", 1)

#         if quantity <= 0:
#             return {"error": "quantity must be greater than 0"}, 400

#         product = Product.query.get_or_404(product_id)

#         if product.stock <= 0:
#             return {"error": "Product is out of stock"}, 400

#         cart = Cart.query.filter_by(user_id=user_id).first()


#         if not cart:
#             cart = Cart(user_id=user_id)
#             db.session.add(cart)
#             db.session.commit()

#         item = CartItem.query.filter_by(cart_id = cart.id, product_id = product.id).first()

#         existing_qty = item.quantity if item else 0

#         new_qty = existing_qty + quantity

#         if new_qty > product.stock:
#             remaining = product.stock - existing_qty
#             return {
#                 "message": f"Only {remaining} items left in stock"
#             }

#         if item :
#             item.quantity = new_qty

#         else:
#             item = CartItem(cart_id = cart.id,product_id = product.id,quantity = quantity,price_at_time = product.price)
#             db.session.add(item)

#         db.session.commit()
#         return {"message": "Product added to cart"}

#     except Exception as e:
#         return ({
#             "error": str(e)
#         })

def add_cart_item_service(user_id, product_id, quantity=1):
    try:

        if quantity <= 0:
            return {"error": "quantity must be greater than 0"}, 400

        product = Product.query.get(product_id)

        if not product:
            return {"error": "Product not found"}, 404

        if product.stock <= 0:
            return {"error": "Product is out of stock"}, 400


        cart = Cart.query.filter_by(user_id=user_id).first()

        if not cart:
            cart = Cart(user_id=user_id)
            db.session.add(cart)
            db.session.commit()


        item = CartItem.query.filter_by(
            cart_id=cart.id,
            product_id=product.id
        ).first()


        existing_qty = item.quantity if item else 0
        new_qty = existing_qty + quantity


        if new_qty > product.stock:
            remaining = product.stock - existing_qty
            return {"message": f"Only {remaining} items left in stock"}, 400


        if item:
            item.quantity = new_qty
        else:
            item = CartItem(
                cart_id=cart.id,
                product_id=product.id,
                quantity=quantity,
                price_at_time=product.price
            )
            db.session.add(item)

        db.session.commit()

        return {"message": "Product added to cart"}, 201

    except Exception as e:
        return {"error": str(e)}, 500


def get_cart_item_service(user_id):
    try:
        cart = Cart.query.filter_by(user_id =user_id).first()
        if not cart:
            return {"cart": []}

        result = []
        for item in cart.items:
            product = Product.query.get(item.product_id)
            result.append({
                "item_id": item.id,
                "product_id": product.id,
                "name" : product.name,
                "model_number": product.model_number,
                "specification": product.specification,
                "quantity": item.quantity,
                "price": item.price_at_time,
                "stock": product.stock,
                "images": product.images,
                "total_price": item.quantity * item.price_at_time

            })

        return {"cart": result}

    except Exception as e:
        return({
            "error": str(e)
        })

def update_cart_item_service(user_id,data,item_id):
    try:
        quantity = data.get("quantity")

        item = CartItem.query.get(item_id)

        if not item:
            return {"error": "Cart item not found"}, 404

        product = Product.query.get(item.product_id)
        if not product:
            return {"error": "Product not found"}, 404


        if quantity > product.stock:
            return {"error": f"Only {product.stock} items available in stock"}, 400

        item.quantity = quantity
        db.session.commit()

        return {"message": "Cart updated successfully"}, 200

    except Exception as e:
        return {"error": str(e)}, 500

def remove_cart_item_service(user_id,item_id):
    try:
        item = CartItem.query.get(item_id)
        if not item:
            return {"error": "Cart item not found"}, 404
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item removed from Cart"}, 200

    except Exception as e:
        return {"error": str(e)}, 500
def clear_cart_service(user_id):
    try:
        cart = Cart.query.filter_by(user_id=user_id).first()

        if not cart:
            return {"message": "cart already empty"}, 200

        CartItem.query.filter_by(cart_id=cart.id).delete()
        db.session.commit()
        return {"message": "Cart cleared successfully"}, 200

    except Exception as e:
        return {"error": str(e)}, 500
