import uuid
from http import HTTPStatus

from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths

logger = Logger()
app = APIGatewayRestResolver()

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
    # Response
    body = {
        'userId': user_id,
    }
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
