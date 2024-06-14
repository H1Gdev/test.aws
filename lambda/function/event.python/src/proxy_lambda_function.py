import json
from http import HTTPStatus

import boto3
from aws_lambda_powertools import Logger

logger = Logger()


@logger.inject_lambda_context
def lambda_handler(event, context):
    if call_from_api(event):
        logger.info('[Event]call from API Gateway')

    query_string_parameters = event.get('queryStringParameters')
    function_name = query_string_parameters.get('functionName') if query_string_parameters is not None else None

    if function_name is not None:
        query_string_parameters.pop('functionName')
        invocation_type = query_string_parameters.pop('invocationType', 'RequestResponse')
        logger.info(f"[Event]{event}")
        # Proxy Lambda
        # - need boto3
        # - need AWSLambdaRole
        response = boto3.client('lambda').invoke(
            FunctionName=function_name,
            InvocationType=invocation_type,
            Payload=json.dumps(event),
        )
        logger.info(f"[Response]{response}")
        # https://docs.aws.amazon.com/lambda/latest/api/API_Invoke.html#API_Invoke_ResponseElements
        successes = {
            'RequestResponse': HTTPStatus.OK.value,
            'Event': HTTPStatus.ACCEPTED.value,
            'DryRun': HTTPStatus.NO_CONTENT.value,
        }
        if response['StatusCode'] != successes.get(invocation_type, HTTPStatus.OK.value):
            logger.error(f"[Error][StatusCode]{response['StatusCode']}")
        # <class 'botocore.response.StreamingBody'> -read()-> <class 'bytes'> -decode()-> <class 'str'> -json.loads()-> <class 'dict'>
        payload = response.get('Payload').read().decode()
        if payload:
            payload = json.loads(payload)
        logger.info(f"[Payload]{payload}")
        # https://docs.aws.amazon.com/lambda/latest/dg/python-exceptions.html
        if response.get('FunctionError'):
            logger.error(f"[Error][FunctionError]{payload.get('errorMessage')}({payload.get('errorType')})")
        return payload

    # Response
    response = {
        'statusCode': HTTPStatus.OK.value,
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': json.dumps({
            'event': event,
        })
    }
    return response


def call_from_api(event):
    return 'requestId' in event.get('requestContext', {})
