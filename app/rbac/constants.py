

from enum import Enum


class Permission(str, Enum):
    # Product permissions
    VIEW_PRODUCT = "product:view"
    CREATE_PRODUCT = "product:create"
    UPDATE_PRODUCT = "product:update"
    DELETE_PRODUCT = "product:delete"
    UPDATE_STOCK = "product:update_stock"
    
    # Cart permissions
    ADD_TO_CART = "cart:add"
    VIEW_CART = "cart:view"
    UPDATE_CART = "cart:update"
    REMOVE_FROM_CART = "cart:remove"
    CLEAR_CART = "cart:clear"
    
    # Order permissions
    PLACE_ORDER = "order:place"
    VIEW_ORDERS = "order:view"
    TRACK_ORDERS = "order:track"
    CANCEL_ORDERS = "order:cancel"
    REQUEST_RETURN = "order:request_return"
    SELECT_PAYMENT = "order:select_payment"
    
    # Address permissions
    CREATE_ADDRESS = "address:create"
    VIEW_ADDRESS = "address:view"
    UPDATE_ADDRESS = "address:update"
    DELETE_ADDRESS = "address:delete"
    
    # User management permissions
    MANAGE_USERS = "user:manage"
    
    # Pricing permissions
    CONTROL_PRICING = "pricing:control"
    MANAGE_PRICING = "pricing:manage"
    
    # Refund permissions
    ISSUE_REFUND = "refund:issue"
    
    # Wishlist permissions   
    ADD_TO_WISHLIST = "wishlist:add"
    VIEW_WISHLIST = "wishlist:view"
    REMOVE_FROM_WISHLIST = "wishlist:remove"
    CLEAR_WISHLIST = "wishlist:clear"
    
    # Review permissions
    ADD_REVIEW = "review:add"
    VIEW_REVIEW = "review:view"
    UPDATE_REVIEW = "review:update"
    DELETE_REVIEW = "review:delete"
    
    


class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"
    SELLER = "seller"
    