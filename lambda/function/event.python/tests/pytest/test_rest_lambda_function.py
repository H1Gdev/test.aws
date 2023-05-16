import json

from src.rest_lambda_function import lambda_handler


def test_get_users(lambda_context):
    print('[Get]')
    event = {
        'httpMethod': 'GET',
        'path': '/users',
    }
    res = lambda_handler(event, lambda_context)
    print('[Response]', res)
    assert res.get('statusCode') == 200


def test_get_user(lambda_context):
    print('[Get]')
    user_id = 'aaaaaaaa-test-test-test-teeeeeeeeest'
    event = {
        'httpMethod': 'GET',
        'path': '/users/' + user_id,
        'pathParameters': {
            'userId': user_id
        },
    }
    res = lambda_handler(event, lambda_context)
    print('[Response]', res)
    assert res.get('statusCode') == 200


def test_post_user(lambda_context):
    print('[Post]')
    event = {
        'httpMethod': 'POST',
        'path': '/users',
        'body': json.dumps({
            'name': 'Mr. REST'
        }),
    }
    res = lambda_handler(event, lambda_context)
    print('[Response]', res)
    assert res.get('statusCode') == 201


def test_post_user_like_api(lambda_context):
    print('[Post](API)')
    event = {
        'resource': '/users',
        'path': '/users',
        'httpMethod': 'POST',
        'headers': {
            'content-type': 'application/json'
        },
        'multiValueHeaders': {
            'content-type': [
                'application/json'
            ]
        },
        'queryStringParameters': {
        },
        'multiValueQueryStringParameters': {
        },
        'pathParameters': {
        },
        'stageVariables': None,
        'requestContext': {
            'requestId': '03bd1fd4-a047-4eba-a07f-f4884c5f9bdb',
            'apiId': 'y61mjcmus7',
        },
        'body': json.dumps({
            'name': 'Mr. REST'
        }),
        'isBase64Encoded': False
    }
    res = lambda_handler(event, lambda_context)
    print('[Response]', res)
    assert res.get('statusCode') == 201


def test_put_user(lambda_context):
    print('[Post]')
    user_id = 'bbbbbbb-test-test-test-teeeeeeeeest'
    event = {
        'httpMethod': 'PUT',
        'path': '/users/' + user_id,
        'pathParameters': {
            'userId': user_id
        },
        'body': json.dumps({
            'name': 'Mr. RESTful'
        }),
    }
    res = lambda_handler(event, lambda_context)
    print('[Response]', res)
    assert res.get('statusCode') == 200
