import * as cdk from "aws-cdk-lib";

import { ApiStack } from "./common/apigw/dsp-apigw-stack";
import { Construct } from "constructs";
import { DatabaseStack } from "./common/database/dsp-database-stack";
import { LambdaStack } from "./common/lambda/dsp-lambda-stack";
import { SecretsStack } from "./common/secrets/dsp-secrets-stack";

export interface DspInfraStackProps extends cdk.StackProps {
  deployEnv: string;
  baseUrl: string;
  jwplayerSecretName: string;
  dspdrmSecretName: string
  adBreaksTableArn: string;
  jwProperty: string;
  cachingTTL: number;
}

export class DspInfraStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: DspInfraStackProps) {
    super(scope, id, props);

    const deployenv = props.deployEnv;
    const baseUrl = props.baseUrl;
    const JWPLAYER_SECRET_NAME = props.jwplayerSecretName;
    const DSP_DRM_SECRET = props.dspdrmSecretName;

    const adBreaksTableArn = props.adBreaksTableArn;
    const cachingTTL = props.cachingTTL;
    const jwProperty = props.jwProperty;

    const databaseStack = new DatabaseStack(this, `tbn-dsp-drm-databasestack-${deployenv}`, { deployenv: deployenv, adBreaksTableArn: adBreaksTableArn });

    const secretsStack = new SecretsStack(this, `tbn-dsp-secretstack-${deployenv}`, {
      jwplayerSecretName: JWPLAYER_SECRET_NAME,
      dspdrmSecretName: DSP_DRM_SECRET
    });

    


    const lambdaEnvironmentVariables = {
      FEED_LINK_URL: baseUrl,
      JWPLAYER_API_KEY: secretsStack.jwplayerSecret.secretName,
      DSP_DRM_SECRET: secretsStack.dspdrmSecret.secretName,
      AD_MARKERS_TABLE: databaseStack.adBreaksTable.tableName,
      JW_PROPERTY: jwProperty,
      env: deployenv
    };

    const lambdaStack = new LambdaStack(this, `tbn-dsp-drm-stack-${deployenv}`, {
      deployenv: deployenv,
      feedLinkUrl: baseUrl,
      environmentVariables: lambdaEnvironmentVariables,
    });

    databaseStack.addDependency(lambdaStack);

    const apiStack = new ApiStack(this, `tbn-api-drm-stack-${deployenv}`, {
      deployenv: deployenv,
      playlistLambdaFunction: lambdaStack.playlistFunction,
      mediaLambdaFunction: lambdaStack.mediaFunction,
      searchLambdaFunction: lambdaStack.searchFunction,
      appConfigLambdaFunction: lambdaStack.appconfigFunction,
      cachingTTL: cachingTTL,
    });

    // permissions
    // databaseStack.adBreaksTable.grantReadData(lambdaStack.mediaFunction);
    databaseStack.adBreaksTable.grantFullAccess(lambdaStack.mediaFunction);
    secretsStack.jwplayerSecret.grantRead(lambdaStack.mediaFunction);
    secretsStack.dspdrmSecret.grantRead(lambdaStack.mediaFunction);

  }
}
