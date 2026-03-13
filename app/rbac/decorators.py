from functools import wraps

from flask import jsonify, g
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.rbac.constants import Permission
from app.models.user import User


def permission_required(permission: Permission):
    def decorator(func):


        @wraps(func)
        def wrapper(*args,**kwargs):
            
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            
            user = User.query.get(user_id)
            
            print("User ID:", user_id)
            print("Roles:", [r.name for r in user.roles])
            print("Permissions:", [
                p.name for r in user.roles for p in r.permissions
            ])
            print("Required Permission:", permission.value)

            if not user:
                return jsonify({"message":"Authentication required"}), 401

            if getattr(user,"is_superadmin", False):
                return func(*args, **kwargs)

            if not user.has_permission(permission.value):
                return jsonify({
                    "message": "You don't have permission"
                }), 403
                
            

            return func(*args,**kwargs)
        return  wrapper
    return decorator