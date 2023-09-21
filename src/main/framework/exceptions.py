"""
Custom-defined Exception classes.
"""


class AppException(Exception):
    """
    Base Exception class.
    """
    statusCode = int()
    message = ""
    errorCode = ""
    severity = "ERROR"

    def __init__(self, *args):
        super().__init__(*args)
        if args:
            if not self.message:
                self.message = args[0]

            else:
                self.message = f"{self.message} {args[0]}"

    def __str__(self):
        if self.message:
            return f"{self.__class__.__qualname__}: {self.message}"

        return self.__class__.__qualname__


class TrackingIdMissingException(AppException):
    """
    Tracking ID Missing Exception.
    Tracking ID not present in request header.
    """
    statusCode = 400
    message = (
        "Invalid incoming request: "
        "trackingId not present in incoming request. "
        "TrackingId must be present in the header."
    )
    errorCode = "K8_PROJECT.TRACKINGIDMISSING"


class DownstreamException(AppException):
    statusCode = 400
    message = "Downstream Error Exception."
    errorCode = "K8_PROJECT.DOWNSTREAMERROR"


class BadConfigException(AppException):
    statusCode = 400
    message = "Bad Config Exception Error."
    errorCode = "K8_PROJECT_1.BADCONFIG"


class PATH1500Exception(AppException):
    statusCode = 500
    message = "K8 500 Exception Error."
    errorCode = "K8_PROJECT_2.APP500"


class BadPATH1URLException(AppException):
    statusCode = 400
    message = "Bad PATH1 URL Exceptions Error."
    errorCode = "K8_PROJECT_5"


# class InvalidTokenException(AppException):
#     statusCode = 400
#     message = "Bad Invalid Token Exception Error."
#     errorCode = "K8_PROJECT_8"


class RequestBodyException(AppException):
    statusCode = 400
    message = "Request Body Exception Error."
    errorCode = "K8_PROJECT_10"


class GraphQLQueryException(AppException):
    statusCode = 400
    message = "GraphQL Query Exception Error."
    errorCode = "K8_PROJECT_11"



# Externally-defined exception classes. #
EXCEPTION_MAPPING = {
    "builtins.Exception": {
        "errorCode": "DOWNSTREAM_500_1_1",
        "severity": "ERROR",
        "statusCode": 500,
        "message": "Internal server error, Please try later."
    },
    "src.main.framework.exceptions.TrackingIdMissingException": {
        "errorCode": "K8_PROJECT.TRACKINGIDMISSING",
        "severity": "ERROR",
        "statusCode": 400,
        "message": "Invalid incoming request: "
            "trackingId not present in incoming request. "
            "TrackingId must be present in the header."
    },
    # "src.main.framework.exceptions.BadConfigException": {
    #     "errorCode": "K8_PROJECT_1.BADCONFIG",
    #     "severity": "ERROR",
    #     "statusCode": 400,
    #     "message": "Bad Config Exception Error."
    # },
    "src.main.framework.exceptions.PATH1500Exception": {
        "errorCode": "K8_PROJECT_2.APP500",
        "severity": "ERROR",
        "statusCode": 500,
        "message": "PATH1 500 Exception Error."
    },
    "src.main.framework.exceptions.PATH1ForbiddenException": {
        "errorCode": "K8_PROJECT_4",
        "severity": "ERROR",
        "statusCode": 400,
        "message": "PATH1 Forbidden Exception Error."
    },
    "src.main.framework.exceptions.BadPATH1URLException": {
        "errorCode": "K8_PROJECT_5",
        "severity": "ERROR",
        "statusCode": 400,
        "message": "Bad PATH1 URL Exception Error."
    },
    "src.main.framework.exceptions.BadIMEIException": {
        "errorCode": "K8_PROJECT_6",
        "severity": "ERROR",
        "statusCode": 400,
        "message": "Bad IMEI Exception Error."
    },
    "src.main.framework.exceptions.BadPhoneNumberException": {
        "errorCode": "K8_PROJECT_7",
        "severity": "ERROR",
        "statusCode": 400,
        "message": "Bad Phone Number Exception Error."
    },
    "src.main.framework.exceptions.InvalidTokenException": {
        "errorCode": "K8_PROJECT_8",
        "severity": "ERROR",
        "statusCode": 400,
        "message": "Bad Invalid Token Exception Error."
    },
    "src.main.framework.exceptions.DownStreamException": {
        "errorCode": "K8_PROJECT.DOWNSTREAMERROR",
        "severity": "ERROR",
        "statusCode": 400,
        "message": "Down Stream Exception Error."
    },
    "src.main.framework.exceptions.RequestBodyException": {
        "errorCode": "K8_PROJECT_10",
        "severity": "ERROR",
        "statusCode": 400,
        "message": "Request Body Exception Error."
    },
    "src.main.framework.exceptions.GraphQLQueryException": {
        "errorCode": "K8_PROJECT_11",
        "severity": "ERROR",
        "statusCode": 400,
        "message": "GraphQL Query Exception Error."
    }
}


from pydantic import BaseModel

class APPExceptions(BaseModel):
    errorMessage: str = "Exception Error."
    errorCode: str  = "K8_PROJECT_"
    severity: str = "ERROR"

class APPValidationException(BaseModel):
    errorMessage: str = "Validation Exception Error."
    errorCode: str  = "K8_PROJECT.VALIDATIONERROR"
    severity: str = "ERROR"

class APPAuthenticationExcept(BaseModel):
    errorMessage: str = "Invalid request. Authentication failed."
    errorCode: str  = "DOWNSTREAM_403_1_1.TOKENAUTHENTICATIONERROR"
    severity: str = "ERROR"

class APPAuthorizationExcept(BaseModel):
    errorMessage: str = "Invalid request. Authorization failed"
    errorCode: str  = "DOWNSTREAM_401_1_1.TOKENAUTHORIZATIONERROR"
    severity: str = "ERROR"

app_except = {
    400: {"model": APPExceptions},
    401: {"model": APPAuthorizationExcept},
    403: {"model": APPAuthenticationExcept},
    422: {"model": APPValidationException},
    500: {"model": APPExceptions},
}