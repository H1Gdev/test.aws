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
    c0 = async_function(5, 'async')

    # call function as async.
    c1 = asyncio.to_thread(sync_function, 10, 'sync')
    # if use boto3 client, create it in main thread.
    # c1 = asyncio.to_thread(sync_function, boto3.client('lambda'))

    # awaitable
    # - Coroutine
    # - Task
    # - Future
    result0, result1 = await asyncio.gather(c0, c1)
    # awaitables is List.
    # result0, result1 = await asyncio.gather(*aws)
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
    return asyncio.run(async_handler(event, context))
