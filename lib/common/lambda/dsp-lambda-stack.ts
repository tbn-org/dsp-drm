import * as cdk from "aws-cdk-lib";
import * as dynamodb from "aws-cdk-lib/aws-dynamodb";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as iam from "aws-cdk-lib/aws-iam";
import * as s3 from "aws-cdk-lib/aws-s3";
import { Construct } from "constructs";
import { Stack } from "aws-cdk-lib";

import path = require("path");

export interface LambdaStackProps extends cdk.StackProps {
  deployenv: string;
  feedLinkUrl: string;
  environmentVariables: { [key: string]: string };
}

export class LambdaStack extends Stack {
  public playlistFunction: lambda.Function;
  public mediaFunction: lambda.Function;
  public searchFunction: lambda.Function;
  public appconfigFunction: lambda.Function;
  public accountFunction: lambda.Function;

  

  constructor(scope: Construct, id: string, props: LambdaStackProps) {
    super(scope, id, props);

    const deployenv = props.deployenv;
    const environmentVariables = props.environmentVariables;

    this.playlistFunction = new lambda.Function(this, `tbn-dsp-drm-playlist-${deployenv}-function`, {
      functionName: `tbn-dsp-drm-playlist-${deployenv}-function`,
      description: "lambda function to handler /playlist dsp endpoint.",
      runtime: lambda.Runtime.PYTHON_3_9, // execution environment
      timeout: cdk.Duration.seconds(60),
      code: lambda.Code.fromAsset(path.join(__dirname, "../../../lambda/"), {
        bundling: {
          image: lambda.Runtime.PYTHON_3_9.bundlingImage,
          command: ["bash", "-c", "pip install -r requirements.txt -t /asset-output && cp -au . /asset-output"],
        },
      }),
      handler: "handler_playlist.lambda_handler", // file is "hello", function is "handler"
      environment: environmentVariables,
    });

    this.mediaFunction = new lambda.Function(this, `tbn-dsp-drm-media-${deployenv}-function`, {
      functionName: `tbn-dsp-drm-media-${deployenv}-function`,
      description: ` lambda function to handler /media dsp endpoint`,
      runtime: lambda.Runtime.PYTHON_3_9, // execution environment
      timeout: cdk.Duration.seconds(60),
      code: lambda.Code.fromAsset(path.join(__dirname, "../../../lambda/"), {
        bundling: {
          image: lambda.Runtime.PYTHON_3_9.bundlingImage,
          command: ["bash", "-c", "pip install -r requirements.txt -t /asset-output && cp -au . /asset-output"],
        },
      }),
      handler: "handler_media.lambda_handler",
      environment: environmentVariables,
    });


    this.accountFunction = new lambda.Function(this, `tbn-dsp-drm-account-${deployenv}-function`, {
      functionName: `tbn-dsp-drm-account-${deployenv}-function`,
      description: "lambda function to handler /account dsp endpoint.",
      runtime: lambda.Runtime.PYTHON_3_9, // execution environment
      timeout: cdk.Duration.seconds(60),
      code: lambda.Code.fromAsset(path.join(__dirname, "../../../lambda/"), {
        bundling: {
          image: lambda.Runtime.PYTHON_3_9.bundlingImage,
          command: ["bash", "-c", "pip install -r requirements.txt -t /asset-output && cp -au . /asset-output"],
        },
      }),
      handler: "handler_account.lambda_handler", // file is "hello", function is "handler"
      environment: environmentVariables,
    });



    this.appconfigFunction = new lambda.Function(this, `tbn-dsp-drm-appconfig-${deployenv}-function`, {
      functionName: `tbn-dsp-drm-appconfig-${deployenv}-function`,
      description: "lambda function to handler /appconfig dsp endpoint.",
      runtime: lambda.Runtime.PYTHON_3_9, // execution environment
      timeout: cdk.Duration.seconds(60),
      code: lambda.Code.fromAsset(path.join(__dirname, "../../../lambda/"), {
        bundling: {
          image: lambda.Runtime.PYTHON_3_9.bundlingImage,
          command: ["bash", "-c", "pip install -r requirements.txt -t /asset-output && cp -au . /asset-output"],
        },
      }),
      handler: "handler_appconfig.lambda_handler",
      environment: environmentVariables,
    });

    this.searchFunction = new lambda.Function(this, `tbn-dsp-drm-search-${deployenv}-function`, {
      functionName: `tbn-dsp-drm-search-${deployenv}-function`,
      description: "lambda function to handler /search dsp endpoint.",
      runtime: lambda.Runtime.PYTHON_3_9, // execution environment
      timeout: cdk.Duration.seconds(60),
      code: lambda.Code.fromAsset(path.join(__dirname, "../../../lambda/"), {
        bundling: {
          image: lambda.Runtime.PYTHON_3_9.bundlingImage,
          command: ["bash", "-c", "pip install -r requirements.txt -t /asset-output && cp -au . /asset-output"],
        },
      }),
      handler: "handler_search.lambda_handler",
      environment: environmentVariables,
    });
  }
}
