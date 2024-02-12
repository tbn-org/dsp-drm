import base64
import json
import json
import logging
import os
import sys
import boto3
from dotenv import load_dotenv
import structlog
from dsp import create_playlist_feed, create_playlist_search_feed
from utils import configure_structured_log, create_struc_log_context, get_cloud_front_context

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
FEED_LINK_URL = os.environ['FEED_LINK_URL']

# AD_MARKERS = {}
dynamodb = boto3.resource('dynamodb', region_name="us-west-2")


AD_MARKERS = {}


def decode_request_context(encoded_string):
    # Fix incorrect padding in decode https://gist.github.com/perrygeo/ee7c65bb1541ff6ac770
    decoded_string = base64.b64decode(encoded_string+'==')
    return json.loads(decoded_string)



def lambda_handler(event, context):
    logger.info(event)
    print("Test this is the latest version, DSP search endpoint")
    query_params = event['queryStringParameters']
    cloudfront_context = get_cloud_front_context(event)
    country, city, timezone = cloudfront_context[
        "country"], cloudfront_context["city"], cloudfront_context["timezone"]

    structlog.contextvars.clear_contextvars()
    struc_log_context = create_struc_log_context(event)
    structlog.contextvars.bind_contextvars(**struc_log_context)
    feed_title_override = None
    page_limit = 50
    page_offset = 1
    playlistId = query_params["playlistid"]

    try: 
        override_feedtype = query_params["override_feedtype"]
    except: 
        override_feedtype = None


    if "feed_title" in query_params:
        feed_title_override = query_params["feed_title"]
    search = ""
    if "search" in query_params:
        search = query_params["search"]
    if "page_limit" in query_params:
        page_limit = query_params["page_limit"]
    if "page_offset" in query_params:
        page_offset = query_params["page_offset"]
    applicaster_feed = create_playlist_search_feed(
        playlistId, search, dsp_base_url=FEED_LINK_URL, 
        page_limit=page_limit, 
        page_offset=page_offset, 
        geo_location=country, 
        feed_title_override=feed_title_override,override_feedtype=override_feedtype)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Credentials" : True            
        },
        "body": json.dumps(applicaster_feed)
    }
