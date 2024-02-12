
import json
import boto3
import decimal
import os
from dateutil import parser
import logging
from boto3.dynamodb.conditions import Key


logger = logging.getLogger(__name__)

history_table_name = os.environ.get("WATCH_HISTORY_TABLE", "UserWatchHistory")

favorites_table_name = os.environ.get(
    "FAVORITES_HISTORY_TABLE", "UserFavoritetList")

jwp_media_table_name = os.environ.get(
    "JWP_MEDIA_TABLE", "JWMediaLibrary")

region_name = os.environ.get("AWS_DEFAULT_REGION", "us-west-2")


dynamodb = boto3.resource(
    'dynamodb', region_name=region_name)


history_table = dynamodb.Table(history_table_name)
fav_table = dynamodb.Table(favorites_table_name)

# Helper class to convert a DynamoDB item to JSON.


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def deserialize_dynamodb_items(items):
    return json.loads(json.dumps(items, cls=DecimalEncoder))


def serialize_dynamodb_items(items):
    return json.loads(json.dumps(items), parse_float=decimal.Decimal)


def save_user_history(user_history, user_id):
    # item = json.loads(json.dumps(user_history), parse_float=Decimal)
    item = serialize_dynamodb_items(user_history)
    response = history_table.put_item(
        Item=item
    )
    return response


def save_user_favorite(fav_item, user_id):
    # item = json.loads(json.dumps(user_history), parse_float=Decimal)
    item = serialize_dynamodb_items(fav_item)
    response = fav_table.put_item(
        Item=item
    )
    return response


def remove_user_favorite(media_id, user_id):
    # item = json.loads(json.dumps(user_history), parse_float=Decimal)
    response = fav_table.delete_item(
        Key={"user_id": user_id, "mediaid": media_id}
    )
    return response


def get_user_favorites(user_id):
    response = fav_table.query(
        KeyConditionExpression=Key('user_id').eq(user_id)
    )
    items = deserialize_dynamodb_items(response['Items'])
    items.sort(key=lambda r: parser.parse(r['last_modified']), reverse=True)
    return items


def is_media_live_stream(media_item):
    tags = media_item["meta_data"]["tags"]
    return "Live" in tags or "Live Feed" in tags


def get_user_watch_history(user_id):
    logger.info("get_user_watch_history with user_id: %s", user_id)
    response = history_table.query(
        KeyConditionExpression=Key('user_id').eq(user_id),
    )
    items = deserialize_dynamodb_items(response['Items'])
    # client side sorting
    items.sort(key=lambda r: parser.parse(r['last_modified']), reverse=True)
    return items[:10]


def get_media_meta_data_cached(media_ids):
    logger.info(
        "Getting media meta data from local cache with media IDs: %s", ",".join(media_ids))
    keys = [{"media_id": media_id} for media_id in media_ids]
    response = dynamodb.batch_get_item(RequestItems={
        jwp_media_table_name: {
            "Keys": keys
        }
    })
    items = deserialize_dynamodb_items(
        response["Responses"][jwp_media_table_name])
    items_filtered = [
        item for item in items if is_media_live_stream(item) is False]
    return items_filtered

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
