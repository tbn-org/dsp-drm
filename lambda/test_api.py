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

    query_parms = {"playlistid": "UgU5yi03",
                   "page_limit": 100, "page_offset": 1,
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

    query_parms = {"mediaid": "jVXwMqFH","mediaid_ssai": "OZpATbsP",
                   "ctx": "eyJhcHBfbmFtZSI6Ik1TTSIsImJ1bmRsZUlkZW50aWZpZXIiOiJjb20ubWVyaXRwbHVzLmFwcGxlIiwiZGV2aWNlSGVpZ2h0Ijo4MjAsImRldmljZVdpZHRoIjoxMTgwLCJsYW5ndWFnZUNvZGUiOiJlbiIsInBsYXRmb3JtIjoiaU9TIiwic2RrX3ZlcnNpb24iOiI4LjEuMCIsInN0b3JlIjoiYXBwbGVfc3RvcmUiLCJ1c2VyQWdlbnQiOiJNb3ppbGxhLzUuMCAoaVBhZDsgQ1BVIE9TIDE3XzNfMSBsaWtlIE1hYyBPUyBYKSBBcHBsZVdlYktpdC82MDUuMS4xNSAoS0hUTUwsIGxpa2UgR2Vja28pIE1vYmlsZS8xNUUxNDgiLCJ2ZXJzaW9uX25hbWUiOiIxLjAuMCIsInF1aWNrLWJyaWNrLWxvZ2luLWZsb3cudWlkIjoiMDB1MXBoZzJxcTcwbG9rYnAxZDgiLCJxdWljay1icmljay1sb2dpbi1mbG93LmFjY2Vzc190b2tlbiI6ImV5SnJhV1FpT2lKYU9Xd3hWVlp1V1hCb2VWQk9ZbUZtUWxKd2NGazFSblpEYUZCMVdHaEJjbWxQYmtSTFgzSmtjRk5KSWl3aVlXeG5Jam9pVWxNeU5UWWlmUS5leUoyWlhJaU9qRXNJbXAwYVNJNklrRlVMazFtYm5GbE5GRlRTUzF1TmxCeWIwWnFTVVpPUm10R1FYUmtVVTR0ZDJoMVh6TnZaM1U1WVVwb2RsVXViMkZ5YjNNMU1Xd3daVUp4YzA5a1lqa3haRFlpTENKcGMzTWlPaUpvZEhSd2N6b3ZMM05sWTNWeVpTNXRaWEpwZEhOMGNtVmxkRzFsWkdsaExtTnZiUzl2WVhWMGFESXZaR1ZtWVhWc2RDSXNJbUYxWkNJNkltMXpiU0lzSW1saGRDSTZNVGN4TWpJek56WXpNQ3dpWlhod0lqb3hOekV5TXpJME1ETXdMQ0pqYVdRaU9pSXdiMkV4YjNsbWFuRmpkbGR1UW5JNGF6RmtPQ0lzSW5WcFpDSTZJakF3ZFRGd2FHY3ljWEUzTUd4dmEySndNV1E0SWl3aWMyTndJanBiSW05bVpteHBibVZmWVdOalpYTnpJaXdpYjNCbGJtbGtJbDBzSW1GMWRHaGZkR2x0WlNJNk1UY3hNakl6TnpZek1Dd2ljM1ZpSWpvaVpIZHZibVZwYkRVNFFHZHRZV2xzTG1OdmJTSXNJbVpwY25OMFRtRnRaU0k2SWtScFlXNWxJaXdpYkdGemRFNWhiV1VpT2lKUDRvQ1pUbVZwYkNKOS5GY0l1SWYzWndkb2NTdFNMbndjaUZEUGMtRjRUMzVzbjVNZTlvNmZMSjkyUkdUMTJydUMzYkFzM1NDRnVyV2RYXzhxaTNSX1dJczZZWlY0M2JnWFNLS255VFpKNWdXMy11elhqMkJtN0pHczdqSDRueWE1cDZlUzhmcTZhZFV6MnBGaEs0RVpKeEd2bUFGZ3RqUkhnMU5oWEktaWtEUjhEWUVqUEVUb3pCOHVTNFRra3l0WXh5OUpiOHBTOUxDRWlGV0drVEZhSzRhRGxnVnNDYXBnR2xhTC15cDJ0S250VEd1SW1HQ2NidVY3eEJWaUJSQ2VpS05Ydkl4T1RSN0otbmVvZmlDck43cFFXM203ZHlvZjRzVnlYcXd6cmtTYVR0NDBUVW5ZS0JNb04yTS1XSWdJem9haW9PMGFRQ2Mwajh2N1BxNXBVTnpBTV90XzR5UnVGTHciLCJxdWljay1icmljay1sb2dpbi1mbG93Lmxhc3ROYW1lIjoiT-KAmU5laWwiLCJxdWljay1icmljay1sb2dpbi1mbG93LmZpcnN0TmFtZSI6IkRpYW5lIiwicXVpY2stYnJpY2stbG9naW4tZmxvdy5zdWIiOiJkd29uZWlsNThAZ21haWwuY29tIiwidGltZVpvbmVPZmZzZXQiOiJVVEMtMDQ6MDAifQ"
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
    app.run(debug=True, port=5000)
