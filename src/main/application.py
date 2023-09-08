"""
Routes for both REST and GraphQL.
"""
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from src.main.exception_handling import exception_handler
from src.main.framework.exceptions import app_excep

from src.main.framework.models import PortInEligibility, XMEligibility
from src.main.graphql_api.graphql import GRAPHQL_APP

from src.main.middleware import RequestMiddleware

# from src.main.request_validation import validate_request
# TODO: add handler functions
from src.main.rest_api.handler import get_eligibility, get_device


app = FastAPI(
    openapi_url=f"/{os.getenv('stage', 'dev')}/k8_project/openapi.json",
    title="K8 Project API",
    description="K8 project built with FastAPI",
    version=os.getenv('build_version', '0.0.0')
)

app.add_middleware(RequestMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
app.add_exception_handler(Exception, exception_handler)


# @app.on_event("startup")
# async def startup_tasks():
    # app.state.config = APP_CONFIG.get_configs()
    # app.state.auth_builder = AuthBuilder(
    #     app.state.config).create_auth_clients()
    # app.state.localization_session = LocalizationSession(app.state.config)


# @app.on_event("shutdown")
# async def shutdown_tasks():
#     await app.state.localization_session.close()


@app.get("/health")
async def get_health():
    """
    Healthcheck endpoint.
    """
    return {
        "message": "Hello from the other side.",
        "version": os.getenv('build_version', "0.0.0")
    }


@app.route("/graphql", methods=["GET", "POST"])
async def byod_graphql(request: Request):
    '''
    GraphQL endpoint.
    '''
    # org_logger.info('GraphQL request started...')
    response = await GRAPHQL_APP._handle_http_request(request)
    return response

# TODO: change path
@app.get("/byod/{imei}", responses=app_excep)
async def get_byod(imei: str, request: Request) -> XMEligibility:
    # req_body = validate_request(request)
    # session_handler = SessionHandler(
    #     app.state.config,
    #     req_body=req_body,
    #     app=APP,
    #     auth_builder=app.state.auth_builder,
    #     imei=imei
    # )
    response = await get_device(request)

    return response

# TODO: change path
@app.get("/port-in-eligibility/{phoneNumber}", responses=app_excep)
async def pie_get(phoneNumber: str, request: Request) -> PortInEligibility:
    # req_body = validate_request(request)
    # session_handler = SessionHandler(
    #     app.state.config,
    #     req_body=req_body,
    #     app=APP,
    #     auth_builder=app.state.auth_builder,
    #     phone_number=phoneNumber
    # )
    response = await get_eligibility(request)
    return response