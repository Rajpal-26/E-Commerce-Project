from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import redis
import time


from config import Config
from flask_caching import Cache




try:
    cache = Cache()
except Exception:
    class _DummyCache:
        def init_app(self, app):
            return None
        def get(self, key):
            return None
        def set(self, key, value, timeout=None):
            return None
        def delete(self, key):
            return None
        def clear(self):
            return None
        def delete_pattern(self, pattern):
            return None
    cache = _DummyCache()

# single SQLAlchemy instance
db = SQLAlchemy()

migrate = Migrate()
jwt = JWTManager()
mail = Mail()

# The rate limiter needs a redis client.
# It's imported at startup, so we need to initialize it here.
# We'll assume the REDIS_URL is in the Config object, same as for the cache.
try:
    # Set a short timeout (e.g., 0.5s) to prevent requests from hanging if Redis is slow
    redis_client = redis.from_url(Config.REDIS_URL, socket_timeout=0.5)
    redis_client.ping()
except Exception:
    class _DummyRedis:
        def __init__(self):
            self.store = {}

        def incr(self, key):
            now = time.time()
            val, expiry = self.store.get(key, (0, float('inf')))
            if now > expiry:
                val = 0
            new_val = val + 1
            self.store[key] = (new_val, expiry)
            return new_val

        def expire(self, key, seconds):
            if key in self.store:
                val, _ = self.store[key]
                self.store[key] = (val, time.time() + seconds)

        def setex(self, key, seconds, value):
            self.store[key] = (value, time.time() + seconds)

        def get(self, key):
            if key in self.store:
                val, expiry = self.store[key]
                if time.time() <= expiry:
                    return val
            return None
    redis_client = _DummyRedis()
    



@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = redis_client.get(jti)
    return token is not None
