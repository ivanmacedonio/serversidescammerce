from fastapi import Request
from ..controllers.auth import verify_access_token
from ..utils.custom_responses import abort, make_response

async def verify_is_request_authenticated(request:Request, call_next):
    SAVE_ROUTES = ["/login", "/users", "/shops"]
    if any(request.url.path.startswith(route) for route in SAVE_ROUTES):
        response = await call_next(request)
        return response
    try:
        access_token = request.headers.get('X-Access-Tokens', None)
        verify_access_token(access_token)
        response = await call_next(request)
        return response
    except Exception as e:
        return make_response(str(e), 500, "verify_is_request_authenticated")
    
async def verify_shop_id(request:Request, call_next):
    SAVE_ROUTES = ["/shops"]
    if any(request.url.path.startswith(route) for route in SAVE_ROUTES):
        response = await call_next(request)
        return response
    try:
        shop_id = request.headers.get('Shop-Id', None)
        if not shop_id: abort(400, "Shop ID is required")
        response = await call_next(request)
        return response
    except Exception as e:
        return make_response(str(e), 500, "verify_shop_id")