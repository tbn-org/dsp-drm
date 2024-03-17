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
env = os.environ['env']

# DSP_DRM_SECRET = json.loads(parameters.get_secret("DSP_DRM_SECRET"))


s3 = boto3.client('s3')

obj = s3.get_object(Bucket="kirandspteststgadconfig", Key="dsp_config.json")
content = obj['Body'].read().decode('utf-8')
dsp_config = json.loads(content)

print(dsp_config)


def lambda_handler(event, context):
    logger.info("event: %s", event)
    logger.info("JWPLAYER_API_KEY: %s", JWPLAYER_API_KEY)
    jwplayer_secret = parameters.get_secret(JWPLAYER_API_KEY)
    print(dsp_config)

    clear_contextvars()
    query_params = event['queryStringParameters']
    applicaster_context = get_applicaster_context(event)
    cloudfront_context = get_cloud_front_context(event)
    country, city, timezone = cloudfront_context[
        "country"], cloudfront_context["city"], cloudfront_context["timezone"]
    type_override = None

    structlog.contextvars.clear_contextvars()
    struc_log_context = create_struc_log_context(event)
    structlog.contextvars.bind_contextvars(**struc_log_context)
    media_id = query_params["mediaid"]
    try:
        tenant = query_params["tenant"]
    except:
        tenant = None
    fast_tag = "no"
    vod_tag = "no"
    # this is MSM DSP
    app_family_id = "meritplus"
    fast_ad_config = {}
    vod_ad_config = {}

    # this is needed for preroll.
    vod_ad_config["vod_tag"] = vod_tag
    fast_ad_config["fast_tag"] = fast_tag

    is_live = "no"
    if applicaster_context["is_live"] == "yes":
        print("is_live?")
        print(applicaster_context)

        fast_tag = "yes"
        fast_ad_config["fast_tag"] = fast_tag
        #fast_ad_config['ad_tag'] = dsp_config['base_settings']['ad_tag_fast']
    else:
        vod_tag = "yes"
        vod_ad_config["vod_tag"] = vod_tag
        
        #vod_ad_config['ad_tag'] = dsp_config['base_settings']['ad_tag_vod']

    # get the type of platform

    

    for x in dsp_config["app_settings"]:
        if x["app_family_id"] == "meritplus":
            for i in x["devices"]:
                if i['platform'].lower() == applicaster_context.get("platform", "android").lower():
                    print("new test here ")
                    print(i)
                    print(applicaster_context)

                    fast_ad_config['app_bundle'] = i["settings"]['app_bundle']
                    fast_ad_config['app_store_url'] = i["settings"]['app_store_url']
                    vod_ad_config['app_bundle'] = i["settings"]['app_bundle']
                    vod_ad_config['app_store_url'] = i["settings"]['app_store_url']
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
                       "fast_ad_config": fast_ad_config
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
