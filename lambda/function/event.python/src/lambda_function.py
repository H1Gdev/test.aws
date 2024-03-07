import json
import os
import threading
from http import HTTPStatus

import boto3
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities import parameters

logger = Logger()
tracer = Tracer()


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    query_string_parameters = event.get('queryStringParameters')

    # User
    user = query_string_parameters.get('user') if query_string_parameters is not None else None
    if user is not None:
        response = boto3.client('sts').get_caller_identity()
        # AWS_PROFILE > AWS_DEFAULT_PROFILE > 'default'
        logger.info(f"[User]{response.get('Arn')}")

    # Logger
    log = query_string_parameters.get('log') if query_string_parameters is not None else None
    if log == 'critical':
        logger.critical(f"[CRITICAL]{event}")
        logger.error(f"[ERROR]{event}")
        logger.warning(f"[WARN]{event}")
        logger.info(f"[INFO]{event}")
        logger.debug(f"[DEBUG]{event}")
    elif log == 'error':
        logger.error(f"[ERROR]{event}")
        logger.warning(f"[WARN]{event}")
        logger.info(f"[INFO]{event}")
        logger.debug(f"[DEBUG]{event}")
    elif log == 'warning':
        logger.warning(f"[WARN]{event}")
        logger.info(f"[INFO]{event}")
        logger.debug(f"[DEBUG]{event}")
    elif log == 'info':
        logger.info(f"[INFO]{event}")
        logger.debug(f"[DEBUG]{event}")
    elif log == 'debug':
        logger.debug(f"[DEBUG]{event}")
    else:
        print(f"[print]({os.getpid()},{threading.get_ident()})", event)

    # Parameters
    ssm = query_string_parameters.get('ssm') if query_string_parameters is not None else None
    if ssm is not None:
        value = parameters.get_parameter('/my/parameter')
        logger.info(f"[Parameters]{value}")

    # Response
    response = {
        'statusCode': HTTPStatus.OK.value,
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': json.dumps({
            'event': event,
            'context': str(context),
        })
    }
    return response
