"""
Exception handling functions.
"""
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import ValidationException

from src.main.framework.exceptions import AppException, EXCEPTION_MAPPING


async def exception_handler(request: Request, exp: Exception) -> JSONResponse:
    """Method to handle exceptions

    Args:
        # request (Request): request object
        exp (Exception): exception object that occured

    Returns:
        JSONResponse : a json response
    """
    if isinstance(exp, AppException):
        return JSONResponse(
            status_code=exp.status_code,
            content={
                'errorCode': exp.error_code,
                'errorMessage': exp.message,
                'severity': exp.severity
            }
        )

    if isinstance(exp, ValidationException):
        return JSONResponse(
            status_code=422,
            content={
                'errorCode': "Validation Exception Error.",
                'errorMessage': exp.message,
                'severity': "ERROR"
            }
        )

    # Else, next check EXCEPTION_MAPPING.
    exception_full_name = (
        f'{exp.__class__.__module__}.{exp.__class__.__qualname__}'
    )

    if exception_full_name in EXCEPTION_MAPPING:
        exception_details = EXCEPTION_MAPPING.get(exception_full_name)
        return JSONResponse(
            status_code=exception_details.get('statusCode'),
            content={
                'errorCode': exception_details.get('errorCode'),
                'errorMessage': (
                    f'{exception_details.get("message")} '
                    f'{str(exp)}'
                ),
                'severity': exception_details.get('severity')
            }
        )

    # Else, use default.
    message = f'{exception_full_name}: {str(exp)}'
    return JSONResponse(
        status_code=500,
        content={
            'errorCode': 'XCP500.UNKNOWN',
            'errorMessage': message,
            'severity': 'ERROR'
        }
    )