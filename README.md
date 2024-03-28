# DSP to serve feeds for applicaster

The MSM API provides the folowing APIS

1. playlist
2. Media
3. appconfig
4. Account
5. Search


# Building a deploying using cdk

The project is CDK enabled and have custom bash commands to deploy

DEV environment :

https://tbn-dsp-api-dev.tbnsandbox.com/v1/playlist/?playlistid=KlFlsAns&page_offset=1&page_limit=100
https://tbn-dsp-api-dev.tbnsandbox.com/v1/appconfig?configid=1noqgj6q&index=0&page_offset=1&page_limit=1
https://tbn-dsp-api-dev.tbnsandbox.com/v1/search?playlistid=h0lwa1JX&page_limit=50&page_offset=1&search=jesus
https://tbn-dsp-api-dev.tbnsandbox.com/v1/media?mediaid=DpkE3yXS&disablePlayNext=false


STG environment:

https://msm-stage-dsp-api.tbnstage.com/v1/playlist?playlistid=i7hJzVlz&related_media_id=8NwBhajM&page_offset=1&page_limit=20

https://msm-stage-dsp-api.tbnstage.com/v1/search?playlistid=h0lwa1JX&=Episodes&page_limit=50&page_offset=1&search=jesus


https://msm-stage-dsp-api.tbnstage.com/v1/appconfig?configid=1noqgj6q&index=0&page_offset=1&page_limit=48&ctx=eyJhZHZlcnRpc2luZ0lkZW50aWZpZXIiOiJENjBBQzc4NS1CMzAzLTRGNUUtODhGNy1CQzVCMDdBQUZCMkQiLCJhcHBfbmFtZSI6IlRCTiIsImJ1bmRsZUlkZW50aWZpZXIiOiJvcmcudGJuLnRibm1vYmlsZSIsImRldmljZUhlaWdodCI6ODUyLCJkZXZpY2VUeXBlIjoicGhvbmUiLCJkZXZpY2VXaWR0aCI6MzkzLCJsYW5ndWFnZUNvZGUiOiJlbiIsInBsYXRmb3JtIjoiaU9TIiwic2RrX3ZlcnNpb24iOiI3LjAuMCIsInN0b3JlIjoiYXBwbGVfc3RvcmUiLCJ1c2VyQWdlbnQiOiJNb3ppbGxhLzUuMCAoaVBob25lOyBDUFUgaVBob25lIE9TIDE2XzFfMiBsaWtlIE1hYyBPUyBYKSBBcHBsZVdlYktpdC82MDUuMS4xNSAoS0hUTUwsIGxpa2UgR2Vja28pIE1vYmlsZS8xNUUxNDgiLCJ2ZXJzaW9uX25hbWUiOiI4LjEuNiIsInphcHBfbG9naW5fcGx1Z2luX29hdXRoXzJfMC51aWQiOiIwMHVqc3ZwcnQwY29PRGJRcTY5NiIsInF1aWNrLWJyaWNrLWxvZ2luLWZsb3cudWlkIjoiMDB1anN2cHJ0MGNvT0RiUXE2OTYifQ

https://msm-stage-dsp-api.tbnstage.com/v1/media?mediaid=nSbxxg0p&override_type=link&ctx=eyJhZHZlcnRpc2luZ0lkZW50aWZpZXIiOiJENjBBQzc4NS1CMzAzLTRGNUUtODhGNy1CQzVCMDdBQUZCMkQiLCJhcHBfbmFtZSI6IlRCTiIsImJ1bmRsZUlkZW50aWZpZXIiOiJvcmcudGJuLnRibm1vYmlsZSIsImRldmljZUhlaWdodCI6ODUyLCJkZXZpY2VUeXBlIjoicGhvbmUiLCJkZXZpY2VXaWR0aCI6MzkzLCJsYW5ndWFnZUNvZGUiOiJlbiIsInBsYXRmb3JtIjoiaU9TIiwic2RrX3ZlcnNpb24iOiI3LjAuMCIsInN0b3JlIjoiYXBwbGVfc3RvcmUiLCJ1c2VyQWdlbnQiOiJNb3ppbGxhLzUuMCAoaVBob25lOyBDUFUgaVBob25lIE9TIDE2XzFfMiBsaWtlIE1hYyBPUyBYKSBBcHBsZVdlYktpdC82MDUuMS4xNSAoS0hUTUwsIGxpa2UgR2Vja28pIE1vYmlsZS8xNUUxNDgiLCJ2ZXJzaW9uX25hbWUiOiI4LjEuNiIsInphcHBfbG9naW5fcGx1Z2luX29hdXRoXzJfMC51aWQiOiIwMHVqc3ZwcnQwY29PRGJRcTY5NiIsInF1aWNrLWJyaWNrLWxvZ2luLWZsb3cudWlkIjoiMDB1anN2cHJ0MGNvT0RiUXE2OTYifQ



PROD environment URLS:

https://tbn-dsp-api-prod.tbncloud.com/v1/playlist?playlistid=KlFlsAns&page_limit=40&page_offset=1
https://tbn-dsp-api-prod.tbncloud.com/v1/appconfig?configid=1noqgj6q&index=0&page_offset=1&page_limit=1
https://tbn-dsp-api-prod.tbncloud.com/v1/search?playlistid=h0lwa1JX&=Episodes&page_limit=50&page_offset=1&search=jesus
https://tbn-dsp-api-prod.tbncloud.com/v1/media?mediaid=DpkE3yXS&disablePlayNext=false

## deployed commands

- `./cdk-deploy-to-dev` deploy to dev
- `./cdk-deploy-to-prod` deploy to dev

" "

# API DOCS :

![Alt text](docs/DSP2.0.png)

https://tbntv.atlassian.net/wiki/spaces/Meritplus/pages/107675667/Production+Apps
