#!/usr/bin/env node

import * as cdk from "aws-cdk-lib";

import { DspInfraStack } from "../lib/dsp-infra-stack";


const app = new cdk.App();
const JWPLAYER_SECRET_NAME = "tbn-dsp-jwplayer"


new DspInfraStack(app, "dsp-drm-infra-stack-dev", {
  deployEnv: "dev",
  baseUrl: "https://msm-stage-dsp-api.tbnstage.com/v1",
  adBreaksTableArn : "arn:aws:dynamodb:us-west-2:595511454258:table/tbn-dsp-adbreaks",
  // Secrets manager Secret name
  jwplayerSecretName: "tbn-dsp-jwplayer",
  cachingTTL:300,
  jwProperty:"",
  env: {
    account: process.env.CDK_DEPLOY_ACCOUNT || process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEPLOY_REGION || process.env.CDK_DEFAULT_REGION,
  },
});

new DspInfraStack(app, "dsp-drm-infra-stack-stg", {
  deployEnv: "stg",
  baseUrl: "https://msm-stage-dsp-api.tbnstage.com/v1",
  adBreaksTableArn : "arn:aws:dynamodb:us-west-2:690231661505:table/tbn-dsp-adbreaks",
  // Secrets manager Secret name
  jwplayerSecretName: "tbn-dsp-jwplayer",
  cachingTTL:300,
  jwProperty:"",
  env: {
    account: process.env.CDK_DEPLOY_ACCOUNT || process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEPLOY_REGION || process.env.CDK_DEFAULT_REGION,
  },
});


new DspInfraStack(app, "dsp-drm-infra-stack-prod", {
  deployEnv: "prod",
  baseUrl: "https://msm-dsp-api-prod.tbncloud.com/v1",
  adBreaksTableArn: "arn:aws:dynamodb:us-west-2:722984510186:table/tbn-dsp-adbreaks",
  // Secrets manager Secret name
  jwplayerSecretName: "JWP_SECRET",
  cachingTTL:1800,
  jwProperty:"",
  env: {
    account: process.env.CDK_DEPLOY_ACCOUNT || process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEPLOY_REGION || process.env.CDK_DEFAULT_REGION,
  },
});


