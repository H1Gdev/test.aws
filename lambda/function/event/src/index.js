exports.handler = async (event/* Request */, context) => {
  // Response
  const response = {
    statusCode: 200,
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      event: event,
      context: context,
    }),
  };
  return response;
};
