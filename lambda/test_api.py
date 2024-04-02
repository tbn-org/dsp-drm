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

    query_parms = {"mediaid": "JLlx6iz4","mediaid_ssai": "OZpATbsP",
                   "ctx": "eyJhcHBfbmFtZSI6IlRCTiIsImJ1bmRsZUlkZW50aWZpZXIiOiJvcmcudGJuLnRibm1vYmlsZSIsImRldmljZUhlaWdodCI6MTA4MCwiZGV2aWNlV2lkdGgiOjE5MjAsImRldmljZVR5cGUiOiJ0diIsImxhbmd1YWdlQ29kZSI6ImVuIiwicGxhdGZvcm0iOiJ0dk9TIiwic2RrX3ZlcnNpb24iOiI4LjAuMiIsInN0b3JlIjoiYXBwbGVfc3RvcmUiLCJ2ZXJzaW9uX25hbWUiOiI5LjEuNjAiLCJxdWljay1icmljay1sb2dpbi1mbG93LnVpZCI6IjAwdTZhNG9xNGdSWkk3TjRENjk3IiwicXVpY2stYnJpY2stbG9naW4tZmxvdy5hY2Nlc3NfdG9rZW4iOiJleUpyYVdRaU9pSm9abXBHV1hOWE5UUkNVVlpsVjNSSU9UZHFVMU55T0RRMFJYaG1ialZYZHpCTVpEbDBVamhRYURSRklpd2lZV3huSWpvaVVsTXlOVFlpZlEuZXlKMlpYSWlPakVzSW1wMGFTSTZJa0ZVTG1KQ09IazNOWHBtZFZWTlUxOXlWbDlwYURsVGFrVkViVGRTYTBwVVdXWTFNMFZ5YVZONWEycHRiV011YjJGeWRYa3dhSHAxVnpSa05tSk5abkEyT1RZaUxDSnBjM01pT2lKb2RIUndjem92TDNObFkzVnlaUzUwWW00dWIzSm5MMjloZFhSb01pOWhkWE5uZEdvNU5HOVZUa1ZCWmtRME5EWTVOaUlzSW1GMVpDSTZJblJpYmlJc0ltbGhkQ0k2TVRjeE1EQXpPVGMwTkN3aVpYaHdJam94TnpFd01USTJNVFEwTENKamFXUWlPaUl3YjJGd01IbzBNbmRSZUc1blEwMUNlVFk1TmlJc0luVnBaQ0k2SWpBd2RUWmhORzl4TkdkU1drazNUalJFTmprM0lpd2ljMk53SWpwYkluQnliMlpwYkdVaUxDSnZabVpzYVc1bFgyRmpZMlZ6Y3lJc0ltOXdaVzVwWkNKZExDSmhkWFJvWDNScGJXVWlPakUyT1RJd01URXhORFFzSW14aGMzUk9ZVzFsSWpvaVVHVmhlU0lzSW1acGNuTjBUbUZ0WlNJNklsTjViSFpwWVNJc0luTjFZaUk2SW5CbFlYa3dOVGcxUUdkdFlXbHNMbU52YlNKOS5mYmdfalhvRF9lcGxZTHYwakFxR1MwV0YyYVljZHJ2ckFVVGtudFlWcnJWSl80bDRUUmEwek9TYkNqR0g5dEg1dU9VekVYRkZCRUFtYUR1THN3M3lVeGx3OTZjVmZyLWNrS003Z0VMOXdmZHdTZW9FbzY4RGRBd1JNNU93dlAtQUpxMmxvdkg1RFBUX0JPZ2l2MEg2WUtnMmtQY0JpWTI2Y0JWVzY0U2RWVXhqQ09KbzY5RF9DZjJHME4xaGNKaFktLXppT1NFWXFLUGJlck1laEp5ZjNJWG1CMXZvcWI0eHdGTFpQQV95OXhxcWhfeWJSdEhwa3JIYzVXbUt6TUFTVlc2NnRsaW1EWERIWnU5bVJXX0VEem9Nb0VwcGIzUTFWdDJmenpuZVZTU3hfVVdRWExjXzdRQmMweVM2Q1duUjJwWjQ1R0QtTmFzcVZ0TW82d3FFVVEiLCJ6YXBwX2xvZ2luX3BsdWdpbl9vYXV0aF90dl8yXzAudWlkIjoiMDB1NmE0b3E0Z1JaSTdONEQ2OTciLCJ6YXBwX2xvZ2luX3BsdWdpbl9vYXV0aF90dl8yXzAuZmlyc3ROYW1lIjoiU3lsdmlhIiwiemFwcF9sb2dpbl9wbHVnaW5fb2F1dGhfdHZfMl8wLmxhc3ROYW1lIjoiUGVheSIsInphcHBfbG9naW5fcGx1Z2luX29hdXRoX3R2XzJfMC5zdWIiOiJwZWF5MDU4NUBnbWFpbC5jb20iLCJxdWljay1icmljay1sb2dpbi1mbG93LmZpcnN0TmFtZSI6IlN5bHZpYSIsInF1aWNrLWJyaWNrLWxvZ2luLWZsb3cubGFzdE5hbWUiOiJQZWF5IiwicXVpY2stYnJpY2stbG9naW4tZmxvdy5zdWIiOiJwZWF5MDU4NUBnbWFpbC5jb20ifQ"
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
