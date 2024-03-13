import logging
import urllib.parse
from urllib.parse import urlparse
from urllib.parse import parse_qs
import requests
import structlog
import copy
from filters import filter_drm,filter_cleanup_feed, filter_geo_location, filter_add_signed_content, filter_need_authentication, filter_inject_ads, fetch_ad_markers_by_mediaid, filter_add_link, filter_feature_image, filter_add_analytics, filter_next_link, filter_override_type, filter_ssai
import sys 
import math
logger = structlog.get_logger(__name__)
import time 
from jose import jwt


def get_jwplayer_app_config(config_id):
    url = "https://cdn.jwplayer.com/apps/configs/{}.json".format(config_id)
    res = requests.get(url)
    if res.status_code != 200:
        logger.exception(res.text())
        raise Exception(
            "Exception while getting jwplayer app config with id :%s.", config_id)
    return res.json()


def get_jwplayer_playlist(playlist_id,query_string, page_offset=1, page_limit=50):
    
    url = "https://cdn.jwplayer.com/v2/playlists/{}?page_limit={}&page_offset={}".format(
        playlist_id, page_limit, page_offset)
    
    if query_string:
        url = url + "&" +  query_string

    headers = {
        "accept": "application/json",
    }

    response = requests.get(url)


    response = requests.get(url, headers=headers)
    logger.info("Api call to get playlist %s with id finised with status: %s",
                playlist_id, response.status_code)
    if response.status_code not in [200]:
        logger.info(f"Error UNKMEDIAID: error_response {response.status_code } playlistid {playlist_id} while getting media with url: %s ", url )
        return "UNKMEDIAID"
    return response.json()



def get_jwplayer_playlist_search(playlist_id, search_text="", page_offset=1, page_limit=50):
    logger.info("Api call to get playlist with id: %s", playlist_id)

    # url = "https://cdn.jwplayer.com/v2/playlists/{}?search={}&page_limit={}&page_offset={}".format(search_text,
    #                                                                                                playlist_id,
    #                                                                                                page_limit)
    params = {"search": search_text,
              "page_limit": page_limit, "page_offset": page_offset}
    url = "https://cdn.jwplayer.com/v2/playlists/{}?".format(playlist_id)

    parms_encoded = urllib.parse.urlencode(params)
    url = url+parms_encoded

    headers = {
        "accept": "application/json",
    }

    response = requests.get(url, headers=headers)
    logger.info("Api call to get playlist %s with id finised with status: %s",
                playlist_id, response.status_code)
    if response.status_code not in [200]:
        raise Exception("Error while getting playlist with url: %s", url)
    return response.json()

def jwt_signed_url(path, API_SECRET , host="https://cdn.jwplayer.com"):
    exp = math.ceil((time.time() + 3600) / 300) * 300
    params = {}
    params["resource"] = path
    params["exp"] = exp
    

    token = jwt.encode(params, API_SECRET, algorithm="HS256")
    url = f"{host}{path}?token={token}"
    return url

def get_jwplayer_media(media_id,tenant="msm"):
    url = "https://cdn.jwplayer.com/v2/media/{}".format(media_id)
    headers = {
        "accept": "application/json",
    }

    response = requests.get(url, headers=headers)
    logger.info("Api call to get media %s with id finished with status: %s",
                media_id, response.status_code)
    if response.status_code not in [200]:
        logger.info(f"Error UNKMEDIAID: error_response {response.status_code } mediaid {media_id} while getting media with url: %s ", url )
        return "UNKMEDIAID"


    return response.json()


def create_applicaster_entry(playlist_item):


    default_attribute_keys = ["title", "description", "mediaid", "link",
                              "image", "images", "sources", "tracks", "tags", "variations"]
    entry = {}
    entry["type"] = {
        "value": "video"
    }
    if "contentType" in playlist_item:
        entry["type"] = {
            "value": playlist_item['contentType']
        }

    entry["title"] = playlist_item['title']
    entry["summary"] = playlist_item['description']
    entry['sources'] = playlist_item['sources']

    content = dict()
    content["type"] = "video/hls"
    entry["content"] = content
    entry["id"] = playlist_item['mediaid']

    media_item = [{"key": str(image["width"]), "src":image["src"]}
                  for image in playlist_item["images"]]
    entry["media_group"] = [{"type": "image", "media_item": media_item}]
    entry["extensions"] = {key: playlist_item[key]
                           for key in playlist_item if key not in default_attribute_keys}

    try:
        entry["tags"] = [tag.lower() for tag in playlist_item["tags"].split(",")]
    except:
        logger.exception("tags not found for ",(playlist_item))


    return entry


def create_applicaster_feed_from_jwplaylist(playlist,override_feedtype, api_base_url, feed_title_override=None):
    feed = {}
    feed["id"] = playlist["feedid"]
    feed["title"] = playlist["title"]
    if feed_title_override is not None:
        feed["title"] = feed_title_override

    if override_feedtype is not None:
        feed["type"] = {"value": override_feedtype }
    else:
        feed["type"] = {"value": "feed" }

    playlist_episodes = playlist["playlist"]
    feed["entry"] = [create_applicaster_entry(
        playlist_item) for playlist_item in playlist_episodes]
    if "links" in playlist:
        if "next" in playlist["links"]:
            next_url = playlist["links"]["next"]
            parsed_url = urlparse(next_url)
            query_parms = parse_qs(parsed_url.query)
            page_offset, page_limit = query_parms["page_offset"][0], query_parms["page_limit"][0]
            params = {
                'playlistid': feed["id"], "page_offset": page_offset, "page_limit": page_limit}
            feed["next"] = "{}/playlist?{}".format(
                api_base_url, urllib.parse.urlencode(params))
    return feed


def create_applicaster_feed_from_media(playlist,override_feedtype):
    feed = {}
    feed["id"] = playlist["playlist"][0]["mediaid"]
    feed["title"] = playlist["title"]

    if override_feedtype is not None:
        feed["type"] = {"value": override_feedtype }
    else:
        feed["type"] = {"value": "feed" }

    playlist_episodes = playlist["playlist"]
    feed["entry"] = [create_applicaster_entry(
        playlist_item) for playlist_item in playlist_episodes]

    return feed


def process_applicaster_feed_pipeline(feed, pipeline_config):
    entries = feed["entry"]
    filtered_entries = []
    for entry in entries:
        pipeline_filter, filter_args = pipeline_config[0], pipeline_config[1]
        updated_entry = entry
        for index, filter_fun in enumerate(pipeline_filter):
            fun_args = copy.deepcopy(filter_args[index])
            fun_args.insert(0, entry)
            updated_entry = filter_fun(*fun_args)
            if updated_entry is None:
                logger.info("found none in filter from :%s",
                            filter_fun.__name__)
                break
        if updated_entry is None:
            continue
        filtered_entries.append(updated_entry)

    feed["entry"] = filtered_entries
    return feed


# API get playlist applicaster pipe2 feed
def create_playlist_feed(playlist_id,
                         media_link_base_url,override_feedtype=None,
                         page_offset=1,
                         page_limit=50,
                         geo_location="",
                         feed_title_override=None,
                         type_override=None,
                         query_string=None
                         ):


    

    if geo_location is None:
        geo_location = ''

    playlist = get_jwplayer_playlist(
        playlist_id=playlist_id,query_string=query_string, page_limit=page_limit, page_offset=page_offset)
    
    if playlist == "UNKMEDIAID":
        return "UNKMEDIAID"

    
    applicaster_feed = create_applicaster_feed_from_jwplaylist(
        playlist,override_feedtype=override_feedtype, api_base_url=media_link_base_url, feed_title_override=feed_title_override)

    # pipline configuration,
    # ([step1, step2, step3],[step1_args, step2_args, step3_args])
    pipeline_config = [
        (
            filter_need_authentication,
            filter_add_link,
            filter_feature_image,
            filter_add_analytics,
            filter_geo_location,
            filter_cleanup_feed,
            filter_override_type),
        (
            [],
            [media_link_base_url],
            [],
            [],
            [geo_location],
            [],
            [type_override],
        )
    ]


    applicaster_feed = process_applicaster_feed_pipeline(
        applicaster_feed, pipeline_config)

    return applicaster_feed


def create_playlist_search_feed(playlist_id,
                                search_text,
                                dsp_base_url,
                                page_offset=1,
                                page_limit=50,
                                geo_location="",
                                feed_title_override=None,override_feedtype=None
                                ):
    # logger.info("calling search api with playlist id: %s and search text:%s", playlist_id, search_text)
    if geo_location is None:
        geo_location = ''

    playlist = get_jwplayer_playlist_search(
        playlist_id, search_text, page_limit=page_limit, page_offset=page_offset)

    # pipline configuration,
    # ([step1, step2, step3],[step1_args, step2_args, step3_args])
    pipeline_config = [
        (
            filter_need_authentication,
            filter_add_link,
            filter_feature_image,
            filter_add_analytics,
            filter_geo_location,
            filter_cleanup_feed),
        (
            [],
            [dsp_base_url],
            [],
            [],
            [geo_location],
            [],
        )
    ]
    applicaster_feed = create_applicaster_feed_from_jwplaylist(
        playlist,override_feedtype, dsp_base_url, feed_title_override=feed_title_override)

    applicaster_feed = process_applicaster_feed_pipeline(
        applicaster_feed, pipeline_config)

    return applicaster_feed


def create_media_feed(args):


    media_id = args.get("media_id")
    env = args.get("env")
    jwplayer_secret = args.get("jwplayer_secret")
    override_feedtype = args.get("override_feedtype")
    ad_breaks_table = args.get("AD_MARKERS_TABLE")  
    device_context = args.get("applicaster_context") 
    cloudfront_context = args.get("cloudfront_context")
    geo_location = args.get("country", "")  
    override_type = args.get("type_override", None)  
    vod_ad_config = args.get("vod_ad_config")
    ad_config = args.get("ad_config")

    playlist = get_jwplayer_media(media_id)
    if playlist == "UNKMEDIAID" :
        return "UNKMEDIAID"

    applicaster_feed = create_applicaster_feed_from_media(playlist,override_feedtype)


    pipeline_config = [
        (
            filter_inject_ads,
            filter_need_authentication,
            filter_feature_image,
            filter_add_signed_content,
            filter_geo_location,
            filter_ssai,
            filter_cleanup_feed,
            filter_override_type),
        (
            [ad_breaks_table, device_context],
            [],
            [],
            [jwplayer_secret],
            [geo_location],
            [device_context,cloudfront_context],            
            [],
            [override_type],
        )
    ]

    applicaster_feed = process_applicaster_feed_pipeline(
        applicaster_feed, pipeline_config)
    return applicaster_feed


def create_app_config_feed(config_id,
                           index,
                           dsp_base_url,
                           geo_location=None,
                           feed_title_override=None,
                           ):
    config = get_jwplayer_app_config(config_id)
    # get the playlist for Landing page from config based on index
    contents = config["content"]
    logger.info("config contents : %s", contents)
    # filter continue watch and favs
    contents_filtered = [
        content for content in contents if content["type"] in ["playlist"]]
    if index+1 > len(contents_filtered):
        empty_feed = {
            "id": "index_not_found",
            "title": "index_not_found",
            "type": {
                "value": "feed"
            }, "entry": []}
        return empty_feed

    playlist_id = contents_filtered[index]["contentId"]
    logging.info("get playlist id from playlist_id:%s", playlist_id)
    return create_playlist_feed(playlist_id=playlist_id,
                                geo_location=geo_location,
                                feed_title_override=feed_title_override,
                                media_link_base_url=dsp_base_url)


