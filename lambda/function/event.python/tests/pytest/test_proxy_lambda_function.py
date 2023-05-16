from src.proxy_lambda_function import lambda_handler

# Mock
# - moto[awslambda]
# - https://pypi.org/project/moto/
# - https://github.com/getmoto/moto
# - Docker is required to execute.


def test_handler(lambda_context, boto_mocker):
    boto_mocker.patch(new=boto_mocker.build_make_api_call({
        'lambda': {
            'Invoke': boto_mocker.build_lambda_invoke_handler({
                'testLambdaFunction': {
                    'StatusCode': 200,
                    'Payload': {
                        'statusCode': 200,
                        'body': ''
                    }
                },
                'errorLambdaFunction': {
                    'StatusCode': 200,
                    'FunctionError': 'Unhandled',
                    'Payload': Exception('error message')
                },
            }),
        },
        's3': {
            'HeadObject': {'ResponseMetadata': {'HTTPStatusCode': 200}},
        },
    }))

    event = {
        'queryStringParameters': {
            'functionName': 'testLambdaFunction'
        }
    }
    context = lambda_context
    print('[Event]', event)
    print('[Context]', context)
    res = lambda_handler(event, context)
    print('[Response]', res)
    assert res.get('statusCode') == 200


def test_pass_through(lambda_context):
    event = {
        'queryStringParameters': {
            'functionName': None
        }
    }
    context = lambda_context
    print('[Event]', event)
    print('[Context]', context)
    res = lambda_handler(event, context)
    print('[Response]', res)
    assert res.get('statusCode') == 200


def test_mocker_0(lambda_context, boto_mocker, mocker):
    boto_mocker.patch(new=boto_mocker.build_make_api_call({
        'lambda': {
            'Invoke': boto_mocker.build_lambda_invoke_handler({
                'testLambdaFunction': {
                    'StatusCode': 200,
                    'Payload': {'statusCode': 200, 'body': ''}
                },
            }),
        },
    }))

    # [return_value]
    # returns MagicMock.
    mocker.patch('src.proxy_lambda_function.call_from_api', return_value=True)

    event = {
        'queryStringParameters': {
            'functionName': 'testLambdaFunction'
        }
    }
    context = lambda_context
    print('[Event]', event)
    print('[Context]', context)
    res = lambda_handler(event, context)
    print('[Response]', res)
    assert res.get('statusCode') == 200


def test_mocker_1(lambda_context, boto_mocker, mocker):
    boto_mocker.patch(new=boto_mocker.build_make_api_call({
        'lambda': {
            'Invoke': boto_mocker.build_lambda_invoke_handler({
                'testLambdaFunction': {
                    'StatusCode': 200,
                    'Payload': {'statusCode': 200, 'body': ''}
                },
            }),
        },
    }))

    def _call_from_api(event):
        # if method, cannot receive self.
        return True

    # [side_effect]
    # - value
    # - iterable
    # - function
    # - lambda
    # - Exception
    # returns MagicMock.
    mocker.patch('src.proxy_lambda_function.call_from_api', side_effect=_call_from_api)

    event = {
        'queryStringParameters': {
            'functionName': 'testLambdaFunction'
        }
    }
    context = lambda_context
    print('[Event]', event)
    print('[Context]', context)
    res = lambda_handler(event, context)
    print('[Response]', res)
    assert res.get('statusCode') == 200


def test_mocker_2(lambda_context, boto_mocker, mocker):
    boto_mocker.patch(new=boto_mocker.build_make_api_call({
        'lambda': {
            'Invoke': boto_mocker.build_lambda_invoke_handler({
                'testLambdaFunction': {
                    'StatusCode': 200,
                    'Payload': {'statusCode': 200, 'body': ''}
                },
            }),
        },
    }))

    def _call_from_api(event):
        return True

    # [new]
    # - class
    # - function
    # - lambda
    # returns new argument object.
    mocker.patch('src.proxy_lambda_function.call_from_api', new=_call_from_api)

    event = {
        'queryStringParameters': {
            'functionName': 'testLambdaFunction'
        }
    }
    context = lambda_context
    print('[Event]', event)
    print('[Context]', context)
    res = lambda_handler(event, context)
    print('[Response]', res)
    assert res.get('statusCode') == 200
