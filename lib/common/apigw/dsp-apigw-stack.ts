import * as apigw from "aws-cdk-lib/aws-apigateway";
import * as cdk from "aws-cdk-lib";
import * as lambda from "aws-cdk-lib/aws-lambda";

import { Construct } from "constructs";
import { Stack } from "aws-cdk-lib";

export interface ApiStackProps extends cdk.StackProps {
    deployenv: string;
    playlistLambdaFunction: lambda.Function;
    mediaLambdaFunction: lambda.Function;
    searchLambdaFunction: lambda.Function;
    accountLambdaFunction: lambda.Function;
    appConfigLambdaFunction: lambda.Function;
    cachingTTL: number;
  }
  
  export class ApiStack extends Stack {

    public restApi: apigw.RestApi;
    
    constructor(scope: Construct, id: string, props: ApiStackProps) {
        super(scope, id, props);

        const deployenv = props.deployenv;
        const playlistLambdaFunction= props.playlistLambdaFunction
        const mediaLambdaFunction= props.mediaLambdaFunction;
        const accountLambdaFunction= props.accountLambdaFunction;
        const searchLambdaFunction= props.searchLambdaFunction
        const appConfigLambdaFunction= props.appConfigLambdaFunction;
        const cachingTTL = props.cachingTTL;

        this.restApi = new apigw.RestApi(this, `tbn-adinjector-drm-${deployenv}-api`, {
            restApiName: `tbn-dsp-drm-${deployenv}-api`,
            endpointConfiguration: { types: [apigw.EndpointType.EDGE] },
            deployOptions: {
              cachingEnabled: true,
              cacheTtl: cdk.Duration.seconds(cachingTTL),
              tracingEnabled: true,
              metricsEnabled: true,
              loggingLevel: apigw.MethodLoggingLevel.INFO,
              methodOptions:{
                "/media/GET":{
                  cachingEnabled: false,
                  metricsEnabled: true,
                } ,
                "/account/GET":{
                  cachingEnabled: false,
                  metricsEnabled: true,
                }
              }
            },
          });
      
          const queryParmsValidator = new apigw.RequestValidator(
            this,
            "playlist-params-validator",
            {
              restApi: this.restApi,
              requestValidatorName: "playlist-params-validator",
              validateRequestBody: false,
              validateRequestParameters: true,
            }
          );
      
          const playlistResource = this.restApi.root.addResource("playlist", {
            defaultMethodOptions: {
              requestParameters: {
                "method.request.querystring.playlistid": true,
                "method.request.querystring.page_limit": true,
                "method.request.querystring.page_offset": true,
                "method.request.querystring.related_media_id": false,
                "method.request.querystring.feed_title":false,
                "method.request.querystring.media_filtering":false,
                "method.request.querystring.override_type":false,
                "method.request.querystring.override_feedtype":false,
                "method.request.header.CloudFront-Viewer-Country": false,
      
              },
            },
          });
          addCorsOptions(playlistResource);

      
          const searchResource = this.restApi.root.addResource("search", {
            defaultMethodOptions: {
              requestParameters: {
                "method.request.querystring.playlistid": true,
                "method.request.querystring.page_limit": true,
                "method.request.querystring.page_offset": true,
                "method.request.querystring.search":true,
                "method.request.querystring.feed_title":false,
                "method.request.header.CloudFront-Viewer-Country": false,
      
              },
            },
          });
          addCorsOptions(searchResource);
      
          const configResorce = this.restApi.root.addResource("appconfig", {
            defaultMethodOptions: {
              requestParameters: {
                "method.request.querystring.configid": true,
                "method.request.querystring.index": true,
                "method.request.querystring.page_limit": true,
                "method.request.querystring.page_offset": true,
                "method.request.querystring.feed_title":false,
                "method.request.header.CloudFront-Viewer-Country": false,
              },
            },
          });
          addCorsOptions(configResorce);

      
        // const mediaResource = this.restApi.root.addResource("media");
        // SSAI Changes - Added headers to the mediaResource
          const mediaResource = this.restApi.root.addResource("media", {
            defaultMethodOptions: {
              requestParameters: {
                "method.request.header.CloudFront-Viewer-Latitude": false,
                "method.request.header.CloudFront-Viewer-Longitude": false,                
              },
            },
          });
          addCorsOptions(mediaResource);
          
                
          playlistResource.addMethod(
            "GET",
            new apigw.LambdaIntegration(playlistLambdaFunction, {
              cacheKeyParameters: [
                "method.request.querystring.playlistid",
                "method.request.querystring.page_limit",
                "method.request.querystring.page_offset",
                "method.request.querystring.feed_title",
                "method.request.querystring.override_type",
                "method.request.querystring.override_feedtype",
                "method.request.querystring.media_filtering",
                "method.request.querystring.related_media_id",
                "method.request.header.CloudFront-Viewer-Country",                             
              ],
            }),
            {
              requestValidator: queryParmsValidator,
            }
          );
      
          searchResource.addMethod(
            "GET",
            new apigw.LambdaIntegration(searchLambdaFunction, {
              cacheKeyParameters: [
                "method.request.querystring.playlistid",
                "method.request.querystring.page_limit",
                "method.request.querystring.page_offset",
                "method.request.querystring.search",
                "method.request.querystring.feed_title",
                "method.request.header.CloudFront-Viewer-Country",
              ],
            }),
            {
              requestValidator: queryParmsValidator,
            }
          );

          const accountResource = this.restApi.root.addResource("account", {
            defaultMethodOptions: {
              requestParameters: {
              },
            },
          });
          addCorsOptions(accountResource);

          accountResource.addMethod(
            "GET",
            new apigw.LambdaIntegration(accountLambdaFunction, {

            }),
            {
              requestValidator: queryParmsValidator,
            }
          );


          configResorce.addMethod(
            "GET",
            new apigw.LambdaIntegration(appConfigLambdaFunction, {
              cacheKeyParameters: [
                "method.request.querystring.configid",
                "method.request.querystring.index",
                "method.request.querystring.feed_title",
                "method.request.querystring.page_limit",
                "method.request.querystring.page_offset",
                "method.request.header.CloudFront-Viewer-Country",
              ],
            }),
            {
              requestValidator: queryParmsValidator,
            }
          );
      
          mediaResource.addMethod("GET", new apigw.LambdaIntegration(mediaLambdaFunction));
    }
  }


  export function addCorsOptions(apiResource: apigw.IResource) {
    apiResource.addMethod('OPTIONS', new apigw.MockIntegration({
      integrationResponses: [{
        statusCode: '200',
        responseParameters: {
          'method.response.header.Access-Control-Allow-Headers': "'*'",
          'method.response.header.Access-Control-Allow-Origin': "'*'",
          'method.response.header.Access-Control-Allow-Credentials': "'false'",
          'method.response.header.Access-Control-Allow-Methods': "'*'",
        },
      }],
      passthroughBehavior: apigw.PassthroughBehavior.NEVER,
      requestTemplates: {
        "application/json": "{\"statusCode\": 200}"
      },
    }), {
      methodResponses: [{
        statusCode: '200',
        responseParameters: {
          'method.response.header.Access-Control-Allow-Headers': true,
          'method.response.header.Access-Control-Allow-Methods': true,
          'method.response.header.Access-Control-Allow-Credentials': true,
          'method.response.header.Access-Control-Allow-Origin': true,
        },
      }]
    })
  }