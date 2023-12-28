import asyncio
import json
import time
from http import HTTPStatus

from aws_lambda_powertools import Logger

logger = Logger()


async def async_function(delay, what):
    logger.info(f"[Async][S]{what}")
    # must do await inside this async function.
    await asyncio.sleep(delay)
    logger.info(f"[Async][E]{what}")
    return what


def sync_function(delay, what):
    logger.info(f"[Sync][S]{what}")
    time.sleep(delay)
    logger.info(f"[Sync][E]{what}")
    return what


async def async_handler(event, context):
    # call async function.
    f0 = async_function(10, 'async')

    # call function as async.
    loop = asyncio.get_event_loop()
    f1 = loop.run_in_executor(None, sync_function, 5, 'sync')
    # if use boto3 client, create it in main thread.
    # f1 = loop.run_in_executor(None, sync_function, boto3.client('lambda'))

    result0, result1 = await asyncio.gather(f0, f1)
    logger.info(f"[Async]{result0}")
    logger.info(f"[Sync]{result1}")

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


@logger.inject_lambda_context
def lambda_handler(event, context):
    loop = asyncio.get_event_loop()
    try:
        return loop.run_until_complete(async_handler(event, context))
    finally:
        loop.close()
