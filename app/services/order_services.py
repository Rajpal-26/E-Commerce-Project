from flask import request
from sqlalchemy import desc, asc

from app.extensions import db
from app.models.addresses import Address
from app.models.cart import Cart
from app.models.cartItems import CartItem
from app.models.enums import OrderStatus, PaymentStatus
from app.models.order import Order
from app.models.orderItems import OrderItem
from app.models.product import Product
from app.services.email_services import send_email
from app.models.user import User


def order_place_service(user_id,address_id):
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        return {"error": "Cart not found"}, 404

    address = Address.query.filter_by(id=address_id,user_id=user_id).first()

    if not address:
        return {"error": "Invalid Address"}, 400

    cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
    if not cart_items:
        return {"error": "Cart is empty"}, 400


    delivery_address = (
        f"{address.house_number}, "
        f"{address.street_name}, {address.city}, "
        f"{address.state}-{address.pincode}"
    )

    total = 0

    for item in cart_items:

        updated = Product.query.filter(
            Product.id == item.product_id,
            Product.stock >= item.quantity
        ).update({
            Product.stock: Product.stock - item.quantity
        })

        if updated == 0:
            db.session.rollback()
            return {
                "error": f"{item.product.name} is out of stock"
            }, 400

        total += item.quantity * item.product.price

    order = Order(
        user_id=user_id,
        total_amount=total,
        address_id = address_id,
        delivery_address = delivery_address,
        order_status=OrderStatus.PENDING,
        payment_status=PaymentStatus.PENDING
    )

    db.session.add(order)
    db.session.flush()

    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.product.price
        )
        db.session.add(order_item)

    CartItem.query.filter_by(cart_id=cart.id).delete()
    db.session.commit()
    
    user = User.query.get(user_id)
    send_email(
        user.email,
        "Order Confirmed",
        f"Your order #{order.id} has been placed successfully."
    )

    return {
        "message": "Order placed successfully",
        "order_id": order.id,
        "order_status": order.order_status.value,
        "payment_status": order.payment_status.value,
        "total_amount": total
    }, 201


def select_payment_service(data):
    order_id = data.get("order_id")
    payment_mode = data.get("payment_mode")

    order = Order.query.get(order_id)
    if not order:
        return {"error": "Order not found"}, 404

    valid_modes = ["COD", "UPI", "CARD", "NET_BANKING", "WALLET"]
    if payment_mode not in valid_modes:
        return {"error": "Invalid payment mode"}, 400

    order.payment_mode = payment_mode

    if payment_mode == "COD":
        order.payment_status = PaymentStatus.PENDING
        order.order_status = OrderStatus.PLACED
    else:
        order.payment_status = PaymentStatus.SUCCESS
        order.order_status = OrderStatus.PLACED

    db.session.commit()

    return {
        "message": "Payment method selected",
        "order_id": order.id,
        "payment_mode": payment_mode,
        "order_status": order.order_status.value,
        "payment_status": order.payment_status.value
    }, 200

ALLOWED_SORT = {
    "id": Order.id,
    "total_amount": Order.total_amount,
    "created_at": Order.created_at
}
def get_order_by_id_details_service(user_id,order_id):
    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    if not order:
        return {"error": "Order not found"}, 404

    items = (
        db.session.query(OrderItem, Product).join(Product, Product.id == OrderItem.product_id).filter(OrderItem.order_id == order.id).all()
    )

    item_list = []
    for order_item, product in items:

        item_list.append({
            "product_id": product.id,
            "product_name": product.name,
            "model_number": product.model_number,
            "specifications": product.specification,
            "images": product.images,
            "quantity": order_item.quantity,
            "price": order_item.price
        })

    return {
        "order_id": order.id,
        "total_amount": order.total_amount,
        "payment_mode": order.payment_mode,
        "payment_status": order.payment_status.value,
        "order_status": order.order_status.value,
        "delivery_address": order.delivery_address,
        "items": item_list
    }, 200

def cancel_order_service(order_id, user_id):
    order = Order.query.filter_by(id = order_id, user_id = user_id).first()

    if not order:
        return {"error": "order not found"}, 404

    if order.order_status in [OrderStatus.SHIPPED,OrderStatus.OUT_FOR_DELIVERY,OrderStatus.DELIVERED]:
        return {"error": "order cannot be cancelled after shipping"}, 400

    if order.order_status == OrderStatus.CANCELLED:
        return {"error": "Order already cancelled"}, 400

    order_items = OrderItem.query.filter_by(order_id= order_id).all()

    for item in order_items:
        Product.query.filter(Product.id == item.product_id).update({Product.stock: Product.stock + item.quantity})

    order.order_status = OrderStatus.CANCELLED

    if order.payment_status == PaymentStatus.SUCCESS:
        order.payment_status = PaymentStatus.REFUNDED

    else:
        order.payment_status = PaymentStatus.FAILED

    db.session.commit()

    return {
        "message": "order cancelled successfully",
        "order_status": order.order_status.value,
        "payment_status": order.payment_status.value
    }, 200


ALLOWED_ORDER_SORT = {
    "id": Order.id,
    "created_at": Order.created_at,
    "total_amount": Order.total_amount,
    "order_status": Order.order_status,
    "payment_status": Order.payment_status
}
def get_all_orders_service(
            user_id,
            page=1,
            limit=10,
            search=None,
            sort_by="created_at",
            order="desc",

):

        query = Order.query.filter(Order.user_id == user_id)

        if search:
            if str(search).isdigit():
                query = query.filter(Order.id == int(search))

        sort_column = ALLOWED_ORDER_SORT.get(sort_by, Order.created_at)

        order = (order or "desc").lower()

        if order not in ["asc", "desc"]:
            order = "desc"

        query = query.order_by(desc(sort_column) if order == "desc" else asc(sort_column))


        pagination = query.paginate(
            page=page,
            per_page=limit,
            error_out=False
        )

        orders_data = []

        for order in pagination.items:
            orders_data.append({
                "order_id": order.id,
                "total_amount": order.total_amount,
                "order_status": order.order_status.value,
                "payment_status": order.payment_status.value,
                "payment_mode": order.payment_mode,
                "delivery_address": order.delivery_address,
                "created_at": order.created_at
            })

        return {
            "orders": orders_data,
            "total_orders": pagination.total,
            "total_pages": pagination.pages,
            "current_page": pagination.page,
            "per_page": limit
        }, 200
