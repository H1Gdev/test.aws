from dataclasses import dataclass

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
