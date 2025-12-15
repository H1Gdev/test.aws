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
    'level', ['critical', 'error', 'warning', 'info', 'debug', ''], indirect=True
)
def test_logger_level(level, lambda_context, levels):
    print('[Logger level: ' + level + ']')
    levels(level)
    event = {
        'queryStringParameters': {'log': level}
    }
    res = lambda_handler(event, lambda_context)
    assert res.get('statusCode') == 200


@pytest.mark.parametrize(
    'correlation_id', ['correlation_id_value', '', None]
)
def test_correlation_id(correlation_id, lambda_context):
    print('[Correlation ID: ' + str(correlation_id) + ']')
    event = {
        'queryStringParameters': {'log': 'info'},
        'requestContext': {'requestId': correlation_id}
    }
    res = lambda_handler(event, lambda_context)
    assert res.get('statusCode') == 200


def test_parameters(lambda_context):
    print('[Parameters]')
    event = {
        'queryStringParameters': {'ssm': True}
    }
    res = lambda_handler(event, lambda_context)
    assert res.get('statusCode') == 200


@pytest.fixture
def level(request):
    # Indirect parametrize value.
    # https://docs.pytest.org/en/latest/example/parametrize.html#indirect-parametrization
    print(f"[Indirect]{request.param}")
    yield request.param


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
