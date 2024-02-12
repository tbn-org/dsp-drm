import asyncio
import logging
import requests
from okta_jwt_verifier import AccessTokenVerifier, JWTUtils, BaseJWTVerifier
from okta_jwt_verifier.exceptions import JWTValidationException

logger = logging.getLogger(__name__)


def jwt_verifier(token, issuer, client_id, audience="tbn"):
    jwt_verifier = BaseJWTVerifier(issuer, client_id, audience=audience)
    headers, claims, signing_input, signature = jwt_verifier.parse_token(token)
    okta_jwk = jwt_verifier.get_jwk(headers['kid'])  # Removed await
    jwt_verifier.verify_signature(token, okta_jwk)
    # jwt_verifier = BaseJWTVerifier(issuer, '{CLIENT_ID}', 'api://default')
    # jwt_verifier = AccessTokenVerifier(
    #     issuer=issuer, audience=audience)
    # await jwt_verifier.verify(token)


# Validate access token using jwt verifier instead of using remote


def validate_access_token_local(token, issuer, client_id):
    logger.info('calling jwt_verifier with issuer:%s  client_id:%s  token%s',
                issuer, client_id, token)
    try:
        jwt_verifier(token, issuer, client_id)  # Removed asyncio.run
    except Exception:
        logger.exception("Invalid access token")
        return False, {}
    headers, payload, signing_input, signature = JWTUtils.parse_token(token)
    logger.info('parse_token payload:%s', payload)
    return True, payload


def validate_access_token_with_client_id(token, issuer, client_id):
    params = {'client_id': client_id}
    data = {'token_type': 'access_token', 'token': token}
    logger.info('calling validate_access_token_with_client_id with issuer:%s  client_id:%s  token%s',
                issuer, client_id, token)
    r = requests.post(
        '{}/v1/introspect'.format(issuer), params=params, data=data)
    if r.status_code != 200:
        return False, None
    response = r.json()
    logger.info('Validate access token response:%s', response)
    return response['active'], response


def validate_access_token_with_client_secret(token, issuer, client_id, client_secret):
    params = {'client_id': client_id, 'client_secret': client_secret}
    data = {'token_type': 'access_token', 'token': token}

    r = requests.post(
        '{}/v1/introspect'.format(issuer), params=params, data=data)
    if r.status_code != 200:
        return False, None
    response = r.json()
    logger.info('Validate access token response:%s', response)
    return response['active'], response


def get_okta_user_info(token, issuer):
    headers = {'Authorization': 'Bearer {}'.format(token)}
    r = requests.get(
        '{}/v1/userinfo'.format(issuer), headers=headers)
    if r.status_code == 200:
        return r.json()
    return None


def validate_access_token(access_token, config, client_key_name):
    is_valid, access_token_response = False, None
    logger.info("validating access token with client_key_name: %s",
                client_key_name)
    if client_key_name == 'OKTA_ROKU_APP_CLIENT_ID':
        logger.info("Found ROKU type access token")
        logger.info(
            "Validating access token for APP:%s", 'TBN Applicaster Roku Device App')
        is_valid, access_token_response = validate_access_token_with_client_secret(
            access_token, config['OKTA_ISSUER'], config[client_key_name], config['OKTA_ROKU_APP_CLIENT_SECRET'])
    else:
        logger.info("Found Mobile/TV type access token")

        logger.info(
            "Validating access token for APP:%s", 'TBN Applicaster Mobile TV Device Apps')
        is_valid, access_token_response = validate_access_token_with_client_id(
            access_token, config['OKTA_ISSUER'], config["OKTA_TV_APP_CLIENT_ID"])

    return is_valid, access_token_response


def revoke_access_token(access_token, client_id, issuer):
    data = {'token_type_hint': 'access_token',
            'token': access_token, "client_id": client_id}

    r = requests.post(
        '{}/v1/revoke'.format(issuer), data=data)
    logger.info('revoke access token status:%s', r.status_code)
    if r.status_code != 200:
        return False, None

    return True, {}


def validate_access_token_in_payload(request):
    logger.info("validating access token in payload")

    # take query parameters as hig priority,
    if not platform_hint:
        platform_hint = platform
    payload = request.json
    access_token, CLIENT_KEY_NAME = get_token_from_payload(
        payload, platform_hint)
    logger.info(
        "Validating access token with APP:%s", CLIENT_KEY_NAME)

    is_valid, access_token_response = validate_access_token_local(
        access_token, config["OKTA_ISSUER"], config[CLIENT_KEY_NAME])
    setattr(request, "token", access_token_response)
    if not is_valid:
        return make_response(jsonify({"message": "No or invalid token found!"}), 401)
    return f(*args, **kwargs)
