const { handler } = require('../src/index');

function lambdaContext() {
  // https://docs.aws.amazon.com/lambda/latest/dg/nodejs-context.html
  return {
    functionName: 'event',
    functionVersion: '$LATEST',
    invokedFunctionArn: 'arn:aws:lambda:REGION:ACCOUNT-ID:function:event',
    memoryLimitInMB: 512,
    awsRequestId: 'test-test',
    logGroupName: '/aws/lambda/event',
    logStreamName: 'test',
    identity: null,
    clientContext: null,
  };
}

it('GET', async () => {
  const event = {};
  const context = lambdaContext();
  console.log('[Event]', event);
  console.log('[Context]', event);
  const res = await handler(event, context);
  console.log('[Response]', res);
  expect(res.statusCode).toBe(200);
});

it('User', async () => {
  const event = {
    queryStringParameters: { user: true },
  };
  const res = await handler(event, lambdaContext());
  expect(res.statusCode).toBe(200);
});

it.each([
  ['critical'],
  ['error'],
  ['warn'],
  ['info'],
  ['debug'],
  [''],
])('Logger level: %s', async (level) => {
  const event = {
    queryStringParameters: { log: level },
  };
  const res = await handler(event, lambdaContext());
  expect(res.statusCode).toBe(200);
});

it.each([
  'correlation_id_value',
  '',
  null,
])('Correlation ID: %s', async (correlationId) => {
  const event = {
    queryStringParameters: { log: 'info' },
    requestContext: { requestId: correlationId },
  };
  const res = await handler(event, lambdaContext());
  expect(res.statusCode).toBe(200);
});

it('Parameters', async () => {
  const event = {
    queryStringParameters: { ssm: true },
  };
  const res = await handler(event, lambdaContext());
  expect(res.statusCode).toBe(200);
});
