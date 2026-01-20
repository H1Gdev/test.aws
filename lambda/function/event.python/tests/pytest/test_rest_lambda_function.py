import copy
import json

import pytest

from src.rest_lambda_function import add_security_headers, lambda_handler, parse_accept_language, parse_bearer_token


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


@pytest.mark.parametrize('event, context, response', [
    ({}, {}, {}),
    ({}, {}, {'headers': {}}),
    ({}, {}, {'headers': {'Content-Type': 'application/json'}}),
    ({}, {}, {'multiValueHeaders': {}}),
    ({}, {}, {'multiValueHeaders': {'Content-Type': ['application/json']}}),
])
def test_add_security_headers(event, context, response):
    @add_security_headers
    def lambda_handler(event, context):
        return response

    original = copy.deepcopy(response)
    actual = lambda_handler(event, context)

    if 'headers' in original:
        assert type(actual['headers']) is dict
        assert type(actual['headers']['Referrer-Policy']) is str
        assert type(actual['headers']['Strict-Transport-Security']) is str
        assert type(actual['headers']['X-DNS-Prefetch-Control']) is str
        assert type(actual['headers']['X-Content-Type-Options']) is str
        assert type(actual['headers']['X-Permitted-Cross-Domain-Policies']) is str
        assert type(actual['headers']['X-Download-Options']) is str
        assert set(original['headers'].keys()) < set(actual['headers'].keys())
    else:
        assert type(actual['multiValueHeaders']) is dict
        assert type(actual['multiValueHeaders']['Referrer-Policy']) is list
        assert type(actual['multiValueHeaders']['Strict-Transport-Security']) is list
        assert type(actual['multiValueHeaders']['X-DNS-Prefetch-Control']) is list
        assert type(actual['multiValueHeaders']['X-Content-Type-Options']) is list
        assert type(actual['multiValueHeaders']['X-Permitted-Cross-Domain-Policies']) is list
        assert type(actual['multiValueHeaders']['X-Download-Options']) is list
        if 'multiValueHeaders' in original:
            assert set(original['multiValueHeaders'].keys()) < set(actual['multiValueHeaders'].keys())


@pytest.mark.parametrize('query', [
    {},
    {'queryStringParameters': {'version': '1'}},
    {'multiValueQueryStringParameters': {'version': ['1']}},
    # API Gateway
    # version=1
    {'queryStringParameters': {'version': '1'}, 'multiValueQueryStringParameters': {'version': ['1']}},
    # version=4&version=1
    {'queryStringParameters': {'version': '1'}, 'multiValueQueryStringParameters': {'version': ['4', '1']}},
])
def test_get_users(lambda_context, query):
    print('[Get]')
    event = {
        'httpMethod': 'GET',
        'path': '/users',
    } | query
    res = lambda_handler(event, lambda_context)
    print('[Response]', res)
    assert res.get('statusCode') == 200


@pytest.mark.parametrize('api_key, uppercase', [
    (True, True),
    (True, False),
    (False, False),
])
@pytest.mark.parametrize('authorization', [True, False])
@pytest.mark.parametrize('accept_language', [True, False])
def test_get_user(api_key, uppercase, authorization, accept_language, lambda_context):
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
    if api_key:
        headers['X-API-KEY' if uppercase else 'x-api-key'] = 'TEST_API_KEY' if uppercase else 'test_api_key'
    if authorization:
        headers['Authorization'] = 'Bearer my_token'
    if accept_language:
        headers['Accept-Language'] = 'fr-CH, fr;q=0.9, de;q=0.7, en;q=0.8, *;q=0.5'
    if len(headers) > 0:
        event['headers'] = headers
    res = lambda_handler(event, lambda_context)
    print('[Response]', res)
    assert res.get('statusCode') == 200

    body = json.loads(res.get('body'))
    if api_key:
        assert body['apiKey'] == headers['X-API-KEY' if uppercase else 'x-api-key']
    else:
        assert 'apiKey' not in body


def test_get_user_icon(lambda_context):
    print('[Get]')
    user_id = 'aaaaaaaa-test-test-test-teeeeeeeeest'
    event = {
        'httpMethod': 'GET',
        'path': '/users/' + user_id + '/icon',
        'pathParameters': {
            'userId': user_id
        },
    }
    res = lambda_handler(event, lambda_context)
    print('[Response]', res)
    assert res.get('statusCode') == 200
    assert res.get('isBase64Encoded') == True


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
    assert 'Strict-Transport-Security' in res.get('multiValueHeaders')
