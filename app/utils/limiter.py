from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=lambda request: request.headers.get("X-Forwarded-For", request.client.host))