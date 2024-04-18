# Get playlist

Get playlist feed with geo filtering enabled.

**URL** : `/playlist/`

**Method** : `GET`

**Query Parameters** :

| KEY         | REQUIRED | TYPE    | EXAMPLE VALUE |
| ----------- | -------- | ------- | ------------- |
| playlistid  | Yes      | String  | xIk7G9nu      |
| page_offset | Yes      | INTEGER | 1             |
| page_limit  | Yes      | INTEGER | 50            |
| feed_title  | No       | String  | Episodes      |

**Auth required** : No

**Permissions required** : None

## Success Response

**Code** : `200 OK`

**Content examples**

Playlist retuns all the episodes for the given playlist with the nextpage pointer in the reposnse.

```json
{
  "id": "xIk7G9nu",
  "title": "Featured",
  "type": {
    "value": "feed"
  },
  "entry": [
    {
      "type": {
        "value": "series"
      },
      "title": "My First Trip To Israel with Sheila Walsh",
      "summary": "Join Sheila Walsh in Israel as she brings a new first-time perspective on the land and home of our Savior. With much excitement, she will show you the Jesus of the Bible and see where He walked and ministered. It's the trip of a lifetime!",
      "content": [
        {
          "type": "video/hls"
        }
      ],
      "id": "hOHkrexL",
      "media_group": [
        {
          "type": "image",
          "media_item": [
            {
              "key": "320",
              "src": "https://cdn.jwplayer.com/v2/media/hOHkrexL/poster.jpg?width=320"
            },
            {
              "key": "480",
              "src": "https://cdn.jwplayer.com/v2/media/hOHkrexL/poster.jpg?width=480"
            },
            {
              "key": "640",
              "src": "https://cdn.jwplayer.com/v2/media/hOHkrexL/poster.jpg?width=640"
            },
            {
              "key": "720",
              "src": "https://cdn.jwplayer.com/v2/media/hOHkrexL/poster.jpg?width=720"
            },
            {
              "key": "1280",
              "src": "https://cdn.jwplayer.com/v2/media/hOHkrexL/poster.jpg?width=1280"
            },
            {
              "key": "1920",
              "src": "https://cdn.jwplayer.com/v2/media/hOHkrexL/poster.jpg?width=1920"
            }
          ]
        }
      ],
      "extensions": {
        "feedid": "xIk7G9nu",
        "duration": 0,
        "pubdate": 1687379623,
        "contentType": "series",
        "contentType2": "seriesNoSeason",
        "seriesId": "mxvxLriB",
        "requires_authentication": false,
        "analyticsCustomProperties": {
          "feedId": "xIk7G9nu",
          "network": "",
          "TBNmediaId": ""
        }
      },
      "link": {
        "rel": "self",
        "href": "https://ac-adin-api-prod.tbncloud.com/v1/media?mediaid=hOHkrexL&disablePlayNext=false"
      }
    }
  ]
}
```

Get appconfig feed

**URL** : `/appcofig/`

**Method** : `GET`

**Query Parameters** :

| KEY         | REQUIRED | TYPE    | EXAMPLE VALUE |
| ----------- | -------- | ------- | ------------- |
| configid    | Yes      | String  | 1noqgj6q      |
| index       | Yes      | INTEGER | 1             |
| page_offset | Yes      | INTEGER | 1             |
| page_limit  | Yes      | INTEGER | 50            |

**Auth required** : No

**Permissions required** : None

## Success Response

**Code** : `200 OK`

**Content examples**

Playlist retuns all the episodes for the given playlist with the nextpage pointer in the reposnse.

```json
{
  "id": "xIk7G9nu",
  "title": "Featured",
  "type": {
    "value": "feed"
  },
  "entry": [
    {
      "type": {
        "value": "series"
      },
      "title": "My First Trip To Israel with Sheila Walsh",
      "summary": "Join Sheila Walsh in Israel as she brings a new first-time perspective on the land and home of our Savior. With much excitement, she will show you the Jesus of the Bible and see where He walked and ministered. It's the trip of a lifetime!",
      "content": [
        {
          "type": "video/hls"
        }
      ],
      "id": "hOHkrexL",
      "media_group": [
        {
          "type": "image",
          "media_item": [
            {
              "key": "320",
              "src": "https://cdn.jwplayer.com/v2/media/hOHkrexL/poster.jpg?width=320"
            },
            {
              "key": "480",
              "src": "https://cdn.jwplayer.com/v2/media/hOHkrexL/poster.jpg?width=480"
            },
            {
              "key": "640",
              "src": "https://cdn.jwplayer.com/v2/media/hOHkrexL/poster.jpg?width=640"
            },
            {
              "key": "720",
              "src": "https://cdn.jwplayer.com/v2/media/hOHkrexL/poster.jpg?width=720"
            },
            {
              "key": "1280",
              "src": "https://cdn.jwplayer.com/v2/media/hOHkrexL/poster.jpg?width=1280"
            },
            {
              "key": "1920",
              "src": "https://cdn.jwplayer.com/v2/media/hOHkrexL/poster.jpg?width=1920"
            }
          ]
        }
      ],
      "extensions": {
        "feedid": "xIk7G9nu",
        "duration": 0,
        "pubdate": 1687379623,
        "contentType": "series",
        "contentType2": "seriesNoSeason",
        "seriesId": "mxvxLriB",
        "requires_authentication": false,
        "analyticsCustomProperties": {
          "feedId": "xIk7G9nu",
          "network": "",
          "TBNmediaId": ""
        }
      },
      "link": {
        "rel": "self",
        "href": "https://ac-adin-api-prod.tbncloud.com/v1/media?mediaid=hOHkrexL&disablePlayNext=false"
      }
    }
  ]
}
```

## Notes

Get appconfig feed

**URL** : `/media/`

**Method** : `GET`

**Query Parameters** :

| KEY     | REQUIRED | TYPE   | EXAMPLE VALUE |
| ------- | -------- | ------ | ------------- |
| mediaid | Yes      | String | 1noqgj6q      |

**Auth required** : No

**Permissions required** : None

## Success Response

**Code** : `200 OK`

**Content examples**

media retuns a given mediaid .

```json
{
  "id": "DpkE3yXS",
  "title": "Understanding God's Holiness - Episode 799",
  "type": {
    "value": "feed"
  },
  "entry": [
    {
      "type": {
        "value": "video"
      },
      "title": "Understanding God's Holiness - Episode 799",
      "summary": "Scripture calls us to holiness, but how can we achieve it? Our imperfect human hearts can only become holy by receiving God's grace. He calls us to rest in His presence and allow His love to transform us from the inside out.  |  TBN Prayer Line: 714-731-1000",
      "content": {
        "type": "video/hls",
        "src": "https://cdn.jwplayer.com/manifests/DpkE3yXS.m3u8?exp=3059&sig=5066a7fa4413712ab806dcd011ffc3b6"
      },
      "id": "DpkE3yXS",
      "media_group": [
        {
          "type": "image",
          "media_item": [
            {
              "key": "320",
              "src": "https://cdn.jwplayer.com/v2/media/DpkE3yXS/poster.jpg?width=320"
            },
            {
              "key": "480",
              "src": "https://cdn.jwplayer.com/v2/media/DpkE3yXS/poster.jpg?width=480"
            },
            {
              "key": "640",
              "src": "https://cdn.jwplayer.com/v2/media/DpkE3yXS/poster.jpg?width=640"
            },
            {
              "key": "720",
              "src": "https://cdn.jwplayer.com/v2/media/DpkE3yXS/poster.jpg?width=720"
            },
            {
              "key": "1280",
              "src": "https://cdn.jwplayer.com/v2/media/DpkE3yXS/poster.jpg?width=1280"
            },
            {
              "key": "1920",
              "src": "https://cdn.jwplayer.com/v2/media/DpkE3yXS/poster.jpg?width=1920"
            }
          ]
        }
      ],
      "extensions": {
        "duration": 3059,
        "pubdate": 1688038200,
        "programName": "Better Together",
        "TBNmediaId": "HD-BT23-1184",
        "episodeNumber": "799",
        "seasonNumber": "5",
        "artistandSong": "Sheila Walsh,  Kristi McLelland,  Janice Gaines,  Kirsten Watson,  Blynda Lane,  Turn Your Eyes Upon Jesus",
        "biblicalPeople": "Isaiah, Jairus, Woman with Issue of Blood, Matthew, James, John the Disciple, Peter, Andrew",
        "networks": "TBN",
        "music": "Hymns",
        "prayerFor": "Thanksgiving, Love",
        "requiresSubscription": "true",
        "collectionSortField": "TBN_OriginalAirDate",
        "collectionSortOrder": "1",
        "revShare": "true",
        "rating": "TV-PG",
        "releaseDate": "January 01, 1900",
        "releaseYear": "1900",
        "seasonEpisode": "S5:E799",
        "publishDate": "June 06, 2023",
        "hqme": "true",
        "watchButtonLabel": "Start Watching",
        "video_ads": [
          {
            "offset": "preroll",
            "ad_url": "https://pbs.getpublica.com/v1/s2s-hb?site_id=24600&avod=1&ua=Mozilla%2F5.0+%28Windows+NT+10.&app_bundle=&content_title=__item-title__&content_id=&format=vast&slot_count=1&app_name=tbn.tv&custom_5=preroll&device_type=Connectedtv&player_height=&player_width="
          }
        ],
        "requires_authentication": true
      }
    }
  ]
}
```

## Notes
