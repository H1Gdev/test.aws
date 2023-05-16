import io
import json
from dataclasses import dataclass

import botocore
import botocore.client
import pytest


@pytest.fixture
def lambda_context():
    # https://docs.aws.amazon.com/lambda/latest/dg/python-context.html
    @dataclass
    class LambdaContext:
        function_name = 'event'
        function_version = '$LATEST'
        invoked_function_arn = 'arn:aws:lambda:REGION:ACCOUNT-ID:function:event'
        memory_limit_in_mb = 512
        aws_request_id = 'test-test'
        log_group_name = '/aws/lambda/event'
        log_stream_name = 'test'
        identity = None
        client_context = None

    return LambdaContext()


# Botocore
_make_api_call = botocore.client.BaseClient._make_api_call


class BotoMocker:
    def __init__(self, mocker):
        self.mocker = mocker

    def _make_api_call(self, new):
        self.mocker.patch('botocore.client.BaseClient._make_api_call', new=new)

    @staticmethod
    def build_lambda_invoke_handler(response_table):
        def handle_lambda_invoke(self, operation_name, kwarg):
            function_name = kwarg.get('FunctionName')

            response = response_table.get(function_name)
            if response is not None:
                payload = response.pop('Payload')
                if isinstance(payload, Exception):
                    if 'FunctionError' in response:
                        payload = json.dumps({'errorMessage': str(payload), 'errorType': type(payload).__name__}).encode()
                    else:
                        raise payload
                return response | {
                    'Payload': botocore.response.StreamingBody(io.BytesIO(payload), len(payload))
                }
            return _make_api_call(self, operation_name, kwarg)

        return handle_lambda_invoke

    @staticmethod
    def build_make_api_call(service_table):
        def make_api_call(self, operation_name, kwarg):
            service_name = type(self).__name__.lower()

            operation_table = service_table.get(service_name)
            if operation_table is not None and operation_name in operation_table:
                operation = operation_table.get(operation_name)
                if isinstance(operation, Exception):
                    raise operation
                return operation(self, operation_name, kwarg) if callable(operation) else operation
            return _make_api_call(self, operation_name, kwarg)

        return make_api_call


@pytest.fixture
def boto_mocker(mocker):
    return BotoMocker(mocker)
