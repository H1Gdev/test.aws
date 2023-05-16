import json
from http import HTTPStatus

from aws_lambda_powertools import Logger

logger = Logger()


@logger.inject_lambda_context
def lambda_handler(event, context):
    # Logger
    query_string_parameters = event.get('queryStringParameters')
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
        print('[print]', event)

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
