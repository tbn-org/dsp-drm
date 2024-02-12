#!/usr/bin/env bash
# cdk-deploy-to-prod.sh
export AWS_DEFAULT_PROFILE=tbnprod
export DEPLOY_ENV=prod
#./build.sh
./cdk-deploy-to.sh 722984510186 us-west-2 "$@" 
