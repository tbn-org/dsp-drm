import * as apigw from "aws-cdk-lib/aws-apigateway";
import * as cdk from "aws-cdk-lib";
import * as dynamodb from "aws-cdk-lib/aws-dynamodb";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as iam from "aws-cdk-lib/aws-iam";

import { Construct } from "constructs";

export interface DatabaseStackProps extends cdk.StackProps {
  deployenv: string;
  adBreaksTableArn: string;
}

export class DatabaseStack extends cdk.Stack {
  public adBreaksTable: dynamodb.ITable;

  constructor(scope: Construct, id: string, props: DatabaseStackProps) {
    super(scope, id, props);

    const deployenv = props.deployenv;

    // this.adBreaksTable = new dynamodb.Table(
    //   this,
    //   `tbn-adinjector-${deployenv}-table`,
    //   {
    //     tableName: `tbn-adinjector-${deployenv}-table`,
    //     partitionKey: { name: "mediaid", type: dynamodb.AttributeType.STRING },
    //     billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
    //   }
    // );
    // this.adBreaksTable.applyRemovalPolicy(cdk.RemovalPolicy.DESTROY);

    this.adBreaksTable = dynamodb.Table.fromTableArn(this, `tbn-adinjector-${deployenv}-table`, props.adBreaksTableArn);
  }
}
