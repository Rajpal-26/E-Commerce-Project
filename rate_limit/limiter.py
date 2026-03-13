from flask import jsonify, request
from flask_jwt_extended import (
    get_jwt,
    get_jwt_identity,
    verify_jwt_in_request
)
from app.extensions import redis_client
from app.logger import logger
from functools import wraps
import time

ROLE_LIMITS = {
    "ADMIN": 100,
    "SELLER": 50,
    "USER": 20
}

_local_rate_store = {}


def _incr_with_fallback(key, window):
    """
    Try Redis first. If Redis is unavailable, use in-memory counters so
    requests keep working instead of failing with 500.
    """
    try:
        if redis_client:
            current = redis_client.incr(key)
            if current == 1:
                redis_client.expire(key, window)
            if current is not None:
                return current
    except Exception as e:
        logger.warning(f"Redis rate limit error: {e}")

    try:
        now = time.time()
        current, expires_at = _local_rate_store.get(key, (0, now + window))
        if now > expires_at:
            current = 0
            expires_at = now + window
        current += 1
        _local_rate_store[key] = (current, expires_at)
        return current
    except Exception as e:
        logger.error(f"Rate limit fallback error: {e}")
        return 1

def ip_based_rate_limit(limit, window=60):
    """Decorator for IP-based rate limiting on specific endpoints."""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            key = f"rate_limit:ip:{request.remote_addr}:{request.endpoint}:{request.method}"
            current = _incr_with_fallback(key, window)

            if current > limit:
                response = jsonify({"msg": "Rate limit exceeded"})
                response.status_code = 429
                response.headers["Retry-After"] = window
                return response

            return f(*args, **kwargs)
        return wrapper
    return decorator

def global_rate_limit(window=60):

    # Ensure JWT exists (since no guests allowed)
    verify_jwt_in_request()

    user_id = get_jwt_identity()
    claims = get_jwt()
    role = claims.get("role")

    if role not in ROLE_LIMITS:
        return jsonify({"msg": "Invalid role"}), 403

    limit = ROLE_LIMITS[role]

    key = f"rate_limit:user:{user_id}"
    current = _incr_with_fallback(key, window)

    if current > limit:
        response = jsonify({"msg": "Rate limit exceeded"})
        response.status_code = 429
        response.headers["Retry-After"] = window
        return response

    return None
