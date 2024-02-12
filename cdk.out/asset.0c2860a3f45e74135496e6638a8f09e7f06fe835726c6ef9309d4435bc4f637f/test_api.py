import json
from flask import Flask
import handler_playlist as handler_playlist
import handler_media as handler_media
import handler_appconfig as handler_appconfig
import handler_search as handler_search

app = Flask(__name__)


@app.route("/playlist")
def test_playlist():
    event = {}
    event["path"] = "/playlsit"
    event["headers"] = {"CloudFront-Viewer-Country": "US"}
    event["resource"] = "playlist"

    query_parms = {"playlistid": "i7hJzVlz",
                   "page_limit": 50, "page_offset": 1,
                   "related_media_id" : "8NwBhajM",
                   "ctx": "eyJidW5kbGVJZGVudGlmaWVyIjoidGJuX21vYmlsZS5hbmRyb2lkIiwicGxhdGZvcm0iOiJlbiIsImFwcF9uYW1lIjoiVEJOIiwiYWR2ZXJ0aXNpbmdJZGVudGlmaWVyIjoiZWY2MjkyM2QtNGE1Yy00NzA3LWE1ZjUtM2E3MmJiZDFjMGIyIiwidXNlckFnZW50IjoiTW96aWxsYS81LjAgKExpbnV4OyBBbmRyb2lkIDEzOyBQaXhlbCA3IFBybyBCdWlsZC9UUTJBLjIzMDUwNS4wMDI7IHd2KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBWZXJzaW9uLzQuMCBDaHJvbWUvMTE0LjAuNTczNS4xMzEgTW9iaWxlIFNhZmFyaS81MzcuMzYiLCJkZXZpY2VXaWR0aCI6MTA4MCwiZGV2aWNlSGVpZ2h0IjoyMTY5LCJsYW5ndWFnZUNvZGUiOiJnb29nbGVfcGxheSIsInN0b3JlIjoicGhvbmUifQ"}
    event["queryStringParameters"] = query_parms
    res = handler_playlist.lambda_handler(event, {})
    return json.loads(res["body"])


@app.route("/search")
def test_search():
    event = {}
    event["path"] = "/search"
    event["resource"] = "playlist"
    query_parms = {"playlistid": "OdNxMP9n",
                   "search": "Jesus",
                   "feed_title": "Episodes",
                   "page_limit": 50, "page_offset": 1,
                   "ctx": "eyJidW5kbGVJZGVudGlmaWVyIjoidGJuX21vYmlsZS5hbmRyb2lkIiwicGxhdGZvcm0iOiJlbiIsImFwcF9uYW1lIjoiVEJOIiwiYWR2ZXJ0aXNpbmdJZGVudGlmaWVyIjoiZWY2MjkyM2QtNGE1Yy00NzA3LWE1ZjUtM2E3MmJiZDFjMGIyIiwidXNlckFnZW50IjoiTW96aWxsYS81LjAgKExpbnV4OyBBbmRyb2lkIDEzOyBQaXhlbCA3IFBybyBCdWlsZC9UUTJBLjIzMDUwNS4wMDI7IHd2KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBWZXJzaW9uLzQuMCBDaHJvbWUvMTE0LjAuNTczNS4xMzEgTW9iaWxlIFNhZmFyaS81MzcuMzYiLCJkZXZpY2VXaWR0aCI6MTA4MCwiZGV2aWNlSGVpZ2h0IjoyMTY5LCJsYW5ndWFnZUNvZGUiOiJnb29nbGVfcGxheSIsInN0b3JlIjoicGhvbmUifQ"}
    event["queryStringParameters"] = query_parms
    res = handler_search.lambda_handler(event, {})
    return json.loads(res["body"])


@app.route("/media")
def test_media():
    event = {}
    event["path"] = "/media"

    query_parms = {"mediaid": "ON5zQOxu",
                   "ctx": "eyJidW5kbGVJZGVudGlmaWVyIjoidGJuX2ZpcmV0di5hbmRyb2lkIiwicGxhdGZvcm0iOiJhbWF6b25fZmlyZV90diIsImFwcF9uYW1lIjoiVEJOIiwidXNlckFnZW50IjoiTW96aWxsYS81LjAgKExpbnV4OyBBbmRyb2lkIDcuMS4yOyBBRlRNTSBCdWlsZC9OUzY3MDA7IHd2KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBWZXJzaW9uLzQuMCBDaHJvbWUvMTE2LjAuMC4wIE1vYmlsZSBTYWZhcmkvNTM3LjM2IiwiZGV2aWNlSGVpZ2h0IjoxMDgwLCJzdG9yZSI6ImFtYXpvbiIsImRldmljZVR5cGUiOiJ0YWJsZXQiLCJsYW5ndWFnZUNvZGUiOiJlbiIsImRldmljZVdpZHRoIjoxOTIwLCJzZGtfdmVyc2lvbiI6IjkuNS4wIiwidmVyc2lvbl9uYW1lIjoiOC4wLjIifQ"
                   }
    event["queryStringParameters"] = query_parms
    res = handler_media.lambda_handler(event, {})
    return json.loads(res["body"])


@app.route("/appconfig")
def test_app_config():
    event = {"headers":{"CloudFront-Viewer-Country":"US"}}
    event["path"] = "/playlsit"
    query_parms = {"configid": "1noqgj6q",
                   "index": 1, "feed_title": "Episodes"}
    event["queryStringParameters"] = query_parms
    res = handler_appconfig.lambda_handler(event, {})
    return json.loads(res["body"])


if __name__ == "__main__":
    app.run(debug=True)
