import json
import boto3
import decimal
import os
from dateutil import parser
import logging
from boto3.dynamodb.conditions import Key
import csv

region_name = os.environ.get("AWS_DEFAULT_REGION", "us-west-2")
dynamodb = boto3.resource('dynamodb', region_name=region_name)

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

table = dynamodb.Table('AdInjectorStack-admarkerscache986FBE06-MU72H1E7N55A')
markers = {}
with open("admarkers.csv") as csv_file:
    logging.info("Processing csv file")
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        media_id = row[0]
        break_mode = row[1]
        breaktime = row[2]
        add_slot = row[3]
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
    
    
            
       