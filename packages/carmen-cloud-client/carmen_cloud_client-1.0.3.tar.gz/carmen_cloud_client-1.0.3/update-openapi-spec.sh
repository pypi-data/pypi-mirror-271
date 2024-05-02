#!/usr/bin/env bash

aws apigateway get-model --rest-api-id jw68bdy2t5 --model-name Response | jq --raw-output '.schema' > ./assets/vehicle/response.schema.json
aws apigateway get-model --rest-api-id 2bzr9vm131 --model-name Response | jq --raw-output '.schema' > ./assets/transport/response.schema.json
