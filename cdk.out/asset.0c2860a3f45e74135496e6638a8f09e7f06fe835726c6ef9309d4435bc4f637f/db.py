import base64
import json
import decimal
import json
import requests
import logging
import copy
import os
from pprint import pprint
import boto3
import urllib.parse
# import csv
import urllib.parse
import copy

logger = logging.getLogger()

dynamodb = boto3.resource(
    'dynamodb',
    # region_name="us-west-2"
)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def decode_request_context(encoded_string):
    # Fix incorrect padding in decode https://gist.github.com/perrygeo/ee7c65bb1541ff6ac770
    decoded_string = base64.b64decode(encoded_string+'==')
    return json.loads(decoded_string)


def deserialize_dynamodb_items(items):
    return json.loads(json.dumps(items, cls=DecimalEncoder))


def fetch_ad_markers_by_mediaid(media_id, table_name):
    query = f"SELECT * FROM \"{table_name}\" WHERE mediaid=?"
    try:
        response = dynamodb.meta.client.execute_statement(
            Statement=query, Parameters=[media_id])
        if "Items" in response:
            item_deserilized = deserialize_dynamodb_items(response["Items"])
            return item_deserilized
    except Exception as e:
        logger.warning("record not found in the ad slots cache %s", e)
    return []
