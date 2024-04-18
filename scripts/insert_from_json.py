import json
import boto3
import decimal
import os
from dateutil import parser
import logging
from boto3.dynamodb.conditions import Key
import csv
import sys

region_name = os.environ.get("AWS_DEFAULT_REGION", "us-west-2")
dynamodb = boto3.resource('dynamodb', region_name=region_name)
# TABLE_PROD = "AdInjectorStack-admarkerscache986FBE06-FAJ014BUZPRP"
TABLE_DEV = "tbn-dsp-adbreaks"
TBN_PROD="tbn-dsp-adbreaks"
# TABLE_NAME = TABLE_PROD
TABLE_NAME = TBN_PROD

FILE_NAME = sys.argv[1]


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def serialize_dynamodb_items(items):
    return json.loads(json.dumps(items), parse_float=decimal.Decimal)

table = dynamodb.Table(TABLE_NAME)
markers = {}
with open(FILE_NAME) as json_file:
    logging.info("Processing json file")
    json_data = json.load(json_file)
    for row in json_data:
        if "Breaks" not in row:
            continue
        breaks = row["Breaks"]
        for ad_break in breaks:
            media_id = row["JWPlayer_MediaId"]
            break_mode = 1
            breaktime = int(ad_break["BreakTime"])
            add_slot = 2
            break_obj = {"mediaid":media_id,"break_mode":break_mode,"breaktime":int(breaktime), "slot":add_slot }
            if media_id not in markers:
                markers[media_id] = [break_obj]
            else:
                markers[media_id].append({"mediaid":media_id,"break_mode":break_mode,"breaktime":int(breaktime), "slot":add_slot })
    with table.batch_writer() as batch:
         for mediaId in markers: 
            print(mediaId)
            obj = {"mediaid": mediaId, "markers": markers[mediaId]}
            batch.put_item(Item=serialize_dynamodb_items(obj))
    
    
            
       