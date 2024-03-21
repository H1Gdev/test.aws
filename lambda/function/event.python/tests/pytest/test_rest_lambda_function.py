import json

import pytest

from src.rest_lambda_function import lambda_handler, parse_accept_language, parse_bearer_token


@pytest.mark.parametrize('bearer_token, expected', [
    (None, None),
    ('', None),
    ('Bearer ', None),
    ('Bearer token1 token2', None),
    ('Bearer token', 'token'),
    ('bearer token', 'token'),
    ('  Bearer  token  ', 'token'),
])
def test_parse_bearer_token(bearer_token, expected):
    token = parse_bearer_token(bearer_token)
    assert token == expected


@pytest.mark.parametrize('accept_language, expected', [
    (None, []),
    ('', []),
    ('ja', [{'language': 'ja', 'quality': 1.0}]),
    ('ja-JP', [{'language': 'ja-JP', 'quality': 1.0}]),
    ('ja-JP;z=1.0', []),
    ('ja-JP;q=100.0', []),
    ('ja-JP;q=value', []),
    ('*;q=0.5, ja-JP', [{'language': 'ja-JP', 'quality': 1.0}, {'language': '*', 'quality': 0.5}]),
    ('fr-CH, fr;q=0.9, en;q=0.8, de;q=0.7, *;q=0.5',
        [{'language': 'fr-CH', 'quality': 1.0}, {'language': 'fr', 'quality': 0.9}, {'language': 'en', 'quality': 0.8}, {'language': 'de', 'quality': 0.7}, {'language': '*', 'quality': 0.5}])
])
def test_parse_accept_language(accept_language, expected):
    languages = parse_accept_language(accept_language)
    assert languages == expected


def test_get_users(lambda_context):
    print('[Get]')
    event = {
        'httpMethod': 'GET',
        'path': '/users',
    }
    res = lambda_handler(event, lambda_context)
    print('[Response]', res)
    assert res.get('statusCode') == 200


@pytest.mark.parametrize('authorization', [True, False])
@pytest.mark.parametrize('accept_language', [True, False])
def test_get_user(authorization, accept_language, lambda_context):
    print('[Get]')
    user_id = 'aaaaaaaa-test-test-test-teeeeeeeeest'
    event = {
        'httpMethod': 'GET',
        'path': '/users/' + user_id,
        'pathParameters': {
            'userId': user_id
        },
    }
    headers = {}
    if authorization:
        headers['Authorization'] = 'Bearer my_token'
    if accept_language:
        headers['Accept-Language'] = 'fr-CH, fr;q=0.9, de;q=0.7, en;q=0.8, *;q=0.5'
    if len(headers) > 0:
        event['headers'] = headers
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
        'resource': '/users',
        'path': '/users',
        'pathParameters': {
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
    assert 'Cache-Control' in res.get('multiValueHeaders')
