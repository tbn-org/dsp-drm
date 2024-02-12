import copy
import hashlib
import math
import time
import urllib
import os
import json
import requests
import logging

from applicaster.db import fetch_ad_markers_by_mediaid
from applicaster.utils import inject_adds

logger = logging.getLogger(__name__)
API_SECRET = os.environ.get("JWPLATFORM_API_SECRET", '')  # Replace


def signed_url(path, expires, secret=API_SECRET, host="https://cdn.jwplayer.com"):
    """
    returns a signed url, can be used for any "non-JWT" endpoint
    Args:
      path(str): the jw player route
      expires(int): the expiration time for the URL
      secret(str): JW account secret
      host:(str): url host
    """
    s = "{path}:{exp}:{secret}".format(
        path=path, exp=str(expires), secret=secret)
    signature = hashlib.md5(s.encode("utf-8")).hexdigest()
    signed_params = dict(exp=expires, sig=signature)
    return "{host}/{path}?{params}".format(
        host=host, path=path, params=urllib.parse.urlencode(signed_params)
    )


def get_signed_player(media_id, player_id):
    """
    Return signed url for the single line embed javascript.

    Args:
      media_id (str): the media id (also referred to as video key)
      player_id (str): the player id (also referred to as player key)
    """
    path = "players/{media_id}-{player_id}.js".format(
        media_id=media_id, player_id=player_id
    )

    # Link is valid for 1 hour but normalized to 5 minutes to promote better caching
    expires = math.ceil((time.time() + 3600) / 300) * 300

    # Generate signature
    return signed_url(path, expires)


def get_signed_content_url(media_id):
    path = "manifests/{}.m3u8".format(
        media_id)
    # Link is valid for 1 hour but normalized to 5 minutes to promote better caching
    expires = math.ceil((time.time() + 3600) / 300) * 300
    return {"type": "video/hls", "src": signed_url(path, expires)}


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def _make_jwt_media(media_ids):
    media_ids_param = ",".join(set(media_ids))
    # Delivery endpoints have no rate limit but can be delayed
    api_endpoint = "https://cdn.jwplayer.com/apps/watchlists/oVYfMs4g?media_ids={}".format(
        media_ids_param)
    logger.info("Media meta fetching : %s", api_endpoint)
    response = requests.get(api_endpoint)
    logger.info("Media meta fetching complete : %s", response.status_code)
    if response.status_code != 200:
        raise Exception('Error while fetching meta from JWT player')
    return response.json()


def get_media_meta_data(media_ids):
    meta_data_response = {}
    media_id_bucket = chunks(media_ids, 10)
    for media_ids in media_id_bucket:
        response = _make_jwt_media(media_ids)
        meta_data_dic = {item['mediaid']: item for item in response['playlist']}
        meta_data_response = {**meta_data_response, **meta_data_dic}
    # create a dic for easy access while building applicaster feed
    return meta_data_response

# This


def create_appli_caster_link_item(mediaid):
    return {"rel": "self", "href": "https://zapp-2257-tbn.web.app/jw/media/{}?disablePlayNext=false".format(mediaid)}


def create_media_group(jwt_item):
    images = jwt_item.get('images')
    media_items = [
        {"key": image.get("width"), "src": image.get("src")} for image in images]
    for key in jwt_item.keys():
        if (key.startswith("img")):
            media_items.append({key: jwt_item[key]})
    return [{"type": "image", "media_item": media_items}]


def create_media_group_from_cache(media_item):
    images = media_item.get('media_assets')
    media_items = [
        {"key": image.get("width"), "src": image.get("src")} for image in images]
    for key in media_item["meta_data"].keys():
        if (key.startswith("img")):
            media_items.append({key:  media_item["meta_data"][key]})
    return [{"type": "image", "media_item": media_items}]


def create_extension(jwt_item):
    jwt_item_clone = copy.deepcopy(jwt_item)
    jwt_item_clone.pop("images")
    # Not suure about this, this exists in current API
    jwt_item_clone['hqme'] = True
    # handle tags
    tags = jwt_item.get("tags", "").split(",")

    tags_lower = [x.lower() for x in tags]
    if "free" in tags_lower:
        jwt_item_clone["free"] = True
    else:
        jwt_item_clone["requires_authentication"] = True

    return jwt_item_clone


# filter to inject video ads based on the ad breaks database
def filter_inject_ads(feed_entry, table_name):
    logger.info("reading adbreaks from table %s", table_name)
    tags = feed_entry["meta_data"]["tags"]
    # dont inject ads if it is a trailer 
    if "trailer" in tags:
        return []
    media_id = feed_entry["media_id"]
    # LIST OF AD BREAKS
    ad_markers = fetch_ad_markers_by_mediaid(media_id, table_name)

    return ad_markers

def create_extension_from_cache(media_item, device_context, table_name):
    item_clone = copy.deepcopy(media_item["meta_data"]["custom_params"])
    # Not suure about this, this exists in current API
    item_clone['hqme'] = True
    # handle tags
    adds = filter_inject_ads(media_item, table_name)
    video_ads = inject_adds(media_item, adds, device_context)
    item_clone['video_ads'] = video_ads

    tags = media_item["meta_data"].get("tags", [])
    item_clone["tags"] = ",".join(tags)
    tags_lower = [x.lower() for x in tags]
    if "free" in tags_lower:
        item_clone["free"] = True
    else:
        item_clone["requires_authentication"] = True

    return item_clone


def create_appli_caster_feed_item(jwp_item):
    media_id = jwp_item.get('mediaid')

    ac_feed_item = {
        "id": media_id,
        "type": {"value": "video"},
        "link": create_appli_caster_link_item(media_id),
        "title": jwp_item.get("title"),
        "summary": jwp_item.get("description"),
        "content": get_signed_content_url(media_id),
        "media_group": create_media_group(jwp_item),
        "extensions": create_extension(jwp_item)
    }
    return ac_feed_item


def create_appli_caster_feed_item_from_cache(media_item, device_context, table_name):
    media_id = media_item.get('media_id')

    ac_feed_item = {
        "id": media_id,
        "type": {"value": "video"},
        "link": create_appli_caster_link_item(media_id),
        "title": media_item.get("meta_data")["title"],
        "summary": media_item.get("meta_data")["description"],
        "content": get_signed_content_url(media_id),
        "media_group": create_media_group_from_cache(media_item),
        "extensions": create_extension_from_cache(media_item, device_context, table_name)
    }
    return ac_feed_item
