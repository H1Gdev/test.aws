#! /bin/bash

FUNCTION_NAME=Test

aws lambda invoke \
  --function-name $FUNCTION_NAME \
  --payload fileb://payload.json \
  response.json
