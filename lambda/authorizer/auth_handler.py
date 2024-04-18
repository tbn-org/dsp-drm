from __future__ import print_function
import os
import json
import asyncio
import logging
from okta_jwt_verifier import AccessTokenVerifier, JWTUtils
from okta_jwt_verifier.exceptions import JWKException, JWTValidationException

# Log level set
logger = logging.getLogger()
LOG_LEVEL = os.environ.get("LOG_LEVEL", "DEBUG")
if LOG_LEVEL == "DEBUG":
    logger.setLevel(logging.DEBUG)
elif LOG_LEVEL == "INFO":
    logger.setLevel(logging.INFO)
else:
    logger.setLevel(logging.DEBUG)


APPLI_CASTER_AUTH_HEADER_KEYS = {
    "Authorization": "",  "Zapp-Login-Plugin-Oauth-2-0.Access-Token": "OKTA_TV_APP_CLIENT_ID", "Zapp-Login-Plugin-Oauth-Tv-2-0.Access-Token": 'OKTA_TV_APP_CLIENT_ID', "Quick-Brick-Login-Flow.Access-Token": "OKTA_ROKU_APP_CLIENT_ID"}

ISSUER = os.environ.get(
    'ISSUER', "https://secure.tbn.org/oauth2/ausgtj94oUNEAfD44696")
AUDIENCE = os.environ.get("AUDIENCE", "tbn")

ANONYMOUS_ALLOWED_METHODS = {"/": "GET"}


def header_has_valid_key(headers, key):
    return headers.get(key) and headers.get(key) != "undefined" and headers.get(key) != None


def get_access_token_from_headers(headers):
    access_token = None
    for key, value in APPLI_CASTER_AUTH_HEADER_KEYS.items():
        if header_has_valid_key(headers, key):
            logger.info("Found access token key:%s  value:%s",
                        key, headers.get(key))
            access_token = headers.get(key)
            return access_token
    logger.error("None of the the valid keys or value frond in the request headers:%s",
                 ",".join(APPLI_CASTER_AUTH_HEADER_KEYS.keys()))
    return None


def _create_allowed_response(event):
    response = {
        "principalId": "usernamex",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": "Allow",
                    "Resource":  event['methodArn']
                }
            ]
        }
    }
    return response


def _create_deny_response(event):
    response = {
        "principalId": "usernamex",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": "Deny",
                    "Resource":  event['methodArn']
                }
            ]
        }
    }
    return response


async def verify_access_token(access_token):
    jwt_verifier = AccessTokenVerifier(issuer=ISSUER, audience=AUDIENCE)
    await jwt_verifier.verify(access_token)


def get_token_context(token):
    headers, payload, signing_input, signature = JWTUtils.parse_token(token)
    return {"token": token, "payload": payload, "headers": headers}


def lambda_handler(event, context):
    logger.debug(json.dumps(event))
    request_headers = event["headers"]
    requestContext = event["requestContext"]
    http_method = requestContext["httpMethod"]
    request_path = requestContext["path"]
    logger.info("httpMethod:%s requestPath:%s", http_method, request_path)
    if request_path in ANONYMOUS_ALLOWED_METHODS:
        if http_method == ANONYMOUS_ALLOWED_METHODS[request_path]:
            logger.info("Found ANONYMOUS_ALLOWED_METHODS")
            return _create_allowed_response(event)

    logger.info("Method ARN:%s", event['methodArn'])
    access_token = None
    if event["type"] == "TOKEN":
        access_token = event["authorizationToken"]
    elif event["type"] == "REQUEST":
        access_token = get_access_token_from_headers(request_headers)
    if access_token != None:
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(verify_access_token(access_token))
            response = _create_allowed_response(event)
            response["context"] = get_token_context(access_token)

        except JWTValidationException as e:
            logger.warning("access token verification failed:%s", e)
    return _create_deny_response(event)
