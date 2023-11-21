import uuid
from http import HTTPStatus
from operator import itemgetter

from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths

logger = Logger()
app = APIGatewayRestResolver()


# https://swagger.io/docs/specification/authentication/bearer-authentication/
# [RFC6750](https://datatracker.ietf.org/doc/html/rfc6750)
def parse_bearer_token(authorization):
    if authorization is None:
        return None

    parts = str(authorization).split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return None
    return parts[1]


# https://developer.mozilla.org/ja/docs/Web/HTTP/Headers/Accept-Language
def parse_accept_language(accept_language):
    if accept_language is None:
        return []

    languages = []
    for part in str(accept_language).split(','):
        values = part.split(';')
        language = values[0].strip()
        if len(language) == 0:
            continue
        if len(values) < 2:
            quality = 1.0
        else:
            try:
                pair = values[1].split('=')
                if pair[0].strip() != 'q':
                    raise Exception
                quality = float(pair[1])
                if quality > 1.0 or quality < 0.0:
                    raise Exception
            except Exception:
                continue
        languages.append({'language': language, 'quality': quality})

    return sorted(languages, key=itemgetter('quality'), reverse=True)


# https://docs.powertools.aws.dev/lambda/python/latest/core/event_handler/api_gateway/
@app.get('/users')
def get_users():
    # Response
    body = [
        {
            'userId': str(uuid.uuid4())
        },
        {
            'userId': str(uuid.uuid4())
        }
    ]
    return body


@app.get('/users/<user_id>')
def get_user(user_id):
    authorization = app.current_event.get_header_value(name='Authorization')
    token = parse_bearer_token(authorization)

    accept_language = app.current_event.get_header_value(name='Accept-Language')
    languages = [lang['language'] for lang in parse_accept_language(accept_language)]

    # Response
    body = {
        'userId': user_id,
        'languages': languages,
    }
    if token is not None:
        body['token'] = token

    return body


@app.post('/users')
def post_user():
    # Response
    body = {
        'userId': str(uuid.uuid4())
    }

    # Create
    request_body = app.current_event.json_body
    name = request_body.get('name') if request_body is not None else None
    if name is not None:
        body['name'] = name

    return body, HTTPStatus.CREATED.value


@app.put('/users/<user_id>')
def put_user(user_id):
    # Response
    body = {
        'userId': user_id
    }

    # Update
    request_body = app.current_event.json_body
    name = request_body.get('name') if request_body is not None else None
    if name is not None:
        body['name'] = name

    return body, HTTPStatus.OK.value


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
def lambda_handler(event, context):
    return app.resolve(event, context)
