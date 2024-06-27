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
                   "ctx": "eyJhcHBfbmFtZSI6Ik1TTSIsImJ1bmRsZUlkZW50aWZpZXIiOiJjb20ubWVyaXRwbHVzLmFwcGxlIiwiZGV2aWNlSGVpZ2h0Ijo4MjAsImRldmljZVdpZHRoIjoxMTgwLCJsYW5ndWFnZUNvZGUiOiJlbiIsInBsYXRmb3JtIjoiaU9TIiwic2RrX3ZlcnNpb24iOiI4LjEuMCIsInN0b3JlIjoiYXBwbGVfc3RvcmUiLCJ1c2VyQWdlbnQiOiJNb3ppbGxhLzUuMCAoaVBhZDsgQ1BVIE9TIDE3XzNfMSBsaWtlIE1hYyBPUyBYKSBBcHBsZVdlYktpdC82MDUuMS4xNSAoS0hUTUwsIGxpa2UgR2Vja28pIE1vYmlsZS8xNUUxNDgiLCJ2ZXJzaW9uX25hbWUiOiIxLjAuMCIsInF1aWNrLWJyaWNrLWxvZ2luLWZsb3cudWlkIjoiMDB1MXBhc2RnMnFxNzBsb2ticDFkOCIsInF1aWNrLWJyaWNrLWxvZ2luLWZsb3cuYWNjZXNzX3Rva2VuIjoiZXlKcmFXUWlPaUphT1d3eFZWWnVXWEJvZVZCT1ltRm1RbEp3Y0ZrMVJuWkRhRkIxV0doQmNtbFBia1JMWDNKa2NGTkpJaXdpWVd4bklqb2lVbE15TlRZaWZRLmV5SjJaWElpT2pFc0ltcDBhU0k2SWtGVUxrMW1ibkZsTkZGVFNTMXVObEJ5YjBacVNVWk9SbXRHUVhSa1VVNHRkMmgxWHpOdlozVTVZVXBvZGxVdWIyRnliM00xTVd3d1pVSnhjMDlrWWpreFpEWWlMQ0pwYzNNaU9pSm9kSFJ3Y3pvdkwzTmxZM1Z5WlM1dFpYSnBkSE4wY21WbGRHMWxaR2xoTG1OdmJTOXZZWFYwYURJdlpHVm1ZWFZzZENJc0ltRjFaQ0k2SW0xemJTSXNJbWxoZENJNk1UY3hNakl6TnpZek1Dd2laWGh3SWpveE56RXlNekkwTURNd0xDSmphV1FpT2lJd2IyRXhiM2xtYW5GamRsZHVRbkk0YXpGa09DSXNJblZwWkNJNklqQXdkVEZ3YUdjeWNYRTNNR3h2YTJKd01XUTRJaXdpYzJOd0lqcGJJbTltWm14cGJtVmZZV05qWlhOeklpd2liM0JsYm1sa0lsMHNJbUYxZEdoZmRHbHRaU0k2TVRjeE1qSXpOell6TUN3aWMzVmlJam9pWkhkdmJtVnBiRFU0UUdkdFlXbHNMbU52YlNJc0ltWnBjbk4wVG1GdFpTSTZJa1JwWVc1bElpd2liR0Z6ZEU1aGJXVWlPaUpQNG9DWlRtVnBiQ0o5LkZjSXVJZjNad2RvY1N0U0xud2NpRkRQYy1GNFQzNXNuNU1lOW82ZkxKOTJSR1QxMnJ1QzNiQXMzU0NGdXJXZFhfOHFpM1JfV0lzNllaVjQzYmdYU0tLbnlUWko1Z1czLXV6WGoyQm03SkdzN2pING55YTVwNmVTOGZxNmFkVXoycEZoSzRFWkp4R3ZtQUZndGpSSGcxTmhYSS1pa0RSOERZRWpQRVRvekI4dVM0VGtreXRZeHk5SmI4cFM5TENFaUZXR2tURmFLNGFEbGdWc0NhcGdHbGFMLXlwMnRLbnRUR3VJbUdDY2J1Vjd4QlZpQlJDZWlLTlh2SXhPVFI3Si1uZW9maUNyTjdwUVczbTdkeW9mNHNWeVhxd3pya1NhVHQ0MFRVbllLQk1vTjJNLVdJZ0l6b2Fpb08wYVFDYzBqOHY3UHE1cFVOekFNX3RfNHlSdUZMdyIsInF1aWNrLWJyaWNrLWxvZ2luLWZsb3cubGFzdE5hbWUiOiJP4oCZTmVpbCIsInF1aWNrLWJyaWNrLWxvZ2luLWZsb3cuZmlyc3ROYW1lIjoiRGlhbmUiLCJxdWljay1icmljay1sb2dpbi1mbG93LnN1YiI6ImR3b25laWw1OEBnbWFpbC5jb20iLCJ0aW1lWm9uZU9mZnNldCI6IlVUQy0wNDowMCIsImFsZyI6IkhTMjU2In0.e30.679dxqa5FNU7ITPM4DZlyvjQh-v534YQjMMDHZ_PH6M"
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
