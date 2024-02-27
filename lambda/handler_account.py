import base64
import json
import json
import logging
import uuid
import sys
import structlog
from utils import configure_structured_log, create_struc_log_context, get_applicaster_context, get_cloud_front_context
import os 

from dotenv import load_dotenv
from structlog.contextvars import (
    bind_contextvars,
    clear_contextvars,
)



load_dotenv()

# table name from ENV
AD_MARKERS_TABLE = os.environ['AD_MARKERS_TABLE']
#todo 
SVOD_SUBS_TBL = os.environ['SVOD_SUBS_TBL']
TVOD_SUBS_TBL = os.environ['TVOD_SUBS_TBL']

FEED_LINK_URL = os.environ['FEED_LINK_URL']
jwplayer_secret = os.environ['JWPLAYER_API_KEY']
db_tables = {"AD_BREAKS_TABLE":AD_MARKERS_TABLE ,"SVOD_SUBS_TBL" :SVOD_SUBS_TBL , "TVOD_SUBS_TBL" :TVOD_SUBS_TBL }

PURCHASE_URL = os.environ['PURCHASE_URL']

logging.basicConfig(
    format="%(asctime)s  %(message)s",
    stream=sys.stdout,
    level=logging.INFO,
    force=True
)

configure_structured_log()
logger = structlog.get_logger(__name__)

def decode_request_context(encoded_string):
    decoded_string = base64.b64decode(encoded_string+'==')
    return json.loads(decoded_string)

def lambda_handler(event, context):
    logger.info("lambda handler event:%s", event)
    query_params = event['queryStringParameters']
    cloudfront_context = get_cloud_front_context(event)
    applicaster_context = get_applicaster_context(event)
    country, city, timezone = cloudfront_context[
        "country"], cloudfront_context["city"], cloudfront_context["timezone"]
    structlog.contextvars.clear_contextvars()
    struc_log_context = create_struc_log_context(event)
    structlog.contextvars.bind_contextvars(**struc_log_context)

    unique_id = str(uuid.uuid4())
    
    applicaster_feed = {"id": unique_id  , "title":"Account Details","type":{"value":"feed"}} 

    entry = []

    src= f"{PURCHASE_URL}/select-plan?open_external_url=true"


    if applicaster_context.get("platform", "android").lower() in  ["ios","tvos"]:
        src= f"tbn-app://externalLinkAccount/?developer=Trinity%20Broadcasting%20Network"

    

    account_details = {"content":{"src":src,"type":"link"},
                  "extensions":{"buttonLabel":"Manage Account"},
                  "id":unique_id,
                  "link":{"href":src,"type":"link"},"title":"Account Details",
                  "type":{"value":"link"}}
    
    account_details['extensions']['email'] = None
    account_details['extensions']['fullName'] = None


    if "email" in applicaster_context:
        account_details['extensions']['email'] = applicaster_context['email']
    if "firstName" in applicaster_context and "lastName" in applicaster_context:
        account_details['extensions']['fullName'] = applicaster_context['firstName'] + " " +  applicaster_context['lastName'] 
    

    entry.append(account_details)

    applicaster_feed["entry"] = entry

    if applicaster_context["okta_user_id"] is None:
        applicaster_feed = {} 

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Credentials" : True            
        },
        "body": json.dumps(applicaster_feed)
    }