import json
import logging
import urllib.parse

logger = logging.getLogger(__name__)

def format_showcase_ad_schedule(marker):
    offset = marker["breaktime"]
    break_mode = marker["break_mode"]
    ad_slot = marker["slot"]
    # For now its 1 ad for pre roll and 2 ads for mid rolls
    if offset == 0:
        return {
            "tag": "https://pbs.getpublica.com/v1/s2s-hb?site_id=26757&site_page=__domain__&format=vast&slot_count=1&site_name=TBN&content_title=__item-title__&content_id=__item-mediaid__&custom_5=preroll",
            "type": "linear",
            "offset": "pre"
        }
    else:
        return {
            "tag": "https://pbs.getpublica.com/v1/s2s-hb?site_id=26757&site_page=__domain__&format=vast&slot_count=2&site_name=TBN&content_title=__item-title__&content_id=__item-mediaid__&custom_5=preroll",
            "type": "linear",
            "offset": offset
        }
    



def create_showcase_ad_schedule(ad_markers):
    ad_schedule = {
        "rules": {
            "startOnSeek": "pre",
            "timeBetweenAds": 0
        },
        "client": "googima",
        "schedule": [
            {
                "tag": "https://pbs.getpublica.com/v1/s2s-hb?site_id=26757&site_page=__domain__&format=vast&slot_count=1&site_name=TBN&content_title=__item-title__&content_id=__item-mediaid__&custom_5=preroll",
                "type": "linear",
                "offset": "pre"
            }
        ],
        "vpaidmode": "insecure",
        "adscheduleid": "4s9nxBP2"
    }
    markers = []

    for marker in ad_markers:
        schedule_item = format_showcase_ad_schedule(marker)
        markers.append(schedule_item)

    ad_schedule["schedule"].extend(markers)
    return ad_schedule

def create_publica_url(ad_parms, base_url="https://pbs.getpublica.com/v1/s2s-hb?"):
    AD_URL = base_url
    return AD_URL + urllib.parse.urlencode(ad_parms)


def create_ssai_url(ad_parms,base_url):
    if "?" not in base_url:
        SSAI_URL = base_url + "?"
        return SSAI_URL + urllib.parse.urlencode(ad_parms)
    SSAI_URL = base_url + "&"
    return SSAI_URL + urllib.parse.urlencode(ad_parms)


def create_default_ad_extentions(ad_parms):
    ad_slot = 1
    offset = "preroll"
    custom5 = "preroll"
    ad_parms["slot_count"] = ad_slot
    ad_parms["custom_5"] = custom5
    # AD_URL = f'https://pbs.getpublica.com/v1/s2s-hb?site_id=24600&ua=__device-ua__&app_bundle=__app-bundle__&content_title=__item-title__&content_id=__item-mediaid__&format=vast&slot_count=1&app_name=TBN&custom_5={custom5}&device_type=Connectedtv&custom6=__platform__'
    return {
        "offset": offset,
        "ad_url": create_publica_url(ad_parms)
    }




def prepare_video_ad_extention(media_item,markers, ad_parms):
    
    # media_item = media_item["id"]
    media_duration = media_item["extensions"]["duration"]
    video_ads = []
    has_preroll = False
    # episode_duration = episode["extensions"]["duration"]
    for marker in markers:

        offset = marker["breaktime"]
  
        break_mode = marker["break_mode"]
        ad_slot = marker["slot"]
        is_live_stream = False
        ad_service_base_url =  "https://pbs.getpublica.com/v1/s2s-hb?site_id=26757"
        if "onAir" in media_item["extensions"]:
            is_live_stream = True
            ad_service_base_url = "https://pbs.getpublica.com/v1/s2s-hb?site_id=26757"

        ad_Service_url =  create_publica_url(ad_parms, ad_service_base_url)
        if offset == 0:

            offset = "preroll"
            custom5 = "preroll"
            ad_parms = ad_parms
            ad_parms["custom_5"] = custom5
            AD_URL = create_publica_url(ad_parms)
            ad_parms["slot_count"] = 1
            # AD_URL = f'https://pbs.getpublica.com/v1/s2s-hb?site_id=24600&ua=__device-ua__&app_bundle=__app-bundle__&content_title=__item-title__&content_id=__item-mediaid__&format=vast&slot_count=1&app_name=TBN&custom_5={custom5}&device_type=Connectedtv&custom6=__platform__'
            
            video_ads.append({
                "offset": offset,
                "ad_url": AD_URL
            })
            has_preroll = True
        else:

            ad_position = media_duration- float(offset)

            # skip the ads towords th end of the video
            if ad_position >= 5:
                ad_parms = ad_parms
                custom5 = "midroll{}".format(break_mode)
                ad_parms["custom_5"] = custom5
                coppa=0
                ad_parms["slot_count"] = ad_slot
                AD_URL = create_publica_url(ad_parms)
                # AD_URL = f'https://pbs.getpublica.com/v1/s2s-hb?site_id=24600&ua=__device-ua__&app_bundle=__app-bundle__&content_title=__item-title__&content_id=__item-mediaid__&format=vast&slot_count={ad_slot}&app_name=TBN&custom_5={custom5}&device_type=Connectedtv&custom6=__platform__'
                video_ads.append({
                    "offset": offset,
                    "ad_url": AD_URL
                })
    if len(video_ads) <= 0:

        ad_parms = ad_parms
        return [create_default_ad_extentions(ad_parms)]

    if not has_preroll:

        ad_parms = ad_parms
        video_ads.insert(0, create_default_ad_extentions(ad_parms))

    return video_ads



def replace_url_values(url, replacement_dict):
    parsed_url = urllib.parse.urlparse(url)
    query_params = dict(urllib.parse.parse_qsl(parsed_url.query))

    for key in replacement_dict:
        if key in query_params:
            query_params[key] = replacement_dict[key]
    new_query = urllib.parse.urlencode(query_params)
    new_url = parsed_url._replace(query= new_query).geturl()
    return new_url



def inject_adds(media_obj, ad_markers, device_context,vod_ad_config,fast_ad_config):


    platform_re = device_context.get("platform", "mobile")
    platform_app_context = device_context.get("platform", "mobile")

    if platform_re.upper() == "ROKU":
        platform_re= "Connectedtv"
    elif platform_re.upper() in ["IOS","IPHONE","IPAD","IPOD"]:
        platform_re = "mobile"
    else:
        platform_re = "Connectedtv"


    if platform_app_context.upper() == "ROKU":
        app_bundle = "4421"
    elif platform_app_context.upper() in ["IOS","IPHONE","IPAD","IPOD","TVOS"]:
        app_bundle = "348738437"
    elif "AMAZON_FIRE_TV" in platform_app_context.upper():
        app_bundle = "B01CV28J7A"
    else:
        app_bundle = "tbn_mobile.android"

    AD_PARAMS = {
        "site_id":24600,
        "avod": 1,
        "ua": device_context.get("user_agent", "Mozilla/5.0 (Linux; Android 13"),
        "app_bundle": app_bundle,
        "content_title": media_obj.get("title"), 
        "content_id": media_obj.get("id"), 
        "format": "vast",
        "slot_count": 1,
        "app_name": device_context.get("app_name"),
        "custom_5": "preroll",
        "device_type": platform_re, 
        "player_height": device_context.get("device_height"),
        "player_width": device_context.get("device_width"),
        "coppa" : 0

    }
    # logger.info("video extension with macros: %s", AD_PARAMS)

    if media_obj.get("title") in ["Yippee Kids TV" , "Smile"]:

        AD_PARAMS["coppa"] = 1
        

    if len(ad_markers) > 0:
        markers = ad_markers[0]['markers']
        return_urls=  prepare_video_ad_extention(media_obj, markers, AD_PARAMS.copy())
    else:
        return_urls=  prepare_video_ad_extention(media_obj, markers, AD_PARAMS.copy())

    for item in return_urls:

        if item['offset'] == "preroll":
            item['ad_url'] = replace_url_values(item['ad_url'], vod_ad_config)
        else: 
            if fast_ad_config["fast_tag"] == "yes":
                item['ad_url'] = replace_url_values(item['ad_url'], fast_ad_config)
            else:
                item['ad_url'] = replace_url_values(item['ad_url'], vod_ad_config)

    return return_urls
    