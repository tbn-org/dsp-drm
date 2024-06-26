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
        ad_service_base_url =  "https://pbs.getpublica.com/v1/s2s-hb?"
        if "onAir" in media_item["extensions"]:
            is_live_stream = True
            ad_service_base_url = "https://pbs.getpublica.com/v1/s2s-hb?"

        #kiran commented april 1
        #ad_Service_url =  create_publica_url(ad_parms, ad_service_base_url)
        if offset == 0:

            offset = "preroll"
            custom5 = "preroll"
            ad_parms = ad_parms
            ad_parms["custom_5"] = custom5
            AD_URL = create_publica_url(ad_parms)
            ad_parms["slot_count"] = 1

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



import urllib.parse

def replace_url_values(url, replacement_dict, new_base_url=None):
    # Parse the original URL
    parsed_url = urllib.parse.urlparse(url)
    
    # Extract and update query parameters
    query_params = dict(urllib.parse.parse_qsl(parsed_url.query))
    query_params.update(replacement_dict)
    
    # Construct the new query string
    new_query = urllib.parse.urlencode(query_params)
    
    # If a new base URL is provided, parse it and reconstruct the URL with it
    if new_base_url:
        new_base_parsed = urllib.parse.urlparse(new_base_url)
        new_url = parsed_url._replace(scheme=new_base_parsed.scheme, netloc=new_base_parsed.netloc, path=new_base_parsed.path, query=new_query).geturl()
    else:
        # If no new base URL is provided, use the original base URL
        new_url = parsed_url._replace(query=new_query).geturl()
    
    return new_url

def inject_adds(media_obj, ad_markers, device_context,vod_ad_config,fast_ad_config,common_ad_config):

    platform_re = device_context.get("platform", "mobile")
    platform_app_context = device_context.get("platform", "mobile")
    platform_re = "Connectedtv"
    app_bundle = "tbn_mobile.android"
    print(device_context)

    AD_PARAMS = {
        "site_id" : "2",
        "ua": device_context.get("user_agent", "Mozilla/5.0 (Linux; Android 13"),
        "app_bundle": app_bundle,
        "content_title": media_obj.get("title"), 
        "content_id": media_obj.get("id"), 
        "slot_count": 1,
        "app_name": device_context.get("app_name"),
        "custom_5": "preroll",
        "device_type": platform_re, 
        "player_height": device_context.get("device_height"),
        
        "did": device_context.get("advertisingidentifier"),


        "player_width": device_context.get("device_width"),
        "coppa": 0
    }
    # logger.info("video extension with macros: %s", AD_PARAMS)


    common_ad_config["content_genre"]  = media_obj.get("extensions", {}).get("genre",common_ad_config["content_genre"] )
    common_ad_config["content_rating"]  = media_obj.get("extensions", {}).get("rating",common_ad_config["content_rating"] )


    # may go to dsp config in future 
    #MSM does not have coppa 
    
    if len(ad_markers) > 0:
        markers = ad_markers[0]['markers']
        return_urls=  prepare_video_ad_extention(media_obj, markers, AD_PARAMS.copy())
    else:
        return_urls=  [create_default_ad_extentions(AD_PARAMS.copy())]
    keys_to_delete = ["vod_tag", "base_url"]

    custom_5_counter = 0
    for item in return_urls:

        vod_ad_config_copy = vod_ad_config.copy()
        fast_ad_config_copy = fast_ad_config.copy()
  
        vod_base_url=vod_ad_config.get("base_url", "")
        fast_base_url=fast_ad_config.get("base_url", "")

        if item['offset'] == "preroll":
 
            for key in keys_to_delete:
                if key in vod_ad_config_copy:
                    del vod_ad_config_copy[key]
                    
            merged_dict = {**vod_ad_config_copy, **common_ad_config}

            item['ad_url'] = replace_url_values(item['ad_url'], merged_dict, new_base_url=vod_base_url)

        else:
            
            fast_ad_config_copy["custom_5"] = custom_5_counter + 1 
            if fast_ad_config["fast_tag"] == "yes":
                custom_5_counter = custom_5_counter + 1
                fast_ad_config_copy["custom_5"] = "midroll" + str(custom_5_counter)

                for key in keys_to_delete:
                    if key in fast_ad_config_copy:
                        del fast_ad_config_copy[key]
          
                item['ad_url'] = replace_url_values(item['ad_url'], fast_ad_config_copy, new_base_url=fast_base_url) 

            else:
                custom_5_counter = custom_5_counter + 1
                vod_ad_config_copy["custom_5"] = "midroll"+ str(custom_5_counter)
                for key in keys_to_delete:
                    if key in vod_ad_config_copy:
                        del vod_ad_config_copy[key]
                merged_dict = {**vod_ad_config_copy, **common_ad_config}
                item['ad_url'] = replace_url_values(item['ad_url'], merged_dict, new_base_url=vod_base_url) 

    return return_urls
    

