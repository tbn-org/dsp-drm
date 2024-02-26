import hashlib
import logging
import urllib.parse
from urllib.parse import urlparse
from urllib.parse import parse_qs
import requests
import structlog

from structlog import configure
from db import fetch_ad_markers_by_mediaid
from adbreaks import inject_adds
from adbreaks import create_ssai_url
import copy
import json
import uuid

logger = structlog.get_logger(__name__)

# filter to process base url


def filter_next_link(feed, api_base_url):
    # feed = copy.deepcopy(applicaster_feed)
    # feed = applicaster_feed
    if "next" in feed:
        next_url = feed["next"]
        parsed_url = urlparse(next_url)
        query_parms = parse_qs(parsed_url.query)
        page_offset, page_limit = query_parms["page_offset"][0], query_parms["page_limit"][0]
        params = {
            'playlistid': feed["id"], "page_offset": page_offset, "page_limit": page_limit}
        feed["next"] = "{}?{}".format(
            api_base_url, urllib.parse.urlencode(params))
    return feed


# filter to add requires_authentication extension
def filter_need_authentication(feed_entry):
    feed_entry["extensions"]["requires_authentication"] = True
    if "tags" in feed_entry:
        if "free" in feed_entry["tags"]:
            feed_entry["extensions"]["requires_authentication"] = False
    return feed_entry


# filter to add media item  for ImgFeaturedImageBranners
def filter_feature_image(feed_entry):
    extentions = feed_entry["extensions"]
    featured_media_items = [{"key": key, "src": extentions[key]}
                            for key in extentions if key.lower().startswith("img")]
    feed_entry["media_group"][0]["media_item"].extend(
        featured_media_items)
    return feed_entry
def filter_drm(feed_entry):

    widevine_url = None
    playready_url = None
    fairplay_license_server_url = None
    fairplay_certificateUrl = None

    for x in feed_entry.get("sources", []):
        drm_info = x.get("drm", {})

        widevine_drm = drm_info.get("widevine", {})
        if "url" in widevine_drm:
            widevine_url = widevine_drm["url"]

        playready_drm = drm_info.get("playready", {})
        if "url" in playready_drm:
            playready_url = playready_drm["url"]

        fairplay_drm = drm_info.get("fairplay", {})
        if "processSpcUrl" in fairplay_drm:
            fairplay_license_server_url = fairplay_drm["processSpcUrl"]
        if "certificateUrl" in fairplay_drm:
            fairplay_certificateUrl = fairplay_drm["certificateUrl"]

    drm = {
        "widevine": {"license_url": widevine_url},
        "playready": {"license_url": playready_url},
        "fairplay": {
            "certificate_url": fairplay_certificateUrl,
            "license_server_url": fairplay_license_server_url,
            "license_server_request_content_type": "application/json",
            "license_server_request_object_key": "server_playback_context",
        },
    }

    feed_entry["extensions"].setdefault("drm", drm)
    #feed_entry["extensions"]["preview_playback"] = feed_entry["content"]["src"]
    return feed_entry


# Filter to add link key to the applicaster feed
def filter_add_link(feed_entry, base_url):
    # extentions = feed_entry["extensions"]
    # content_type = None
    # content_type= extentions.get("contentType", None)
    # content_type = extentions.get("contentType2", content_type)

    # if content_type not in  ["movie"]:
    #     feed_entry["link"] = {"rel": "self", "href": "{}/media?mediaid={}&disablePlayNext=false".format(
    #         base_url, feed_entry["id"])}

    feed_entry["link"] = {
        "rel": "self", "href": "{}/media?mediaid={}&disablePlayNext=false".format(base_url, feed_entry["id"])}

    return feed_entry


# Filter to add analytics
def filter_add_analytics(feed_entry):
    extensions = feed_entry["extensions"]
    network = extensions.get("networks", "")
    TBNmediaId = extensions.get("TBNmediaId", "")
    analyticsCustomProperties = {
        "feedId": extensions["feedid"],
        # "programName": extensions["programName"],
        "network": network,
        "TBNmediaId": TBNmediaId
    }
    feed_entry["extensions"]["analyticsCustomProperties"] = analyticsCustomProperties
    return feed_entry

# create signed URLs
def signed_url(path, expires, secret, host="https://cdn.jwplayer.com"):
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


# Filter to add signed content to the applicaster feed
def filter_add_signed_content(feed_entry, jwplayer_api_secret):
    media_id = feed_entry["id"]
    duration = feed_entry["extensions"]["duration"]
    source = feed_entry['sources']
    if len(source) > 0:
        file = source[0]["file"]
        type = source[0]["type"]
        if not file.startswith("https://cdn.jwplayer.com"):
            feed_entry["content"] = {
                "type": type,
                "src": file
            }
            return feed_entry

    # TODO create experiration based on  the item lengh
    media_signed_url = signed_url(
        "manifests/{}.m3u8".format(media_id), expires=duration, secret=jwplayer_api_secret)
    feed_entry["content"] = {
        "type": "video/hls",
        "src": media_signed_url
    }
    return feed_entry


# Filter to support geo filtering
def filter_geo_location(feed_entry, geo_location):
    logger.debug("processing geo filtering for media id: %s and cdk location:%s",
                 feed_entry['id'], geo_location)
    if geo_location is None:
        logger.warning("no geo location found for cloudfront")
        return feed_entry
    ''' This the custom property comed from jwplayer feed at playlist item level
        geo_allow = "US, CA"
        geo_allow is execlusive allow and inclusive deny for the rest of the locations in the world
        example: the above will include the episodes in the playlist if the users comes from the US or Canada and deny everyones else.
    '''
    geo_tag_key = "geo_allow"
    extensions = feed_entry["extensions"]
    geo_filter = extensions.get(geo_tag_key, None)
    if geo_filter is None:
        logger.debug("geo_allow tag not found in extesnsions.")
        return feed_entry
    allowed_states = [state.lower() for state in geo_filter.split(",")]
    logger.info("geo_allow tag  found: allowed_states:%s cloudfront_location:%s",
                allowed_states, geo_location)
    if geo_location.lower() not in allowed_states:
        logger.info(
            "geo filter not matched geo_location:%s  with geo_allow:%s", geo_location, geo_filter)
        feed_entry['type'] = {'value': "warning"}
        warning_extensions = {"warningMessage": "The content you are trying to view is not available in your viewing area.",
                              "warningTitle": "Oops, Something Happened."}
        feed_entry["extensions"] = {
            **feed_entry["extensions"], **warning_extensions}
        return feed_entry

    return feed_entry


# filter to inject video ads based on the ad breaks database
def filter_inject_ads(feed_entry, table_name, device_context):
    logger.info("reading adbreaks from table %s", table_name)
    #handle the prod failure due to missing tags. 
    try:
        tags = feed_entry["tags"]
    except:
        tags = []
    tags_lower = [item.lower() for item in tags]
    tags = tags_lower

    if "noads" in tags:
        noAds = True
    else:
        noAds = False


    # dont inject ads if it is a trailer 
    if "trailer" in tags or noAds:
        return feed_entry
    media_id = feed_entry["id"]
    ad_markers = fetch_ad_markers_by_mediaid(media_id, table_name)
    video_ads = inject_adds(feed_entry, ad_markers, device_context)
    feed_entry["extensions"]["video_ads"] = video_ads
    return feed_entry

# clean all the additional keys in each entry


def filter_cleanup_feed(feed_entry):
    if "sources" in feed_entry:
        feed_entry.pop('sources', None)
    if "tags" in feed_entry:
        feed_entry.pop('tags', None)

    return feed_entry


def filter_override_type(feed_entry, overide_type):
    if overide_type is None:
        return feed_entry
    feed_entry["type"] = {
        "value": overide_type
    }

    return feed_entry


def filter_ssai(feed_entry,device_context, cloudfront_context):

    content_src = feed_entry["content"]["src"]

    if not content_src.startswith("https://ssai.jwplayer.com") and "now.amagi.tv" not in content_src :
        return feed_entry

    app_store_url = "" 

    if "now.amagi.tv" in content_src:
        ssai_vendor = "amagi"
    else:
        ssai_vendor = "jwplayer"

    app_bundle = "tbn_mobile.android"
    
    if "roku" == device_context.get("platform", "android").lower():
        app_store_url= "https://channelstore.roku.com/details/adee2de8413d590eaadec69d4136d101/tbn-networks-tv"
        app_bundle = "4421"

    if "firetv" == device_context.get("platform", "android").lower():
        app_store_url= "https://www.amazon.com/TBN-Watch-Shows-Live-Free/dp/B01CV28J7A"
        app_bundle = "B01CV28J7A"

    if "ios" == device_context.get("platform", "android").lower():
        app_store_url= "https://apps.apple.com/us/app/tbn-watch-tv-live-on-demand/id348738437"
        app_bundle = "348738437"

    if "appletv" == device_context.get("platform", "android").lower():
        app_store_url= "https://apps.apple.com/us/app/tbn-watch-tv-live-on-demand/id348738437?platform=appleTV"
        app_bundle = "348738437"

    if "tvos" == device_context.get("platform", "android").lower():
        app_store_url= "https://apps.apple.com/us/app/tbn-watch-tv-live-on-demand/id348738437?platform=appleTV"
        app_bundle = "348738437"

    if "androidmobile" == device_context.get("platform", "android").lower():
        app_store_url= "https://play.google.com/store/apps/details?id=tbn_mobile.android"
        app_bundle = "tbn_mobile.android"

    if device_context.get("platform", "android").lower() in  ["samsungtv","lgtv","androidtv","android"]:
        app_store_url= "https://play.google.com/store/apps/details?id=tbn_mobile.android"
        app_bundle = "tbn_mobile.android"
        

    SSAI_PARAMS = {
        #"site_id":24906,
        "site_page":"https://tbn.org",
        "format": "vast",        
        "min_ad_duration": 6,  
        "max_ad_duration": 120,                  
        "ua": device_context.get("user_agent", "Mozilla/5.0 (Linux; Android 13"),
        "player_height": device_context.get("device_height"),
        "player_width": device_context.get("device_width"),
        "device_type": device_context.get("device_type"),         
        "site_name": "TBN",       
        "lat": cloudfront_context.get("latitude"),
        "lon": cloudfront_context.get("longitude"),
        "livestream": 1,
        "ssai_enabled": 1,
        "ssai_vendor": ssai_vendor,
        "ip": cloudfront_context.get("source_ip"),             
        "pod_duration": feed_entry["extensions"]["duration"],  
        "cb": str(uuid.uuid4()), 
        "did" : device_context.get("advertisingidentifier", "None"),
        "app_store_url" : app_store_url,
        "app_domain" : "https://www.tbn.org/",
        "platform" : device_context.get("platform", "android"),
        "app_bundle" : app_bundle 

    }
    
    # logger.info("SSAI macros: %s", SSAI_PARAMS)   

    ssai_new_url =  create_ssai_url(SSAI_PARAMS.copy(),content_src)
    feed_entry["content"]["src"] = ssai_new_url

    return feed_entry






