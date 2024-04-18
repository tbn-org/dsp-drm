import * as apigw from "aws-cdk-lib/aws-apigateway";
import * as cdk from "aws-cdk-lib";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as secretsManager from "aws-cdk-lib/aws-secretsmanager";

import { Construct } from "constructs";

export interface SecretsStackProps extends cdk.StackProps {
    jwplayerSecretName: string;
}

export class SecretsStack extends cdk.Stack {
    
  public jwplayerSecret: secretsManager.ISecret;
  public dspdrmSecret: secretsManager.ISecret;
  

  constructor(scope: Construct, id: string, props: SecretsStackProps) {
    super(scope, id, props);

    this.jwplayerSecret = secretsManager.Secret.fromSecretNameV2(this, "jwplayerSecret",props.jwplayerSecretName);


  }
}
