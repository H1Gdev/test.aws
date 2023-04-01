const { handler } = require('../src/index');

it('GET', async () => {
  const event = {};
  // https://docs.aws.amazon.com/lambda/latest/dg/nodejs-context.html
  const context = {};
  console.log('[Event]', event);
  console.log('[Context]', event);
  const res = await handler(event, context);
  console.log('[Response]', res);
  expect(res.statusCode).toBe(200);
});
