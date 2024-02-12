#!/usr/bin/env bash
# cdk-deploy-to-prod.sh
export AWS_DEFAULT_PROFILE=default
./build.sh
./cdk-destroy-from.sh 595511454258 us-west-2 "$@" 