#!/usr/bin/env bash
# cdk-deploy-to-prod.sh
export AWS_DEFAULT_PROFILE=tbn-prod
./build.sh
./cdk-destroy-from.sh 722984510186 us-west-2 "$@" 