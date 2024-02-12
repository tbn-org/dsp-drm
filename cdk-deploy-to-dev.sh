#!/usr/bin/env bash
# cdk-deploy-to-prod.sh
export AWS_DEFAULT_PROFILE=tbndev
export DEPLOY_ENV=dev
# ./build.sh
./cdk-deploy-to.sh 595511454258 us-west-2 "$@" 