'''
Incoming API request validation.
'''

from fastapi import Request

# from tpx_token_validator.exceptions import TokenAuthenticationError
# from src.main.framework.metrics_utils import update_user_source_in_metrics

from src.main.framework.models import RequestModel

# from src.main.utils import validator_scopes, TokenValidator

from src.main.framework.exceptions import (
    TrackingIdMissingException
)


# def _get_auth_token(request: Request):
    # if not request.headers.get('Authorization'):
    #     raise TokenAuthenticationError('No token passed.')

    # try:
    #     # Remove 'Bearer'
    #     token = request.headers.get('Authorization', '').split(' ')[1]

    # except IndexError as err:
    #     raise TokenAuthenticationError(
    #         'Malformed Authorization header.'
    #     ) from err

    # return token


def validate_request(
        request: Request,
        # req_body: RequestModel
) -> RequestModel:
    '''
    Validate incoming request (headers, body), validate auth token.

    Parameters
    ----------
        request
            The incoming FastAPI Request.
        req_body
            The request body validated against the pydantic model.

    Returns
    -------
    RequestModel
        The modified request body.
    '''
    # validator = TokenValidator.get_validator()  # "singleton" pattern

    # # Authentication
    # token = _get_auth_token(request)
    # decoded_token = validator.validate(token, scopes=validator_scopes())

    headers = request.headers
    # TODO: trackingId will be used later.
    tracking_id = headers.get("trackingId", "")
    if not tracking_id:
        raise TrackingIdMissingException

    # update_user_source_in_metrics(decoded_token.user)

    query_params = request.query_params
    req_body = RequestModel(
        query_params=dict(query_params),
        headers=dict(headers),
        trackingId=tracking_id
    )
    return req_body
