import base64
import json
import logging
import re

import urllib.parse

logger = logging.getLogger(__name__)


APPLI_CASTER_AUTH_CTX_KEYS = {
    "zapp_login_plugin_oauth_2_0": "OKTA_TV_APP_CLIENT_ID", "zapp_login_plugin_oauth_tv_2_0": 'OKTA_TV_APP_CLIENT_ID', "quick-brick-login-flow": "OKTA_ROKU_APP_CLIENT_ID"}

APPLI_CASTER_AUTH_HEADER_KEYS = {
    "Zapp-Login-Plugin-Oauth-2-0.Access-Token": "OKTA_TV_APP_CLIENT_ID", "Zapp-Login-Plugin-Oauth-Tv-2-0.Access-Token": 'OKTA_TV_APP_CLIENT_ID', "Quick-Brick-Login-Flow.Access-Token": "OKTA_ROKU_APP_CLIENT_ID"}


def decode_request_context(encoded_string):
    # Fix incorrect padding in decode https://gist.github.com/perrygeo/ee7c65bb1541ff6ac770
    decoded_string = base64.b64decode(encoded_string+'==')
    return json.loads(decoded_string)

# function extracts access token from the ctx data and return the access_token,the env variable to read the CLIENT ID from
# Get access token from applicaster context encoded base64 string from query param called ctx


def get_access_token_from_context(query_params):
    ctx = query_params['ctx']
    context_obj = decode_request_context(ctx)
    logger.info("get_access_token_from_context:%s", ctx)
    for key in APPLI_CASTER_AUTH_CTX_KEYS.keys():
        if "{}.access_token".format(key) in context_obj:
            logging.debug("Found access token in the applicaster context")
            return context_obj['{}.access_token'.format(key)], APPLI_CASTER_AUTH_CTX_KEYS[key]
    logger.error("None of the the valid keys frond in the request context:%s",
                 ",".join(APPLI_CASTER_AUTH_CTX_KEYS.keys()))
    return None, None


def header_has_valid_key(headers, key):
    return headers.get(key) and headers.get(key) != "undefined" and headers.get(key) != None


def get_client_key_by_hint(platform_hint):
    if platform_hint is None:
        return None
    roku_devices = ("roku")
    other_devices = ("android_tv", "android", "ios",
                     "appletv", "samsung_tv", "amazon_fire_tv", "default", "tvos")
    if platform_hint in roku_devices:
        return "OKTA_ROKU_APP_CLIENT_ID"
    elif platform_hint in other_devices:
        return "OKTA_TV_APP_CLIENT_ID"


def get_access_token_from_headers(headers, platform_hint=None):
    client_key = get_client_key_by_hint(platform_hint)
    access_token = None
    for key, value in APPLI_CASTER_AUTH_HEADER_KEYS.items():
        if header_has_valid_key(headers, key):
            logger.info("Found access token key:%s  value:%s",
                        key, headers.get(key))
            access_token = headers.get(key)
            if client_key == None:
                client_key = APPLI_CASTER_AUTH_HEADER_KEYS[key]
            return access_token, client_key

    logger.error("None of the the valid keys or value frond in the request context:%s",
                 ",".join(APPLI_CASTER_AUTH_HEADER_KEYS.keys()))
    return None, None


def get_token_from_payload(payload, platform_hint):
    client_key = get_client_key_by_hint(platform_hint.lower())
    return payload['data']['userIdentifier'], client_key

#  INJECT ADDS TO CW
def create_publica_url(ad_parms, base_url="https://pbs.getpublica.com/v1/s2s-hb?"):
    AD_URL = base_url
    return AD_URL + urllib.parse.urlencode(ad_parms)

def create_default_ad_extentions(ad_parms):
    ad_slot = 1
    offset = "preroll"
    custom5 = "preroll"
    ad_parms["slot_count"] = ad_slot
    ad_parms["custom_5"] = custom5
    # AD_URL = f'https://pbs.getpublica.com/v1/s2s-hb?site_id=24600&ua=__device-ua__&app_bundle=__app-bundle__&content_title=__item-title__&content_id=__item-mediaid__&format=vast&slot_count=1&app_name=TBN&custom_5={custom5}&device_type=Connectedtv&custom6=__platform__'
    return {
        "offset": offset,
        "ad_url": create_publica_url(ad_parms)
    }

def prepare_video_ad_extention(media_item,markers, ad_parms):
    # media_item = media_item["id"]
    media_duration = media_item["duration"]
    video_ads = []
    has_preroll = False
    # episode_duration = episode["extensions"]["duration"]
    for marker in markers:
        offset = marker["breaktime"]
        break_mode = marker["break_mode"]
        ad_slot = marker["slot"]
        is_live_stream = False
        ad_service_base_url =  "https://pbs.getpublica.com/v1/s2s-hb?site_id=26757"
        if "onAir" in media_item:
            is_live_stream = True
            ad_service_base_url = "https://pbs.getpublica.com/v1/s2s-hb?site_id=26757"

        ad_Service_url =  create_publica_url(ad_parms, ad_service_base_url)
        if offset == 0:
            offset = "preroll"
            custom5 = "preroll"
            ad_parms = ad_parms
            ad_parms["custom_5"] = custom5
            ad_parms["slot_count"] = 1
            # AD_URL = f'https://pbs.getpublica.com/v1/s2s-hb?site_id=24600&ua=__device-ua__&app_bundle=__app-bundle__&content_title=__item-title__&content_id=__item-mediaid__&format=vast&slot_count=1&app_name=TBN&custom_5={custom5}&device_type=Connectedtv&custom6=__platform__'
            
            video_ads.append({
                "offset": offset,
                "ad_url": AD_URL
            })
            has_preroll = True
        else:
            ad_position = media_duration- float(offset)
            # skip the ads towords th end of the video
            if ad_position >= 5:
                ad_parms = ad_parms
                custom5 = "midroll{}".format(break_mode)
                ad_parms["custom_5"] = custom5
                ad_parms["slot_count"] = ad_slot
                AD_URL = create_publica_url(ad_parms)
                # AD_URL = f'https://pbs.getpublica.com/v1/s2s-hb?site_id=24600&ua=__device-ua__&app_bundle=__app-bundle__&content_title=__item-title__&content_id=__item-mediaid__&format=vast&slot_count={ad_slot}&app_name=TBN&custom_5={custom5}&device_type=Connectedtv&custom6=__platform__'
                video_ads.append({
                    "offset": offset,
                    "ad_url": AD_URL
                })
    if len(video_ads) <= 0:
        ad_parms = ad_parms
        return [create_default_ad_extentions(ad_parms)]

    if not has_preroll:
        ad_parms = ad_parms
        video_ads.insert(0, create_default_ad_extentions(ad_parms))

    return video_ads


def inject_adds(media_obj, ad_markers, device_context):

    AD_PARAMS = {
        "site_id":24600,
        "avod": 1,
        "ua": device_context.get("user_agent", "Mozilla/5.0 (Linux; Android 13"),
        "app_bundle": device_context.get("bundle_identifier","com.apptbn"),
        "content_title": "__item-title__",
        "content_id": "",
        "format": "vast",
        "slot_count": 1,
        "app_name": device_context.get("app_name"),
        "custom_5": "preroll",
        "device_type": "Connectedtv",
        "player_height": device_context.get("device_height"),
        "player_width": device_context.get("device_width"),

    }
    # logger.info("video extension with macros: %s", AD_PARAMS)
    
    # media_id = media_obj['id']
    # ad_markers = ad_markers["markers"]
    # if media_id in ad_markers:
    if len(ad_markers) > 0:
        markers = ad_markers[0]['markers']
        return prepare_video_ad_extention(media_obj, markers, AD_PARAMS.copy())
    else:
        return [create_default_ad_extentions(AD_PARAMS.copy())]
    
def get_applicaster_context(event):
    query_params = event['queryStringParameters']
    path = event['path']
    bundle_identifier = ''
    platform = ''
    app_name = 'tbn.tv'
    user_agent = 'Mozilla/5.0 (Windows NT 10.'
    device_type = ''
    device_height=''
    device_width=''
    language = 'en'
    app_store = ''
    
    ctx_query_params = {}
    if "ctx" in query_params:
        ctx_base64_str = query_params['ctx']
        ctx_query_params = decode_request_context(ctx_base64_str)

    if "bundleIdentifier" in ctx_query_params:
        bundle_identifier = ctx_query_params["bundleIdentifier"]
    if "platform" in ctx_query_params:
        platform = ctx_query_params["platform"]
    if "app_name" in ctx_query_params:
        app_name = ctx_query_params["app_name"]
    if "userAgent" in ctx_query_params:
        user_agent = ctx_query_params["userAgent"]
    if "store" in ctx_query_params:
        app_store = ctx_query_params["store"]
    if "languageCode" in ctx_query_params:
        language = ctx_query_params["languageCode"]
    if "deviceHeight" in ctx_query_params:
        device_width = ctx_query_params["deviceHeight"]
    if "deviceWidth" in ctx_query_params:
        device_height = ctx_query_params["deviceWidth"]
    if "deviceType" in ctx_query_params:
        device_type = ctx_query_params["deviceType"]

    device_context = {
        'bundle_identifier': bundle_identifier,
        'platform': platform,
        'app_name': app_name,
        'user_agent': user_agent,
        'device_width': device_width,
        'device_height': device_height,
        'app_store': app_store,
        'language': language,
        "device_type": device_type
        
    }
    return device_context
