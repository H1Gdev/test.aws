from src.async_lambda_function import lambda_handler


def test_handler(lambda_context):
    event = {}
    context = lambda_context
    print('[Event]', event)
    print('[Context]', context)
    res = lambda_handler(event, context)
    print('[Response]', res)
    assert res.get('statusCode') == 200
