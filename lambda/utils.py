import json
import base64
import structlog

logger = structlog.get_logger(__name__)


def decode_request_context(encoded_string):
    # Fix incorrect padding in decode https://gist.github.com/perrygeo/ee7c65bb1541ff6ac770
    decoded_string = base64.b64decode(encoded_string+'==')
    return json.loads(decoded_string)


def get_applicaster_context(event):

    print("get_applicaster_contextget_applicaster_context",event)
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
    source_ip =''
    advertisingidentifier = ''

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
    if "deviceWidth" in ctx_query_params:
        device_width = ctx_query_params["deviceWidth"]
    if "deviceHeight" in ctx_query_params:
        device_height = ctx_query_params["deviceHeight"]
    if "deviceType" in ctx_query_params:
        device_type = ctx_query_params["deviceType"]
    if "advertisingIdentifier" in ctx_query_params:
        advertisingidentifier = ctx_query_params["advertisingIdentifier"]

    try:
        source_ip = event['requestContext']['identity']['sourceIp']
    except:
        pass


    device_context = {
        'bundle_identifier': bundle_identifier,
        'platform': platform,
        'app_name': app_name,
        'user_agent': user_agent,
        'device_width': device_width,
        'device_height': device_height,
        'app_store': app_store,
        'language': language,
        "device_type": device_type,
        "source_ip": source_ip ,
        "advertisingidentifier" : advertisingidentifier               
    }
    return device_context

def get_cloud_front_context(event):
    if "headers" not in event:
        return {"country":None, "city":None, "timezone":None, "latitude":None, "longitude":None}

    headers = event['headers']
    country = headers.get('CloudFront-Viewer-Country', None)
    city= headers.get('CloudFront-Viewer-City', None)
    timezone = headers.get('CloudFront-Viewer-Timezone', None)
    latitude = headers.get('CloudFront-Viewer-Latitude', None)
    longitude = headers.get('CloudFront-Viewer-Longitude', None)
    
    return {"country":country, "city":city, "timezone":timezone, "latitude":latitude, "longitude":longitude}

def create_struc_log_context(event):
    cloudfront_context =  get_cloud_front_context(event)
    applicaster_context = get_applicaster_context(event)
    event_context = {}
    try:
        event_context["path"] = event["resource"]
        event_context["sourceIp"] = event['requestContext']['identity']['sourceIp']
    except:
        pass
    
    stuct_log_context = {**cloudfront_context, **applicaster_context, **event_context}

    return stuct_log_context



def configure_structured_log():
    structlog.configure(
    processors=[
        # If log level is too low, abort pipeline and throw away log entry.
        structlog.stdlib.filter_by_level,
        # Add the name of the logger to event dict.
        structlog.stdlib.add_logger_name,
        # Add log level to event dict.
        structlog.stdlib.add_log_level,
        # Perform %-style formatting.
        structlog.stdlib.PositionalArgumentsFormatter(),
        # Add a timestamp in ISO 8601 format.
        structlog.processors.TimeStamper(fmt="iso"),
        # If the "stack_info" key in the event dict is true, remove it and
        # render the current stack trace in the "stack" key.
        structlog.processors.StackInfoRenderer(),
        # If the "exc_info" key in the event dict is either true or a
        # sys.exc_info() tuple, remove "exc_info" and render the exception
        # with traceback into the "exception" key.
        structlog.processors.format_exc_info,
        # If some value is in bytes, decode it to a unicode str.
        structlog.processors.UnicodeDecoder(),
        
        # Add callsite parameters.
        structlog.processors.CallsiteParameterAdder(
            {
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.LINENO,
            }
        ),

        structlog.contextvars.merge_contextvars,
        
        # Render the final event dict as JSON.
        structlog.processors.JSONRenderer()
    ],
    # `wrapper_class` is the bound logger that you get back from
    # get_logger(). This one imitates the API of `logging.Logger`.
    wrapper_class=structlog.stdlib.BoundLogger,
    # `logger_factory` is used to create wrapped loggers that are used for
    # OUTPUT. This one returns a `logging.Logger`. The final value (a JSON
    # string) from the final processor (`JSONRenderer`) will be passed to
    # the method of the same name as that you've called on the bound logger.
    logger_factory=structlog.stdlib.LoggerFactory(),
    # Effectively freeze configuration after creating the first bound
    # logger.
    cache_logger_on_first_use=True,
)
