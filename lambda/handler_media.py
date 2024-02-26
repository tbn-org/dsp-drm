import json
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

#DSP_DRM_SECRET = json.loads(parameters.get_secret("DSP_DRM_SECRET"))


def lambda_handler(event, context):
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

    structlog.contextvars.clear_contextvars()
    struc_log_context = create_struc_log_context(event)
    structlog.contextvars.bind_contextvars(**struc_log_context)
    media_id = query_params["mediaid"]
    try: 
        tenant = query_params["tenant"]
    except: 
        tenant = None


    logger.info("Getting media feed with id :%s", media_id)
    if "override_type" in query_params:
        type_override = query_params['override_type'] 
    try: 
        override_feedtype = query_params["override_feedtype"]
    except: 
        override_feedtype = None


    applicaster_feed = create_media_feed(
        media_id,env, jwplayer_secret,override_feedtype, AD_MARKERS_TABLE, applicaster_context, cloudfront_context, country,type_override)
    

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
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Credentials" : True            
        },
        "body": json.dumps(applicaster_feed)
    }

