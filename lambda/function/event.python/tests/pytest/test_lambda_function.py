# [pytest](https://docs.pytest.org/)
import pytest

from src.lambda_function import lambda_handler


def test_handler(lambda_context):
    print('[Get]')
    event = {}
    context = lambda_context
    print('[Event]', event)
    print('[Context]', context)
    res = lambda_handler(event, context)
    print('[Response]', res)
    assert res.get('statusCode') == 200


def test_user(lambda_context):
    print('[User]')
    event = {
        'queryStringParameters': {'user': True}
    }
    res = lambda_handler(event, lambda_context)
    assert res.get('statusCode') == 200


@pytest.mark.parametrize(
    'level', ['critical', 'error', 'warning', 'info', 'debug', '']
)
def test_logger_level(level, lambda_context, levels):
    print('[Logger level: ' + level + ']')
    levels(level)
    event = {
        'queryStringParameters': {'log': level}
    }
    res = lambda_handler(event, lambda_context)
    assert res.get('statusCode') == 200


@pytest.fixture(scope='module')
def levels():
    # Setup
    # - if exception occurs during Setup, Teardown will not be executed.
    levels = []

    def _levels(level):
        levels.append(level)

    yield _levels

    # Teardown
    print(f"Tested log levels are {','.join(levels)}.")
