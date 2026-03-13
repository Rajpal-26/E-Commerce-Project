from app import db
from app.models.permissions import Permission as PermissionModel
from app.models.roles import Role as RoleModel
from app.rbac.constants import Permission, Role


def seed_permissions():
    """Seed all permissions into the database"""
    all_permissions = [
        (Permission.VIEW_PRODUCT, "View products"),
        (Permission.CREATE_PRODUCT, "Create new products"),
        (Permission.UPDATE_PRODUCT, "Update product details"),
        (Permission.DELETE_PRODUCT, "Delete products"),
        (Permission.UPDATE_STOCK, "Update product stock"),

        (Permission.ADD_TO_CART, "Add items to cart"),
        (Permission.VIEW_CART, "View cart items"),
        (Permission.UPDATE_CART, "Update cart items"),
        (Permission.REMOVE_FROM_CART, "Remove items from cart"),
        (Permission.CLEAR_CART, "Clear cart"),

        (Permission.PLACE_ORDER, "Place orders"),
        (Permission.VIEW_ORDERS, "View orders"),
        (Permission.TRACK_ORDERS, "Track order status"),
        (Permission.CANCEL_ORDERS, "Cancel orders"),
        (Permission.REQUEST_RETURN, "Request order return"),
        (Permission.SELECT_PAYMENT, "Select payment method"),

        (Permission.CREATE_ADDRESS, "Create addresses"),
        (Permission.VIEW_ADDRESS, "View addresses"),
        (Permission.UPDATE_ADDRESS, "Update addresses"),
        (Permission.DELETE_ADDRESS, "Delete addresses"),

        (Permission.MANAGE_USERS, "Manage users"),
        (Permission.CONTROL_PRICING, "Control product pricing"),
        (Permission.MANAGE_PRICING, "Manage seller pricing"),
        (Permission.ISSUE_REFUND, "Issue refunds"),
        
        (Permission.ADD_TO_WISHLIST, "Add items to wishlist"),
        (Permission.VIEW_WISHLIST, "View wishlist items"),
        (Permission.REMOVE_FROM_WISHLIST, "Remove items from wishlist"),
        (Permission.CLEAR_WISHLIST, "Clear wishlist"),
        
        (Permission.ADD_REVIEW, "Add product reviews"),
        (Permission.VIEW_REVIEW, "View product reviews"),
        (Permission.UPDATE_REVIEW, "Update product reviews"),
        (Permission.DELETE_REVIEW, "Delete product reviews"),
    
    ]

    for perm_name, description in all_permissions:
        exists = PermissionModel.query.filter_by(name=perm_name).first()
        if not exists:
            db.session.add(PermissionModel(name=perm_name, description=description))

    db.session.commit()


def seed_roles():
    """Seed roles with their permissions"""

    user_permissions = [
        Permission.VIEW_PRODUCT,
        Permission.ADD_TO_CART,
        Permission.VIEW_CART,
        Permission.UPDATE_CART,
        Permission.REMOVE_FROM_CART,
        Permission.CLEAR_CART,
        Permission.PLACE_ORDER,
        Permission.VIEW_ORDERS,
        Permission.TRACK_ORDERS,
        Permission.CANCEL_ORDERS,
        Permission.REQUEST_RETURN,
        Permission.SELECT_PAYMENT,
        Permission.CREATE_ADDRESS,
        Permission.VIEW_ADDRESS,
        Permission.UPDATE_ADDRESS,
        Permission.DELETE_ADDRESS,
        Permission.ADD_TO_WISHLIST,
        Permission.VIEW_WISHLIST,
        Permission.REMOVE_FROM_WISHLIST,
        Permission.CLEAR_WISHLIST,
        Permission.ADD_REVIEW,
        Permission.VIEW_REVIEW,
        Permission.UPDATE_REVIEW,
        Permission.DELETE_REVIEW
    ]

    admin_permissions = [
        Permission.VIEW_PRODUCT,
        Permission.CREATE_PRODUCT,
        Permission.UPDATE_PRODUCT,
        Permission.DELETE_PRODUCT,
        Permission.UPDATE_STOCK,
        Permission.ADD_TO_CART,
        Permission.VIEW_CART,
        Permission.UPDATE_CART,
        Permission.REMOVE_FROM_CART,
        Permission.CLEAR_CART,
        Permission.PLACE_ORDER,
        Permission.VIEW_ORDERS,
        Permission.TRACK_ORDERS,
        Permission.CANCEL_ORDERS,
        Permission.REQUEST_RETURN,
        Permission.SELECT_PAYMENT,
        Permission.CREATE_ADDRESS,
        Permission.VIEW_ADDRESS,
        Permission.UPDATE_ADDRESS,
        Permission.DELETE_ADDRESS,
        Permission.MANAGE_USERS,
        Permission.CONTROL_PRICING,
        Permission.ISSUE_REFUND,
        Permission.ADD_TO_WISHLIST,
        Permission.VIEW_WISHLIST,
        Permission.REMOVE_FROM_WISHLIST,
        Permission.CLEAR_WISHLIST,
        Permission.ADD_REVIEW,
        Permission.VIEW_REVIEW,
        Permission.UPDATE_REVIEW,
        Permission.DELETE_REVIEW
    ]

    seller_permissions = [
        Permission.VIEW_PRODUCT,
        Permission.CREATE_PRODUCT,
        Permission.UPDATE_PRODUCT,
        Permission.UPDATE_STOCK,
        Permission.VIEW_ORDERS,
        Permission.MANAGE_PRICING,
        Permission.VIEW_REVIEW
    ]

    roles_data = [
        (Role.USER, "Regular user - can browse and place orders", user_permissions),
        (Role.ADMIN, "Administrator - full system access", admin_permissions),
        (Role.SELLER, "Seller - can manage products and orders", seller_permissions),
    ]

    for role_name, description, permissions in roles_data:
        role = RoleModel.query.filter_by(name=role_name).first()

        if not role:
            role = RoleModel(name=role_name)
            db.session.add(role)
            db.session.flush()

        # Always update description (keeps DB consistent)
        role.description = description

        for perm_name in permissions:
            permission = PermissionModel.query.filter_by(name=perm_name).first()
            if permission and permission not in role.permissions:
                role.permissions.append(permission)

    db.session.commit()


def seed_rbac():
    """Run all seeding functions"""
    seed_permissions()
    seed_roles()