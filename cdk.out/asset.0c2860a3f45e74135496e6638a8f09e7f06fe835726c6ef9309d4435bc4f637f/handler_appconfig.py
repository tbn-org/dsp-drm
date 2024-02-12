import json
import json
import logging
import os
import sys

from dotenv import load_dotenv
import structlog

from dsp import create_app_config_feed
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



def lambda_handler(event, context):
    print("Test this is the latest version, DSP appconfig endpoint")
    logger.info("Received event:%s", event)
    cloud_front_context  = get_cloud_front_context(event)
    country = cloud_front_context.get("country")

    struc_log_context = create_struc_log_context(event)
    structlog.contextvars.bind_contextvars(**struc_log_context)

    feed_title_override = None
    query_params = event['queryStringParameters']
    config_id = query_params["configid"]
    index = int(query_params["index"])

    if "feed_title" in query_params:
        feed_title_override = query_params["feed_title"]

    logging.info(
        "Getting  feed for applicaster config with configid:%s and index :%s", config_id, index)

    applicaster_feed = create_app_config_feed(
        config_id, index, dsp_base_url=FEED_LINK_URL, geo_location=country, feed_title_override=feed_title_override)

    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Credentials" : True            
        },
        "body": json.dumps(applicaster_feed)
    }
