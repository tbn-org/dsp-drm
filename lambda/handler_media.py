import json
import boto3
import json
import logging
import os
import sys
from dsp import create_media_feed
from utils import configure_structured_log, create_struc_log_context, get_applicaster_context, get_cloud_front_context
from dotenv import load_dotenv
from aws_lambda_powertools.utilities import parameters
import structlog
from structlog.contextvars import (
    bind_contextvars,
    clear_contextvars,
)

load_dotenv()

logging.basicConfig(
    format="%(asctime)s  %(message)s",
    stream=sys.stdout,
    level=logging.INFO,
    force=True
)

configure_structured_log()

logger = structlog.get_logger(__name__)
# table name from ENV
AD_MARKERS_TABLE = os.environ['AD_MARKERS_TABLE']
FEED_LINK_URL = os.environ['FEED_LINK_URL']
JWPLAYER_API_KEY = os.environ['JWPLAYER_API_KEY']

dsp_config_bucket = os.environ['S3_BUCKET_NAME']

env = os.environ['env']
# DSP_DRM_SECRET = json.loads(parameters.get_secret("DSP_DRM_SECRET"))
s3 = boto3.client('s3')

obj = s3.get_object(Bucket=dsp_config_bucket, Key="dsp_config.json")
content = obj['Body'].read().decode('utf-8')
dsp_config = json.loads(content)

def lambda_handler(event, context):
    print("MEDIA event: ",event)
    print("MEDIA context: ",context)


    logger.info("event: %s", event)
    logger.info("JWPLAYER_API_KEY: %s", JWPLAYER_API_KEY)
    jwplayer_secret = parameters.get_secret(JWPLAYER_API_KEY)

    clear_contextvars()
    query_params = event['queryStringParameters']

    applicaster_context = get_applicaster_context(event)
    cloudfront_context = get_cloud_front_context(event)
    country, city, timezone = cloudfront_context[
        "country"], cloudfront_context["city"], cloudfront_context["timezone"]
    type_override = None
    

    gdpr_countries = [
    "AT", "BE", "BG", "CY", "CZ",
    "DK", "EE", "FI", "FR", "DE",
    "GR", "HU", "IE", "IT", "LV",
    "LT", "LU", "MT", "NL", "PL",
    "PT", "RO", "SK", "SI", "ES",
    "SE", "IS", "LI", "NO"]

    if country in gdpr_countries:
        gdpr = 1
    else:
        gdpr = 0
    
    structlog.contextvars.clear_contextvars()
    struc_log_context = create_struc_log_context(event)
    structlog.contextvars.bind_contextvars(**struc_log_context)
    media_id = query_params["mediaid"]

    fast_tag = "no"
    vod_tag = "no"
    fast_ad_config = {}
    vod_ad_config = {}
    common_ad_config = {
    "max_ad_duration": "",
    "format": "",
    "content_cat": "",
    "content_genre": "",
    "content_rating": "",
    "content_channel": "",
    "content_network": ""}
    common_ad_config["ip"] = cloudfront_context["ip_address"]
    common_ad_config["gdpr"] = gdpr

    # this is needed for preroll.
    vod_ad_config["vod_tag"] = vod_tag
    fast_ad_config["fast_tag"] = fast_tag
    is_live = "no"
    if applicaster_context["is_live"] == "yes":

        fast_tag = "yes"
        fast_ad_config["fast_tag"] = fast_tag
        fast_ad_config['base_url'] = dsp_config['base_settings']['ad_tag_fast']
    else:
        vod_tag = "yes"
        vod_ad_config["vod_tag"] = vod_tag
        
        vod_ad_config['base_url'] = dsp_config['base_settings']['ad_tag_vod']
    override_feedtype = None
    
    # get the type of platform
    for x in dsp_config["app_settings"]:
        if x["app_family_id"] == applicaster_context["tenant"]:
            vod_ad_config["site_id"] = x.get("global_settings", {}).get('vod_site_id', '')
            fast_ad_config["site_id"] = x.get("global_settings", {}).get('fast_site_id', '')
            common_ad_config["min_ad_duration"] = x.get("global_settings", {}).get('min_ad_duration', '')
            common_ad_config["max_ad_duration"] = x.get("global_settings", {}).get('max_ad_duration', '')
            common_ad_config["format"] = x.get("global_settings", {}).get('format', '')
            common_ad_config["content_cat"] = x.get("global_settings", {}).get('content_cat', '')
            common_ad_config["content_genre"] = x.get("global_settings", {}).get('content_genre', '')
            common_ad_config["content_rating"] = x.get("global_settings", {}).get('content_rating', '')
            common_ad_config["content_channel"] = x.get("global_settings", {}).get('content_channel', '')
            common_ad_config["content_network"] = x.get("global_settings", {}).get('content_network', '')

            for i in x["devices"]:
                if i['platform'].lower() == applicaster_context.get("platform", "android").lower():

                    fast_ad_config['app_bundle'] = i["settings"]['app_bundle']
                    fast_ad_config['app_store_url'] = i["settings"]['app_store_url']
                    vod_ad_config['app_bundle'] = i["settings"]['app_bundle']
                    vod_ad_config['app_store_url'] = i["settings"]['app_store_url']
                    # have a logic to reatin default if blank tag is present in the settings dict. 
                    if vod_tag == "yes":
                        vod_ad_config['site_id'] = i["settings"]['ad_tag_vod_id']
                    if fast_tag == "yes":
                        fast_ad_config['site_id'] = i["settings"]['ad_tag_fast_id']
                    vod_ad_config['site_id'] = i["settings"]['ad_tag_vod_id']

    logger.info("Getting media feed with id :%s", media_id)
    if "override_type" in query_params:
        type_override = query_params['override_type']
    try:
        override_feedtype = query_params["override_feedtype"]
    except:
        override_feedtype = None

    media_feed_args = {"media_id": media_id, "env": env,
                       "jwplayer_secret": jwplayer_secret, "override_feedtype": override_feedtype,
                       "AD_MARKERS_TABLE": AD_MARKERS_TABLE,
                       "applicaster_context": applicaster_context,
                       "cloudfront_context": cloudfront_context,
                       "country": country,
                       "type_override": type_override,
                       "vod_ad_config": vod_ad_config,
                       "fast_ad_config": fast_ad_config,
                       "common_ad_config" : common_ad_config
                       }

    applicaster_feed = create_media_feed(media_feed_args)

    if applicaster_feed == "UNKMEDIAID":
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"message": "Unknown media id"})
        }
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },
        "body": json.dumps(applicaster_feed)
    }