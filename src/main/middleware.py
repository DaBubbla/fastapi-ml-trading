'''
Application middleware functions.
'''
import json
import os

from fastapi import Request
from fastapi.responses import JSONResponse

# from src.main.framework.metrics_utils import (
#     CustomFrontendMetricsCollector, update_user_source_in_metrics
# )
from starlette.middleware.base import BaseHTTPMiddleware

# from src.main.request_validation import _get_auth_token
# from src.main.utils import TokenValidator, validator_scopes


class AsyncIteratorWrapper:
    '''
    Async iterator wrapper class.
    '''
    def __init__(self, obj):
        self._it = iter(obj)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            value = next(self._it)
        except StopIteration as err:
            raise StopAsyncIteration from err
        return value


class RequestMiddleware(BaseHTTPMiddleware):
    '''
    Application middleware to wrap incoming request.
    '''
    # TODO put appd back

    # @CollectMetrics(frontend_metrics_collector=CustomFrontendMetricsCollector())
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # return response for swagger docs or openapi
        response = await call_next(request)
        process_request(path, request, response)

        # Consuming FastAPI response and grabbing body here
        resp_body = [
            section async for section in response.body_iterator
        ]

        # Repairing FastAPI response
        response.body_iterator = AsyncIteratorWrapper(resp_body)

        if path in [
            "/docs",
            "/redoc"
        ]: 
            return response

        resp_body = json.loads(resp_body[0].decode())
        return JSONResponse(resp_body, status_code=response.status_code)

def process_request(path, request, response):
    """
    Process the request based on the specified path, request, and response.

    Args:
        path (str): The URL path of the request.
        request (Request): The incoming request object.
        response: The current response object.

    Returns:
        Response
    """

    raw_response_resources = [
        "/graphql"
    ]

    if path in raw_response_resources or "/graphql" in path:
        # validator = TokenValidator.get_validator()
        # scopes = validator_scopes()
        # token = _get_auth_token(request)
        # decoded_token = validator.validate(token, scopes=scopes)
        # update_user_source_in_metrics(decoded_token.user)
        return response