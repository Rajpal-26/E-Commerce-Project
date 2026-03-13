from datetime import datetime, timedelta, timezone

from flask import jsonify
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.addresses import Address

def create_address(data, user_id):
    try:
        address = Address(
            user_id=user_id,
            house_number=data["house_number"],
            street_name=data["street_name"],
            city=data["city"],
            state=data["state"],
            pincode=data["pincode"]
        )
        db.session.add(address)
        db.session.commit()
        return address

    except IntegrityError:
        db.session.rollback()
        raise ValueError("This address is already exist for this user")


def get_address(user_id):
    try:
        return Address.query.filter_by(user_id=user_id).all()

    except Exception as e :
        return jsonify({
            "error" :str(e)
        })


def get_address_by_id(address_id, user_id):
    try:
        return Address.query.filter_by(id=address_id, user_id=user_id).first()

    except Exception as e:
        return jsonify({
            "error": str(e)
        })


def update_address(address, data):
    try:
        address.house_number = data.get("house_number", address.house_number)
        address.street_name = data.get("street_name", address.street_name)
        address.city = data.get("city", address.city)
        address.state = data.get("state", address.state)
        address.pincode = data.get("pincode", address.pincode)

        db.session.commit()
        return address

    except Exception as e:
        return jsonify({
            "error": str(e)
        })


def delete_address(address_id,user_id):
    try:
        address = Address.query.filter_by(id=address_id, user_id=user_id).first()

        if not address:
            return {"error": "Address not found"}, 404

        now = datetime.now(timezone.utc).replace(tzinfo=None)

        if now > address.created_at + timedelta(days=7):
            return {"error": "You can delete this address only within 7 days"}, 403

        db.session.delete(address)
        db.session.commit()

        return {"message" : f"Address id {address_id} deleted Successfully"}, 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        })

