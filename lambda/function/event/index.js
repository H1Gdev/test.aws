exports.handler = async (event/* Request */, context) => {
  // Response
  const response = {
    statusCode: 200,
    body: JSON.stringify({
      event: event,
      context: context,
    }),
  };
  return response;
}

// Test
async function test() {
  var event = {};
  var context = {};
  console.log('[Event]', event);
  console.log('[Context]', event);
  var res = await exports.handler(event, context);
  console.log('[Response]', res);
}
//test();
