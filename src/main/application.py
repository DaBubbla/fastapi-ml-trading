"""
Routes for both REST and GraphQL.
"""
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from src.main.exception_handling import exception_handler
from src.main.framework.config_manager import APP_CONFIG
from src.main.framework.exceptions import app_except
from src.main.framework.models import ResponseModel
from src.main.framework.session_handler import SessionHandler

# from src.main.framework.models import PortInEligibility, XMEligibility
# from src.main.graphql_api.graphql import GRAPHQL_APP

from src.main.middleware import RequestMiddleware
from src.main.request_validation import validate_request

from src.main.rest_api.handler import call_api, prediction_handler


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


@app.on_event("startup")
async def startup_tasks():
    app.state.config = APP_CONFIG.get_configs()


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


@app.get("/predict")
async def predict_stock_price(
    request: Request,
):
    # ticker_symbol = data.ticker_symbol
    # start_date = data.start_date
    # end_date = data.end_date

    req_body = validate_request(request)

    session_handler = SessionHandler(
        app.state.config,
        req_body=req_body,
        app=app,
    )
    response = prediction_handler(session_handler)
    return response.model_dump()
    