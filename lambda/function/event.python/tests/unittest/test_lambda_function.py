import unittest
from dataclasses import dataclass

from src.lambda_function import lambda_handler


class TestCase(unittest.TestCase):

    def test_handler(self):
        print('[Get]')
        event = {}
        context = self.lambda_context()
        print('[Event]', event)
        print('[Context]', context)
        res = lambda_handler(event, context)
        print('[Response]', res)
        self.assertEqual(res.get('statusCode'), 200)

    def test_logger_level(self):
        levels = ['critical', 'error', 'warn', 'info', 'debug', '']
        for level in levels:
            print('[Logger level: ' + level + ']')
            event = {
                'queryStringParameters': {'log': level}
            }
            context = self.lambda_context()
            res = lambda_handler(event, context)
            self.assertEqual(res.get('statusCode'), 200)

    def lambda_context(self):
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


if __name__ == '__main__':
    unittest.main()
